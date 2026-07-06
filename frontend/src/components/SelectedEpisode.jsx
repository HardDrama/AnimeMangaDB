function SelectedEpisode({ episode }) {
    if (!episode) {
        return null;
    }

    return (
        <section>
            <h2>Selected Episode</h2>

            <p>
                <strong>
                    Episode {episode.episode_number}
                </strong>
            </p>

            <p>{episode.title}</p>

            {episode.arc && (
                <p>Arc: {episode.arc}</p>
            )}
        </section>
    );
}

export default SelectedEpisode;