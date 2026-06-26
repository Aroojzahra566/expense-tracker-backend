from fastapi import APIRouter

from app import storage

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
def list_categories() -> list[str]:
    return storage.get_categories()
