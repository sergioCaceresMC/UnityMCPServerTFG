

from mcp.server.mcpserver import MCPServer

from .UnityBridge import UnityBridge


unity = UnityBridge()

unity.start()


# ============================================================
# MCP SERVER
# ============================================================

mcp = MCPServer("Unity Phy")

@mcp.tool()
def get_game_state() -> dict:
    """
    Get the current state of the player in Unity.
    """

    return unity.call(
        "get_state"
    )


@mcp.tool()
def move_player(
    direction: str,
    distance: float = 1.0
) -> dict:
    """
    Move the player.

    direction must be:
    forward, backward, left or right.

    distance is expressed in Unity units.
    """

    return unity.call(
        "move",
        {
            "direction": direction,
            "distance": distance
        }
    )


@mcp.tool()
def interact(
    object_id: str
) -> dict:
    """
    Interact with an object in the game world
    using its stable object ID.
    """

    return unity.call(
        "interact",
        {
            "object_id": object_id
        }
    )


# ============================================================

if __name__ == "__main__":

    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=3001
    )
