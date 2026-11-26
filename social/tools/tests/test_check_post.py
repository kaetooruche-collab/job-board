"""Unit tests for social/tools/check_post.py. Run: python3 -m pytest social/tools/tests -q"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_post as cp  # noqa: E402

BASE = {"id": "t", "date": "2026-12-01", "platforms": ["instagram"], "pillar": "tips", "format": "image"}


def post(**kw):
    p = dict(BASE)
    p.update(kw)
    return p


def rules(p, mode="draft", level=cp.BLOCK):
    return {f.rule for f in cp.check_post(p, mode) if f.level == level}


GOOD = post(caption="Before you apply, read where the role is open to.\nLink in bio.",
            on_screen=["Read the location line first"])


def test_clean_post_passes():
    assert rules(GOOD) == set()


@pytest.mark.parametrize("text,rule", [
    ("Guaranteed interviews in a week", "guarantee"),
    ("We guarantee you'll hear back", "guarantee"),
    ("The only job board you need", "the-only"),
    ("the only legit board for remote work", "the-only"),
    ("Every link goes straight to the employer", "direct-to-employer"),
    ("Apply directly from our board", "direct-to-employer"),
    ("A direct link to the employer", "direct-to-employer"),
    ("Taken from the employer's own posting", "employer-own-page"),
    ("Perfect for graduates", "suits-background"),
    ("Remote jobs for students", "suits-background"),
    ("Ideal for nurses who want to work from home", "suits-background"),
    ("DM me for the list", "scam-cta"),
    ("Comment JOBS and I'll send it", "scam-cta"),
    ("comment for the list", "scam-cta"),
    ("Send us your CV on WhatsApp", "scam-cta"),
    ("No work permit needed", "work-permit"),
    ("All remote jobs in one place", "all-remote-jobs"),
    ("Every job shows who can apply", "every-job-shows"),
])
def test_forbidden_claims_block(text, rule):
    assert rule in rules(post(caption=text))


@pytest.mark.parametrize("name", ["Greenhouse", "lever", "Ashby", "Recruitee", "Personio", "Workable", "Workday", "SmartRecruiters"])
def test_hiring_system_names_block(name):
    text = f"Listings from {name} boards" if name != "lever" else "Listings from Lever"
    assert "hiring-system" in rules(post(caption=text))


def test_common_words_are_not_hiring_systems():
    # "lever" and "workday" as ordinary lower-case words are fine
    assert "hiring-system" not in rules(post(caption="Pull every lever in your workday."))


@pytest.mark.parametrize("text", ["Open to people in India", "Hiring in Nigeria now", "US residents only",
                                  "Jobs in the Philippines", "UK only roles", "Remote from South Africa"])
def test_countries_block(text):
    assert "country" in rules(post(caption=text))


@pytest.mark.parametrize("text", ["Thank us later", "Tell us where you live", "North America and the Americas",
                                  "Open across EMEA and APAC", "Africa and Asia", "Worldwide"])
def test_regions_and_pronouns_are_not_countries(text):
    assert "country" not in rules(post(caption=text))


def test_allowed_country_needs_reason():
    p = post(caption="US residents only.", allow_countries=["US"])
    assert "country" in rules(p)
    p["allow_reason"] = "Video 1 hook quoting a posting, approved by KT 26 Nov 2026"
    assert "country" not in rules(p)


def test_demonym_only_warns():
    assert "country-word" in rules(post(caption="French-speaking support role"), level=cp.WARN)
    assert "country" not in rules(post(caption="French-speaking support role"))


def test_numbers_need_measured_date():
    p = post(on_screen=["19 jobs open worldwide"], number_dated_on_screen=True)
    assert "numbers" in rules(p)
    p["measured_on"] = "2026-12-01"
    assert "numbers" not in rules(p, "schedule")


def test_stale_numbers_block_when_scheduling_but_warn_in_draft():
    p = post(on_screen=["19 jobs open worldwide"], measured_on="2026-11-26", number_dated_on_screen=True)
    assert "numbers" in rules(p, "schedule")
    assert "numbers" not in rules(p, "draft")
    assert "numbers" in rules(p, "draft", cp.WARN)


def test_number_on_media_needs_date_line():
    p = post(on_screen=["19 jobs open worldwide"], measured_on="2026-12-01")
    assert "numbers" in rules(p)


def test_years_and_urls_are_not_numbers():
    p = post(caption="Since 2025. yirehcareers.vercel.app/?utm_source=instagram&utm_campaign=p1", on_screen=["Updated daily"])
    assert "numbers" not in rules(p)


def test_spelling_known_typo_blocks():
    assert "spelling" in rules(post(on_screen=["REMOTE DOSEN'T MEAN ANYWHERE"]))


def test_spelling_dictionary_blocks_unknown_word():
    if cp._spell() is False:
        pytest.skip("pyspellchecker not installed")
    assert "spelling" in rules(post(caption="Check the locaton line first."))
    assert "spelling" not in rules(post(caption="Check the location line first."))


def test_spelling_ok_list_allows_names():
    if cp._spell() is False:
        pytest.skip("pyspellchecker not installed")
    assert "spelling" in rules(post(caption="Zorblax is hiring."))
    assert "spelling" not in rules(post(caption="Zorblax is hiring.", spelling_ok=["Zorblax"]))


def test_ai_label_required():
    assert "ai-label" in rules(post(format="video", ai_presenter=True))
    assert "ai-label" in rules(post(format="video", ai_voice=True))
    assert "ai-label" not in rules(post(format="video", ai_presenter=True, ai_label=True))


def test_featured_jobs_must_be_reopened_on_post_day():
    p = post(featured_jobs=[{"id": "j1", "checked_open_on": "2026-11-26"}])
    assert "featured-open" in rules(p, "schedule")
    p["featured_jobs"][0]["checked_open_on"] = "2026-12-01"
    assert "featured-open" not in rules(p, "schedule")


def test_free_claim_stacked():
    p = post(script="It's free. No fee. We never charge you to apply.")
    assert "free-stacked" in rules(p)
    assert "free-stacked" not in rules(post(script="It's completely free, and we never charge you to apply."))


def test_service_never_in_jobs_post():
    assert "service-in-jobs-post" in rules(post(pillar="jobs", caption="Three roles. Need help? Our CV service is $29."))
    assert "service-in-jobs-post" not in rules(post(pillar="service", caption="Our CV service starts at $29.", measured_on="2026-12-01"))


def test_instagram_hashtag_cap():
    assert "hashtags" in rules(post(caption="Hi #a #b #c #d #e #f"))
    assert "hashtags" not in rules(post(caption="Hi #a #b #c #d #e"))


def test_caption_length_limit():
    assert "caption-length" in rules(post(caption="word " * 500))


def test_utm_warning():
    assert "utm" in rules(post(caption="https://yirehcareers.vercel.app/"), level=cp.WARN)


def test_cli_exit_codes(tmp_path):
    f = tmp_path / "p.json"
    f.write_text(json.dumps([GOOD]))
    assert cp.main([str(f)]) == 0
    f.write_text(json.dumps([post(caption="Guaranteed jobs")]))
    assert cp.main([str(f)]) == 1


def test_calendar_files_pass_in_draft_mode():
    """Every planned post in social/calendar/*.posts.json passes the checker (draft mode)."""
    cal = Path(__file__).resolve().parents[2] / "calendar"
    files = sorted(cal.glob("*.posts.json"))
    if not files:
        pytest.skip("no calendar yet")
    for path in files:
        for p in cp.load_posts(path):
            blocks = [str(x) for x in cp.check_post(p, "draft") if x.level == cp.BLOCK]
            assert not blocks, f"{path.name} {p.get('id')}: {blocks}"
