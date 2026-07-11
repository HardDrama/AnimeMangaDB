function ChapterLookup({
    chapterSearch,
    setChapterSearch,
    chapterResults,
    chapterLoading,
    chapterError,
    onSearch,
    onResultClick,
}) {
    return (
        <section id="chapter-lookup">
            <h2>Chapter Lookup</h2>

            <input
                type="number"
                placeholder="Enter manga chapter..."
                value={chapterSearch}
                onChange={(event) =>
                    setChapterSearch(event.target.value)
                }
            />

            <button onClick={onSearch}>
                Search
            </button>

            {chapterLoading && (
                <p className="status">Searching...</p>
            )}

            {chapterError && (
                <p className="status error">
                    Error: {chapterError}
                </p>
            )}

            {!chapterLoading &&
                !chapterError &&
                chapterResults.length > 0 && (
                    <ul>
                        {chapterResults.map((episode) => (
                            <li
                                key={episode.id}
                                onClick={() =>
                                    onResultClick(episode)
                                }
                            >
                                <strong>{episode.anime_title}</strong>
                                <br />
                                Episode {episode.episode_number}
                                <br />
                                {episode.title}

                                {episode.arc && (
                                    <>
                                        <br />
                                        <span>Arc: {episode.arc}</span>
                                    </>
                                )}
                            </li>
                        ))}
                    </ul>
                )}

            {!chapterLoading &&
                !chapterError &&
                chapterSearch &&
                chapterResults.length === 0 && (
                    <p>No matching episodes found.</p>
                )}
        </section>
    );
}

export default ChapterLookup;