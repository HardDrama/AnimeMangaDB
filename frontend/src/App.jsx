import { useEffect, useState } from "react";
import { getAnime } from "./api/client";
import "./App.css";

function App() {
    const [anime, setAnime] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

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
                        <li key={item.id}>
                            <strong>{item.title}</strong>
                            <br />
                            <span>{item.provider}</span>
                            <br />
                            <span>{item.episode_count ?? 0} episodes</span>
                        </li>
                    ))}
                </ul>
            )}
        </main>
    );
}

export default App;