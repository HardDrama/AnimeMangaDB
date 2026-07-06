import {
    Routes,
    Route,
    Link,
} from "react-router-dom";
import { useEffect, useState } from "react";
import {
    getAnime,
    getEpisodesForAnime,
    getEpisodeChapters,
    getEpisodesByChapter,
    searchDatabase,
} from "./api/client";
import GlobalSearch from "./components/GlobalSearch";
import AnimeBrowser from "./components/AnimeBrowser";
import ChapterLookup from "./components/ChapterLookup";
import EpisodeBrowser from "./components/EpisodeBrowser";
import SelectedEpisode from "./components/SelectedEpisode";
import ChapterMapping from "./components/ChapterMapping";
import AnimeDetailPage from "./pages/AnimeDetailPage";
import EpisodeDetailPage from "./pages/EpisodeDetailPage";
import "./App.css";

function App() {
    const [globalSearch, setGlobalSearch] = useState("");

    const [globalSearchResults, setGlobalSearchResults] = useState(null);
    const [globalSearchLoading, setGlobalSearchLoading] = useState(false);
    const [globalSearchError, setGlobalSearchError] = useState("");
    
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

    const filteredAnimeList = animeList.filter((anime) => {
        const search = globalSearch.toLowerCase();

        return anime.title.toLowerCase().includes(search);
    });
    
    const filteredEpisodes = episodes.filter((episode) => {
        const search = episodeSearch.toLowerCase();

        return (
            episode.title.toLowerCase().includes(search) ||
            episode.episode_number.toString().includes(search)
        );
    });

    async function handleGlobalSearch(query) {
        setGlobalSearch(query);

        if (!query.trim()) {
            setGlobalSearchResults(null);
            setGlobalSearchError("");
            return;
        }

        setGlobalSearchLoading(true);
        setGlobalSearchError("");

        try {
            const data = await searchDatabase(query);
            setGlobalSearchResults(data);
        } catch (err) {
            setGlobalSearchError(err.message);
        } finally {
            setGlobalSearchLoading(false);
        }
    }
    
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
                    <Link to="/" className="site-title">
                        AnimeMangaDB
                    </Link>
                </div>

                <nav>
                    <Link to="/lookup">Chapter Lookup</Link>
                    <a href="#anime-browser">Anime Browser</a>
                </nav>
            </header>

            <main>
                <Routes>
                    <Route
                        path="/"
                        element={
                            <>
                                <h1>AnimeMangaDB</h1>

                                <p>
                                    Anime to manga chapter lookup database.
                                </p>

                                <GlobalSearch
                                    value={globalSearch}
                                    onChange={handleGlobalSearch}
                                />
                                
                                <ChapterLookup
                                    chapterSearch={chapterSearch}
                                    setChapterSearch={setChapterSearch}
                                    chapterLoading={chapterLoading}
                                    chapterError={chapterError}
                                    chapterResults={chapterResults}
                                    onSearch={handleChapterLookup}
                                    onResultClick={handleLookupEpisodeClick}
                                    animeList={filteredAnimeList}
                                />

                                <AnimeBrowser
                                    animeList={filteredAnimeList}
                                    loading={loading}
                                    error={error}
                                    selectedAnime={selectedAnime}
                                    onSelectAnime={handleSelectAnime}
                                    searchText={globalSearch}
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

                                <SelectedEpisode
                                    episode={selectedEpisode}
                                />

                                <ChapterMapping
                                    selectedEpisode={selectedEpisode}
                                    chapters={chapters}
                                    chaptersLoading={chaptersLoading}
                                    chaptersError={chaptersError}
                                />
                            </>
                        }
                    />
                    <Route
                        path="*"
                        element={
                            <section>
                                <h2>Page Not Found</h2>
                                <p>The page you are looking for does not exist.</p>
                            </section>
                        }
                    />
                    <Route
                        path="/lookup"
                        element={
                            <ChapterLookup
                                chapterSearch={chapterSearch}
                                setChapterSearch={setChapterSearch}
                                chapterLoading={chapterLoading}
                                chapterError={chapterError}
                                chapterResults={chapterResults}
                                onSearch={handleChapterLookup}
                                onResultClick={handleLookupEpisodeClick}
                            />
                        }
                    />
                    <Route
                        path="/anime/:animeId"
                        element={<AnimeDetailPage />}
                    />
                    <Route
                        path="/episodes/:episodeId"
                        element={<EpisodeDetailPage />}
                    />
                </Routes>
            </main>
        </>
    );
}

export default App;