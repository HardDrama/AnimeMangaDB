import argparse

from dataclasses import dataclass


def main():
    parser = argparse.ArgumentParser(
        description="AnimeMangaDB Metadata Repair Tool"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply repair actions instead of performing a dry run.",
    )

    args = parser.parse_args()

    print("Metadata Repair Tool")
    print("--------------------")

    if args.apply:
        print("Running in APPLY mode.")
    else:
        print("Running in DRY RUN mode.")
        print("No database changes will be made.")

    actions = []

    print()

    if not actions:
        print("No repair actions found.")
        return

    for action in actions:
        if args.apply:
            action.apply()
        else:
            action.preview()

@dataclass
class RepairAction:
    description: str

    def preview(self):
        print(f"Would repair: {self.description}")

    def apply(self):
        print(f"Applied repair: {self.description}")


if __name__ == "__main__":
    main()