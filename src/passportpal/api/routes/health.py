"""Health and readiness endpoints."""

from fastapi import APIRouter, Response

from passportpal.api.deps import DbCheckDep, SettingsDep

router = APIRouter(tags=["health"])


@router.api_route("/health", methods=["GET", "HEAD"])
def health(settings: SettingsDep) -> dict[str, str]:
    """Liveness: check whether the application process is alive."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
        "version": settings.git_sha,
    }


@router.get("/ready")
async def ready(
    db_ok: DbCheckDep,
    response: Response,
) -> dict:
    """Readiness: check whether the application can access the database."""
    checks = {"database": db_ok}
    ok = all(checks.values())

    if not ok:
        response.status_code = 503

    return {
        "status": "ready" if ok else "not_ready",
        "checks": checks,
    }
