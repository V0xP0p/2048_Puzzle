from BaseAI_3 import BaseAI
import math
from collections import namedtuple as nt
from collections import deque as dq
import time
from random import randint

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05


class PlayerAI(BaseAI):

    _ALPHA = -math.inf
    _BETA = math.inf

    def __init__(self):
        self.alpha = PlayerAI._ALPHA
        self.beta = PlayerAI._BETA

    def get_alpha(self):
        return self.alpha

    def get_beta(self):
        return self.beta

    def set_alpha(self, new_alpha):
        self.alpha = new_alpha

    def set_beta(self, new_beta):
        self.beta = new_beta

    def update_alpha(self, alpha):
        if alpha > self.get_alpha():
            self.set_alpha(alpha)

    def update_beta(self, beta):
        if beta < self.get_beta():
            self.set_beta(beta)

    @staticmethod
    def update_grid(grid, move):
        grid.move(move)

    def getMove(self, grid, w1, w2, w3):
        """
        A function the finds the next moves for the player AI
        :param grid:
        :return: a tuple
        """

        return self.minmax(grid, w1, w2, w3)

    def minmax(self, grid, w1, w2, w3):

        # get the time
        prev_time = time.clock()
        # reset the grid to the initial
        grid_current = grid.clone()
        # Initiate a new frontier list to store the nodes currently in the frontier
        frontier = dq()
        # initiate a set to store the nodes expanded
        explored = set()
        # get the possible max moves for the input grid
        max_available_moves = grid.getAvailableMoves()
        # create the nodes for the available moves and append them to the frontier
        for max_move in max_available_moves:
            # update the current grid with the next max move
            self.update_grid(grid_current, max_move)
            # create the next node
            max_node = Node("max", heuristic(grid_current, w1, w2, w3), grid_current, max_move, None)
            # append the node to the frontier
            frontier.append(max_node)
            # add the node to the explored set
            explored.add(max_node)
            # reset the grid to the initial
            grid_current = grid.clone()
        # exit move initialization
        exit_node = max(frontier, key=lambda x: x.heu)
        # iterate while time is within limits and frontier not empty
        # while time.clock() - prev_time < timeLimit-allowance:
        # iterate while there are no more nodes on the frontier for this depth
        while frontier and time.clock() - prev_time < timeLimit-allowance:
            # check if the next frontier node is of kind max
            if frontier[0].kind == "max":
                # pop the first node from the frontier
                max_node = frontier.popleft()
                # get the available cells on the grid
                cells = max_node.grid.getAvailableCells()
                # get the value for the new tile
                value = self.get_new_tile_value()
                # check if there are any moves left
                if len(cells) < 1:
                    # if there are no empty tiles return the grid as it is
                    grid_current = max_node.grid
                else:
                    # else update the grid with new min moves
                    # iterating over the available tiles
                    min_nodes = []
                    for tile in cells:
                        # create a copy of the grid
                        grid_current = max_node.grid.clone()
                        # insert the new value in the grid
                        grid_current.insertTile(tile, value)
                        # create the min_node
                        min_node = Node("min", heuristic(grid_current, w1, w2, w3), grid_current, tile, max_node)
                        # get the min moves for the node
                        min_nodes.append(min_node)
                        # update bete
                        self.update_beta(min_node.heu)
                        if self.get_beta() <= self.get_alpha():
                            break
                    # sort the min nodes from small to large based on heuristics
                    min_nodes.sort(key=lambda x: x.heu, reverse=False)
                    # add the min node to the frontier
                    frontier.extend(min_nodes)
                    # add the min nodes to the explored set
                    explored.union(min_nodes)
                    # set the exit node to the max value of the min nodes
                    exit_node = max(exit_node, min_nodes[0], key=lambda x: x.heu)
                    # update alpha
                    self.update_alpha(exit_node.heu)
            # check if the next frontier node is of kind min
            elif frontier[0].kind == "min":
                # pop the next min node
                min_node = frontier.popleft()
                # update the current grid
                grid_current = min_node.grid.clone()
                # get the possible max moves for the grid
                max_available_moves = grid_current.getAvailableMoves()
                if max_available_moves:
                    # initiate a max_nodes list
                    max_nodes = []
                    # create the nodes for the available moves and append them to the frontier
                    for max_move in max_available_moves:
                        # update the current grid with the next max move
                        self.update_grid(grid_current, max_move)
                        # create the next node
                        max_nodes.append(Node("max", heuristic(grid_current, w1, w2, w3), grid_current, max_move, min_node))
                        # reset the grid to the initial
                        grid_current = min_node.grid.clone()
                    # sort the max nodes list from high to low
                    max_nodes.sort(key=lambda x: x.heu, reverse=True)
                    # append the max nodes to the frontier
                    frontier.extendleft(max_nodes)
                    # add the nodes to the explored set
                    explored.union(max_nodes)
                    # set the exit node to the max value of the max nodes
                    exit_node = max(exit_node, max_nodes[0], key=lambda x: x.heu)

        return exit_node.path().move



    @staticmethod
    def get_new_tile_value():
        if randint(0, 99) < 100 * 0.9:
            return 2
        else:
            return 4


