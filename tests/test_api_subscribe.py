"""Runs the Node tests for api/subscribe.js (node:test). Skipped when Node is not installed."""
import os, shutil, subprocess, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@unittest.skipUnless(shutil.which("node"), "node not installed")
class SubscribeFunction(unittest.TestCase):
    def test_node_suite(self):
        r = subprocess.run(["node", "--test", os.path.join(ROOT, "tests", "node", "subscribe.test.js")], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout[-3000:] + r.stderr[-1500:])


if __name__ == "__main__":
    unittest.main()
