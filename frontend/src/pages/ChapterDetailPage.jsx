import { useEffect, useState } from "react";
import {
    Link,
    useParams,
} from "react-router-dom";
import {
    getAnimeById,
    getAnimeChapter,
} from "../api/client";
import Breadcrumbs from "../components/Breadcrumbs";

function formatLastUpdated(value) {
    if (!value) {
        return "Unavailable";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString();
}

function ChapterDetailPage() {
    const {
        animeId,
        chapterNumber,
    } = useParams();

    const [anime, setAnime] = useState(null);
    const [chapter, setChapter] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadChapterDetail() {
            try {
                const [
                    animeData,
                    chapterData,
                ] = await Promise.all([
                    getAnimeById(animeId),
                    getAnimeChapter(
                        animeId,
                        chapterNumber,
                    ),
                ]);

                setAnime(animeData);
                setChapter(chapterData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadChapterDetail();
    }, [
        animeId,
        chapterNumber,
    ]);

    if (loading) {
        return (
            <p className="status">
                Loading chapter metadata...
            </p>
        );
    }

    if (error) {
        return (
            <section>
                <p className="status error">
                    Error: {error}
                </p>

                <p>
                    <Link to={`/anime/${animeId}`}>
                        Back to Anime
                    </Link>
                </p>
            </section>
        );
    }

    if (!anime || !chapter) {
        return (
            <section>
                <p>Chapter metadata not found.</p>

                <p>
                    <Link to={`/anime/${animeId}`}>
                        Back to Anime
                    </Link>
                </p>
            </section>
        );
    }

    const mangaArc =
        chapter.manga_arc ?? "Not applicable";

    return (
        <section className="chapter-detail-page">
            <Breadcrumbs
                items={[
                    {
                        label: "Home",
                        to: "/",
                    },
                    {
                        label: anime.title,
                        to: `/anime/${anime.id}`,
                    },
                    {
                        label: `Chapter ${chapter.chapter_number}`,
                    },
                ]}
            />

            <h2>
                Chapter {chapter.chapter_number}
            </h2>

            <p className="chapter-detail-title">
                {chapter.chapter_title}
            </p>

            <dl className="chapter-detail-metadata">
                <div>
                    <dt>Anime</dt>
                    <dd>{anime.title}</dd>
                </div>

                <div>
                    <dt>Manga Arc</dt>
                    <dd>{mangaArc}</dd>
                </div>

                <div>
                    <dt>Last Updated</dt>
                    <dd>
                        {formatLastUpdated(
                            chapter.last_updated
                        )}
                    </dd>
                </div>

                <div>
                    <dt>Canonical Source</dt>
                    <dd>
                        <a
                            href={chapter.source_url}
                            target="_blank"
                            rel="noreferrer"
                        >
                            View chapter source
                        </a>
                    </dd>
                </div>
            </dl>

            <p>
                <Link to={`/anime/${anime.id}`}>
                    Back to {anime.title}
                </Link>
            </p>
        </section>
    );
}

export default ChapterDetailPage;