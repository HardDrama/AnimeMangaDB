function ChapterMapping({
    selectedEpisode,
    chapters,
    chaptersLoading,
    chaptersError,
}) {
    if (!selectedEpisode) {
        return null;
    }

    return (
        <section>
            <h2>Chapter Mapping</h2>

            {chaptersLoading && (
                <p className="status">Loading chapters...</p>
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
    );
}

export default ChapterMapping;