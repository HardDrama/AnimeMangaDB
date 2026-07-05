import AnimeCard from "./AnimeCard";

function AnimeBrowser({
    animeList,
    loading,
    error,
    selectedAnime,
    onSelectAnime,
}) {
    return (
        <section id="anime-browser">
            <h2>Available Anime</h2>

            {loading && (
                <p className="status">Loading anime...</p>
            )}

            {error && (
                <p className="status error">
                    Error: {error}
                </p>
            )}

            {!loading && !error && animeList.length === 0 && (
                <p>No anime found.</p>
            )}

            {!loading && !error && animeList.length > 0 && (
                <ul>
                    {animeList.map((item) => (
                        <AnimeCard
                            key={item.id}
                            anime={item}
                            selected={selectedAnime?.id === item.id}
                            onSelect={onSelectAnime}
                        />
                    ))}
                </ul>
            )}
        </section>
    );
}

export default AnimeBrowser;