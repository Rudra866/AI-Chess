import time

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

def current_time():
    return time.perf_counter()

class MiniMax:
    """
    Implements the Minimax algorithm with Alpha-Beta pruning, transposition table, 
    and a depth cutoff.
    """
    INF = 2**20

    def __init__(self, game):
        self.game = game
        self.nodes_expanded = 0
        self.transposition_table = {}

    def choose_move_max(self, state):
        start_time = current_time()
        self.nodes_expanded = 0
        self.transposition_table = {}

        best_value = -self.INF
        best_move = None
        alpha = -self.INF
        beta = self.INF

        for action in self.game.actions(state):
            value = self._min_value(self.game.result(state, action), alpha, beta, 1)
            if value > best_value:
                best_value = value
                best_move = action
            alpha = max(alpha, best_value)

        elapsed = current_time() - start_time
        if best_move is None:
            legal_moves = self.game.actions(state)
            if legal_moves:
                best_move = legal_moves[0]
            else:
                raise ValueError("No legal moves available.")
        return SearchResult(best_value, best_move, elapsed, self.nodes_expanded)

    def choose_move_min(self, state):
        start_time = current_time()
        self.nodes_expanded = 0
        self.transposition_table = {}

        best_value = self.INF
        best_move = None
        alpha = -self.INF
        beta = self.INF

        for action in self.game.actions(state):
            value = self._max_value(self.game.result(state, action), alpha, beta, 1)
            if value < best_value:
                best_value = value
                best_move = action
            beta = min(beta, best_value)

        elapsed = current_time() - start_time
        if best_move is None:
            legal_moves = self.game.actions(state)
            if legal_moves:
                best_move = legal_moves[0]
            else:
                raise ValueError("No legal moves available.")
        return SearchResult(best_value, best_move, elapsed, self.nodes_expanded)

    def _max_value(self, state, alpha, beta, depth):
        string = self.game.transposition_string(state)
        if string in self.transposition_table:
            return self.transposition_table[string]
        if self.game.is_terminal(state):
            return self.game.utility(state)
        if self.game.cutoff_test(state, depth):
            return self.game.eval(state)
        
        value = -self.INF
        self.nodes_expanded += 1
        for action in self.game.actions(state):
            value = max(value, self._min_value(self.game.result(state, action), alpha, beta, depth+1))
            if value >= beta:
                self.transposition_table[string] = value
                return value
            alpha = max(alpha, value)
        self.transposition_table[string] = value
        return value

    def _min_value(self, state, alpha, beta, depth):
        string = self.game.transposition_string(state)
        if string in self.transposition_table:
            return self.transposition_table[string]
        if self.game.is_terminal(state):
            return self.game.utility(state)
        if self.game.cutoff_test(state, depth):
            return self.game.eval(state)

        value = self.INF
        self.nodes_expanded += 1
        for action in self.game.actions(state):
            value = min(value, self._max_value(self.game.result(state, action), alpha, beta, depth+1))
            if value <= alpha:
                self.transposition_table[string] = value
                return value
            beta = min(beta, value)
        self.transposition_table[string] = value
        return value
