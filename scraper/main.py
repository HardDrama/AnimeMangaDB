from scraper.utils.config_loader import load_provider_config


def main():

    config = load_provider_config(
        "configs/fandom/example.json"
    )

    print(config.model_dump_json(indent=4))


if __name__ == "__main__":
    main()