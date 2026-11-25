#!/usr/bin/env python3
"""Turns a red or green workflow run into one GitHub issue per workflow, so a failure reaches someone.

Why: from 18 to 25 Nov 2026 the refresh failed 28 times in a row and the live-site monitor flagged it 13
times, and nobody saw it, because a red mark on the Actions tab notifies no one who acts on it. An issue
does: GitHub emails the repository owner when one opens, and the daily Claude doctor routine reads the open
`autopilot` issues first (drafts/operations/autopilot.md).

Usage inside a workflow (needs `permissions: issues: write` and GH_TOKEN=${{ github.token }}):
    python -I scripts/gh_alert.py fail "Refresh job listings" "<one-line reason>"
    python -I scripts/gh_alert.py ok   "Refresh job listings"

One open issue per workflow, never a new issue per failed run: a repeat failure updates the issue body
(count, last run link) and adds at most one comment a day, so an outage is one email, not twenty-eight.
A green run closes the issue with a short comment. Without a token (a local run) it only prints.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

LABEL = "autopilot"
API = "https://api.github.com"


def title_for(workflow):
    return f"Autopilot: {workflow} is failing"


def run_url():
    s, r, i = (os.environ.get(k, "") for k in ("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"))
    return f"{s}/{r}/actions/runs/{i}" if s and r and i else "(local run)"


def body_for(workflow, reason, count, first_seen, now):
    return (f"**{workflow}** has failed {count} time(s) in a row since {first_seen}.\n\n"
            f"- Last failure: {now} ({run_url()})\n"
            f"- Reason given by the run: {reason or 'see the run log'}\n\n"
            "What happens next: the daily Claude doctor routine reads this issue, diagnoses the cause, fixes it "
            "through a reviewed pull request with tests, and closes this issue when the workflow is green again "
            "(runbook: `drafts/operations/autopilot.md`). KT does not need to do anything unless a comment here "
            "asks for a login or a decision.\n\n"
            f"<!-- autopilot-state {json.dumps({'count': count, 'first_seen': first_seen})} -->")


def parse_state(body):
    marker = "<!-- autopilot-state "
    if not body or marker not in body:
        return {}
    try:
        return json.loads(body.split(marker, 1)[1].split(" -->", 1)[0])
    except ValueError:
        return {}


class GitHub:
    def __init__(self, token, repo):
        self.token, self.repo = token, repo

    def call(self, method, path, payload=None):
        req = urllib.request.Request(f"{API}/repos/{self.repo}{path}", method=method,
                                     data=json.dumps(payload).encode() if payload is not None else None)
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "yireh-careers-autopilot")
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read() or b"null")

    def open_issue(self, title):
        issues = self.call("GET", f"/issues?state=open&labels={LABEL}&per_page=100") or []
        return next((i for i in issues if i.get("title") == title and "pull_request" not in i), None)


def decide(action, existing, workflow, reason, now, last_comment_at=None):
    """Pure decision so it can be tested: returns a list of (method, path_suffix, payload) to send."""
    title = title_for(workflow)
    if action == "ok":
        if not existing:
            return []
        n = existing["number"]
        return [("POST", f"/issues/{n}/comments", {"body": f"Recovered: {workflow} passed at {now} ({run_url()}). Closing."}),
                ("PATCH", f"/issues/{n}", {"state": "closed", "state_reason": "completed"})]
    if not existing:
        return [("POST", "/issues", {"title": title, "labels": [LABEL],
                                     "body": body_for(workflow, reason, 1, now, now)})]
    st = parse_state(existing.get("body"))
    count = int(st.get("count", 1)) + 1
    n = existing["number"]
    out = [("PATCH", f"/issues/{n}", {"body": body_for(workflow, reason, count, st.get("first_seen", now), now)})]
    # one comment a day at most, so the owner gets a reminder, not a flood
    if not last_comment_at or (datetime.fromisoformat(now.replace("Z", "+00:00")) -
                               datetime.fromisoformat(last_comment_at.replace("Z", "+00:00"))).total_seconds() > 86400:
        out.append(("POST", f"/issues/{n}/comments", {"body": f"Still failing ({count} runs in a row). Latest: {run_url()}"}))
    return out


def main(argv):
    if len(argv) < 3 or argv[1] not in ("fail", "ok"):
        print(__doc__)
        return 2
    action, workflow = argv[1], argv[2]
    reason = argv[3] if len(argv) > 3 else ""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    token, repo = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print(f"[gh_alert] no token: would record '{action}' for {workflow}: {reason}")
        return 0
    gh = GitHub(token, repo)
    try:
        existing = gh.open_issue(title_for(workflow))
        last_comment_at = None
        if existing and action == "fail" and existing.get("comments"):
            comments = gh.call("GET", f"/issues/{existing['number']}/comments?per_page=100") or []
            last_comment_at = comments[-1]["created_at"] if comments else None
        if existing and action == "fail" and not last_comment_at:
            last_comment_at = existing.get("created_at")
        for method, path, payload in decide(action, existing, workflow, reason, now, last_comment_at):
            gh.call(method, path, payload)
            print(f"[gh_alert] {method} {path}")
    except urllib.error.HTTPError as e:
        # an alerting problem must never turn a green run red or hide the real failure
        print(f"::warning::gh_alert could not update the issue: HTTP {e.code}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
