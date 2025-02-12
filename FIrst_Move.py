import Players as p
import AlphaBeta as ab
import Chess as Game

# List for input depths to generate table
depth_list = [1,2,3,4,5]

for depth in depth_list:
    print('Running depth', depth)
    game = Game.Game(depthlimit=depth)
    state = game.initial_state()

    current_player = p.VerboseComputer(game, ab.Minimax(game))
    current_player.ask_move(state)