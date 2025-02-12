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
        state.display()
        moves = self.game.actions(state)
        exp = [str(x) for i in moves[0]]
        exp = " ".join(exp)

        print("Player turn! Type your move (example:" + exp + ")")

        valid = False
        while not valid:
            choice = input("Your Move: ")
            choice = choice.split(" ")
            for i in range(len(choice)):
                if choice[i].isdigit():
                    choice[i] = int(choice[i])
            choice = tuple(choice)
            if choice not in moves:
                print("Not a valid move")
            else:
                valid = True
        return choice

class ComputerInt:
    """
    This is a subclass of players and stores a search class object.
    The searcher needs minimax_min and minimax_max methods
    """
    def __init__(self,game,search):
        Player.__init__(self, game)
        self.searcher = search
    
    def _ask_move_search(self, state):
        if self.game.is_max_turn(state):
            res = self.searcher.minimax_decision_max(state)
        else:
            res = self.searcher.minimax_decision_min(state) 
        return res
    
class VerboseComp:
    """
    This interface uses ComputerInterface to get a move from seacrher.
    """
    def __init__(self,game, search):
        ComputerInt.__init__(self, game, search)
    
    def ask_move(self, state):
        print("Thinking...")
        res = super._ask_move_search(state)
        print("...done")
        res.display()
        return res.move
    
class SilentComp:
    """
    This interface uses ComputerInterface to get a move from seacrher.
    """
    def __init__(self, game, search):
        ComputerInt.__init__(self, game, search)

    def ask_move(self, state):
        res = super._ask_move_search(state)
        return res.move