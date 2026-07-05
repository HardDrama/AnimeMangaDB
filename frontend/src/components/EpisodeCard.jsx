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
                Episode {episode.episode_number}
            </strong>
            <br />
            <span>{episode.title}</span>
        </li>
    );
}

export default EpisodeCard;