from typing import List
from .playlist_create_request import PlaylistCreateRequest

class UnplayedTracksRequest(PlaylistCreateRequest):
    base_playlist_id: int
    played_playlist_ids: List[int]
