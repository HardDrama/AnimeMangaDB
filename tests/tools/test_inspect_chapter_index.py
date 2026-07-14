from tools import inspect_chapter_index


def test_inspects_numbered_section():
    html = """
    <html>
        <body>
            <h2>
                <span id="Tankōbon">
                    Tankōbon
                </span>
            </h2>

            <h3>
                <span id="Part_I">
                    Part I
                </span>
            </h3>

            <table>
                <tr>
                    <td>
                        <ul>
                            <li>
                                001.
                                <a href="/wiki/Chapter_1">
                                    Chapter One
                                </a>
                            </li>
                            <li>
                                002.
                                <a href="/wiki/Chapter_2">
                                    Chapter Two
                                </a>
                            </li>
                        </ul>
                    </td>
                </tr>
            </table>

            <h3>
                <span id="Part_II">
                    Part II
                </span>
            </h3>

            <table>
                <tr>
                    <td>
                        <ul>
                            <li>
                                003.
                                <a href="/wiki/Chapter_3">
                                    Chapter Three
                                </a>
                            </li>
                        </ul>
                    </td>
                </tr>
            </table>

            <h2>
                <span id="Naruto_Gaiden">
                    Naruto Gaiden
                </span>
            </h2>

            <table>
                <tr>
                    <td>
                        <ul>
                            <li>
                                001.
                                <a href="/wiki/Gaiden_1">
                                    Gaiden Chapter
                                </a>
                            </li>
                        </ul>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """

    report = (
        inspect_chapter_index
        .inspect_numbered_section(
            html=html,
            section_id="Tankōbon",
            subsection_ids=[
                "Part_I",
                "Part_II",
            ],
        )
    )

    assert report["entry_count"] == 3
    assert report["unique_chapter_count"] == 3
    assert report["minimum_chapter"] == 1
    assert report["maximum_chapter"] == 3
    assert report["missing_chapter_count"] == 0
    assert report["duplicate_chapter_count"] == 0

    assert [
        entry["chapter_number"]
        for entry in report["entries"]
    ] == [
        1,
        2,
        3,
    ]


def test_excludes_unconfigured_subsections():
    html = """
    <html>
        <body>
            <h2>
                <span id="Tankōbon">
                    Tankōbon
                </span>
            </h2>

            <h3>
                <span id="Part_I">
                    Part I
                </span>
            </h3>

            <ul>
                <li>
                    001.
                    <a href="/wiki/Main_1">
                        Main One
                    </a>
                </li>
            </ul>

            <h3>
                <span id="Part_II">
                    Part II
                </span>
            </h3>

            <ul>
                <li>
                    700.
                    <a href="/wiki/Main_700">
                        Main Seven Hundred
                    </a>
                </li>
            </ul>

            <h3>
                <span id="Naruto_Gaiden">
                    Naruto Gaiden
                </span>
            </h3>

            <ul>
                <li>
                    000.
                    <a href="/wiki/Gaiden_0">
                        Gaiden Zero
                    </a>
                </li>
                <li>
                    001.
                    <a href="/wiki/Gaiden_1">
                        Gaiden One
                    </a>
                </li>
            </ul>

            <h3>
                <span id="Sasuke_Retsuden">
                    Sasuke Retsuden
                </span>
            </h3>

            <ul>
                <li>
                    001.
                    <a href="/wiki/Retsuden_1">
                        Retsuden One
                    </a>
                </li>
            </ul>
        </body>
    </html>
    """

    report = (
        inspect_chapter_index
        .inspect_numbered_section(
            html=html,
            section_id="Tankōbon",
            subsection_ids=[
                "Part_I",
                "Part_II",
            ],
        )
    )

    assert report["entry_count"] == 2
    assert (
        report["duplicate_chapter_count"]
        == 0
    )

    assert [
        entry["chapter_number"]
        for entry in report["entries"]
    ] == [
        1,
        700,
    ]


def test_stops_at_next_h2_section():
    html = """
    <html>
        <body>
            <h2>
                <span id="Tankōbon">
                    Tankōbon
                </span>
            </h2>

            <ul>
                <li>
                    001.
                    <a href="/wiki/Main_1">
                        Main Chapter
                    </a>
                </li>
            </ul>

            <h2>
                <span id="Spin-offs">
                    Spin-offs
                </span>
            </h2>

            <ul>
                <li>
                    002.
                    <a href="/wiki/Spin_2">
                        Spin-off Chapter
                    </a>
                </li>
            </ul>
        </body>
    </html>
    """

    report = (
        inspect_chapter_index
        .inspect_numbered_section(
            html=html,
            section_id="Tankōbon",
        )
    )

    assert report["unique_chapter_count"] == 1
    assert report["maximum_chapter"] == 1


def test_reports_missing_and_duplicate_numbers():
    html = """
    <html>
        <body>
            <h2>
                <span id="Tankōbon">
                    Tankōbon
                </span>
            </h2>

            <ul>
                <li>
                    001.
                    <a href="/wiki/Chapter_1">
                        One
                    </a>
                </li>
                <li>
                    003.
                    <a href="/wiki/Chapter_3A">
                        Three A
                    </a>
                </li>
                <li>
                    003.
                    <a href="/wiki/Chapter_3B">
                        Three B
                    </a>
                </li>
            </ul>
        </body>
    </html>
    """

    report = (
        inspect_chapter_index
        .inspect_numbered_section(
            html=html,
            section_id="Tankōbon",
        )
    )

    assert (
        report["missing_chapter_numbers"]
        == [2]
    )
    assert (
        report["duplicate_chapter_numbers"]
        == [3]
    )


def test_missing_section_raises():
    html = """
    <html>
        <body></body>
    </html>
    """

    try:
        (
            inspect_chapter_index
            .inspect_numbered_section(
                html=html,
                section_id="Tankōbon",
            )
        )

    except ValueError as error:
        assert (
            str(error)
            == 'Index section not found: "Tankōbon"'
        )

    else:
        raise AssertionError(
            "Expected ValueError."
        )