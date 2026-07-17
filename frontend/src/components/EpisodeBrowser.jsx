import EpisodeCard from "./EpisodeCard";

function EpisodeBrowser({
    selectedAnime,
    episodes,
    filteredEpisodes,
    episodeSearch,
    setEpisodeSearch,
    episodesLoading,
    episodesError,
    selectedEpisode,
    onSelectEpisode,
}) {
    if (!selectedAnime) {
        return null;
    }

    return (
        <section>
            <h2>Episodes</h2>

            <input
                type="text"
                aria-label="Search episodes"
                placeholder="Search episodes..."
                value={episodeSearch}
                onChange={(event) =>
                    setEpisodeSearch(event.target.value)
                }
            />

            {episodesLoading && (
                <p className="status">Loading episodes...</p>
            )}

            {episodesError && (
                <p className="status error">
                    Error: {episodesError}
                </p>
            )}

            {!episodesLoading &&
                !episodesError &&
                filteredEpisodes.length === 0 &&
                episodes.length > 0 && (
                    <p>No episodes match your search.</p>
                )}

            {!episodesLoading &&
                !episodesError &&
                episodes.length === 0 && (
                    <p>No episodes found.</p>
                )}

            {!episodesLoading &&
                !episodesError &&
                filteredEpisodes.length > 0 && (
                    <ul className="episode-list">
                        {filteredEpisodes.map((episode) => (
                            <EpisodeCard
                                key={episode.id}
                                episode={episode}
                                selected={
                                    selectedEpisode?.id === episode.id
                                }
                                onSelect={onSelectEpisode}
                            />
                        ))}
                    </ul>
                )}
        </section>
    );
}

export default EpisodeBrowser;