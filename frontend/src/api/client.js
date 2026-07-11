const API_BASE_URL = "http://127.0.0.1:8000";

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

export async function getEpisodeChapters(episodeId) {
    const response = await fetch(
        `${API_BASE_URL}/episodes/${episodeId}/chapters`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch chapter mappings.");
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