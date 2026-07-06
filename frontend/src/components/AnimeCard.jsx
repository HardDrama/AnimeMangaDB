import { Link } from "react-router-dom";

function AnimeCard({
    anime,
    selected,
}) {
    return (
        <li className={selected ? "selected" : ""}>
            <Link
                to={`/anime/${anime.id}`}
                className="card-link"
            >
                <strong>{anime.title}</strong>
                <br />
                <span>{anime.provider}</span>
                <br />
                <span>
                    {anime.episode_count}{" "}
                    {anime.episode_count === 1
                        ? "episode"
                        : "episodes"}
                </span>
            </Link>
        </li>
    );
}

export default AnimeCard;