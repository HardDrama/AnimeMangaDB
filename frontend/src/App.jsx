import { useEffect, useState } from "react";
import {
    getAnime,
    getEpisodesForAnime,
    getEpisodeChapters,
    getEpisodesByChapter,
} from "./api/client";
import AnimeBrowser from "./components/AnimeBrowser";
import ChapterLookup from "./components/ChapterLookup";
import EpisodeBrowser from "./components/EpisodeBrowser";
import "./App.css";

function App() {
    const [animeList, setAnimeList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [selectedAnime, setSelectedAnime] = useState(null);

    const [episodes, setEpisodes] = useState([]);
    const [episodesLoading, setEpisodesLoading] = useState(false);
    const [episodesError, setEpisodesError] = useState("");
    const [episodeSearch, setEpisodeSearch] = useState("");

    const [selectedEpisode, setSelectedEpisode] = useState(null);

    const [chapters, setChapters] = useState([]);
    const [chaptersLoading, setChaptersLoading] = useState(false);
    const [chaptersError, setChaptersError] = useState("");

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

    const filteredEpisodes = episodes.filter((episode) => {
        const search = episodeSearch.toLowerCase();

        return (
            episode.title.toLowerCase().includes(search) ||
            episode.episode_number.toString().includes(search)
        );
    });

    async function handleSelectAnime(item) {
        setSelectedAnime(item);
        setSelectedEpisode(null);
        setEpisodes([]);
        setChapters([]);
        setEpisodeSearch("");
        setEpisodesError("");
        setEpisodesLoading(true);

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

    async function handleLookupEpisodeClick(episode) {
        const anime = animeList.find(
            (item) => item.id === episode.anime_id
        );

        if (!anime) {
            return;
        }

        await handleSelectAnime(anime);
        await handleSelectEpisode(episode);
    }

    return (
        <>
            <header className="site-header">
                <div>
                    <strong>AnimeMangaDB</strong>
                </div>

                <nav>
                    <a href="#chapter-lookup">Chapter Lookup</a>
                    <a href="#anime-browser">Anime Browser</a>
                </nav>
            </header>

            <main>
                <h1>AnimeMangaDB</h1>
                <p>Anime to manga chapter lookup database.</p>

                <ChapterLookup
                    chapterSearch={chapterSearch}
                    setChapterSearch={setChapterSearch}
                    chapterLoading={chapterLoading}
                    chapterError={chapterError}
                    chapterResults={chapterResults}
                    onSearch={handleChapterLookup}
                    onResultClick={handleLookupEpisodeClick}
                    animeList={animeList}
                />

                <AnimeBrowser
                    animeList={animeList}
                    loading={loading}
                    error={error}
                    selectedAnime={selectedAnime}
                    onSelectAnime={handleSelectAnime}
                />

                <EpisodeBrowser
                    selectedAnime={selectedAnime}
                    episodes={episodes}
                    filteredEpisodes={filteredEpisodes}
                    episodeSearch={episodeSearch}
                    setEpisodeSearch={setEpisodeSearch}
                    episodesLoading={episodesLoading}
                    episodesError={episodesError}
                    selectedEpisode={selectedEpisode}
                    onSelectEpisode={handleSelectEpisode}
                />

                {selectedEpisode && (
                    <section>
                        <h2>Selected Episode</h2>

                        <p>
                            <strong>
                                Episode {selectedEpisode.episode_number}
                            </strong>
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
                            <p className="status">
                                Loading chapters...
                            </p>
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
        </>
    );
}

export default App;