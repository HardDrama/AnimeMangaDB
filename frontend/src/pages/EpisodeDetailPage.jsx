import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
    getEpisodeById,
    getEpisodeChapters,
} from "../api/client";

function EpisodeDetailPage() {
    const { episodeId } = useParams();

    const [episode, setEpisode] = useState(null);
    const [chapters, setChapters] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadEpisode() {
            try {
                const episodeData = await getEpisodeById(
                    episodeId
                );

                const chapterData =
                    await getEpisodeChapters(episodeId);

                setEpisode(episodeData);
                setChapters(chapterData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadEpisode();
    }, [episodeId]);

    if (loading) {
        return (
            <p className="status">
                Loading episode...
            </p>
        );
    }

    if (error) {
        return (
            <p className="status error">
                Error: {error}
            </p>
        );
    }

    if (!episode) {
        return <p>Episode not found.</p>;
    }

    return (
        <section>
            <h2>
                Episode {episode.episode_number}
            </h2>

            <p>{episode.title}</p>

            {episode.arc && (
                <p>Arc: {episode.arc}</p>
            )}

            <p>
                <Link
                    to={`/anime/${episode.anime_id}`}
                >
                    Back to Anime
                </Link>
            </p>

            <h3>Chapter Mapping</h3>

            {chapters.length === 0 ? (
                <p>No chapter mapping available.</p>
            ) : (
                <ul>
                    {chapters.map((chapter) => (
                        <li
                            key={
                                chapter.chapter_number
                            }
                        >
                            Chapter{" "}
                            {chapter.chapter_number}
                        </li>
                    ))}
                </ul>
            )}
        </section>
    );
}

export default EpisodeDetailPage;