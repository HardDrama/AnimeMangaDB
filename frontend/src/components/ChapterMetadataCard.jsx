function ChapterMetadataCard({
    chapter,
}) {
    const mangaArc =
        chapter.manga_arc ?? "Not applicable";

    return (
        <li className="chapter-metadata-card">
            <div className="chapter-metadata-heading">
                <strong>
                    Chapter {chapter.chapter_number}
                </strong>

                <span>
                    {chapter.chapter_title}
                </span>
            </div>

            <p>
                <strong>Manga Arc:</strong>{" "}
                {mangaArc}
            </p>

            <p>
                <a
                    href={chapter.source_url}
                    target="_blank"
                    rel="noreferrer"
                >
                    View canonical source
                </a>
            </p>
        </li>
    );
}

export default ChapterMetadataCard;