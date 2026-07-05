import { useEffect, useState } from "react";
import {
    getAnime,
    getEpisodesForAnime,
    getEpisodeChapters,
    getEpisodesByChapter,
} from "./api/client";
import "./App.css";

function App() {
    const [animeList, setAnimeList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [selectedAnime, setSelectedAnime] = useState(null);

    const [episodes, setEpisodes] = useState([]);
    const [episodesLoading, setEpisodesLoading] = useState(false);
    const [episodesError, setEpisodesError] = useState("");
    const [selectedEpisode, setSelectedEpisode] = useState(null);

    const [chapters, setChapters] = useState([]);
    const [chaptersLoading, setChaptersLoading] = useState(false);
    const [chaptersError, setChaptersError] = useState("");

    const [episodeSearch, setEpisodeSearch] = useState("");

    const [chapterSearch, setChapterSearch] = useState("");
    const [chapterResults, setChapterResults] = useState([]);
    const [chapterLoading, setChapterLoading] = useState(false);
    const [chapterError, setChapterError] = useState("");

    useEffect(() => {
        async function loadAnime() {
            try {
                const data = await getAnime();
                setAnimeList(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadAnime();
    }, []);

    async function handleSelectAnime(item) {
        setSelectedAnime(item);
        setEpisodes([]);
        setEpisodesError("");
        setEpisodesLoading(true);
        setEpisodeSearch("");
        setSelectedEpisode(null);
        setChapters([]);

        try {
            const data = await getEpisodesForAnime(item.id);
            setEpisodes(data);
        } catch (err) {
            setEpisodesError(err.message);
        } finally {
            setEpisodesLoading(false);
        }
    }

    async function handleSelectEpisode(episode) {
        setSelectedEpisode(episode);
        setChapters([]);
        setChaptersError("");
        setChaptersLoading(true);

        try {
            const data = await getEpisodeChapters(episode.id);
            setChapters(data);
        } catch (err) {
            setChaptersError(err.message);
        } finally {
            setChaptersLoading(false);
        }
    }

    const filteredEpisodes = episodes.filter((episode) => {
        const search = episodeSearch.toLowerCase();

        return (
            episode.title.toLowerCase().includes(search) ||
            episode.episode_number.toString().includes(search)
        );
    });

    async function handleChapterLookup() {
        if (!chapterSearch.trim()) {
            return;
        }

        setChapterLoading(true);
        setChapterError("");
        setChapterResults([]);

        try {
            const data = await getEpisodesByChapter(chapterSearch);
            setChapterResults(data);
        } catch (err) {
            setChapterError(err.message);
        } finally {
            setChapterLoading(false);
        }
    }

    function handleLookupEpisodeClick(episode) {
        const anime = animeList.find(
            (item) => item.id === episode.anime_id
        );

        if (!anime) {
            return;
        }

        handleSelectAnime(anime).then(() => {
            setSelectedEpisode(episode);
            handleSelectEpisode(episode);
        });
    }

    return (
        <main>
            <h1>AnimeMangaDB</h1>
            <p>Anime to manga chapter lookup database.</p>

            <section>
                <h2>Chapter Lookup</h2>

                <input
                    type="number"
                    placeholder="Enter manga chapter..."
                    value={chapterSearch}
                    onChange={(event) =>
                        setChapterSearch(event.target.value)
                    }
                />

                <button onClick={handleChapterLookup}>
                    Search
                </button>

                {chapterLoading && (
                    <p className="status">
                        Searching...
                    </p>
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
                                    onClick={() => handleLookupEpisodeClick(episode)}
                                >
                                    <strong>Anime ID {episode.anime_id}</strong>
                                    <br />
                                    Episode {episode.episode_number}
                                    <br />
                                    {episode.title}
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
            
            <h2>Available Anime</h2>

            {loading && (
                <p className="status">Loading anime...</p>
            )}

            {error && (
                <p className="status error">Error: {error}</p>
            )}

            {!loading && !error && animeList.length === 0 && (
                <p>No anime found.</p>
            )}

            {!loading && !error && animeList.length > 0 && (
                <ul>
                    {animeList.map((item) => (
                        <li
                            key={item.id}
                            onClick={() => handleSelectAnime(item)}
                            className={
                                selectedAnime?.id === item.id
                                    ? "selected"
                                    : ""
                            }
                        >
                            <strong>{item.title}</strong>
                            <br />
                            <span>{item.provider}</span>
                            <br />
                            <span>
                                {item.episode_count ?? 0}{" "}
                                {item.episode_count === 1 ? "episode" : "episodes"}
                            </span>
                        </li>
                    ))}
                </ul>
            )}

            {selectedAnime && (
                <section>
                    <h2>Selected Anime</h2>
                    <p>
                        {selectedAnime.title} has{" "}
                        {selectedAnime.episode_count ?? 0}{" "}
                        {selectedAnime.episode_count === 1 ? "episode" : "episodes"}.
                    </p>
                </section>
            )}

            {selectedAnime && (
                <section>
                    <h2>Episodes</h2>

                    {episodesLoading && (
                        <p className="status">Loading episodes...</p>
                    )}

                    {episodesError && (
                        <p className="status error">Error: {episodesError}</p>
                    )}

                    {!episodesLoading && !episodesError && filteredEpisodes.length === 0 && (
                        <p>No episodes found.</p>
                    )}

                    <input
                        type="text"
                        placeholder="Search episodes..."
                        value={episodeSearch}
                        onChange={(event) => setEpisodeSearch(event.target.value)}
                    />

                    {!episodesLoading && !episodesError && episodes.length > 0 && (
                        <ul className="episode-list">
                            {filteredEpisodes.map((episode) => (
                                <li
                                    key={episode.id}
                                    onClick={() => handleSelectEpisode(episode)}
                                    className={
                                        selectedEpisode?.id === episode.id
                                            ? "selected"
                                            : ""
                                    }
                                >
                                    <strong>
                                        Episode {episode.episode_number}
                                    </strong>
                                    <br />
                                    <span>{episode.title}</span>
                                </li>
                            ))}
                        </ul>
                    )}
                </section>
            )}

            {selectedEpisode && (
                <section>
                    <h2>Selected Episode</h2>

                    <p>
                        <strong>Episode {selectedEpisode.episode_number}</strong>
                    </p>

                    <p>{selectedEpisode.title}</p>

                    {selectedEpisode.arc && (
                        <p>Arc: {selectedEpisode.arc}</p>
                    )}
                </section>
            )}

            {selectedEpisode && (
                <section>
                    <h2>Chapter Mapping</h2>

                    {chaptersLoading && (
                        <p className="status">Loading chapters...</p>
                    )}

                    {chaptersError && (
                        <p className="status error">
                            Error: {chaptersError}
                        </p>
                    )}

                    {!chaptersLoading &&
                        !chaptersError &&
                        chapters.length === 0 && (
                            <p>No chapter mapping available.</p>
                        )}

                    {!chaptersLoading &&
                        !chaptersError &&
                        chapters.length > 0 && (
                            <ul>
                                {chapters.map((chapter) => (
                                    <li key={chapter.chapter_number}>
                                        Chapter {chapter.chapter_number}
                                    </li>
                                ))}
                            </ul>
                        )}
                </section>
            )}
        </main>
    );
}

export default App;