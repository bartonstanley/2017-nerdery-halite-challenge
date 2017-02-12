import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

myID, game_map = hlt.get_init()
hlt.send_init("AmbiturnerBot")

def findNearestEnemyDirection(square):
   nearestEnemyDirection = NORTH
   maxDistance = min(game_map.height, game_map.width) / 2
 
   for neighborDirection, neighbor in enumerate(game_map.neighbors(square)):
      current = neighbor
      distance = 0
      while (current.owner == myID and distance < maxDistance):
         distance = distance + 1
         current = game_map.get_target(current, neighborDirection)

      if distance < maxDistance:
         maxDistance = distance
         nearestEnemyDirection = neighborDirection

   return nearestEnemyDirection

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
       return Move(square, findNearestEnemyDirection(square))

while True:
   game_map.get_frame()
   moves = [assign_move(square) for square in game_map if square.owner == myID]
   hlt.send_frame(moves)
