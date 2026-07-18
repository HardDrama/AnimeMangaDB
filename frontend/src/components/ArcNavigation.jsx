function ArcNavigation({
    arcs,
    selectedArc,
    onSelectArc,
}) {const hasArcs = arcs.length > 0;

    return (
        <section className="arc-navigation">
            <h3>Arc Navigation</h3>

            {!hasArcs && (
                <p>
                    No arc information is available
                    for this series.
                </p>
            )}

            {hasArcs && (
                <div className="arc-navigation-list">
                    <button
                        type="button"
                        className={
                            selectedArc === null
                                ? "arc-navigation-button active"
                                : "arc-navigation-button"
                        }
                        onClick={() =>
                            onSelectArc(null)
                        }
                    >
                        All Arcs
                    </button>

                    {arcs.map((arc) => (
                        <button
                            key={arc.name}
                            type="button"
                            className={
                                selectedArc?.name ===
                                arc.name
                                    ? "arc-navigation-button active"
                                    : "arc-navigation-button"
                            }
                            onClick={() =>
                                onSelectArc(arc)
                            }
                        >
                            <strong>
                                {arc.name}
                            </strong>

                            <span>
                                {arc.episode_count}
                                {" "}
                                episode
                                {arc.episode_count === 1
                                    ? ""
                                    : "s"}
                            </span>

                            <span>
                                {arc.chapter_count}
                                {" "}
                                chapter
                                {arc.chapter_count === 1
                                    ? ""
                                    : "s"}
                            </span>
                        </button>
                    ))}
                </div>
            )}
        </section>
    );}

export default ArcNavigation;