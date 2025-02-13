import random as rand

class GameState(object):
    """ The GameState class stores the information about the state of the game.
    """
    
    def __init__(self, life=75, dim=8):
        self.dim = dim
        self.maxs_turn = True # true means titan's turn
        self.cachedTerminal = False  
        self.cachedOutcome = None       
        self.moves_made = 0
        self.life = life
        self.positions = {}
        
        self.positions["T"] = (7,3)
        self.positions["P"] = (0,3)
        for i, p in enumerate(['A','B','C','D','E','F','G','H']):
            self.positions[p] = (1,i)
        self.emblems = set()
        self.stringified = str(self)


    def myclone(self):
        """ Make and return an exact copy of the state.
        """
        new_state = GameState()
        
        #TODO: copy portions of the state that need to be copied

        
        new_state.life = self.life
        new_state.maxs_turn = self.maxs_turn
        new_state.cachedTerminal = self.cachedTerminal
        new_state.cachedOutcome = self.cachedOutcome
        new_state.stringified = self.stringified 
        new_state.moves_made = self.moves_made
        new_state.positions = self.positions.copy()
        new_state.emblems = self.emblems.copy()

        return new_state

    def display(self):
        """
        Present the game state to the console.
        """
        board = [['.' for _ in range(self.dim)] for _ in range(self.dim)]
        for piece, (r, c) in self.positions.items():
            board[r][c] = piece
        print(f"Current turn: {'Titan Hero' if self.maxs_turn else "The Pantheon"}")
        print(f"Titan Hero Health: {self.life}")
        print("Board:")
        for row in board:
            print(" ".join(row))

    def __str__(self):
        """ Translate the board description into a string.  
            Could be used as a key for a hash table.  
            :return: A string that describes the board in the current state.
        """
        pieces_str = ",".join(f"{p}:{self.positions[p][0]}-{self.positions[p][1]}" for p in sorted(self.positions))
        return f"T{self.life}|{'M' if self.maxs_turn else 'E'}|{pieces_str}|Mvs:{self.moves_made}"
    

        
