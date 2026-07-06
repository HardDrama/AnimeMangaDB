function GlobalSearch({
    value,
    onChange,
    results,
    loading,
    error,
}) {
    return (
        <section>
            <h2>Global Search</h2>

            <input
                type="text"
                placeholder="Search anime, episodes, or chapters..."
                value={value}
                onChange={(event) =>
                    onChange(event.target.value)
                }
            />

            {value && (
                <button onClick={() => onChange("")}>
                    Clear Search
                </button>
            )}

            {loading && (
                <p className="status">Searching...</p>
            )}

            {error && (
                <p className="status error">Error: {error}</p>
            )}

            {results && !loading && !error && (
                <div>
                    <h3>Anime</h3>

                    {results.anime.length === 0 ? (
                        <p>No anime results.</p>
                    ) : (
                        <ul>
                            {results.anime.map((anime) => (
                                <li key={anime.id}>
                                    {anime.title}
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
        </section>
    );
}

export default GlobalSearch;