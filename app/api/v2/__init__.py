"""API v2 endpoints - Content Distribution System."""

from fastapi import APIRouter
from .templates import router as templates_router
from .content import router as content_router
from .distribution import router as distribution_router

router = APIRouter(prefix="/v2", tags=["v2"])

router.include_router(templates_router)
router.include_router(content_router)
router.include_router(distribution_router)
