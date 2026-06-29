from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config


def main():
    config = load_provider_config("configs/fandom/one_piece.json")

    provider = FandomProvider(config)

    print(provider.build_episode_url(1130))


if __name__ == "__main__":
    main()