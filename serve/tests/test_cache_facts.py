"""The conversation cache's live figures, read from the engine's own log lines: park, restore and drop
all end with the cache's state, and only park lines spell out evictions."""
import unittest

from serve.engine.process import cache_stats_update


class CacheFacts(unittest.TestCase):
    def test_park_restore_drop_and_quiet_lines(self):
        stats = cache_stats_update(
            "basalt serve: conversation cache: parked 605 tokens in 18.5 ms; parked=1 bytes=245414512 "
            "evictions=0 snapshot_bytes=245414512 reused_kv_bytes=0", {})
        self.assertEqual(stats, {"parked": 1, "bytes": 245414512, "evictions": 0})
        stats = cache_stats_update(
            "basalt serve: conversation cache: restored 126562 tokens (live) in 91.1 ms; parked=1 bytes=2169774032",
            stats)
        self.assertEqual(stats, {"parked": 1, "bytes": 2169774032, "evictions": 0, "restores": 1})
        stats = cache_stats_update(
            "basalt serve: conversation cache: dropped 2 superseded copies of this conversation; parked=3", stats)
        self.assertEqual((stats["parked"], stats["restores"]), (3, 1))
        self.assertIsNone(cache_stats_update("basalt serve: s1 done  pp=109197/109108c 0.3s tg=169", stats))

    def test_a_skipped_park_still_reports_the_state(self):
        stats = cache_stats_update(
            "basalt serve: conversation cache: skipped 512 tokens in 4.0 ms; parked=2 bytes=900 evictions=1 "
            "snapshot_bytes=0 reused_kv_bytes=0", {"parked": 5, "bytes": 9999, "evictions": 0})
        self.assertEqual(stats, {"parked": 2, "bytes": 900, "evictions": 1})


if __name__ == "__main__":
    unittest.main()
