from pydantic import BaseModel
from ..sc_playlist_manager import PlaylistVisibility

class PlaylistCreateRequest(BaseModel):
    """Base class for playlist creation requests."""
    title: str
    visibility: PlaylistVisibility = PlaylistVisibility.PRIVATE
