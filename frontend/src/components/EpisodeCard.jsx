import { Link } from "react-router-dom";

function EpisodeCard({
    episode,
    selected,
    onSelect,
}) {
    return (
        <li
            onClick={() => onSelect(episode)}
            className={selected ? "selected" : ""}
        >
            <strong>
                <Link to={`/episodes/${episode.id}`}>
                    Episode {episode.episode_number}
                </Link>
            </strong>
            <br />
            <span>{episode.title}</span>
        </li>
    );
}

export default EpisodeCard;