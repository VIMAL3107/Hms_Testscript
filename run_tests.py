"""
Run Tests — entry point to execute all or specific test suites.

Usage:
    python run_tests.py                     # Run ALL tests
    python run_tests.py login               # Run only login tests
    python run_tests.py bulk_invoice        # Run only bulk invoice tests
    python run_tests.py stay_view           # Run only stay view tests
    python run_tests.py reservation         # Run only reservation tests
    python run_tests.py full_flow           # Run the full end-to-end flow
"""

import sys
import unittest


def get_suite(test_name=None):
    """Build a test suite based on the given test name."""
    loader = unittest.TestLoader()

    if test_name is None:
        # Run all tests
        suite = loader.discover("tests", pattern="test_*.py")
    else:
        test_map = {
            "login": "tests.test_login",
            "bulk_invoice": "tests.test_bulk_invoice",
            "stay_view": "tests.test_stay_view",
            "reservation": "tests.test_reservation",
            "checkin": "tests.test_checkin",
            "checkout": "tests.test_checkout",
            "full_flow": "tests.test_full_flow",
        }
        module = test_map.get(test_name)
        if module is None:
            print(f"[ERROR] Unknown test: '{test_name}'")
            print(f"Available tests: {', '.join(test_map.keys())}")
            sys.exit(1)
        suite = loader.loadTestsFromName(module)

    return suite


def main():
    test_name = sys.argv[1] if len(sys.argv) > 1 else None

    if test_name:
        print(f"\n{'=' * 50}")
        print(f"  Running: {test_name}")
        print(f"{'=' * 50}\n")
    else:
        print(f"\n{'=' * 50}")
        print(f"  Running: ALL TESTS")
        print(f"{'=' * 50}\n")

    suite = get_suite(test_name)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
