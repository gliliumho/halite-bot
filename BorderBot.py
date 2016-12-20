import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random, math


myID, game_map = hlt.get_init()
hlt.send_init("BorderBot")

def nearest_enemy_direction(square):
    min_direction = WEST
    max_dist = min(game_map.width, game_map.height)/2

    for direction, neighbor in enumerate(game_map.neighbors(square)):
        distance = 0
        current = neighbor
        while current.owner == myID and distance < max_dist:
            distance += 1
            current = game_map.get_target(current, direction)

        if distance < max_dist:
            min_direction = direction
            max_dist = distance

    return min_direction



def assign_move(square):
    border = False
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID:
            border = True
            if neighbor.strength < square.strength:
                return Move(square, direction)

    if square.strength < 5 * square.production:
        return Move(square, STILL)
    elif (not border):
        return Move(square, nearest_enemy_direction(square))
        # return Move(square, random.choice((NORTH, WEST)))
    else:
        return Move(square, STILL)



while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
