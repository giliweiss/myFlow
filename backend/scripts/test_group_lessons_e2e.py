"""End-to-end smoke test for group lessons phase."""

import sys
import uuid

import httpx

BASE_URL = "http://127.0.0.1:8001"


def request(method: str, path: str, **kwargs):
    response = httpx.request(method, f"{BASE_URL}{path}", timeout=30.0, **kwargs)
    print(f"{method} {path} -> {response.status_code}")
    if response.status_code >= 400:
        print(response.text)
        response.raise_for_status()
    return response.json()


def main():
    groups = request("GET", "/groups")
    if not groups["groups"]:
        print("No groups found; create a group in Swagger first")
        sys.exit(1)

    group_id = groups["groups"][0]["id"]
    print(f"Using group {group_id}")

    suffix = uuid.uuid4().hex[:8]
    member_one = request(
        "POST",
        f"/groups/{group_id}/members",
        json={"name": f"Test Member A {suffix}"},
    )
    member_two = request(
        "POST",
        f"/groups/{group_id}/members",
        json={"name": f"Test Member B {suffix}"},
    )

    group = next(group for group in groups["groups"] if group["id"] == group_id)
    exercises = request("GET", "/exercises")

    level_rank = {"beginner": 0, "intermediate": 1, "advanced": 2}
    group_rank = level_rank[group["level"]]
    available_equipment = set(group.get("available_equipment") or ["mat"])

    suitable_exercises = []
    for exercise in exercises["exercises"]:
        if level_rank[exercise["difficulty_level"]] > group_rank:
            continue
        possible_equipment = exercise.get("possible_equipment") or []
        if possible_equipment and not available_equipment.intersection(possible_equipment):
            continue
        suitable_exercises.append(exercise)
        if len(suitable_exercises) == 2:
            break

    if len(suitable_exercises) < 2:
        print("Not enough suitable exercises for this group")
        sys.exit(1)

    exercise_ids = [exercise["id"] for exercise in suitable_exercises]

    lesson = request(
        "POST",
        f"/groups/{group_id}/lessons",
        json={
            "title": "E2E Test Lesson",
            "lesson_exercises": [
                {
                    "exercise_id": exercise_ids[0],
                    "order_index": 0,
                    "section": "warmup",
                    "planned_duration_seconds": 300,
                },
                {
                    "exercise_id": exercise_ids[1],
                    "order_index": 1,
                    "section": "main",
                    "planned_duration_seconds": 600,
                },
            ],
        },
    )
    lesson_id = lesson["id"]
    assert lesson["status"] == "upcoming"
    assert len(lesson["lesson_exercises"]) == 2

    exercise_item_id = lesson["lesson_exercises"][0]["id"]
    completed = request(
        "PATCH",
        f"/lessons/{lesson_id}",
        json={
            "status": "completed",
            "actual_duration_minutes": 55,
            "exercise_completions": [
                {
                    "id": exercise_item_id,
                    "completion_status": "completed",
                    "actual_duration_seconds": 280,
                }
            ],
        },
    )
    assert completed["status"] == "completed"
    assert len(completed["attendance"]) >= 2

    request(
        "PATCH",
        f"/lessons/{lesson_id}/attendance",
        json={
            "attendance": [
                {"member_id": member_one["id"], "registered": True, "attended": True},
                {"member_id": member_two["id"], "registered": True, "attended": False},
            ]
        },
    )

    assert completed["status"] == "completed"

    review = request(
        "POST",
        f"/lessons/{lesson_id}/review",
        json={
            "perceived_difficulty": 3,
            "group_response": "appropriate",
            "goals_achieved": ["core strength"],
            "issues": ["one member arrived late"],
            "instructor_notes": "Good session",
        },
    )
    assert review["issues"] == ["one member arrived late"]

    updated_review = request(
        "POST",
        f"/lessons/{lesson_id}/review",
        json={
            "perceived_difficulty": 4,
            "group_response": "too_hard",
            "goals_achieved": ["core strength", "balance"],
            "issues": ["timing"],
        },
    )
    assert updated_review["perceived_difficulty"] == 4

    history = request("GET", f"/groups/{group_id}/lessons")
    assert any(item["id"] == lesson_id and item["has_review"] for item in history["lessons"])

    print("E2E smoke test passed")


if __name__ == "__main__":
    main()
