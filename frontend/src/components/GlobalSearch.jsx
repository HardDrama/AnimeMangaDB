import { Link } from "react-router-dom";


function GlobalSearch({
    value,
    onChange,
    results,
    loading,
    error,
}) {
    const chapterMetadata =
        results?.chapter_metadata ?? [];

    return (
        <section>
            <h2>Global Search</h2>

            <input
                type="text"
                aria-label="Search anime, episodes, and chapters"
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
                                    <Link to={`/anime/${anime.id}`}>
                                        {anime.title}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    )}

                    <h3>Episodes</h3>

                    {results.episodes.length === 0 ? (
                        <p>No episode results.</p>
                    ) : (
                        <ul>
                            {results.episodes.map((episode) => (
                                <li key={episode.id}>
                                    <Link to={`/episodes/${episode.id}`}>
                                        {episode.anime_title} — Episode{" "}
                                        {episode.episode_number}: {episode.title}
                                        {episode.arc && ` — ${episode.arc}`}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    )}

                    <h3>Episode Adaptation Matches</h3>

                    {results.chapters.length === 0 ? (
                        <p>No episode adaptation matches.</p>
                    ) : (
                        <ul>
                            {results.chapters.map((chapter) => (
                                <li key={chapter.chapter_number}>
                                    <strong>
                                        Chapter {chapter.chapter_number}
                                    </strong>

                                    <ul>
                                        {chapter.episodes.map((episode) => (
                                            <li key={episode.id}>
                                                <Link to={`/episodes/${episode.id}`}>
                                                    {episode.anime_title} — Episode{" "}
                                                    {episode.episode_number}: {episode.title}
                                                    {episode.arc && ` — ${episode.arc}`}
                                                </Link>
                                            </li>
                                        ))}
                                    </ul>
                                </li>
                            ))}
                        </ul>
                    )}

                    <h3>Chapter Metadata</h3>

                    {chapterMetadata.length === 0 ? (
                        <p>
                            No chapter metadata results.
                        </p>
                    ) : (
                        <ul className="search-result-list">
                            {chapterMetadata.map(
                                (chapter) => (
                                    <li
                                        key={
                                            `${chapter.source_url}-` +
                                            `${chapter.chapter_number}`
                                        }
                                        className={
                                            "chapter-search-result"
                                        }
                                    >
                                        <strong>
                                            Chapter{" "}
                                            {
                                                chapter.chapter_number
                                            }
                                            {" — "}
                                            {
                                                chapter.chapter_title
                                            }
                                        </strong>

                                        <p>
                                            <strong>
                                                Manga Arc:
                                            </strong>{" "}
                                            {chapter.manga_arc
                                                ?? "Not applicable"}
                                        </p>

                                        <p>
                                            <a
                                                href={
                                                    chapter.source_url
                                                }
                                                target="_blank"
                                                rel="noreferrer"
                                            >
                                                View canonical source
                                            </a>
                                        </p>
                                    </li>
                                )
                            )}
                        </ul>
                    )}
                </div>
            )}
        </section>
    );
}

export default GlobalSearch;