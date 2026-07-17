import { Link } from "react-router-dom";

function formatCount(
    count,
    singular,
    plural,
) {
    const safeCount = count ?? 0;

    return `${safeCount} ${
        safeCount === 1
            ? singular
            : plural
    }`;
}

function AnimeCard({
    anime,
    selected,
}) {
    const cardClassName = selected
        ? "anime-card selected"
        : "anime-card";

    return (
        <li className={cardClassName}>
            <Link
                to={`/anime/${anime.id}`}
                className="anime-card-link"
            >
                <div className="anime-card-header">
                    <h3>{anime.title}</h3>

                    <span className="anime-card-provider">
                        {anime.provider}
                    </span>
                </div>

                <dl className="anime-card-counts">
                    <div>
                        <dt>Episodes</dt>
                        <dd>
                            {formatCount(
                                anime.episode_count,
                                "episode",
                                "episodes",
                            )}
                        </dd>
                    </div>

                    <div>
                        <dt>Chapters</dt>
                        <dd>
                            {formatCount(
                                anime.chapter_count,
                                "chapter",
                                "chapters",
                            )}
                        </dd>
                    </div>
                </dl>

                <span className="anime-card-action">
                    View Series
                    <span aria-hidden="true">
                        {" "}→
                    </span>
                </span>
            </Link>
        </li>
    );
}

export default AnimeCard;