def heuristic(grid, w1, w2, w3):

    empty_cells = len(grid.getAvailableCells())
    # non_empty_cells = 16 - empty_cells
    # average_cells = empty_cells/16
    #
    edged = 0
    # max_tile = [-1, (0, 0)]
    # merge_heu = 0
    monotonic = 0
    trans_grid = list(zip(*grid.map))
    #
    for x in range(grid.size):
        if all(i < j for i, j in zip(grid.map[x][:], grid.map[x][1:])) or \
                all(i > j for i, j in zip(grid.map[x][:], grid.map[x][1:])):
            monotonic += 1  # max(sum(grid.map[x][:]), 256)/256
        # else:
        #     monotonic -= 0.125  # max(sum(grid.map[x][:]), 256)/256
        for y in range(grid.size):
            if all(i < j for i, j in zip(trans_grid[y][:], trans_grid[y][1:])) or \
                    all(i > j for i, j in zip(trans_grid[y][:], trans_grid[y][1:])):
                monotonic += 1  # max(sum(grid.map[y][:]), 256)/256
            # else:
            #     monotonic -= 0.125  # max(sum(grid.map[y][:]), 256) / 256
            # max_tile = max(max_tile, (grid.map[x][y], (x, y)), key=lambda w: w[0])
            if grid.map[x][y] != 0 and (x in range(0, 4) or y in range(0, 4)):
                edged += 1

    # cornered = 0
    #
    # if max_tile[1][0] in (0, 3) and max_tile[1][1] in (0, 3):
    #     cornered = 1
    #
    # neighbours = [(max_tile_x-1, max_tile_y), (max_tile_x + 1, max_tile_y), (max_tile_x, max_tile_y-1), (max_tile_x, max_tile_y+1)]
    #
    # for pos in neighbours:
    #     if pos[0] not in range(0, 4) or pos[1] not in range(0, 4):
    #         neighbours.remove(pos)
    #
    # for pos in neighbours:
    #     if grid.map[pos[0]][pos[1]] and grid.map[pos[0]][pos[1]] == max_tile:
    #         merge_heu += max_tile/4096
    #
    edged = edged/12

    empty_cells = empty_cells/14

    monotonic = monotonic/8

    return w1*empty_cells + w2*monotonic + w3*edged  # w1*average_cells + w2*merge_heu + w3*edged_heu + w4*monotonic + w5*cornered


class Node(nt("Node", ["kind", "heu", "grid", "move", "parent"])):
    """

    """

    def __new__(cls, kind, heu, grid, move, parent=None):
        return super().__new__(cls, kind, heu, grid, move, parent)

    def __init__(self, kind, heu, grid, player_move, parent):
        super().__init__()
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def __hash__(self):
        return hash(self.heu)

    def path(self):

        move = self

        while move.parent:
                move = move.parent

        return move





