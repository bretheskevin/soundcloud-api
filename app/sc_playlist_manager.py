from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from soundcloud import SoundCloud, BasicAlbumPlaylist, User, BasicTrack

from .api_responses.api_response import ApiResponse

class PlaylistVisibility(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"

@dataclass
class PlaylistCreateOptions:
    title: str
    visibility: PlaylistVisibility = PlaylistVisibility.PRIVATE
    track_limit: int = 500


class PlaylistManagerError(Exception):
    """Base exception for playlist manager errors"""
    pass


class TrackLimitExceededError(PlaylistManagerError):
    """Raised when track limit is exceeded"""
    pass


class InvalidTokenError(PlaylistManagerError):
    """Raised when SoundCloud token is invalid"""
    pass


class SoundCloudPlaylistManager:
    """
    Manages SoundCloud playlist operations with improved error handling,
    type safety, and separation of concerns.
    """

    def __init__(self, token: str):
        """
        Initialize the playlist manager with a SoundCloud client.

        Args:
            token: SoundCloud authentication token

        Raises:
            InvalidTokenError: If the provided token is invalid
        """
        self._validate_token(token)
        self._client = SoundCloud(auth_token=token)

    def _validate_token(self, token: str) -> None:
        """Validate the SoundCloud authentication token."""
        try:
            client = SoundCloud(auth_token=token)
            if not client.is_auth_token_valid():
                raise InvalidTokenError("Invalid SoundCloud authentication token")
        except Exception as e:
            raise InvalidTokenError(f"Failed to validate token: {str(e)}")

    def _get_track_ids(self, playlist_id: int) -> List[int]:
        """
        Get track IDs from a playlist.

        Args:
            playlist_id: ID of the playlist

        Returns:
            List of track IDs
        """
        try:
            playlist = self._client.get_playlist(playlist_id)
            return [track.id for track in playlist.tracks]
        except Exception as e:
            raise PlaylistManagerError(f"Failed to get track IDs: {str(e)}")

    def _create_playlist(self, options: PlaylistCreateOptions, track_ids: List[int]) -> ApiResponse:
        """
        Create a new playlist with the given tracks.

        Args:
            options: Playlist creation options
            track_ids: List of track IDs to add to the playlist

        Returns:
            ApiResponse indicating success/failure

        Raises:
            TrackLimitExceededError: If track limit is exceeded
        """
        if len(track_ids) > options.track_limit:
            raise TrackLimitExceededError(
                f"Track limit exceeded: {len(track_ids)} tracks (limit: {options.track_limit})"
            )

        try:
            self._client.post_playlist(
                options.visibility.value,
                options.title,
                track_ids
            )
            return ApiResponse(
                success=True,
                message="Playlist created successfully. Check your playlists :)"
            )
        except Exception as e:
            return ApiResponse(
                success=False,
                message=f"Failed to create playlist: {str(e)}"
            )

    def get_user(self, user_id: Optional[int] = None) -> User:
        """
        Get user information.

        Args:
            user_id: Optional user ID. If None, returns current user

        Returns:
            User information
        """
        try:
            if user_id is None:
                return self._client.get_me()
            return self._client.get_user(user_id)
        except Exception as e:
            raise PlaylistManagerError(f"Failed to get user: {str(e)}")

    def get_playlists(self, user_id: Optional[int] = None) -> List[BasicAlbumPlaylist]:
        """
        Get user's playlists.

        Args:
            user_id: Optional user ID. If None, returns current user's playlists

        Returns:
            List of playlists
        """
        try:
            user_id = user_id or self.get_user().id
            return self._client.get_user_playlists(user_id)
        except Exception as e:
            raise PlaylistManagerError(f"Failed to get playlists: {str(e)}")

    def get_tracks(self, user_id: Optional[int] = None) -> List[BasicTrack]:
        """
        Get user's tracks.

        Args:
            user_id: Optional user ID. If None, returns current user's tracks

        Returns:
            List of tracks
        """
        try:
            user_id = user_id or self.get_user().id
            return self._client.get_user_tracks(user_id)
        except Exception as e:
            raise PlaylistManagerError(f"Failed to get tracks: {str(e)}")

    def create_unplayed_tracks_playlist(
            self,
            base_playlist_id: int,
            played_playlist_ids: List[int],
            options: PlaylistCreateOptions
    ) -> ApiResponse:
        """
        Create a playlist of unplayed tracks.

        Args:
            base_playlist_id: ID of the base playlist
            played_playlist_ids: List of playlist IDs containing played tracks
            options: Playlist creation options

        Returns:
            ApiResponse indicating success/failure
        """
        try:
            base_tracks = set(self._get_track_ids(base_playlist_id))
            played_tracks = set()

            for playlist_id in played_playlist_ids:
                played_tracks.update(self._get_track_ids(playlist_id))

            unplayed_tracks = list(base_tracks - played_tracks)
            return self._create_playlist(options, unplayed_tracks)

        except Exception as e:
            return ApiResponse(
                success=False,
                message=f"Failed to create unplayed tracks playlist: {str(e)}"
            )

    def merge_playlists(
            self,
            playlist_ids: List[int],
            options: PlaylistCreateOptions
    ) -> ApiResponse:
        """
        Merge multiple playlists into a new playlist.

        Args:
            playlist_ids: List of playlist IDs to merge
            options: Playlist creation options

        Returns:
            ApiResponse indicating success/failure
        """
        try:
            all_tracks = set()
            for playlist_id in playlist_ids:
                all_tracks.update(self._get_track_ids(playlist_id))

            return self._create_playlist(options, list(all_tracks))
        except TrackLimitExceededError as e:
            return ApiResponse(
                success=False,
                message="playlistTrackLimitExceeded"
            )
        except Exception as e:
            return ApiResponse(
                success=False,
                message=f"Failed to merge playlists: {str(e)}"
            )

    def create_random_playlist(
            self,
            base_playlist_id: int,
            track_count: int,
            options: PlaylistCreateOptions
    ) -> ApiResponse:
        """
        Create a playlist with random tracks from a base playlist.

        Args:
            base_playlist_id: ID of the base playlist
            track_count: Number of tracks to include
            options: Playlist creation options

        Returns:
            ApiResponse indicating success/failure
        """
        try:
            track_ids = self._get_track_ids(base_playlist_id)

            if track_count > len(track_ids):
                return ApiResponse(
                    success=False,
                    message=f"Requested track count ({track_count}) exceeds available tracks ({len(track_ids)})"
                )

            random.shuffle(track_ids)
            selected_tracks = track_ids[:track_count]

            return self._create_playlist(options, selected_tracks)

        except Exception as e:
            return ApiResponse(
                success=False,
                message=f"Failed to create random playlist: {str(e)}"
            )

    def delete_playlist(self, playlist_id: int) -> ApiResponse:
        """
        Delete a playlist.

        Args:
            playlist_id: ID of the playlist to delete

        Returns:
            ApiResponse indicating success/failure
        """
        try:
            self._client.delete_playlist(playlist_id)
            return ApiResponse(
                success=True,
                message=f"Playlist {playlist_id} deleted successfully"
            )
        except Exception as e:
            return ApiResponse(
                success=False,
                message=f"Failed to delete playlist: {str(e)}"
            )
