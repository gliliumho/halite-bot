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

    return (min_direction, max_dist)



def heuristic(square):
    if (square.owner == 0) and (square.strength > 0):
        return square.production/square.strength
    else:
        total_damage = 0
        for neighbor in game_map.neighbors(square):
            if(neighbor.owner != myID) and (neighbor.owner != 0):
                total_damage += neighbor.strength

        return total_damage


def assign_move(square, force_moves):
    if len(force_moves) != 0:
        for m in force_moves:
            if (square.x, square.y) == (m.square.x, m.square.y):
                return m

    production_ready = square.strength < 10 * square.production and square.strength < 50

    # Select direction with best production/strength or most damage
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                            if neighbor.owner != myID),
                            default = (None, None),
                            key = lambda t: heuristic(t[0]))


    # Attack if enough strength
    if (target != None) and (target.strength < square.strength):
        force_moves.append(Move(square, direction))
        return Move(square, direction)

    elif (target != None) and production_ready:
        for d, neighbor in enumerate(game_map.neighbors(square)):
            if neighbor.owner == myID and \
                (neighbor.strength + square.strength) > target.strength and \
                neighbor.strength >= 5*neighbor.production and \
                square.strength > neighbor.strength:

                forced = any((neighbor.x, neighbor.y) == (m.square.x, m.square.y) for m in force_moves)
                if not forced:
                    force_moves.append(Move(neighbor, hlt.opposite_cardinal(d)) )
                    force_moves.append(Move(square, direction) )
                    return Move(square, direction)


    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))

    # Keep producing if strength still too little
    if production_ready:
        force_moves.append(Move(square, STILL))
        return Move(square, STILL)

    # If not at border (around by allies) then transport strength to nearest border
    elif (not border):
        d, dist = nearest_enemy_direction(square)
        force_moves.append(Move(square, d))
        return Move(square, nearest_enemy_direction(square))

    # Wait until stronger than enemy
    else:
        force_moves.append(Move(square, STILL))
        return Move(square, STILL)



while True:
    force_moves = []
    game_map.get_frame()
    moves = [assign_move(square, force_moves) for square in game_map if square.owner == myID]

    # moves += force_moves
    # hlt.send_frame(moves)
    hlt.send_frame(force_moves)
