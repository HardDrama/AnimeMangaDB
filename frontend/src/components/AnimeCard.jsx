import { Link } from "react-router-dom";

function AnimeCard({
    anime,
    selected,
    onSelect,
}) {
    return (
        <li
            onClick={() => onSelect(anime)}
            className={selected ? "selected" : ""}
        >
            <strong>
                <Link to={`/anime/${anime.id}`}>
                    {anime.title}
                </Link>
            </strong>
            <br />
            <span>{anime.provider}</span>
            <br />
            <span>
                {anime.episode_count}{" "}
                {anime.episode_count === 1
                    ? "episode"
                    : "episodes"}
            </span>
        </li>
    );
}

export default AnimeCard;