"""Board discovery and pruning: the pure rules, with no network."""
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import discover_boards as D  # noqa: E402

AUTOMATTIC = """---
title: "Automattic"
slug: automattic
website: https://automattic.com/
careers_url: https://automattic.com/work-with-us/
region: worldwide
remote_policy: fully-remote
technologies:
  - php
---

## Company blurb
"""


class Resp:
    def __init__(self, code, data=None):
        self.status_code, self._d = code, data

    def json(self):
        return self._d


class Discovery(unittest.TestCase):
    def test_frontmatter_of_a_real_directory_file(self):
        fm = D.parse_frontmatter(AUTOMATTIC)
        self.assertEqual(fm["title"], "Automattic")
        self.assertEqual(fm["region"], "worldwide")
        self.assertNotIn("technologies", fm, "list keys are ignored, not mangled")

    def test_hiring_system_links_give_the_board_name(self):
        cases = {
            "https://boards.greenhouse.io/gitlab": ("greenhouse", "gitlab"),
            "https://job-boards.greenhouse.io/brex/jobs/8943783002": ("greenhouse", "brex"),
            "https://boards.greenhouse.io/embed/job_board?for=doist": ("greenhouse", "doist"),
            "https://jobs.lever.co/15five": ("lever", "15five"),
            "https://jobs.ashbyhq.com/ashby/7458d4e9": ("ashby", "ashby"),
        }
        for url, want in cases.items():
            self.assertEqual(D.ats_from_url(url), want, url)
        self.assertIsNone(D.ats_from_url("https://automattic.com/work-with-us/"))

    def test_guesses_and_company_matching(self):
        self.assertEqual(D.slug_guesses({"title": "Close.com", "slug": "close", "website": "https://close.com"})[:2], ["close", "closecom"])
        self.assertTrue(D.same_company("Doist", "doist"))
        self.assertTrue(D.same_company("GitLab", "GitLab Inc."))
        self.assertFalse(D.same_company("Ada", "Adapt Health"), "a short name must not match a longer different company")

    def test_worldwide_fully_remote_companies_are_tried_first(self):
        entries = [{"title": "B", "region": "north-america", "remote_policy": "fully-remote"},
                   {"title": "C", "region": "worldwide", "remote_policy": "remote-friendly"},
                   {"title": "A", "region": "worldwide", "remote_policy": "fully-remote"}]
        self.assertEqual([e["title"] for e in sorted(entries, key=D.priority)], ["A", "C", "B"])

    def test_a_board_is_retired_only_after_repeated_weekly_evidence(self):
        rec, why = None, None
        for _ in range(D.DEAD_WEEKS_TO_RETIRE - 1):
            rec, why = D.update_health(rec, "dead", 0)
            self.assertIsNone(why)
        rec, why = D.update_health(rec, "error", 0)
        self.assertIsNone(why, "a network error neither counts nor resets")
        rec, why = D.update_health(rec, "dead", 0)
        self.assertIn("404", why)

    def test_one_publishable_week_resets_the_empty_counter(self):
        rec = {"emptyWeeks": D.EMPTY_WEEKS_TO_RETIRE - 1}
        rec, why = D.update_health(rec, "ok", 2)
        self.assertEqual(rec["emptyWeeks"], 0)
        self.assertIsNone(why)
        rec = {"emptyWeeks": D.EMPTY_WEEKS_TO_RETIRE - 1}
        self.assertIn("nothing publishable", D.update_health(rec, "ok", 0)[1])

    def test_probe_reads_status_and_greenhouse_name(self):
        self.assertEqual(D.probe("greenhouse", "x", get=lambda u: Resp(200, {"name": "Doist"})), ("ok", "Doist"))
        self.assertEqual(D.probe("lever", "x", get=lambda u: Resp(404)), ("dead", None))
        self.assertEqual(D.probe("ashby", "x", get=lambda u: Resp(503)), ("error", None))

    def test_a_guessed_board_must_prove_it_is_the_same_company(self):
        entry = {"title": "Doist", "slug": "doist"}
        wrong = lambda u: Resp(200, {"name": "Doist Plumbing LLC"}) if "greenhouse" in u else Resp(404)
        self.assertIsNone(D.identify(entry, get=wrong))
        right = lambda u: Resp(200, {"name": "Doist"}) if "greenhouse" in u else Resp(404)
        self.assertEqual(D.identify(entry, get=right)[:2], ("greenhouse", "doist"))
        # Lever has no name field: the company must be named in its own postings
        lever_only = lambda u: Resp(200, []) if "lever" in u else Resp(404)
        self.assertIsNone(D.identify(entry, get=lever_only, items_fn=lambda k, b: [{"description": "Join Acme"}]))
        self.assertEqual(D.identify(entry, get=lever_only, items_fn=lambda k, b: [{"description": "<p>At Doist we</p>"}])[0], "lever")

    def test_probe_window(self):
        st = {"probed": {"doist": {"at": "2026-10-01"}}}
        self.assertFalse(D.due_for_probe(st, "doist", date(2026, 11, 25)))
        self.assertTrue(D.due_for_probe(st, "doist", date(2027, 1, 5)))
        self.assertTrue(D.due_for_probe(st, "new", date(2026, 11, 25)))


if __name__ == "__main__":
    unittest.main()
