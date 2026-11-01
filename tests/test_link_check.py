"""Link checking must tell "gone" from "could not check", and a blocked checker must not empty the board.
Regression: 31 Oct 2026, one refresh saw 229 failing links (normal 34-50) and removed 208 open jobs for about four hours."""
import pathlib, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import link_check as L
import qa_checks as Q
import requests


class Resp:
    def __init__(self, code, url="https://x.test/job"):
        self.status_code, self.url = code, url
    def close(self): pass


class FakeSession:
    def __init__(self, head, get=None):
        self.head_v, self.get_v = head, get
    def _do(self, v):
        if isinstance(v, Exception): raise v
        return v
    def head(self, url, **k): return self._do(self.head_v)
    def get(self, url, **k): return self._do(self.get_v if self.get_v is not None else self.head_v)


def verdict(head, get=None):
    return L.link_verdict("https://x.test/job", FakeSession(head, get), sleep=lambda s: None)


class Verdicts(unittest.TestCase):
    def test_open_gone_and_could_not_tell(self):
        self.assertEqual(verdict(Resp(200)), L.ALIVE)
        self.assertEqual(verdict(Resp(404)), L.DEAD)
        self.assertEqual(verdict(Resp(410)), L.DEAD)
        self.assertEqual(verdict(Resp(200, "https://job-boards.greenhouse.io/co?error=true")), L.DEAD)   # Greenhouse's closed-role redirect
        for code in (400, 401, 429, 500, 502, 503):
            self.assertEqual(verdict(Resp(code)), L.UNKNOWN, code)
        self.assertEqual(verdict(requests.Timeout()), L.UNKNOWN)
        self.assertEqual(verdict(requests.ConnectionError()), L.UNKNOWN)

    def test_a_403_on_head_is_retried_with_get(self):
        self.assertEqual(verdict(Resp(403), Resp(200)), L.ALIVE)
        self.assertEqual(verdict(Resp(403), Resp(403)), L.UNKNOWN)      # blocked, not gone
        self.assertEqual(verdict(Resp(403), Resp(404)), L.DEAD)


def listings(n):
    return [{"url": f"https://job-boards.greenhouse.io/co{i % 40}/jobs/{i}", "title": f"Role {i}", "company": f"Co{i % 40}"} for i in range(n)]


def run(items, bad, state=None, published=True, bad_verdict=L.UNKNOWN):
    bad_urls = {j["url"] for j in items[:bad]}
    pub = {j["url"]: "2026-10-31T12:00:00+00:00" for j in items} if published is True else (published or {})
    removed = []
    ok, stats, ns = L.check_links(items, None, state or L.load_state(pathlib.Path("/nonexistent")), pub, removed,
                                  verdict_fn=lambda u: bad_verdict if u in bad_urls else L.ALIVE, retry_delay=0, sleep=lambda s: None)
    return ok, stats, ns, removed


