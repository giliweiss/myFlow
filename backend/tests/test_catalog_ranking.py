from app.services.catalog_ranking import limit_preparation_catalog_for_llm


def make_exercise(name_en: str, exercise_id: str) -> dict:
    return {
        "id": exercise_id,
        "name_en": name_en,
        "name_he": name_en,
        "canonical_key": name_en.lower().replace(" ", "_"),
        "aliases_en": [],
        "aliases_he": [],
        "body_focus": ["core"],
    }


def test_limit_preparation_catalog_prefers_intention_matches():
    catalog = [
        make_exercise("Teaser 1", "1"),
        make_exercise("Roll Up", "2"),
        make_exercise("Alpha", "3"),
        make_exercise("Beta", "4"),
    ]

    limited = limit_preparation_catalog_for_llm(
        "Prepare the group for Teaser",
        catalog,
        limit=2,
    )

    assert len(limited) == 2
    assert limited[0]["name_en"] == "Teaser 1"
