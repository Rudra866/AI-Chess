class Player:
    """
    Base class for player interface
    """
    def __init__(self,game):
        self.game = game

class HumanInterface(Player):
    """
    Puts actions in a menu and asks for a choice from menu
    """
    def __init__(self, game):
        super().__init__(game)
    
    def move(self,state):
        """
        Present player with a menu of legal moves from the game
        """
        state.display()
        moves = self.game.actions(state)
        if not moves:
            print("No valid moves available.")
            return None

        exp = [str(i) for i in moves[0]]
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

class ComputerInt(Player):
    """
    This is a subclass of players and stores a search class object.
    The searcher needs minimax_min and minimax_max methods
    """
    def __init__(self,game,search):
        super().__init__(game)
        self.searcher = search
    
    def _ask_move_search(self, state):
        if self.game.is_maxs_turn(state):
            res = self.searcher.choose_move_max(state)
        else:
            res = self.searcher.choose_move_min(state) 
        return res.move
    def move(self, state):
        return self._ask_move_search(state)
    
class VerboseComp(ComputerInt):
    """
    This interface uses ComputerInterface to get a move from seacrher.
    """
    def __init__(self,game, search):
        super().__init__( game, search)
    
    def ask_move(self, state):
        print("Thinking...")
        res = self._ask_move_search(state)
        print("...done")
        res.display()
        return res.move
    
class SilentComp(ComputerInt):
    """
    This interface uses ComputerInterface to get a move from seacrher.
    """
    def __init__(self, game, search):
        ComputerInt.__init__(self, game, search)

    def ask_move(self, state):
        res = self._ask_move_search(state)
        return res.move