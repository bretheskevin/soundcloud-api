from typing import List

from fastapi import APIRouter, HTTPException, Query

from .sc_playlist_manager import SoundCloudPlaylistManager

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/check-token")
def check_token(
        token: str = Query("", description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return manager.check_token()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/playlists/{playlist_id}/track-ids", response_model=List[int])
def get_track_ids(
        playlist_id: int,
        token: str = Query(..., description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return manager.get_track_ids(playlist_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/unplayed-track-ids", response_model=List[int])
def get_unplayed_track_ids(
        token: str = Query(..., description="SoundCloud API token"),
        base_playlist_id: int = Query(..., description="Base playlist ID"),
        played_playlist_ids: List[int] = Query(..., description="List of played playlist IDs")
):
    try:
        manager = SoundCloudPlaylistManager(
            token=token,
            base_playlist_id=base_playlist_id,
            played_playlist_ids=played_playlist_ids
        )
        return manager.get_udnplayed_track_ids()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-unplayed-tracks")
def create_unplayed_tracks(
        token: str = Query(..., description="SoundCloud API token"),
        base_playlist_id: int = Query(..., description="Base playlist ID"),
        played_playlist_ids: List[int] = Query(..., description="List of played playlist IDs"),
        title: str = Query("Unplayed Tracks", description="Playlist title")
):
    try:
        manager = SoundCloudPlaylistManager(
            token=token,
            base_playlist_id=base_playlist_id,
            played_playlist_ids=played_playlist_ids,
            title=title
        )
        manager.create_unplayed_tracks()
        return {"message": "Unplayed tracks playlist created successfully. Check you playlists :)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-random-playlist")
def generate_random_playlist(
        token: str = Query(..., description="SoundCloud API token"),
        playlist_id: int = Query(..., description="Playlist ID from which the random playlist will be generated"),
        tracks_count: int = Query(30, description="Number of tracks in the random playlist")
):
    try:
        manager = SoundCloudPlaylistManager(
            token=token,
            base_playlist_id=playlist_id
        )
        manager.generate_random_playlist(tracks_count=tracks_count)
        return {"message": "Random playlist generated successfully. Check you playlists :)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/playlists/{playlist_id}")
def delete_playlist(
        playlist_id: int,
        token: str = Query(..., description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(
            token=token,
        )
        manager.delete_playlist(playlist_id)
        return {"message": f"Playlist {playlist_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
