#!/usr/bin/env python3
"""One-screen health check of the whole board. The daily Claude doctor routine runs this first
(drafts/operations/autopilot.md); anyone can run it:  python3 scripts/health_check.py [--json]

It reads only public things: the repository's own data files, the GitHub REST API for this public repository
(workflow runs, workflow state, open autopilot issues; GH_TOKEN is used when set) and the live site.
Every check returns green, amber or red with the reason in plain words. Exit code: 0 green, 1 amber, 2 red.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = os.environ.get("GITHUB_REPOSITORY", "kaetooruche-collab/job-board")
SITE = "https://yirehcareers.vercel.app"
WORKFLOWS = {  # file -> (plain name, hours after which the last run is overdue)
    # GitHub runs scheduled workflows best-effort and skips many: measured 18-25 Nov 2026, the "every 6 hours"
    # refresh really ran every 10-16 hours and the "every 3 hours" monitor every 6-12. Thresholds sit above that.
    "fetch-jobs.yml": ("6-hourly refresh", 26),
    "site-monitor.yml": ("3-hourly live-site check", 18),
    "ci.yml": ("daily tests", 30),
    "discover-boards.yml": ("weekly board discovery", 8 * 24),
    "weekly-snapshot.yml": ("weekly analytics snapshot", 8 * 24),
}
GREEN, AMBER, RED = "green", "amber", "red"
RANK = {GREEN: 0, AMBER: 1, RED: 2}


def get_json(url, token=None):
    req = urllib.request.Request(url, headers={"User-Agent": "yireh-careers-health", "Accept": "application/vnd.github+json"})
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def hours_since(ts, now):
    return (now - datetime.fromisoformat(ts.replace("Z", "+00:00"))).total_seconds() / 3600


# ---- pure checks (tested in tests/test_health_check.py) ----

def check_freshness(metrics, now):
    h = hours_since(metrics["generatedAt"], now)
    if h > 26:
        return RED, f"listings last refreshed {h:.0f} hours ago (GitHub normally manages every 10-16)"
    if h > 18:
        return AMBER, f"listings last refreshed {h:.0f} hours ago"
    return GREEN, f"refreshed {h:.1f} hours ago, {metrics.get('activeListings')} listings"


def check_volume(history, current):
    """history: list of recent published counts (oldest first)."""
    past = sorted(history[-28:])
    if len(past) < 4:
        return GREEN, "not enough history yet"
    median = past[len(past) // 2]
    if current < 0.7 * median:
        return RED, f"{current} listings, under 70% of the recent median {median}"
    if current < 0.85 * median:
        return AMBER, f"{current} listings, under 85% of the recent median {median}"
    return GREEN, f"{current} listings (recent median {median})"


def check_link_state(state, metrics):
    """Since 25 Nov 2026 the feed decides; only sampled pages that are really gone matter, not throttling."""
    lc = metrics.get("linkCheck") or {}
    streak = state.get("mismatchStreak", 0)
    share = lc.get("deadShare")
    if streak >= 2:
        return RED, f"sampled pages gone although the feed lists them, {streak} runs in a row (share {share})"
    if streak == 1:
        return AMBER, f"one run with many sampled pages gone (share {share})"
    return GREEN, f"feed-checked; sampled pages gone: {share if share is not None else 'n/a'}"


def check_workflow(name, overdue_h, wf_state, last_run, now):
    if wf_state and wf_state != "active":
        return RED, f"workflow is {wf_state} (re-enable it in the Actions tab or via the API)"
    if not last_run:
        return AMBER, "no runs yet"
    age = hours_since(last_run["created_at"], now)
    if last_run.get("conclusion") == "failure":
        return RED, f"last run failed ({last_run.get('html_url')})"
    if age > overdue_h:
        return RED, f"last run {age:.0f} hours ago, overdue"
    return GREEN, f"last run {last_run.get('conclusion') or last_run.get('status')} {age:.0f}h ago"


def check_repo_activity(last_commit_at, now):
    """GitHub disables scheduled workflows in a public repository after 60 days without activity."""
    days = hours_since(last_commit_at, now) / 24
    if days > 45:
        return RED, f"no commit for {days:.0f} days: scheduled workflows stop at 60"
    if days > 30:
        return AMBER, f"no commit for {days:.0f} days"
    return GREEN, f"last commit {days:.1f} days ago"


def check_feed_size(nbytes):
    """The home page downloads all of jobs.json; past a few MB it gets slow on phones."""
    mb = nbytes / 1e6
    if mb > 6:
        return RED, f"jobs.json is {mb:.1f} MB: too heavy for phones, lower the discovery limits"
    if mb > 4:
        return AMBER, f"jobs.json is {mb:.1f} MB: approaching the limit"
    return GREEN, f"jobs.json is {mb:.1f} MB"


def overall(results):
    return max((r[1] for r in results), key=RANK.get, default=GREEN)


# ---- gather ----

def gather(now=None):
    now = now or datetime.now(timezone.utc)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    out = []
    metrics = json.loads((ROOT / "data" / "metrics.json").read_text(encoding="utf-8"))
    out.append(("Fresh listings", *check_freshness(metrics, now)))
    out.append(("Listings file size", *check_feed_size((ROOT / "jobs.json").stat().st_size)))
    try:
        hist = json.loads((ROOT / "data" / "qa_history.json").read_text(encoding="utf-8"))
        counts = [(h.get("summary") or {}).get("count") for h in (hist if isinstance(hist, list) else []) if isinstance(h, dict)]
        out.append(("Listing volume", *check_volume([c for c in counts if c], metrics.get("activeListings", 0))))
    except (OSError, ValueError):
        out.append(("Listing volume", AMBER, "data/qa_history.json unreadable"))
    try:
        state = json.loads((ROOT / "data" / "link_state.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    out.append(("Link checker", *check_link_state(state, metrics)))
    api = f"https://api.github.com/repos/{REPO}"
    try:
        wfs = {Path(w["path"]).name: w for w in get_json(f"{api}/actions/workflows?per_page=100", token)["workflows"]}
        for f, (name, overdue) in WORKFLOWS.items():
            w = wfs.get(f)
            runs = get_json(f"{api}/actions/workflows/{f}/runs?per_page=1&exclude_pull_requests=true", token)["workflow_runs"] if w else []
            out.append((name, *check_workflow(name, overdue, (w or {}).get("state", "missing"), runs[0] if runs else None, now)))
        commits = get_json(f"{api}/commits?per_page=1", token)
        out.append(("Repository activity", *check_repo_activity(commits[0]["commit"]["committer"]["date"], now)))
        issues = [i for i in get_json(f"{api}/issues?state=open&labels=autopilot&per_page=50", token) if "pull_request" not in i]
        out.append(("Open autopilot issues", RED if issues else GREEN,
                    "; ".join(f"#{i['number']} {i['title']}" for i in issues) or "none"))
    except Exception as e:  # the check must still report what it could read
        out.append(("GitHub API", AMBER, f"could not read workflow state: {e}"))
    try:
        live = get_json(f"{SITE}/jobs.json")
        newest = max(r["firstSeenAt"] for r in live)
        out.append(("Live site", RED if hours_since(newest, now) > 30 else GREEN,
                    f"{len(live)} listings live, newest first seen {hours_since(newest, now):.0f}h ago"))
    except Exception as e:
        out.append(("Live site", RED, f"could not load {SITE}/jobs.json: {e}"))
    return out


def main(argv):
    res = gather()
    status = overall(res)
    if "--json" in argv:
        print(json.dumps({"status": status, "checks": [{"check": c, "status": s, "detail": d} for c, s, d in res]}, indent=1))
    else:
        print(f"OVERALL: {status.upper()}")
        for c, s, d in res:
            print(f"  [{s:5}] {c}: {d}")
    return RANK[status]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
