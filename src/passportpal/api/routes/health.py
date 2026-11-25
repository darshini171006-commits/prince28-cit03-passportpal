from fastapi import APIRouter, Response

from passportpal.api.deps import DbCheckDep, SettingsDep

router = APIRouter(tags=["health"])


@router.api_route("/health", methods=["GET", "HEAD"])
def health(settings: SettingsDep) -> dict[str, str]:
    """Liveness: is the process alive?"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
    }


@router.get("/ready")
def ready(db_ok: DbCheckDep, response: Response) -> dict:
    """Readiness: can this instance access the database?"""
    checks = {"database": db_ok}
    ok = all(checks.values())

    if not ok:
        response.status_code = 503

    return {
        "status": "ready" if ok else "not_ready",
        "checks": checks,
    }
