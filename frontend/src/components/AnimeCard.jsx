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
        </li>
    );
}

export default AnimeCard;