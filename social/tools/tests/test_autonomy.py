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
