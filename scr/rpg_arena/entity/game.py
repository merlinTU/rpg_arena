class Game:
    """
    Represents the overall game state.

    Attributes:
        player (Fighter | None): The current player character.
        round (int): The current game round.
        convoy (list): Shared storage for items not carried by the player.
        player_weapons (list): List of weapons owned by the player.
        max_items (int): Maximum number of items the player can carry.
    """

    def __init__(self):
        """
        Initialize the game state.

        Returns:
            None
        """
        self.player = None
        self.round = 1
        self.convoy = []
        self.player_weapons = []
        self.max_items = 5