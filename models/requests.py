"""Совместимое имя сущности «Заявка» для практических работ.

В проекте заявка исторически называется Application; этот alias сохраняет
совместимость существующего консольного приложения.
"""
from .applications import Application

Request = Application

__all__ = ["Request"]
