from typing import List

from fastapi import APIRouter, HTTPException, Query, Body
from soundcloud import BasicAlbumPlaylist, User, BasicTrack

from .api_responses.check_token_response import CheckTokenResponse
from .api_responses.health_check_response import HealthCheckResponse
from .api_responses.message_response import MessageResponse
from .sc_playlist_manager import SoundCloudPlaylistManager

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    return {"status": "healthy"}


@router.get("/check-token", response_model=CheckTokenResponse)
def check_token(
    token: str = Query("", description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return {"is_valid": manager.check_token()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=User)
def get_me(
    token: str = Query("", description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return manager.get_me()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user-playlists/{user_id}", response_model=List[BasicAlbumPlaylist])
def get_user_playlists(
    user_id: int,
    token: str = Query("", description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return manager.get_user_playlists(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-playlists", response_model=List[BasicAlbumPlaylist])
def get_my_playlists(
    token: str = Query("", description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return manager.get_my_playlists()
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
    played_playlist_ids: List[int] = Query(
        ..., description="List of played playlist IDs"
    ),
):
    try:
        manager = SoundCloudPlaylistManager(
            token=token,
            base_playlist_id=base_playlist_id,
            played_playlist_ids=played_playlist_ids,
        )
        return manager.get_unplayed_track_ids()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-tracks/{user_id}", response_model=list[BasicTrack])
def get_user_tracks(
    user_id: int,
    token: str = Query(..., description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return manager.get_user_tracks(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-tracks", response_model=list[BasicTrack])
def get_my_tracks(
    token: str = Query(..., description="SoundCloud API token"),
):
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return manager.get_my_tracks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-unplayed-tracks", response_model=MessageResponse)
def create_unplayed_tracks(
    token: str = Query(..., description="SoundCloud API token"),
    base_playlist_id: int = Body(..., description="Base playlist ID"),
    played_playlist_ids: List[int] = Body(
        ..., description="List of played playlist IDs"
    ),
    title: str = Body("Unplayed Tracks", description="Playlist title"),
):
    try:
        manager = SoundCloudPlaylistManager(
            token=token,
            base_playlist_id=base_playlist_id,
            played_playlist_ids=played_playlist_ids,
            title=title,
        )
        manager.create_unplayed_tracks()
        return {
            "message": "Unplayed tracks playlist created successfully. Check you playlists :)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-random-playlist", response_model=MessageResponse)
def generate_random_playlist(
    token: str = Query(..., description="SoundCloud API token"),
    playlist_id: int = Body(
        ..., description="Playlist ID from which the random playlist will be generated"
    ),
    tracks_count: int = Body(
        30, description="Number of tracks in the random playlist"
    ),
):
    try:
        manager = SoundCloudPlaylistManager(token=token, base_playlist_id=playlist_id)
        manager.generate_random_playlist(tracks_count=tracks_count)
        return {
            "message": "Random playlist generated successfully. Check you playlists :)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/playlists/{playlist_id}", response_model=MessageResponse)
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
