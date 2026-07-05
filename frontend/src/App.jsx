import { useEffect, useState } from "react";
import { getAnime, getEpisodesForAnime } from "./api/client";
import "./App.css";

function App() {
    const [anime, setAnime] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [selectedAnime, setSelectedAnime] = useState(null);
    const [episodes, setEpisodes] = useState([]);
    const [episodesLoading, setEpisodesLoading] = useState(false);
    const [episodesError, setEpisodesError] = useState("");

    useEffect(() => {
        async function loadAnime() {
            try {
                const data = await getAnime();
                setAnime(data);
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

        try {
            const data = await getEpisodesForAnime(item.id);
            setEpisodes(data);
        } catch (err) {
            setEpisodesError(err.message);
        } finally {
            setEpisodesLoading(false);
        }
    }

    return (
        <main>
            <h1>AnimeMangaDB</h1>
            <p>Anime to manga chapter lookup database.</p>

            <h2>Available Anime</h2>

            {loading && (
                <p className="status">Loading anime...</p>
            )}

            {error && (
                <p className="status error">Error: {error}</p>
            )}

            {!loading && !error && anime.length === 0 && (
                <p>No anime found.</p>
            )}

            {!loading && !error && anime.length > 0 && (
                <ul>
                    {anime.map((item) => (
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

                    {!episodesLoading && !episodesError && episodes.length === 0 && (
                        <p>No episodes found.</p>
                    )}

                    {!episodesLoading && !episodesError && episodes.length > 0 && (
                        <ul>
                            {episodes.map((episode) => (
                                <li key={episode.id}>
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
        </main>
    );
}

export default App;