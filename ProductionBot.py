import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

myId, game_map = hlt.get_init()
hlt.send_init("ProductionBot") 

def findNearestEnemyDirection(square):
   nearestEnemyDirection = NORTH
   maxDistance = min(game_map.height, game_map.width) / 2
 
   for neighborDirection, neighbor in enumerate(game_map.neighbors(square)):
      current = neighbor
      distance = 0
      while (current.owner == myId and distance < maxDistance):
         distance = distance + 1
         current = game_map.get_target(current, neighborDirection)

      if distance < maxDistance:
         maxDistance = distance
         nearestEnemyDirection = neighborDirection

   return nearestEnemyDirection

def notMe(square):
    return square[1].owner != myId 

def assign_move(square):
    border = False

    neighbors = list(enumerate(game_map.neighbors(square)))
    notMySquares = list(filter(notMe, neighbors))
    if (notMySquares):
       notMySquaresSorted = sorted(notMySquares, key=lambda tup: tup[1].production, reverse=True)
       target = notMySquares[0]
       if (target !=None and target[1].strength < square.strength):
          return Move(square, target[0])

    if square.strength < 5 * square.production:
       return Move(square, STILL)
    else:
       return Move(square, findNearestEnemyDirection(square))

def setPdbTrace():
    import sys
    lines = sys.stdin.readlines()
    sys.stdin = open('/dev/tty')
    import pdb; pdb.set_trace()

while True:
   game_map.get_frame()
   moves = [assign_move(square) for square in game_map if square.owner == myId]
   hlt.send_frame(moves)
