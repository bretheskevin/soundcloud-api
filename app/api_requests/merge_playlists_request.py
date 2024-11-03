from typing import List
from .playlist_create_request import PlaylistCreateRequest

class MergePlaylistsRequest(PlaylistCreateRequest):
    playlist_ids: List[int]
