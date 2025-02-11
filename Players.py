class Player:
    """
    Base class for player interface
    """
    def __init__(self,game):
        self.game = game

class HumanInterface:
    """
    Puts actions in a menu and asks for a choice from menu
    """
    def __init__(self,game):
        Player.__init__(self,game)
    
    def move(self,state):
        """
        Present player with a menu of legal moves from the game
        """
        