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

Swagger documentatin at `http://localhost:8000/docs`

## Error Handling

All endpoints will return appropriate HTTP status codes and error messages in case of failures.

## Authentication

Most of endpoints require a SoundCloud API token to be provided as a query parameter `token`.

## Note

Make sure to keep your SoundCloud API token secure and do not share it publicly.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
