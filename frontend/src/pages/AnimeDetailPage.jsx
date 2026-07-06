import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getAnimeById, getEpisodesForAnime } from "../api/client";
import EpisodeCard from "../components/EpisodeCard";
import Breadcrumbs from "../components/Breadcrumbs";

function AnimeDetailPage() {
    const { animeId } = useParams();

    const [anime, setAnime] = useState(null);
    const [episodes, setEpisodes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadAnimeDetail() {
            try {
                const animeData = await getAnimeById(animeId);
                const episodeData = await getEpisodesForAnime(animeId);

                setAnime(animeData);
                setEpisodes(episodeData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadAnimeDetail();
    }, [animeId]);

    if (loading) {
        return <p className="status">Loading anime...</p>;
    }

    if (error) {
        return <p className="status error">Error: {error}</p>;
    }

    if (!anime) {
        return <p>No anime found.</p>;
    }

    return (
        <section>
            <Breadcrumbs
                items={[
                    {
                        label: "Home",
                        to: "/",
                    },
                    {
                        label: anime.title,
                    },
                ]}
            />
            <h2>{anime.title}</h2>
            <p>{anime.provider}</p>
            <p>{anime.episode_count ?? 0} episodes</p>

            <h3>Episodes</h3>

            <ul className="episode-list">
                {episodes.map((episode) => (
                    <EpisodeCard
                        key={episode.id}
                        episode={episode}
                        selected={false}
                        onSelect={() => {}}
                    />
                ))}
            </ul>
        </section>
    );
}

export default AnimeDetailPage;