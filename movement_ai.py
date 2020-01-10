import arcade
import csv


class ShortestPath():
    def __init__(self):
        self.map = []
        with open("Maps/tilemap.txt") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.map.append(row)

    def shortest_distance(self, current_x, current_y, next_x, next_y):
        pass