import Players
import sys
import AlphaBeta as Computer
import Chess as Game

if len(sys.argv) <= 2:
    print("Usage: python human_vs_machine.py <side> <search>")
    print("Side T is for player to play Titan Hero , L is for player to play the Legion")
    print("Choosing a higher depth limit should make the computer player stronger")
    exit()

side = sys.argv[1]
depth_lim = int(sys.argv[2])

#Create game and initial state
game1 =Game.Game(depthlimit=depth_lim)
game2 = Game.Game(depthlimit=depth_lim)
state = game1.initial_state()
state2 = game2.initial_state()

if side == "T":
    current_player = Players.HumanInterface(game1)
    other_player = Players.ComputerInt(game2, Computer.MiniMax(game2))
else:
    current_player = Players.VerboseComp(game1, Computer.MiniMax(game1))
    other_player = Players.HumanInterface(game2)

current_game, other_game = game1, game2
# Play the game
while not current_game.is_terminal(state):

    # ask the current player for a move
    choice = current_player.move(state)

    # check the move
    assert choice in current_game.actions(state), "The action <{}> is not legal in this state".format(choice)

    # apply the move
    state = current_game.result(state, choice)

    # swap the players
    current_player, current_game, other_player, other_game = other_player, other_game, current_player, current_game

game1.congratulate(state)