class Game(object):
    """ The Game object defines the interface that is used by Game Tree Search
        implementation.
    """
    
    
    def __init__(self, dim=8,depthlimit=0):
        """ Initialization.  
        """
        self.dim = dim
        self.depth_limit = depthlimit
        
        self.base_dam = 8
        self.weapon_dam = 3
        self.shot_dam = 3
        self.perturn_dam = 1
        self.weaknesses = { "A":"H", "B":"A", "C":"B", "D":"C", "E":"D", "F":"E", "G":"F", "H":"G"}

    def initial_state(self, starting_life=75):
        """ Return an initial state for the game.
        """
        state = GameState(life=starting_life, dim=self.dim)
        state.stringified = str(state)
        return state
        
    def is_mins_turn(self, state):
        """ Indicate if it's Min's turn
            :return: True if it's Min's turn to play
        """
        return not state.maxs_turn

    def is_maxs_turn(self, state):
        """ Indicate if it's Min's turn
            :return: True if it's Max's turn to play
        """
        return state.maxs_turn

    def is_terminal(self, state):
        """ Indicate if the game is over.
            :param node: a game state with stored game state
            :return: a boolean indicating if node is terminal
        """
        return state.cachedTerminal

    def cutoff_test(self, state, depth):
        """
            Check if the search should be cut-off early.
            In a more interesting game, you might look at the state
            and allow a deeper search in important branches, and a shallower
            search in boring branches.

            :param state: a game state
            :param depth: the depth of the state,
                          in terms of levels below the start of search.
            :return: True if search should be cut off here.
        """
        return depth > self.depth_limit
        
    def transposition_string(self, state):
        """ Returns a unique string for the given state.  For use in 
            any Game Tree Search that employs a transposition table.
            :param state: a legal game state
            :return: a unique string representing the state
        """
        return state.stringified
    
    def in_line_of_sight(self, pos1, pos2, state):
        """
        Check if there is a clear line of sight between pos1 and pos2 on the board.
        pos1: (row, col) for Pantheon.
        pos2: (row, col) for Titan Hero.
        Returns True if pos1 and pos2 are in the same row, column, or diagonal and no other
        pieces are in between.
        """
        r1, c1 = pos1
        r2, c2 = pos2

        # Check if in the same row, column, or diagonal.
        if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
            # Determine step increments.
            dr = (r2 - r1) // (abs(r2 - r1) if r2 != r1 else 1)
            dc = (c2 - c1) // (abs(c2 - c1) if c2 != c1 else 1)
            
            # Move one step at a time from pos1 towards pos2.
            r, c = r1 + dr, c1 + dc
            while (r, c) != (r2, c2):
                # If any piece is in the way, return False.
                for piece, pos in state.positions.items():
                    if pos == (r, c):
                        return False
                r += dr
                c += dc
            return True

        return False


    def actions(self, state):
        """ Returns all the legal actions in the given state.
            :param state: a state object
            :return: a list of actions legal in the given state
        """
        moves = []
        if state.maxs_turn:  # Titan Hero's turn.
            current_pos = state.positions['T']
            directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
            for dx, dy in directions:
                for step in range(1, 4):
                    new_r = current_pos[0] + dx * step
                    new_c = current_pos[1] + dy * step
                    # Check boundaries.
                    if 0 <= new_r < state.dim and 0 <= new_c < state.dim:
                        # If destination is Pantheon, only allow if all lesser titans are defeated.
                        dest_piece = None
                        for p, pos in state.positions.items():
                            if pos == (new_r, new_c):
                                dest_piece = p
                                break
                        if dest_piece == 'P' and any(p in state.positions for p in ['A','B','C','D','E','F','G','H']):
                            continue
                        moves.append(('T', new_r, new_c))
                    else:
                        break  # Off-board, no need to check further in this direction.
        else:
            # Enemy's turn: For each enemy piece (Lesser Titans and Pantheon)
            enemy_moves = []
            for piece in list(state.positions.keys()):
                if piece in ['A','B','C','D','E','F','G','H','P']:
                    current_pos = state.positions[piece]
                    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                                (1, 0), (1, -1), (0, -1), (-1, -1)]
                    for dx, dy in directions:
                        new_r = current_pos[0] + dx
                        new_c = current_pos[1] + dy
                        # Check boundaries.
                        if 0 <= new_r < state.dim and 0 <= new_c < state.dim:
                            # Check collisions: enemy pieces cannot share a square.
                            collision = False
                            for other, pos in state.positions.items():
                                if other in ['A','B','C','D','E','F','G','H','P'] and pos == (new_r, new_c):
                                    collision = True
                                    break
                            # Pantheon cannot move onto Titan Hero.
                            if piece == 'P' and state.positions['T'] == (new_r, new_c):
                                collision = True
                            if not collision:
                                enemy_moves.append((piece, new_r, new_c))
            # Randomize the order of enemy moves so that moves by lesser titans get a chance
            rand.shuffle(enemy_moves)
            moves.extend(enemy_moves)
        return moves


    def result(self, state, action):
        """ Return the state that results from the application of the
            given action in the given state.
            :param state: a legal game state
            :param action: a legal action in the game state
            :return: a new game state
        """        
        new_state = state.myclone()
        piece, new_r, new_c = action

        if new_state.maxs_turn:  # Titan Hero's move.
            # Move Titan Hero.
            old_pos = new_state.positions['T']
            new_state.positions['T'] = (new_r, new_c)
            
            # Check if moving onto an enemy.
            enemy_hit = None
            for p in ['A','B','C','D','E','F','G','H','P']:
                if p in new_state.positions and new_state.positions[p] == (new_r, new_c):
                    enemy_hit = p
                    break
            
            if enemy_hit:
                if enemy_hit in ['A','B','C','D','E','F','G','H']:
                    # Combat: Determine damage based on emblem effectiveness.
                    required_emblem = self.weaknesses[enemy_hit]
                    if required_emblem in new_state.emblems:
                        damage = 3
                    else:
                        damage = 8
                    new_state.life -= damage
                    # Collect the emblem.
                    new_state.emblems.add(enemy_hit)
                    # Remove the enemy piece.
                    del new_state.positions[enemy_hit]
                elif enemy_hit == 'P':
                    # If Pantheon is captured legally, Titan Hero wins.
                    new_state.cachedTerminal = True
                    new_state.cachedOutcome = True
                    new_state.stringified = str(new_state)
                    return new_state
            else:
                # No combat: apply end-of-turn energy drain.
                new_state.life -= self.perturn_dam

            # Switch turn.
            new_state.maxs_turn = False

        else:  # Enemy's turn.
            # Move the enemy piece.
            if piece in new_state.positions:  # It should be present.
                new_state.positions[piece] = (new_r, new_c)
                
                # Check for combat if a Lesser Titan moves onto Titan Hero.
                if piece in ['A','B','C','D','E','F','G','H'] and new_state.positions['T'] == (new_r, new_c):
                    required_emblem = self.weaknesses[piece]
                    if required_emblem in new_state.emblems:
                        damage = 3
                    else:
                        damage = 8
                    new_state.life -= damage
                    # Collect emblem and remove enemy.
                    new_state.emblems.add(piece)
                    del new_state.positions[piece]
            
            # Pantheon's Divine Smite: Check if Pantheon sees Titan Hero.
            pantheon_pos = new_state.positions.get('P', None)
            hero_pos = new_state.positions['T']
            if pantheon_pos and self.in_line_of_sight(pantheon_pos, hero_pos, new_state):
                new_state.life -= self.shot_dam

            # Switch turn.
            new_state.maxs_turn = True

        new_state.moves_made += 1

        # Terminal check: if Titan Hero's life drops to 0 or below.
        if new_state.life <= 0:
            new_state.cachedTerminal = True
            new_state.cachedOutcome = False

        new_state.stringified = str(new_state)
        return new_state


    def utility(self, state):
        """ Calculate the utility of the given state.
        This method is only called in TERMINAL states
            
            :param state: a legal game state
            :return: utility of the terminal state
        """
        # For example, +100 for Titan Hero win, -100 for loss.
        if state.cachedOutcome is True:
            return 100
        elif state.cachedOutcome is False:
            return -100
        else:
            return 0


    

    def eval(self, state):
        """
        A refined evaluation function that differentiates enemy piece types.
        
        Factors considered:
        - Titan Hero's remaining life.
        - Penalty for enemy pieces remaining.
        - Average Manhattan distance from Titan Hero to lesser titans.
        - Bonus for each collected emblem.
        - Bonus for being close to the Pantheon if it's the only enemy left.
        - Penalty if the Pantheon can shoot Titan Hero.
        - **Extra penalty if Pantheon is moved away from its ideal position.**
        """
        # Weight constants (tweak these as needed)
        LIFE_WEIGHT = 1.0                # per health point of Titan Hero
        ENEMY_WEIGHT = 20.0              # penalty per enemy piece
        DISTANCE_WEIGHT = 1.5            # penalty per unit of average distance from lesser titans
        EMBLEM_WEIGHT = 5.0              # bonus per collected emblem
        BONUS_CAPTURE_PANTHEON = 50.0    # bonus when only Pantheon remains and is close
        DIVINE_SMITE_PENALTY = 15.0      # penalty if Pantheon can shoot Titan Hero
        # NEW: Extra penalty parameters for Pantheon’s position
        IDEAL_PANTHEON = (0, 3)
        PANTHEON_MOVE_PENALTY = 40.0     # penalty multiplier per unit distance from ideal

        hero_pos = state.positions['T']
        total_enemy_count = 0
        total_distance = 0
        pantheon_distance = None

        lesser_count = 0
        for p, pos in state.positions.items():
            if p in ['A','B','C','D','E','F','G','H']:
                total_enemy_count += 1
                lesser_count += 1
                total_distance += abs(hero_pos[0] - pos[0]) + abs(hero_pos[1] - pos[1])
            elif p == 'P':
                total_enemy_count += 1
                pantheon_distance = abs(hero_pos[0] - pos[0]) + abs(hero_pos[1] - pos[1])

        avg_distance = (total_distance / lesser_count) if lesser_count > 0 else 0

        # Start with Titan Hero's life.
        score = LIFE_WEIGHT * state.life
        # Penalize for enemy pieces remaining.
        score -= ENEMY_WEIGHT * total_enemy_count
        # Penalize based on average distance to lesser titans.
        score -= DISTANCE_WEIGHT * avg_distance
        # Bonus for collected emblems.
        score += EMBLEM_WEIGHT * len(state.emblems)

        # If only Pantheon remains, reward states where it's close.
        if total_enemy_count == 1 and 'P' in state.positions and pantheon_distance is not None:
            score += BONUS_CAPTURE_PANTHEON / (pantheon_distance + 1)

        # Penalty if Pantheon can shoot Titan Hero.
        if 'P' in state.positions and self.in_line_of_sight(state.positions['P'], hero_pos, state):
            score -= DIVINE_SMITE_PENALTY

        # NEW: Extra penalty if Pantheon is not at its ideal position.
        if 'P' in state.positions:
            current_pantheon = state.positions['P']
            distance_from_ideal = abs(current_pantheon[0] - IDEAL_PANTHEON[0]) + abs(current_pantheon[1] - IDEAL_PANTHEON[1])
            # The farther P is from the ideal position, the higher the penalty.
            score -= PANTHEON_MOVE_PENALTY * distance_from_ideal

        return score




    def congratulate(self, state):
        """ Called at the end of a game, display some appropriate 
            sentiments to the console. Could be used to display 
            game statistics as well.
            :param state: a legal game state
        """

        if state.cachedOutcome:
            print("Congratulations! The Titan Hero has defeated the Pantheon and restored balance!")
        else:
            print("Alas! The forces of the Pantheon have drained the Titan Hero’s vitality. Better luck next time!")
    

   
# eof