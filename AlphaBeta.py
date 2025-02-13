import time as time

class SearchResult:
    """
    A record containing the result of the search.
    """
    def __init__(self, value, move, elapsed_time, nodes, cutoff=False):
        self.value = value          # The minimax value of the chosen move
        self.move = move            # The move that was chosen
        self.elapsed_time = elapsed_time  # Total time spent searching
        self.nodes = nodes          # Total number of nodes expanded during search
        self.cutoff = cutoff        # True if the search ended due to cutoff

    def __str__(self):
        return (f"Chosen move: {self.move} with value {self.value} "
                f"(Elapsed time: {self.elapsed_time:.4f} sec, Nodes expanded: {self.nodes})")
    
    def display(self):
        print(self.__str__())

class MiniMax:
    """
    Implements the Minimax algorithm with Alpha-Beta pruning,
    transposition table, and a depth cutoff.
    
    The 'game' object passed in should provide the following methods:
      - actions(state): returns a list of legal moves for the given state.
      - result(state, action): returns the new state after making 'action' in 'state'.
      - transposition_string(state): returns a string that uniquely represents 'state'.
      - is_terminal(state): returns True if 'state' is a terminal state.
      - utility(state): returns the utility value of a terminal state.
      - cutoff_test(state, depth): returns True if the search should be cut off at this depth.
      - eval(state): returns an evaluation of 'state' when cutoff occurs.
    """
    #A large constant value
    INF = 2**20

    def __init__(self, game):
        self.game = game
        self.nodes_expanded = 0
        self.transposition_table = {}

    def choose_move_max(self, state):
        """
        Returns best move for given state
        """
        start_time = time.perf_counter()
        self.nodes_expanded = 0
        self.transposition_table = {}

        best_value  = -self.INF
        best_move = None
        #Alpha beta params initialized
        alpha = -self.INF
        beta = self.INF

        self.nodes_expanded += 1
        for action in self.game.actions(state):
            value = self.__min_value(self.game.result(state, action), alpha,beta,1)
            if value > best_value:
                best_value = value
                best_move = action
            alpha = max(alpha, best_value)
        end = time.perf_counter()
        return SearchResult(best_value, best_move, end - start_time, self.nodes_expanded)
    
    def choose_move_min(self, state):
        """
        Returns best move for min in given state
        """
        start_time = time.perf_counter()
        self.nodes_expanded = 0
        self.transposition_table = {}

        best_value  = -self.INF
        best_move = None
        #Alpha beta params initialized
        alpha = -self.INF
        beta = self.INF

        self.nodes_expanded += 1
        for action in self.game.actions(state):
            value = self.max_val(self.game.result(state, action), alpha,beta,1)
            if value < best_value:
                best_value = value
                best_move = action
            beta = min(alpha, best_value)
        end = time.perf_counter()

        if best_move is None:
            legal_moves = self.game.actions(state)
        if legal_moves:
            best_move = legal_moves[0]
        else:
            raise ValueError("No legal moves available.")
        return SearchResult(best_value, best_move, end - start_time, self.nodes_expanded)
    
    def max_val(self, state, alpha, beta, depth):
        """ 
        Returns minimax value of given state assuming max'x turn to move
        """
        string = self.game.transposition_string(state)
        if string in self.transposition_table:
            return self.transposition_table[string]
        elif self.game.is_terminal(state):
            move = self.transposition_table[string]
        elif self.game.cutoff_test(state, depth):
            move = self.game.eval(state)

        else:
            move = -self.INF
            self.nodes_expanded += 1
            for action in self.game.actions(state):
                value = self.min_val(self.game.result(state, action), alpha, beta, depth+1)
                if value > move:
                    move = value
                if move >= beta: 
                    return move
                alpha = max(alpha, move)
            self.transposition_table[string] = move
        return move
        
    def min_val(self, state, alpha, beta, depth):
        """
        Returns minimax value of given state assuming min's turn to move
        """
        string = self.game.transposition_string(state)
        if string in self.transposition_table:
            return self.transposition_table[string]
        elif self.game.is_terminal(state):
            move = self.transposition_table[string]
        elif self.game.cutoff_test(state, depth):
            move = self.game.eval(state)

        else:
            move = self.INF
            self.nodes_expanded += 1
            for action in self.game.actions(state):
                value = self.max_val(self.game.result(state, action), alpha, beta, depth+1)
                if value < move:
                    move = value
                if move <= alpha:
                    return move
                beta = min(beta, move)
            self.transposition_table[string] = move
        return move