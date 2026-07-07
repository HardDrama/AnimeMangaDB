import argparse


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

    print()
    print("No repair actions are implemented yet.")


if __name__ == "__main__":
    main()