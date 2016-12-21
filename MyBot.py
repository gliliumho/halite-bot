import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random, math


myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")


def nearest_enemy_direction(square):
    min_direction = WEST
    # min2_direction = NORTH
    max_dist = min(game_map.width, game_map.height)/2

    for direction, neighbor in enumerate(game_map.neighbors(square)):
        distance = 0
        current = neighbor
        while current.owner == myID and distance < max_dist:
            distance += 1
            current = game_map.get_target(current, direction)

        if distance < max_dist:
            # min2_direction = min_direction
            min_direction = direction
            max_dist = distance

    # nearest_square = game_map.get_target(current,min_direction)
    # if (nearest_square.strength + square.strength) >= 255:
    #     return min2_direction

    return min_direction



def heuristic(square):
    if (square.owner == 0) and (square.strength > 0):
        return square.production/square.strength
    else:
        total_damage = 0
        for neighbor in game_map.neighbors(square, n=2):
            if(neighbor.owner != myID) and (neighbor.owner != 0):
                total_damage += neighbor.strength

        return total_damage



def assign_move(square):
    # Select direction with best production/strength or most damage
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                            if neighbor.owner != myID),
                            default = (None, None),
                            key = lambda t: heuristic(t[0]))
    # Attack if enough strength
    if (target != None) and (target.strength < square.strength):
        return Move(square, direction)

    # Keep producing if strength still too little
    if square.strength < 10 * square.production and square.strength < 50:
        return Move(square, STILL)

    # If not at border (around by allies) then transport strength to nearest border
    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if (not border):
        return Move(square, nearest_enemy_direction(square))

    # Wait until stronger than enemy
    else:
        return Move(square, STILL)



while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