class CheckLinks(unittest.TestCase):
    def test_normal_run_drops_only_dead_and_carries_unknown_with_old_time(self):
        items = listings(200)
        verdicts = {items[0]["url"]: L.DEAD, items[1]["url"]: L.DEAD, items[2]["url"]: L.UNKNOWN, items[3]["url"]: L.UNKNOWN}
        removed = []
        ok, st, ns = L.check_links(items, None, L.load_state(pathlib.Path("/nonexistent")),
                                   {j["url"]: "2026-10-31T12:00:00+00:00" for j in items[1:]}, removed,
                                   verdict_fn=lambda u: verdicts.get(u, L.ALIVE), retry_delay=0, sleep=lambda s: None)
        urls = {j["url"] for j in ok}
        self.assertNotIn(items[0]["url"], urls)                        # gone, and also not published before: simply dropped
        self.assertNotIn(items[1]["url"], urls)                        # gone: dropped even though it was published
        self.assertIn(items[2]["url"], urls)                           # could not check, was published: kept
        self.assertIn(items[3]["url"], urls)
        kept = next(j for j in ok if j["url"] == items[2]["url"])
        self.assertEqual(kept["verifiedAt"], "2026-10-31T12:00:00+00:00")   # the card shows the real last check
        self.assertEqual(ns["unknown"][items[2]["url"]], 1)
        self.assertEqual((st["dead"], st["unknown"], st["droppedDead"], st["carriedOnOldCheck"]), (2, 2, 2, 2))
        self.assertFalse(st["degraded"])
        self.assertEqual(len([r for r in removed if r.startswith("link-dead")]), 2)

    def test_new_listing_that_cannot_be_checked_is_not_published_yet(self):
        items = listings(100)
        ok, st, ns, removed = run(items, 1, published={})              # nothing published before
        self.assertEqual(len(ok), 99)
        self.assertEqual(st["newHeldUntilChecked"], 1)
        self.assertEqual(removed, [])                                  # not removed forever, just not yet shown

    def test_unknown_four_runs_in_a_row_is_dropped(self):
        items = listings(100)
        state = L.load_state(pathlib.Path("/nonexistent"))
        state["unknown"] = {items[0]["url"]: L.MAX_UNKNOWN_RUNS}
        ok, st, ns, removed = run(items, 1, state=state)
        self.assertNotIn(items[0]["url"], {j["url"] for j in ok})
        self.assertEqual(st["droppedUnverifiable"], 1)
        self.assertTrue(removed[0].startswith("link-unverifiable"))

    def test_incident_replay_229_of_1038_failing_could_not_check(self):
        items = listings(1038)
        state = {"unknown": {}, "failRates": [0.032, 0.033, 0.046, 0.048, 0.033], "degradedStreak": 0, "driftAborts": 0}
        ok, st, ns, removed = run(items, 229, state=state)
        self.assertTrue(st["degraded"])
        self.assertEqual(len(ok), 1038, "a blocked checker must not remove a single open job")
        self.assertEqual(removed, [])
        self.assertEqual(ns["degradedStreak"], 1)
        self.assertEqual(ns["failRates"], state["failRates"], "a degraded run must not poison the baseline")

    def test_incident_replay_even_if_the_failures_look_like_404s(self):
        items = listings(1038)
        state = {"unknown": {}, "failRates": [0.04] * 5, "degradedStreak": 0, "driftAborts": 0}
        ok, st, ns, removed = run(items, 229, state=state, bad_verdict=L.DEAD)
        self.assertTrue(st["degraded"])
        self.assertEqual(len(ok), 1038)

    def test_normal_failure_rate_is_not_degraded(self):
        items = listings(1000)
        state = {"unknown": {}, "failRates": [0.04] * 5, "degradedStreak": 0, "driftAborts": 0}
        ok, st, ns, removed = run(items, 45, state=state, bad_verdict=L.DEAD)   # 4.5%: real closures
        self.assertFalse(st["degraded"])
        self.assertEqual(len(ok), 955)
        self.assertEqual(ns["degradedStreak"], 0)
        self.assertEqual(ns["failRates"][-1], 0.045)

    def test_threshold_follows_a_noisier_baseline(self):
        items = listings(1000)
        state = {"unknown": {}, "failRates": [0.10] * 5, "degradedStreak": 0, "driftAborts": 0}   # baseline 10% -> threshold 25%
        _, st, _, _ = run(items, 200, state=state)
        self.assertFalse(st["degraded"])
        _, st, _, _ = run(items, 300, state=state)
        self.assertTrue(st["degraded"])

    def test_small_runs_are_never_degraded(self):
        _, st, _, _ = run(listings(30), 20)
        self.assertFalse(st["degraded"])

    def test_degraded_streak_counts_up_and_resets(self):
        items = listings(300)
        state = {"unknown": {}, "failRates": [0.04] * 5, "degradedStreak": 2, "driftAborts": 0}
        _, st, ns, _ = run(items, 120, state=state)
        self.assertEqual(ns["degradedStreak"], 3)
        _, st, ns2, _ = run(items, 5, state=ns)
        self.assertEqual(ns2["degradedStreak"], 0)

    def test_state_round_trip_keeps_only_recent_rates(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "state.json"
            L.save_state(p, {"unknown": {"u": 1}, "failRates": list(range(30)), "degradedStreak": 1, "driftAborts": 2})
            s = L.load_state(p)
            self.assertEqual(len(s["failRates"]), L.RATE_HISTORY)
            self.assertEqual((s["unknown"], s["degradedStreak"], s["driftAborts"]), ({"u": 1}, 1, 2))
        self.assertEqual(L.load_state(pathlib.Path("/nonexistent"))["failRates"], [])


class Reasons(unittest.TestCase):
    def test_unknown_links_record_why(self):
        from collections import Counter
        c = Counter()
        for head in (Resp(403), Resp(429), Resp(503), requests.Timeout(), requests.ConnectionError(), Resp(200), Resp(404)):
            L.link_verdict("https://x.test/job", FakeSession(head), sleep=lambda s: None, reasons=c)
        self.assertEqual(dict(c), {"http-403": 1, "http-429": 1, "http-503": 1, "timeout": 1, "connection-error": 1})

    def test_stats_carry_the_reasons(self):
        items = listings(60)
        ok, st, ns = L.check_links(items, FakeSession(Resp(403)), L.load_state(pathlib.Path("/nonexistent")), {}, [],
                                   retry_delay=0, sleep=lambda s: None)
        self.assertEqual(st["unknownReasons"], {"http-403": 120})     # 60 links, counted once in the first pass and once in the second


class SecondPass(unittest.TestCase):
    def test_throttled_links_that_open_on_the_second_try_are_published_normally(self):
        """1 Nov: all 46 unreachable links were on one host and opened fine minutes later (burst throttling)."""
        items = listings(300)
        seen = {}
        def flaky(u):
            seen[u] = seen.get(u, 0) + 1
            return L.UNKNOWN if (u in {j["url"] for j in items[:40]} and seen[u] == 1) else L.ALIVE
        ok, st, ns = L.check_links(items, None, L.load_state(pathlib.Path("/nonexistent")), {}, [], verdict_fn=flaky,
                                   retry_delay=0, sleep=lambda s: None)
        self.assertEqual(len(ok), 300)
        self.assertEqual((st["firstPassUnknown"], st["recoveredOnRetry"], st["unknown"]), (40, 40, 0))
        self.assertEqual(ns["failRates"][-1], 0.0)                      # the baseline records the real, post-retry failure rate

    def test_only_unknown_links_are_retried_and_dead_ones_are_not(self):
        items = listings(120)
        calls = {}
        def v(u):
            calls[u] = calls.get(u, 0) + 1
            return {items[0]["url"]: L.DEAD, items[1]["url"]: L.UNKNOWN}.get(u, L.ALIVE)
        L.check_links(items, None, L.load_state(pathlib.Path("/nonexistent")), {}, [], verdict_fn=v, retry_delay=0, sleep=lambda s: None)
        self.assertEqual(calls[items[0]["url"]], 1)
        self.assertEqual(calls[items[1]["url"]], 2)
        self.assertEqual(calls[items[2]["url"]], 1)

    def test_the_pause_before_the_second_pass_is_used(self):
        slept = []
        L.check_links(listings(80), None, L.load_state(pathlib.Path("/nonexistent")), {}, [],
                      verdict_fn=lambda u: L.UNKNOWN, retry_delay=8, sleep=slept.append)
        self.assertEqual(slept, [8])


class DriftGuard(unittest.TestCase):
    def test_the_31_oct_drop_of_20_percent_now_stops_the_run(self):
        abort, _ = Q.drift({"count": 826, "bySource": {}}, {"count": 1038, "bySource": {}})
        self.assertTrue(abort)

    def test_normal_movement_passes(self):
        for now in (1047, 1038, 1000, 900):
            abort, _ = Q.drift({"count": now, "bySource": {}}, {"count": 1038, "bySource": {}})
            self.assertFalse(abort, now)

    def test_a_source_losing_a_fifth_is_flagged(self):
        _, warn = Q.drift({"count": 900, "bySource": {"Greenhouse": 400}}, {"count": 950, "bySource": {"Greenhouse": 549}})
        self.assertTrue(any("Greenhouse" in w for w in warn))


if __name__ == "__main__":
    unittest.main()
