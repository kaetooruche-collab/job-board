"""Tests for the agency's autonomous parts: hook bank, planner and publishing gate."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import buffer_payloads as bp  # noqa: E402
import check_post  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
STATS = {"open_to_audience_regions": 120, "worldwide": 36, "jobs": 1987}


def test_every_hook_bank_line_passes_the_checker():
    bank = json.loads((ROOT / "social/data/hook_bank.json").read_text(encoding="utf-8"))
    for series, lines in bank.items():
        if series == "note":
            continue
        for line in lines:
            text = line.format(**STATS)
            post = {"id": "bank", "date": "2026-12-20", "hook": text, "caption": text + "\n\nLink in bio.",
                    "platforms": ["instagram"], "funnel": "awareness", "goal_metric": "saves",
                    "measured_on": "2026-12-20", "number_dated_on_screen": True}
            blocks = [str(f) for f in check_post.check_post(post, "draft") if f.level == check_post.BLOCK]
            assert not blocks, (series, line, blocks)


@pytest.mark.parametrize("mode", ["drafts-only", "hold", None])
def test_gate_refuses_when_not_allowed(mode):
    with pytest.raises(bp.Refused):
        bp.gate_mode({"mode": mode, "approvals": []}, "2026-12-15")


def test_approve_week_needs_kts_yes_for_that_week():
    with pytest.raises(bp.Refused):
        bp.gate_mode({"mode": "approve-week", "approvals": [{"week": "2026-12-08", "by": "KT"}]}, "2026-12-15")
    bp.gate_mode({"mode": "approve-week", "approvals": [{"week": "2026-12-15", "by": "KT"}]}, "2026-12-15")


def test_autopilot_passes_mode_gate():
    bp.gate_mode({"mode": "autopilot", "approvals": []}, "2026-12-15")


def test_state_file_starts_safe():
    s = json.loads((ROOT / "social/state.json").read_text(encoding="utf-8"))
    assert s["mode"] in s["modes_help"]
    assert s["bhuman_monthly_credit_budget"] >= 0


def test_gate_refuses_blocked_post():
    post = {"id": "x", "date": "2030-01-08", "hook": "Guaranteed remote jobs", "caption": "Guaranteed remote jobs. Link in bio.",
            "platforms": ["instagram"], "funnel": "awareness", "goal_metric": "saves"}
    with pytest.raises(bp.Refused):
        bp.payloads_for(post, "2030-01-08", check_urls=False)


def test_facebook_caption_gets_tagged_board_link():
    post = {"id": "w49-p2", "pillar": "jobs", "caption": "Hook.\n\nMore on the board: link in bio. Check rules."}
    t = bp.facebook_text(post)
    assert "utm_source=facebook&utm_campaign=w49-p2" in t and "link in bio" not in t.lower()
    tip = {"id": "w49-p3", "pillar": "tips", "caption": "Hook.\n\nLink in bio.\n\n#jobtips"}
    assert "utm_campaign=w49-p3" in bp.facebook_text(tip)


def test_format_plan_needs_video_for_single_role(tmp_path, monkeypatch):
    monkeypatch.setattr(bp, "ROOT", tmp_path)
    d = tmp_path / "social/output/2030-01-11/x"
    d.mkdir(parents=True)
    (d / "01.jpg").write_bytes(b"jpg")
    post = {"id": "x", "date": "2030-01-11", "series": "role-single", "pillar": "jobs", "format": "image",
            "hook": "A remote role open worldwide.", "caption": "A remote role open worldwide. Link in bio.",
            "platforms": ["instagram"], "funnel": "consideration", "goal_metric": "visits", "render": {"slides": []}}
    with pytest.raises(bp.Refused, match="video"):
        bp.payloads_for(post, "2030-01-11", check_urls=False, formats=True)


def test_cast_rotates_presenter_and_setting():
    import plan_week as pw
    used = [{"date": "2026-12-01", "cast": {"presenter": "amara", "setting": "home desk by a window, morning light, plant in the background"}}]
    c = pw.pick_cast("2026-12-08", used)
    assert c["presenter"] != "amara"          # used last week: a new presenter is brought in
    c2 = pw.pick_cast("2026-12-15", used + [{"date": "2026-12-08", "cast": c}])
    assert c2["setting"] != "home desk by a window, morning light, plant in the background"


def test_no_answer_means_backup_not_publish_everything():
    import datetime as dt
    st = {"mode": "approve-week", "approvals": [], "backup_after_deadline": "approved-material-only"}
    before = dt.datetime(2026, 12, 7, 22, 0, tzinfo=bp.ACCOUNT_TZ)
    after = dt.datetime(2026, 12, 7, 23, 1, tzinfo=bp.ACCOUNT_TZ)
    with pytest.raises(bp.Refused, match="waiting"):
        bp.gate_mode(st, "2026-12-08", before)
    assert bp.week_status(st, "2026-12-08", after) == "backup"


def test_backup_lets_through_only_approved_material():
    import backup
    approved = [{"id": "a1", "series": "tips", "hook": "Remote doesn't always mean anywhere.",
                 "caption": "Remote doesn't always mean anywhere.\n\n36 roles today. Link in bio."}]
    same_new_numbers = {"id": "n1", "series": "tips", "hook": "Remote doesn't always mean anywhere.",
                        "caption": "Remote doesn't always mean anywhere.\n\n41 roles today. Link in bio."}
    new_words = dict(same_new_numbers, hook="A brand new hook KT never saw.")
    assert backup.is_approved_material(same_new_numbers, approved)
    assert not backup.is_approved_material(new_words, approved)
    assert not backup.is_approved_material(dict(same_new_numbers, ai_presenter=True), approved)
    assert not backup.is_approved_material(dict(same_new_numbers, series="service"), approved)
    sub = backup.substitute(dict(new_words, date="2026-12-10"), approved, set())
    assert sub["hook"] == approved[0]["hook"] and sub["date"] == "2026-12-10"


def test_gate_refuses_unapproved_post_in_backup():
    post = {"id": "x", "series": "tips", "hook": "Never seen.", "caption": "Never seen. Link in bio."}
    with pytest.raises(bp.Refused, match="approved material"):
        bp.payloads_for(post, "2030-01-08", check_urls=False, backup_only=[])


def test_kts_no_still_stops_the_week():
    import datetime as dt
    st = {"mode": "approve-week", "backup_after_deadline": "approved-material-only",
          "approvals": [{"week": "2026-12-08", "by": "KT", "decision": "no"}]}
    with pytest.raises(bp.Refused, match="no"):
        bp.gate_mode(st, "2026-12-08", dt.datetime(2026, 12, 9, 12, 0, tzinfo=bp.ACCOUNT_TZ))
    with pytest.raises(bp.Refused):
        bp.gate_mode({"mode": "hold", "approvals": []}, "2026-12-08")


def test_free_video_uses_only_approved_lines_and_refreshes_the_number():
    import free_video
    lines = ["Stop paying to look at remote jobs", "Free to search · no account", "Only the jobs open to where you live",
             "36 open to applicants anywhere", "From our live board, 26 Nov 2026", "Link in bio", "AI-generated presenter"]
    slides, after, date_line = free_video.slides_from(lines, {"worldwide": 41, "measured_on": "2026-12-01"})
    titles = [s["title"] for s in slides]
    assert titles[0] == "Stop paying to look at remote jobs" and slides[0]["sub"] == "Free to search · no account"
    assert "41 open to applicants anywhere" in titles and not any("AI" in t for t in titles)
    assert date_line == "From our live board, 1 Dec 2026"


def _job(kind, label, salary=None):
    return {"id": "t", "title": "T", "company": "C", "sourceUrl": "https://x", "salaryText": salary,
            "eligibility": {"type": kind, "label": label}}


@pytest.mark.parametrize("kind,label,locs,text,salary,ok", [
    ("worldwide", "Worldwide", ["South America - LATAM Argentina", "Brasil Brazil"], "", None, False),   # Trafilea case
    ("region", "EMEA", ["UK - Manchester", "UK - Birmingham"], "", None, False),                        # Airwallex case
    ("region", "Americas", ["Americas Remote"], "Starting salary for this role is $105k–$122k USD", None, False),  # Customer.io
    ("region", "Americas", ["Americas Remote"], "Starting salary for this role is $105k–$122k USD", "$105K - $122K", True),
    ("worldwide", "Worldwide", ["Remote, Global"], "We raised $1B. Home-office budget $1,500.", None, True),
    ("region", "EMEA", ["Remote - EMEA"], "", None, True),
])
def test_source_check_rules(monkeypatch, kind, label, locs, text, salary, ok):
    import verify_source
    monkeypatch.setattr(verify_source, "fetch", lambda url: {"locations": locs, "text": text})
    assert verify_source.check_job(_job(kind, label, salary))["ok"] is ok


def test_gate_needs_todays_source_check(tmp_path, monkeypatch):
    monkeypatch.setattr(bp, "ROOT", tmp_path)
    d = tmp_path / "social/output/2030-01-08/x"
    d.mkdir(parents=True)
    (d / "01.jpg").write_bytes(b"jpg")
    (d / "manifest.json").write_text(json.dumps({"jobs": [{"id": "j1", "check": {"ok": True, "checked_open_on": "2030-01-08"},
                                                          "source_check": {"ok": False, "checked_on": "2030-01-08", "reason": "x"}}]}))
    post = {"id": "x", "date": "2030-01-08", "series": "roles-carousel", "pillar": "jobs", "format": "carousel",
            "hook": "Remote roles open beyond one country.", "caption": "Remote roles open beyond one country. Link in bio.",
            "platforms": ["instagram"], "funnel": "consideration", "goal_metric": "visits", "render": {"slides": []}}
    with pytest.raises(bp.Refused, match="employer's own data"):
        bp.payloads_for(post, "2030-01-08", check_urls=False)


# Regressions from the QA run of 27 Nov 2026
def test_facebook_text_replaces_the_whole_bio_sentence():
    t = bp.facebook_text({"id": "w49-p5", "pillar": "jobs", "caption": "Hook.\n\nThe rest are on the board: link in bio. Check rules.\n\n#a"})
    assert "The rest are on the board" not in t and t.count("See them on the board") == 1
    t2 = bp.facebook_text({"id": "w49-p6", "pillar": "safety", "caption": "Hook.\n\nSave this.\n\n#jobscams"})
    assert t2.index("On the board") < t2.index("#jobscams")
    own = "Read more: https://yirehcareers.vercel.app/verify?utm_source=facebook&utm_campaign=w49-p7"
    assert bp.facebook_text({"id": "w49-p7", "caption": own}) == own


def test_same_platform_posts_are_spaced_out():
    p = [{"_platform": "facebook", "dueAt": "2026-12-05T18:00:00+03:00"}, {"_platform": "facebook", "dueAt": "2026-12-05T18:00:00+03:00"},
         {"_platform": "instagram_story", "dueAt": "2026-12-05T18:30:00+03:00"}]
    out = bp.space_out(p)
    assert out[1]["dueAt"] == "2026-12-05T21:00:00+03:00" and out[2]["dueAt"] == "2026-12-05T18:30:00+03:00"


def test_captions_use_the_script_words_not_the_recogniser():
    import compose_video
    heard = "Must be based in our country that isn't yours. Links in the bio.".split()
    timed = [{"word": w, "start": i * 0.5, "end": i * 0.5 + 0.4} for i, w in enumerate(heard)]
    words = compose_video.align_to_script(timed, '"Must be based in" a country that isn\'t yours. Link\'s in the bio.')
    text = " ".join(w["word"] for w in words)
    assert "a country" in text and "our" not in text.split() and "Link's" in text


def test_picker_skips_north_america_only_and_country_titles():
    import datetime as dt
    import feed
    now = dt.datetime(2026, 11, 27, tzinfo=dt.timezone.utc)
    base = {"postedAt": "2026-11-25T10:00:00Z", "company": "X", "eligibility": {"type": "region", "regions": ["EMEA"], "label": "EMEA"}}
    assert feed.featurable(dict(base, id="a", title="Engineer"), now)
    assert not feed.featurable(dict(base, id="b", title="Engineer", eligibility={"type": "region", "regions": ["North America"], "label": "North America"}), now)
    assert not feed.featurable(dict(base, id="c", title="Head of US, Clearing"), now)


def test_voice_qc_flags_a_misheard_brand():
    import voice_qc
    import inspect
    src = inspect.getsource(voice_qc)
    assert "BRAND said wrong" in src
    # the brand compare: script 'Yai-ray' normalises to yireh, a heard 'Y Ray' does not
    assert "yireh" in voice_qc.words("On Yai-ray Careers")
    assert "yireh" not in voice_qc.words("On Y Ray Careers")
