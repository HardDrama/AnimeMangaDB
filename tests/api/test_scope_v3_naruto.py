from fastapi.testclient import TestClient

from scraper.api.app import app


client = TestClient(app)


def get_naruto() -> dict:
    response = client.get(
        "/anime"
    )

    assert response.status_code == 200

    return next(
        anime
        for anime in response.json()
        if anime["title"] == "Naruto"
    )


def test_naruto_scope_v3_chapter_coverage():
    naruto = get_naruto()

    response = client.get(
        f"/anime/{naruto['id']}/chapters"
    )

    assert response.status_code == 200

    chapters = response.json()

    assert len(chapters) == 700

    chapter_numbers = [
        chapter["chapter_number"]
        for chapter in chapters
    ]

    assert chapter_numbers == list(
        range(
            1,
            701,
        )
    )


def test_naruto_scope_v3_required_metadata_complete():
    naruto = get_naruto()

    response = client.get(
        f"/anime/{naruto['id']}/chapters"
    )

    assert response.status_code == 200

    chapters = response.json()

    assert all(
        chapter["chapter_title"]
        for chapter in chapters
    )

    assert all(
        chapter["source_url"]
        for chapter in chapters
    )

    assert all(
        chapter["last_updated"]
        for chapter in chapters
    )

    missing_arcs = [
        chapter
        for chapter in chapters
        if chapter["manga_arc"] is None
    ]

    assert len(missing_arcs) == 1

    assert (
        missing_arcs[0]["chapter_number"]
        == 700
    )


def test_naruto_scope_v3_boundary_chapters():
    naruto = get_naruto()

    chapter_1_response = client.get(
        f"/anime/{naruto['id']}/chapters/1"
    )

    chapter_244_response = client.get(
        f"/anime/{naruto['id']}/chapters/244"
    )

    chapter_245_response = client.get(
        f"/anime/{naruto['id']}/chapters/245"
    )

    chapter_700_response = client.get(
        f"/anime/{naruto['id']}/chapters/700"
    )

    assert chapter_1_response.status_code == 200
    assert chapter_244_response.status_code == 200
    assert chapter_245_response.status_code == 200
    assert chapter_700_response.status_code == 200

    chapter_1 = chapter_1_response.json()
    chapter_244 = chapter_244_response.json()
    chapter_245 = chapter_245_response.json()
    chapter_700 = chapter_700_response.json()

    assert chapter_1["chapter_number"] == 1
    assert chapter_244["chapter_number"] == 244
    assert chapter_245["chapter_number"] == 245
    assert chapter_700["chapter_number"] == 700

    assert chapter_1["chapter_title"]
    assert chapter_244["chapter_title"]
    assert chapter_245["chapter_title"]
    assert chapter_700["chapter_title"]

    assert chapter_1["manga_arc"]
    assert chapter_244["manga_arc"]
    assert chapter_245["manga_arc"]

    assert chapter_700["manga_arc"] is None


def test_naruto_scope_v3_list_and_detail_match():
    naruto = get_naruto()

    list_response = client.get(
        f"/anime/{naruto['id']}/chapters"
    )

    detail_response = client.get(
        f"/anime/{naruto['id']}/chapters/245"
    )

    assert list_response.status_code == 200
    assert detail_response.status_code == 200

    list_chapter = next(
        chapter
        for chapter in list_response.json()
        if chapter["chapter_number"] == 245
    )

    detail_chapter = detail_response.json()

    assert detail_chapter == list_chapter


def test_naruto_scope_v3_chapter_10_main_series_source():
    naruto = get_naruto()

    response = client.get(
        f"/anime/{naruto['id']}/chapters/10"
    )

    assert response.status_code == 200

    chapter = response.json()

    assert chapter["chapter_number"] == 10

    assert (
        chapter["chapter_title"]
        == "The Second Critter"
    )

    source_url = chapter[
        "source_url"
    ].lower()

    assert "sasuke_retsuden" not in source_url
    assert "gaiden" not in source_url
    assert "boruto" not in source_url


def test_naruto_scope_v3_chapter_700_null_arc():
    naruto = get_naruto()

    response = client.get(
        f"/anime/{naruto['id']}/chapters/700"
    )

    assert response.status_code == 200

    chapter = response.json()

    assert chapter["chapter_number"] == 700
    assert chapter["chapter_title"]
    assert chapter["manga_arc"] is None
    assert chapter["source_url"]
    assert chapter["last_updated"]


def test_naruto_scope_v3_numeric_search():
    response = client.get(
        "/search",
        params={
            "query": "700",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    chapter_700_results = [
        chapter
        for chapter in results
        if chapter["chapter_number"] == 700
    ]

    assert chapter_700_results

    assert any(
        chapter["manga_arc"] is None
        for chapter in chapter_700_results
    )


def test_naruto_scope_v3_title_search():
    response = client.get(
        "/search",
        params={
            "query": "The Second Critter",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    assert any(
        chapter["chapter_number"] == 10
        and chapter["chapter_title"]
        == "The Second Critter"
        for chapter in results
    )


def test_naruto_scope_v3_arc_search():
    response = client.get(
        "/search",
        params={
            "query": "Land of Waves",
        },
    )

    assert response.status_code == 200

    results = response.json()[
        "chapter_metadata"
    ]

    assert results

    assert any(
        chapter["manga_arc"]
        and "Land of Waves"
        in chapter["manga_arc"]
        for chapter in results
    )


def test_naruto_scope_v3_excludes_spin_off_sources():
    naruto = get_naruto()

    response = client.get(
        f"/anime/{naruto['id']}/chapters"
    )

    assert response.status_code == 200

    chapters = response.json()

    forbidden_terms = {
        "sasuke_retsuden",
        "naruto_gaiden",
        "boruto",
    }

    contaminated = [
        chapter
        for chapter in chapters
        if any(
            term in chapter[
                "source_url"
            ].lower()
            for term in forbidden_terms
        )
    ]

    assert contaminated == []