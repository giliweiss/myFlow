"""
Seed exercises into Supabase from JSON import file.
Usage: python scripts/seed_exercises.py <path/to/exercises.json>
"""

import json
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python seed_exercises.py <path/to/exercises.json>")
        sys.exit(1)

    # To be implemented in Phase 1
    print("Seeding exercises - to be implemented in Phase 1")


if __name__ == "__main__":
    main()
