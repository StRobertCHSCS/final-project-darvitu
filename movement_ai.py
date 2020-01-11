import arcade
import csv
import math
import sys
from blob import Blob
from tiledmap import TiledMap

class ShortestPath():
    def __init__(self):
        self.map = []
        with open("Maps/tilemap.txt") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.map.append(row)

    def shortest_distance(self, current_x, current_y, next_x, next_y)-> None:
        """
        Finds the shortest distance from a start and end points, utilizes a csv file of obstacles
        :param current_x: start x
        :param current_y: start y
        :param next_x: end x
        :param next_y: end y
        :return: none
        """
        # create step/distance array
        self.step = [[999999 for x in range(50)] for y in range(50)]
        # create queues
        queue_r = []
        queue_r.append(current_x)
        queue_y = []
        queue_y.append(current_y)
        # add first node
        self.step[current_x][current_y] = 0
        # add end node
        self.step[next_x][next_y] = -1
        # perform breadth-first-search
        while len(queue_r) is not 0:
            # current location
            r = queue_r.pop(0)
            c = queue_y.pop(0)

            # move up
            if r - 1 >= 0:
                if self.map[r - 1][c] is not 1:
                    if self.step[r - 1][c] > self.step[r][c] + 1:
                        self.step[r - 1][c] = self.step[r][c] + 1
                        queue_r.append(r - 1)
                        queue_y.append(c)
            # move down
            if r + 1 < 50:
                if self.map[r + 1][c] is not 1:
                    if self.step[r + 1][c] > self.step[r][c] + 1:
                        self.step[r + 1][c] = self.step[r][c] + 1
                        queue_r.append(r + 1)
                        queue_y.append(c)
            # move left
            if c - 1 >= 0:
                if self.map[r][c - 1] is not 1:
                    if self.step[r][c - 1] > self.step[r][c] + 1:
                        self.step[r][c - 1] = self.step[r][c] + 1
                        queue_r.append(r)
                        queue_y.append(c - 1)

            # move left
            if c + 1 < 50:
                if self.map[r][c + 1] is not 1:
                    if self.step[r][c + 1] > self.step[r][c] + 1:
                        self.step[r][c + 1] = self.step[r][c] + 1
                        queue_r.append(r)
                        queue_y.append(c + 1)
        # setting direction of enemy
        count = 1

    def avoid_wall(self, enemy: Blob, walls: TiledMap)-> None:
        """
        Causes enemy to go around a wall should it hit one
        :param enemy: enemy
        :param walls: spritelist of walls
        :return: none
        """
        pass


ShortestPath().shortest_distance(0, 0, 0, 0)
