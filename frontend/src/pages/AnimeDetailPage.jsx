import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
    getAnimeById,
    getChaptersForAnime,
    getEpisodesForAnime,
} from "../api/client";
import Breadcrumbs from "../components/Breadcrumbs";
import ChapterMetadataList from "../components/ChapterMetadataList";
import EpisodeCard from "../components/EpisodeCard";

function AnimeDetailPage() {
    const { animeId } = useParams();

    const [anime, setAnime] = useState(null);
    const [episodes, setEpisodes] = useState([]);
    const [chapters, setChapters] = useState([]);
    const [chaptersLoading, setChaptersLoading] =
        useState(true);
    const [chaptersError, setChaptersError] =
        useState("");
    const [chapterSearch, setChapterSearch] =
        useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadAnimeDetail() {
            try {
                const [
                    animeData,
                    episodeData,
                ] = await Promise.all([
                    getAnimeById(animeId),
                    getEpisodesForAnime(animeId),
                ]);

                setAnime(animeData);
                setEpisodes(episodeData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }

            try {
                const chapterData =
                    await getChaptersForAnime(
                        animeId
                    );

                setChapters(chapterData);
            } catch (err) {
                setChaptersError(err.message);
            } finally {
                setChaptersLoading(false);
            }
        }

        loadAnimeDetail();
    }, [animeId]);

        const normalizedChapterSearch =
        chapterSearch.trim().toLowerCase();

    const filteredChapters = chapters.filter(
        (chapter) => {
            if (!normalizedChapterSearch) {
                return true;
            }

            const chapterNumber =
                chapter.chapter_number.toString();

            const chapterTitle =
                chapter.chapter_title.toLowerCase();

            const mangaArc =
                chapter.manga_arc?.toLowerCase()
                ?? "not applicable";

            return (
                chapterNumber.includes(
                    normalizedChapterSearch
                )
                || chapterTitle.includes(
                    normalizedChapterSearch
                )
                || mangaArc.includes(
                    normalizedChapterSearch
                )
            );
        }
    );

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
            
            <ChapterMetadataList
                chapters={chapters}
                filteredChapters={
                    filteredChapters
                }
                search={chapterSearch}
                onSearchChange={
                    setChapterSearch
                }
                loading={chaptersLoading}
                error={chaptersError}
            />
        </section>
    );
}

export default AnimeDetailPage;