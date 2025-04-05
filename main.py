from mcp.server.fastmcp import FastMCP
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("spotify")

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SCOPE = "user-read-currently-playing," \
        "user-read-playback-state," \
        "app-remote-control,streaming," \
        "playlist-read-private,playlist-read-collaborative," \
        "playlist-modify-private," \
        "playlist-modify-public," \
        "user-read-playback-position," \
        "user-top-read," \
        "user-read-recently-played," \
        "user-library-modify," \
        "user-library-read"

# Initialize Spotipy client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

@mcp.tool()
async def play():
    """
    Start or resume playback.
    """
    sp.start_playback()
    return "Playback started."

@mcp.tool()
async def pause():
    """
    Pause playback.
    """
    sp.pause_playback()
    return "Playback paused."

@mcp.tool()
async def next_track():
    """
    Skip to the next track.
    """
    sp.next_track()
    return "Skipped to next track."

@mcp.tool()
async def previous_track():
    """
    Skip to the previous track.
    """
    sp.previous_track()
    return "Skipped to previous track."

@mcp.tool()
async def search_track(query: str):
    """
    Search for a track by name.
    """
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        return f"Found track: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}"
    else:
        return "No track found."

@mcp.tool()
async def play_song(query: str):
    """
    Search for a song and start playback of the first result.
    """
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        return f"Now playing: {results['tracks']['items'][0]['name']} by {', '.join(artist['name'] for artist in results['tracks']['items'][0]['artists'])}"
    else:
        return "No track found to play."

@mcp.tool()
async def get_current_track():
    """
    Get the currently playing track.
    """
    current = sp.current_playback()
    if current and current.get("item"):
        track = current["item"]
        artists = ', '.join(artist["name"] for artist in track["artists"])
        return f"Currently playing: {track['name']} by {artists}"
    else:
        return "No track is currently playing."

@mcp.tool()
async def add_to_queue(uri: str):
    """
    Add a track to the playback queue.
    """
    try:
        sp.add_to_queue(uri)
        return f"Track with URI {uri} added to queue."
    except spotipy.exceptions.SpotifyException as e:
        return f"Failed to add to queue: {str(e)}"

if __name__ == "__main__":
    mcp.run()