# SoundCloud Playlist Manager

This project is a FastAPI-based application that manages SoundCloud playlists. It provides various functionalities such as retrieving track IDs, creating playlists of unplayed tracks, generating random playlists, and more.

## Getting Started

### Prerequisites

- Python 3.7+
- pip

OR

- Docker

### Installation (If you're not using Docker)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/soundcloud-playlist-manager.git
   cd soundcloud-playlist-manager
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   ```

### Running the Application

To run the application, use the following command:

```
uvicorn main:app --reload
```

OR

1. Build the Docker image:
   ```
   docker compose build
   ```

2. Run the Docker container:
   ```
   docker compose up
   ```

The API will be available at `http://localhost:8000`.

## API Documentation

### Health Check

- **GET** `/health`
    - Description: Check the health status of the API
    - Response: `{"status": "healthy"}`

### Get Track IDs

- **GET** `/playlists/{playlist_id}/track-ids`
    - Description: Retrieve track IDs from a specific playlist
    - Parameters:
        - `playlist_id` (path): ID of the playlist
        - `token` (query): SoundCloud API token
    - Response: List of track IDs

### Get Unplayed Track IDs

- **GET** `/unplayed-track-ids`
    - Description: Retrieve unplayed track IDs
    - Parameters:
        - `token` (query): SoundCloud API token
        - `base_playlist_id` (query): Base playlist ID
        - `played_playlist_ids` (query): List of played playlist IDs
    - Response: List of unplayed track IDs

### Create Unplayed Tracks Playlist

- **POST** `/create-unplayed-tracks`
    - Description: Create a playlist of unplayed tracks
    - Parameters:
        - `token` (query): SoundCloud API token
        - `base_playlist_id` (query): Base playlist ID
        - `played_playlist_ids` (query): List of played playlist IDs
        - `title` (query, optional): Playlist title (default: "Unplayed Tracks")
    - Response: Success message

### Generate Random Playlist

- **POST** `/generate-random-playlist`
    - Description: Generate a random playlist from an existing playlist
    - Parameters:
        - `token` (query): SoundCloud API token
        - `playlist_id` (query): ID of the source playlist
        - `tracks_count` (query, optional): Number of tracks in the random playlist (default: 30)
    - Response: Success message

### Delete Playlist

- **DELETE** `/playlists/{playlist_id}`
    - Description: Delete a specific playlist
    - Parameters:
        - `playlist_id` (path): ID of the playlist to delete
        - `token` (query): SoundCloud API token
    - Response: Success message

## Error Handling

All endpoints will return appropriate HTTP status codes and error messages in case of failures.

## Authentication

All endpoints require a SoundCloud API token to be provided as a query parameter `token`.

## Note

Make sure to keep your SoundCloud API token secure and do not share it publicly.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
