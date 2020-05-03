from typing import List, TypedDict


class TokenDetails(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: List[str]
    expires_at: float
