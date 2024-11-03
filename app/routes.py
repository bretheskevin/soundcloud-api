from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from soundcloud import BasicAlbumPlaylist, User, BasicTrack

from .api_responses.health_check_response import HealthCheckResponse
from .api_responses.api_response import ApiResponse
from .sc_playlist_manager import (
    SoundCloudPlaylistManager,
    PlaylistCreateOptions,
    PlaylistManagerError,
    InvalidTokenError,
    TrackLimitExceededError,
)
from .api_requests.unplayed_tracks_request import UnplayedTracksRequest
from .api_requests.merge_playlists_request import MergePlaylistsRequest
from .api_requests.random_playlist_request import RandomPlaylistRequest

router = APIRouter(prefix="/api/v1/sdpm", tags=["soundcloud"])

async def get_playlist_manager(
        token: str = Query(..., description="SoundCloud API token")
) -> SoundCloudPlaylistManager:
    """
    Dependency to create and validate SoundCloudPlaylistManager instance.
    """
    try:
        return SoundCloudPlaylistManager(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@router.get("/users/me", response_model=User)
async def get_current_user(
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Get current user information."""
    try:
        return manager.get_user()
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=User)
async def get_user(
        user_id: int,
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Get user information by ID."""
    try:
        return manager.get_user(user_id)
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/playlists", response_model=List[BasicAlbumPlaylist])
async def get_playlists(
        user_id: Optional[int] = Query(None, description="User ID (optional, defaults to current user)"),
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Get playlists for a user."""
    try:
        return manager.get_playlists(user_id)
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tracks", response_model=List[BasicTrack])
async def get_tracks(
        user_id: Optional[int] = Query(None, description="User ID (optional, defaults to current user)"),
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Get tracks for a user."""
    try:
        return manager.get_tracks(user_id)
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/token/validate", response_model=ApiResponse)
async def validate_token(
        token: str = Query(..., description="SoundCloud API token to validate")
):
    """
    Validate a SoundCloud API token.

    Returns:
        ApiResponse with success status and appropriate message
    """
    try:
        manager = SoundCloudPlaylistManager(token=token)
        return ApiResponse(
            success=True,
            message="Token is valid"
        )
    except InvalidTokenError as e:
        return ApiResponse(
            success=False,
            message=str(e)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/playlists/unplayed", response_model=ApiResponse)
async def create_unplayed_tracks_playlist(
        request: UnplayedTracksRequest = Body(...),
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Create a playlist of unplayed tracks."""
    try:
        options = PlaylistCreateOptions(
            title=request.title,
            visibility=request.visibility
        )
        return manager.create_unplayed_tracks_playlist(
            base_playlist_id=request.base_playlist_id,
            played_playlist_ids=request.played_playlist_ids,
            options=options
        )
    except TrackLimitExceededError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/playlists/merge", response_model=ApiResponse)
async def merge_playlists(
        request: MergePlaylistsRequest = Body(...),
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Merge multiple playlists into a new playlist."""
    try:
        options = PlaylistCreateOptions(
            title=request.title,
            visibility=request.visibility
        )
        return manager.merge_playlists(
            playlist_ids=request.playlist_ids,
            options=options
        )
    except TrackLimitExceededError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/playlists/random", response_model=ApiResponse)
async def create_random_playlist(
        request: RandomPlaylistRequest = Body(...),
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Create a playlist with random tracks from a base playlist."""
    try:
        options = PlaylistCreateOptions(
            title=request.title,
            visibility=request.visibility
        )
        return manager.create_random_playlist(
            base_playlist_id=request.base_playlist_id,
            track_count=request.track_count,
            options=options
        )
    except TrackLimitExceededError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/playlists/{playlist_id}", response_model=ApiResponse)
async def delete_playlist(
        playlist_id: int,
        manager: SoundCloudPlaylistManager = Depends(get_playlist_manager)
):
    """Delete a playlist."""
    try:
        return manager.delete_playlist(playlist_id)
    except PlaylistManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

router.description = """
SoundCloud Playlist Manager API

This API provides endpoints for managing SoundCloud playlists, including:
- User information retrieval
- Playlist management
- Track management
- Playlist creation and modification
"""

router.tags = [{
    "name": "soundcloud",
    "description": "SoundCloud playlist management operations"
}]
