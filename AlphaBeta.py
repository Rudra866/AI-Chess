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
        
    