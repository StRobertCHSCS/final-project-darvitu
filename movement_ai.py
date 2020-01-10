import arcade
import csv
import math
import sys


class ShortestPath():
    def __init__(self):
        self.map = []
        with open("Maps/tilemap.txt") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.map.append(row)

    def shortest_distance(self, current_x, current_y, next_x, next_y):
        # create step/distance array
        step = [[999999 for x in range(50)] for y in range(50)]
        # create queues
        queue_x = []
        queue_x.append(current_x)
        queue_y = []
        queue_y.append(current_y)
        # add first node
        step[current_x][current_y] = 0
        # add end node
        step[next_x][next_y] = -1
        # perform breadth-first-search
        while len(queue_x) is not 0:
            # current location
            r = queue_x.pop(0)
            c = queue_y.pop(0)

            #move up

ShortestPath().shortest_distance(0, 0, 0, 0)
