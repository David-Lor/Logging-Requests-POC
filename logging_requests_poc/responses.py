"""RESPONSES
HTTP Responses
"""

# # Native # #
import json
from typing import Optional

# # Installed # #
# noinspection PyPackageRequirements
from starlette.responses import Response

__all__ = ("Responses",)


class PatchedResponse(Response):
    def __init__(self, content, media_type="application/json", **kwargs):
        if not isinstance(content, str):
            content = json.dumps(content)
        super().__init__(content=content, media_type=media_type, **kwargs)


class Responses:
    @staticmethod
    def created(data: str):
        return PatchedResponse(
            content=data,
            status_code=201
        )

    @staticmethod
    def no_content(content: Optional[str] = None):
        return PatchedResponse(
            content=content or {"status": "OK"},
            status_code=204
        )

    @staticmethod
    def ok(content: Optional[str] = None):
        return PatchedResponse(
            content=content or {"status": "OK"},
            status_code=200
        )
