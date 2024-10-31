import random

from soundcloud import SoundCloud


class SoundCloudPlaylistManager:
    __title__ = "UNPLAYED TRACKS"

    def __init__(
        self,
        token: str,
        base_playlist_id: int = -1,
        played_playlist_ids=None,
        title: str = None,
    ):
        if played_playlist_ids is None:
            played_playlist_ids = []
        self.sc = SoundCloud(auth_token=token)
        self.base_playlist_id = base_playlist_id
        self.played_playlist_ids = played_playlist_ids

        if title:
            self.__title__ = title

    def check_token(self) -> bool:
        return self.sc.is_auth_token_valid()

    def get_track_ids(self, playlist_id: int) -> list:
        return [track.id for track in self.sc.get_playlist(playlist_id).tracks]

    def get_unplayed_track_ids(self) -> list:
        base_track_ids = self.get_track_ids(self.base_playlist_id)
        played_track_ids = [
            track_id
            for playlist_id in self.played_playlist_ids
            for track_id in self.get_track_ids(playlist_id)
        ]
        return [
            track_id for track_id in base_track_ids if track_id not in played_track_ids
        ]

    def get_track_ids_from_playlist_ids(self, playlist_ids: list) -> list:
        return [
            track_id
            for playlist_id in playlist_ids
            for track_id in self.get_track_ids(playlist_id)
        ]

    def create_unplayed_tracks(self) -> None:
        unplayed_track_ids = self.get_unplayed_track_ids()
        self.sc.post_playlist("private", self.__title__, unplayed_track_ids)

    def create_playlist_from_playlist_ids(self, playlist_ids: list) -> None:
        track_ids = self.get_track_ids_from_playlist_ids(playlist_ids)
        self.sc.post_playlist("private", self.__title__, track_ids)

    def generate_random_playlist(self, tracks_count: int = 30) -> None:
        unplayed_track_ids = self.get_unplayed_track_ids()
        random.shuffle(unplayed_track_ids)

        self.sc.post_playlist(
            "private", self.__title__, unplayed_track_ids[:tracks_count]
        )

    def delete_playlist(self, playlist_id: int) -> None:
        self.sc.delete_playlist(playlist_id)

    def get_me(self):
        return self.sc.get_me()

    def get_user_playlists(self, user_id: int) -> list:
        return self.sc.get_user_playlists(user_id)

    def get_my_playlists(self) -> list:
        return self.get_user_playlists(self.sc.get_me().id)

    def get_user_tracks(self, user_id: int) -> list:
        return self.sc.get_user_tracks(user_id)

    def get_my_tracks(self) -> list:
        return self.get_user_tracks(self.sc.get_me().id)
