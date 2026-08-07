from fastapi import APIRouter

router = APIRouter()


@router.post("")
def create_review():
    """Create a lesson review."""
    return {"review": {}, "message": "create review - to be implemented in Phase 1"}
