from datetime import datetime

from scraper.models import EpisodeData

def main():
    episode = EpisodeData(
        anime_title="One Piece",
        episode_number=1130,
        episode_title="Example Episode",
        manga_start=1108,
        manga_end=1108,
        arc="Egghead",
        source_url="https://onepiece.fandom.com/wiki/Episode_1130",
        last_updated=datetime.now(),
    )

    print(episode.model_dump_json(indent=4))

if __name__ == "__main__":
    main()