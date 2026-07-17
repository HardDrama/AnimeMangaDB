import { Link } from "react-router-dom";

function EpisodeCard({
    episode,
    selected,
    onSelect,
}) {
    function handleSelect() {
        if (onSelect) {
            onSelect(episode);
        }
    }

    return (
        <li
            className={
                selected
                    ? "episode-card selected"
                    : "episode-card"
            }
        >
            <Link
                to={`/episodes/${episode.id}`}
                className="episode-card-link"
                onClick={handleSelect}
            >
                <strong>
                    Episode {episode.episode_number}
                </strong>

                <span>{episode.title}</span>
            </Link>
        </li>
    );
}

export default EpisodeCard;