# 🎧 Spotify MCP Server

This is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that connects to the Spotify Web API and exposes a set of playback and search tools to AI clients like Claude Desktop.

Built using:
- [`spotipy`](https://spotipy.readthedocs.io/) — lightweight Python wrapper for the Spotify Web API
- [`mcp`](https://pypi.org/project/mcp/) — for exposing tool functions over the Model Context Protocol
- `FastMCP` — for rapid server implementation
- `.env` and `dotenv` — for securely managing credentials

---

## 🚀 Features

This server exposes the following Spotify tools:

- `play` — Start or resume playback
- `pause` — Pause playback
- `next_track` — Skip to the next song
- `previous_track` — Go back to the previous song
- `search_track(query: str)` — Search for a track by name
- `get_current_track()` — Get info on the currently playing song
- `add_to_queue(uri: str)` — Add a track to the queue using its Spotify URI

---

## 🔧 Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/spotify_mcp.git
cd spotify_mcp
```

### 2. Create a virtual environment

Using uv (recommended):

```bash
uv venv
source .venv/bin/activate
uv pip install spotipy mcp[cli] python-dotenv
```

Or using standard venv and pip:
```bash
python3 -m venv venv
source venv/bin/activate
pip install spotipy mcp[cli] python-dotenv
```

### 3. Set up environment variables
Create a .env file in the root of your project:
```bash
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

## 🧪 Running the server
```bash
python main.py
```

## 🤖 Using with Claude Desktop
1.	Open your claude_desktop_config.json
2.	Add an MCP server entry like this:
```json
{
  "mcpServers": {
    "spotify_mcp": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/main.py"]
    }
  }
}
```
3.	Restart Claude Desktop.
4.	You should now see “Spotify” as a tool in your Claude interface.
