function GlobalSearch({
    value,
    onChange,
}) {
    return (
        <section>
            <h2>Global Search</h2>

            <input
                type="text"
                placeholder="Search anime, episodes, or chapters..."
                value={value}
                onChange={(event) =>
                    onChange(event.target.value)
                }
            />
        </section>
    );
}

export default GlobalSearch;