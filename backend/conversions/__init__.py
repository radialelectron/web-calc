"""Unit-conversion API. Each module in this package registers its own routes."""

import importlib
import pkgutil

from fastapi import APIRouter

router = APIRouter(prefix="/api/convert", tags=["conversion"])

for _module in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{_module.name}")
