import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

myId, game_map = hlt.get_init()
hlt.send_init("DiscerningBot") 

def findNearestEnemyDirection(square):
   nearestEnemyDirection = STILL
   maxDistance = min(game_map.height, game_map.width) / 2
 
   for neighborDirection, neighbor in enumerate(game_map.neighbors(square)):
      target = neighbor
      distance = 0
      while (target.owner == myId and distance < maxDistance):
         distance = distance + 1
         target = game_map.get_target(target, neighborDirection)

      if distance < maxDistance:
         maxDistance = distance
         nearestEnemyDirection = neighborDirection

   return nearestEnemyDirection

def heuristic(neighbor):
    square = neighbor[1]
    key = square.production
    if (square.strength != 0):
        key = square.production / square.strength

    return key

def notMe(square):
    return square[1].owner != myId 

def assign_move(square):
    border = False

    neighbors = list(enumerate(game_map.neighbors(square)))
    notMySquares = list(filter(notMe, neighbors))
    if (notMySquares):
       border = True
       notMySquaresSorted = sorted(notMySquares, key=heuristic, reverse=True)
       target = notMySquares[0]
       if (target[1].strength < square.strength):
          return Move(square, target[0])

    if square.strength <  square.production * 5:
       return Move(square, STILL)

    if border == False:
       return Move(square, findNearestEnemyDirection(square))

    return Move(square, STILL)

def setPdbTrace():
    import sys
    lines = sys.stdin.readlines()
    sys.stdin = open('/dev/tty')
    import pdb; pdb.set_trace()

while True:
   game_map.get_frame()
   moves = [assign_move(square) for square in game_map if square.owner == myId]
   hlt.send_frame(moves)
