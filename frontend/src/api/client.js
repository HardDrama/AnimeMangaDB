const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ??
    "http://127.0.0.1:8000";

/**
 * Certified Scope v3 chapter metadata.
 *
 * @typedef {Object} ChapterMetadata
 * @property {number} chapter_number
 * @property {string} chapter_title
 * @property {string|null} manga_arc
 * @property {string} source_url
 * @property {string} last_updated
 */

/**
 * Anime-scoped arc summary.
 *
 * @typedef {Object} ArcSummary
 * @property {string} name
 * @property {string|null} episode_arc
 * @property {string|null} manga_arc
 * @property {number} episode_count
 * @property {number} chapter_count
 */

/**
 * Scope v2 chapter-to-episode mapping result.
 *
 * @typedef {Object} ChapterMappingSearchResult
 * @property {number} chapter_number
 * @property {Array<Object>} episodes
 */

/**
 * Combined global search response.
 *
 * `chapters` preserves the Scope v2 adaptation-mapping
 * contract.
 *
 * `chapter_metadata` contains Scope v3 chapter records.
 *
 * @typedef {Object} SearchResponse
 * @property {Array<Object>} anime
 * @property {Array<Object>} episodes
 * @property {Array<ChapterMappingSearchResult>} chapters
 * @property {Array<ChapterMetadata>} chapter_metadata
 */

export async function getAnime() {
    const response = await fetch(`${API_BASE_URL}/anime`);

    if (!response.ok) {
        throw new Error("Failed to fetch anime.");
    }

    return response.json();
}

export async function getEpisodes() {
    const response = await fetch(`${API_BASE_URL}/episodes`);

    if (!response.ok) {
        throw new Error("Failed to fetch episodes.");
    }

    return response.json();
}

export async function getEpisodesForAnime(animeId) {
    const response = await fetch(
        `${API_BASE_URL}/anime/${animeId}/episodes`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch episodes.");
    }

    return response.json();
}

/**
 * Return all arc summaries for an anime.
 *
 * @param {number|string} animeId
 * @returns {Promise<Array<ArcSummary>>}
 */
export async function getArcsForAnime(animeId) {
    const response = await fetch(
        `${API_BASE_URL}/anime/${animeId}/arcs`
    );

    if (!response.ok) {
        throw new Error(
            "Failed to fetch arc summaries."
        );
    }

    return response.json();
}

/**
 * Return all certified chapter metadata for an anime.
 *
 * @param {number|string} animeId
 * @returns {Promise<Array<ChapterMetadata>>}
 */
export async function getChaptersForAnime(animeId) {
    const response = await fetch(
        `${API_BASE_URL}/anime/${animeId}/chapters`
    );

    if (!response.ok) {
        throw new Error(
            "Failed to fetch chapter metadata."
        );
    }

    return response.json();
}

/**
 * Return one anime-scoped chapter metadata record.
 *
 * @param {number|string} animeId
 * @param {number|string} chapterNumber
 * @returns {Promise<ChapterMetadata>}
 */
export async function getAnimeChapter(
    animeId,
    chapterNumber,
) {
    const response = await fetch(
        (
            `${API_BASE_URL}/anime/${animeId}` +
            `/chapters/${chapterNumber}`
        )
    );

    if (!response.ok) {
        throw new Error(
            "Failed to fetch chapter metadata."
        );
    }

    return response.json();
}

export async function getEpisodeChapters(episodeId) {
    const response = await fetch(
        `${API_BASE_URL}/episodes/${episodeId}/chapters`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch chapter mappings.");
    }

    return response.json();
}

/**
 * Return episodes adapting one anime-scoped chapter.
 */
export async function getEpisodesForAnimeChapter(
    animeId,
    chapterNumber,
) {
    const response = await fetch(
        (
            `${API_BASE_URL}/anime/${animeId}`
            + `/chapters/${chapterNumber}/episodes`
        )
    );

    if (!response.ok) {
        throw new Error(
            "Failed to fetch episodes for anime chapter."
        );
    }

    return response.json();
}

export async function getEpisodesByChapter(chapterNumber) {
    const response = await fetch(
        `${API_BASE_URL}/chapters/${chapterNumber}/episodes`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch episodes for chapter.");
    }

    return response.json();
}

export async function getAnimeById(animeId) {
    const response = await fetch(
        `${API_BASE_URL}/anime/${animeId}`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch anime.");
    }

    return response.json();
}

export async function getEpisodeById(episodeId) {
    const response = await fetch(
        `${API_BASE_URL}/episodes/id/${episodeId}`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch episode.");
    }

    return response.json();
}

/**
 * Search anime, episodes, Scope v2 chapter mappings,
 * and Scope v3 chapter metadata.
 *
 * @param {string} query
 * @returns {Promise<SearchResponse>}
 */

export async function searchDatabase(query) {
    const params = new URLSearchParams({
        query,
    });

    const response = await fetch(
        `${API_BASE_URL}/search?${params.toString()}`
    );

    if (!response.ok) {
        throw new Error("Failed to search database.");
    }

    return response.json();
}