"""implement the api routes"""
from fastapi import APIRouter
from dataclasses import dataclass
from app.controllers import users


@dataclass
class Router:
    """this class implements the api routes"""

    router = APIRouter()
    router.include_router(users.router)
