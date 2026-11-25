"""Is a listing still open? Since 25 Nov 2026 the employer's live feed decides and a page sample is a second opinion.
Regressions: 31 Oct 2026 a throttled checker removed 208 open jobs; 25 Nov 2026 it held back 375 new jobs and went red,
while 149 of 150 in-feed pages opened normally when sampled by hand."""
import pathlib, sys, tempfile, unittest
from datetime import datetime, timezone

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
        self.assertEqual(verdict(Resp(403), Resp(403)), L.UNKNOWN)      # blockfrom datetime import datetime, timezone

NOW = datetime(2026, 11, 25, 20, 0, tzinfo=timezone.utc)


def listings(n, start=0):
    return [{"url": f"https://job-boards.greenhouse.io/co{i % 40}/jobs/{i}", "title": f"Role {i}", "company": f"Co{i % 40}"} for i in range(start, start + n)]


def run(items, verdicts=None, state=None, published=True, sample=60, now=NOW):
    verdicts = verdicts or {}
    pub = {j["url"]: "2026-11-24T12:00:00+00:00" for j in items} if published is True else (published or {})
    removed, asked = [], []
    def fn(u):
        asked.append(u)
        return verdicts.get(u, L.ALIVE)
    ok, stats, ns = L.check_links(items, None, state or {}, pub, removed, verdict_fn=fn, retry_delay=0,
                                  sleep=lambda s: None, now=now, sample_size=sample)
    return ok, stats, ns, removed, asked


class FeedDecides(unittest.TestCase):
    def test_the_25_nov_day_a_throttled_checker_no_longer_holds_anything_back(self):
        items = listings(1000)
        blocked = {j["url"]: L.UNKNOWN for j in items}          # every page answers 403
        ok, stats, ns, removed, asked = run(items, blocked)
        self.assertEqual(len(ok), 1000, "every in-feed listing is published")
        self.assertEqual(stats["newHeldUntilChecked"], 0)
        self.assertFalse(stats["mismatch"], "being blocked is not an alarm")
        self.assertEqual(ns["mismatchStreak"], 0)

    def test_only_a_sample_of_pages_is_opened_and_new_listings_come_first(self):
        old, new = listings(200), listings(30, start=500)
        pub = {j["url"]: "2026-11-24T12:00:00+00:00" for j in old}
        ok, stats, ns, removed, asked = run(old + new, published=pub, sample=60)
        self.assertEqual(len(asked), 60)
        self.assertTrue({j["url"] for j in new} <= set(asked), "all 30 new listings are in the sample")

    def test_the_longest_unchecked_pages_are_opened_next(self):
        items = listings(100)
        state = {"pageChecked": {j["url"]: "2026-11-25T10:00:00Z" for j in items[:90]}}   # 90 checked today, 10 never
        ok, stats, ns, removed, asked = run(items, state=state, sample=10)
        self.assertEqual(set(asked), {j["url"] for j in items[90:]})

    def test_a_page_that_is_gone_removes_the_listing_and_keeps_it_off_for_a_week(self):
        items = listings(50)
        gone = items[0]["url"]
        ok, stats, ns, removed, asked = run(items, {gone: L.DEAD})
        self.assertNotIn(gone, {j["url"] for j in ok})
        self.assertIn(gone, ns["dead"])
        self.assertTrue(any(r.startswith("link-dead") for r in removed))
        # next run, still in the feed, not due for a re-check: stays off without being opened again
        ok2, _, ns2, _, asked2 = run(items, state=ns, sample=5, now=datetime(2026, 11, 27, tzinfo=timezone.utc))
        self.assertNotIn(gone, {j["url"] for j in ok2})
        self.assertNotIn(gone, asked2)
        # a week later it is opened again first, and comes back if it opens
        ok3, _, ns3, _, asked3 = run(items, state=ns2, sample=5, now=datetime(2026, 12, 3, tzinfo=timezone.utc))
        self.assertEqual(asked3[0], gone)
        self.assertIn(gone, {j["url"] for j in ok3})
        self.assertNotIn(gone, ns3["dead"])

    def test_a_role_that_leaves_the_feed_leaves_the_board_and_the_state(self):
        items = listings(20)
        ok, stats, ns, removed, asked = run(items, {items[0]["url"]: L.DEAD})
        ok2, _, ns2, _, _ = run(items[1:], state=ns)              # the employer took it down
        self.assertNotIn(items[0]["url"], ns2["dead"])
        self.assertEqual(len(ok2), 19)

    def test_many_gone_pages_in_the_sample_raise_the_alarm_after_two_runs(self):
        items = listings(100)
        gone = {j["url"]: L.DEAD for j in items[:15]}            # 15 of 60 answered = 25%
        _, s1, ns1, _, _ = run(items, gone, sample=60)
        self.assertTrue(s1["mismatch"])
        self.assertEqual(ns1["mismatchStreak"], 1)
        fresh = listings(100, start=1000)
        _, s2, ns2, _, _ = run(fresh, {j["url"]: L.DEAD for j in fresh[:15]}, state=ns1, sample=60)
        self.assertEqual(ns2["mismatchStreak"], 2)
        _, s3, ns3, _, _ = run(listings(100, start=2000), state=ns2, sample=60)
        self.assertEqual(ns3["mismatchStreak"], 0, "a clean run resets it")

    def test_a_small_sample_never_raises_the_alarm(self):
        items = listings(10)
        _, s, ns, _, _ = run(items, {j["url"]: L.DEAD for j in items[:5]}, sample=10)
        self.assertFalse(s["mismatch"])

    def test_old_state_keys_are_dropped_and_other_keys_kept(self):
        _, _, ns, _, _ = run(listings(5), state={"unknown": {"x": 1}, "failRates": [0.1], "degradedStreak": 3, "driftAborts": 1})
        self.assertNotIn("unknown", ns); self.assertNotIn("failRates", ns); self.assertNotIn("degradedStreak", ns)
        self.assertEqual(ns["driftAborts"], 1, "the drift guard's own counter survives")


class SecondPass(unittest.TestCase):
    def test_sampled_pages_that_open_on_the_second_try_count_as_open(self):
        items = listings(10)
        calls = {}
        def fn(u):
            calls[u] = calls.get(u, 0) + 1
            return L.UNKNOWN if calls[u] == 1 else L.ALIVE
        ok, stats, ns = L.check_links(items, None, {}, {}, [], verdict_fn=fn, retry_delay=0, sleep=lambda s: None, now=NOW)
        self.assertEqual(stats["recoveredOnRetry"], 10)
        self.assertEqual(stats["unknown"], 0)



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
