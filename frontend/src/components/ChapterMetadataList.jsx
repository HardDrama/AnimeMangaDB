import ChapterMetadataCard from "./ChapterMetadataCard";

function ChapterMetadataList({
    animeId,
    chapters,
    filteredChapters,
    search,
    onSearchChange,
    loading,
    error,
}) {
    return (
        <section className="chapter-metadata-section">
            <h3>Chapter Metadata</h3>

            <input
                type="search"
                placeholder="Search chapters by number, title, or arc..."
                value={search}
                onChange={(event) =>
                    onSearchChange(
                        event.target.value
                    )
                }
                aria-label="Search chapter metadata"
            />

            {loading && (
                <p className="status">
                    Loading chapter metadata...
                </p>
            )}

            {error && (
                <p className="status error">
                    Error: {error}
                </p>
            )}

            {!loading &&
                !error &&
                chapters.length === 0 && (
                    <p>
                        No chapter metadata is currently
                        available for this series.
                    </p>
                )}

            {!loading &&
                !error &&
                chapters.length > 0 &&
                filteredChapters.length === 0 && (
                    <p>
                        No chapter metadata matches your
                        search.
                    </p>
                )}

            {!loading &&
                !error &&
                filteredChapters.length > 0 && (
                    <>
                        <p className="result-count">
                            Showing{" "}
                            {filteredChapters.length} of{" "}
                            {chapters.length} chapters
                        </p>

                        <ul className="chapter-metadata-list">
                            {filteredChapters.map(
                                (chapter) => (
                                    <ChapterMetadataCard
                                        key={
                                            chapter.chapter_number
                                        }
                                        animeId={animeId}
                                        chapter={chapter}
                                    />
                                )
                            )}
                        </ul>
                    </>
                )}
        </section>
    );
}

export default ChapterMetadataList;