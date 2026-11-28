from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from passportpal.api.deps import RepoDep

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
async def list_documents(
    repo: RepoDep,
    q: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> dict:
    total, items = await repo.list(
        q=q,
        filters={},
        limit=limit,
        offset=offset,
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


@router.get("/{doc_id}")
async def get_document(doc_id: str, repo: RepoDep) -> dict:
    record = await repo.get(doc_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"No document with id '{doc_id}'.",
        )

    return record
