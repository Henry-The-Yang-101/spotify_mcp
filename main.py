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

@mcp.tool()
async def get_user_profile():
    """
    Retrieve the current user's profile information.
    """
    try:
        user = sp.current_user()
        return f"User: {user['display_name']}, Email: {user.get('email', 'N/A')}, Country: {user['country']}, Subscription: {user.get('product', 'N/A')}"
    except spotipy.exceptions.SpotifyException as e:
        return f"Failed to retrieve user profile: {str(e)}"

@mcp.tool()
async def get_user_top_items(item_type: str = "tracks", time_range: str = "medium_term", limit: int = 10):
    """
    Fetch the user's top items (artists or tracks) over a specified time range.
    """
    if item_type not in ["tracks", "artists"]:
        return "Invalid item_type. Choose 'tracks' or 'artists'."
    try:
        top_items = sp.current_user_top_items(time_range=time_range, limit=limit, type=item_type)
        names = [item['name'] for item in top_items[item_type]]
        return f"Top {item_type}: {', '.join(names)}"
    except spotipy.exceptions.SpotifyException as e:
        return f"Failed to retrieve top {item_type}: {str(e)}"

@mcp.tool()
async def get_saved_tracks(limit: int = 10):
    """
    Retrieve tracks saved to the user's library.
    """
    try:
        saved = sp.current_user_saved_tracks(limit=limit)
        tracks = [f"{item['track']['name']} by {', '.join(artist['name'] for artist in item['track']['artists'])}" for item in saved['items']]
        return f"Saved tracks: {', '.join(tracks)}"
    except spotipy.exceptions.SpotifyException as e:
        return f"Failed to retrieve saved tracks: {str(e)}"

if __name__ == "__main__":
    mcp.run()