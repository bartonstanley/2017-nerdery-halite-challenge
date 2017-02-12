import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

myID, game_map = hlt.get_init()
hlt.send_init("PatientBot")

def assign_move(square):
    border = False
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID:
            border = True
            if neighbor.strength < square.strength:
                return Move(square, direction)

    if square.strength < 5 * square.production or border == True:
        return Move(square, STILL)
    else:
        return Move(square, random.choice((NORTH, WEST)))

while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
