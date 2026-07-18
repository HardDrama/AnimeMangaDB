import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
    getAnimeById,
    getArcsForAnime,
    getChaptersForAnime,
    getEpisodesForAnime,
} from "../api/client";
import ArcNavigation from "../components/ArcNavigation";
import Breadcrumbs from "../components/Breadcrumbs";
import ChapterMetadataList from "../components/ChapterMetadataList";
import EpisodeCard from "../components/EpisodeCard";

function AnimeDetailPage() {
    const { animeId } = useParams();

    const [anime, setAnime] = useState(null);
    const [episodes, setEpisodes] = useState([]);
    const [chapters, setChapters] = useState([]);
    const [arcs, setArcs] = useState([]);
    const [chaptersLoading, setChaptersLoading] =
        useState(true);
    const [chaptersError, setChaptersError] =
        useState("");
    const [chapterSearch, setChapterSearch] =
        useState("");
    const [selectedArc, setSelectedArc] =
        useState(null);
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
                const [
                    chapterData,
                    arcData,
                ] = await Promise.all([
                    getChaptersForAnime(
                        animeId
                    ),
                    getArcsForAnime(
                        animeId
                    ),
                ]);

                setChapters(chapterData);
                setArcs(arcData);
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

    const arcFilteredChapters =
        selectedArc?.manga_arc
            ? chapters.filter(
                (chapter) =>
                    chapter.manga_arc ===
                    selectedArc.manga_arc
            )
            : chapters;

    const filteredChapters =
        arcFilteredChapters.filter(
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

    function handleSelectArc(arc) {
        setSelectedArc(arc);
    }

    const filteredEpisodes =
        selectedArc === null
            ? episodes
            : episodes.filter(
                (episode) =>
                    episode.arc ===
                    selectedArc.episode_arc
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

            <ArcNavigation
                arcs={arcs}
                selectedArc={selectedArc}
                onSelectArc={handleSelectArc}
            />

            <h3>
                {selectedArc === null
                    ? "Episodes"
                    : `${selectedArc.name} Episodes`}
            </h3>

            {filteredEpisodes.length === 0 && (
                <p>
                    No episodes were found for this
                    arc.
                </p>
            )}

            {filteredEpisodes.length > 0 && (
                <ul className="episode-list">
                    {filteredEpisodes.map((episode) => (
                        <EpisodeCard
                            key={episode.id}
                            episode={episode}
                            selected={false}
                            onSelect={() => {}}
                        />
                    ))}
                </ul>
            )}
            
            <ChapterMetadataList
                animeId={anime.id}
                chapters={arcFilteredChapters}
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