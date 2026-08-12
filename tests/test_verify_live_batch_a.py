from __future__ import annotations

import unittest

from scripts import verify_live_batch_a


class VerifyLiveBatchATests(unittest.TestCase):
    def test_exact_batch_a_route_set(self) -> None:
        self.assertEqual(
            tuple(path for path, _ in verify_live_batch_a.BATCH_A_ROUTES),
            (
                "/understand/dyslexia/",
                "/understand/developmental-coordination-disorder/",
                "/understand/tourette-syndrome/",
                "/understand/learning-disability/",
                "/understand/developmental-language-disorder/",
            ),
        )

    def test_non_https_origin_is_refused(self) -> None:
        self.assertEqual(verify_live_batch_a.main(["--origin", "http://ndoracle.org"]), 2)


if __name__ == "__main__":
    unittest.main()
