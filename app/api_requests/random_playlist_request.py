from .playlist_create_request import PlaylistCreateRequest

class RandomPlaylistRequest(PlaylistCreateRequest):
    base_playlist_id: int
    track_count: int = 30
