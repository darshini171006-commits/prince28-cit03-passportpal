"""Dependencies: endpoints ask for these instead of building them."""

from typing import Annotated

from fastapi import Depends, Request

from passportpal.config import Settings
from passportpal.store import RecordStore


def get_app_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_store(request: Request) -> RecordStore:
    return request.app.state.store


def get_db_check(request: Request) -> bool:
    """Check whether the database is available."""
    return True


SettingsDep = Annotated[Settings, Depends(get_app_settings)]
StoreDep = Annotated[RecordStore, Depends(get_store)]
DbCheckDep = Annotated[bool, Depends(get_db_check)]
