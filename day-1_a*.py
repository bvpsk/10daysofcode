
#   start => loop(check => plot shortest path => grow)

import numpy as np
from random import randint as r
import pygame
from time import sleep
screen_x = 1000
screen_y = 750
last_child = []
background = (51,51,51)
total_cities = 30
sleep_time = 0.1
probability_for_second_con = 0.7
probability_for_third_con = 0.45
screen = pygame.display.set_mode((screen_x,screen_y))
class Node:
    def __init__(self,val):
        self.val = val
        self.child = []
        self.parent = None
class CITY:
    def __init__(self,i):
        self.i = i
        self.x = r(50,screen_x-50)
        self.y = r(50,screen_y-50)
        self.h = 0
        self.f = 0
        self.g = 0
        self.neighbors = []
    def show(self):
        pygame.draw.circle(screen,(255,0,0),(self.x,self.y),5,0)
cities = [CITY(i) for i in range(total_cities)]
class ROAD:
    def __init__(self,a,b):
        self.c1 = a
        self.c2 = b
    def show(self):
        pygame.draw.line(screen,(255,255,255),(self.c1.x,self.c1.y),(self.c2.x,self.c2.y),2)



def find_extremes(tree):
    global last_child
    if len(tree.child) != 0:
        for ch in tree.child:
            find_extremes(ch)
    else:
        last_child.append(tree)

cities_dict = {j.x:i for (i,j) in zip(range(total_cities),cities)}
order = [i.x for i in cities]
for i in range(total_cities):
    for j in range(total_cities - i - 1):
        if order[j] > order[j+1]:
            temp = order[j]
            order[j] = order[j+1]
            order[j+1] = temp
order = [cities_dict[o] for o in order]
roads = []
for i in range(total_cities-1):
    roads.append(ROAD(cities[order[i]],cities[order[i+1]]))
    cities[order[i]].neighbors.append(order[i+1])
    cities[order[i+1]].neighbors.append(order[i])
    if i > 1 and i < total_cities-2:
        if np.random.random() <= probability_for_second_con:
            roads.append(ROAD(cities[order[i]],cities[order[i+2]]))
            cities[order[i]].neighbors.append(order[i+2])
            cities[order[i+2]].neighbors.append(order[i])
        if np.random.random() <= probability_for_third_con:
            roads.append(ROAD(cities[order[i]],cities[order[i-2]]))
            cities[order[i]].neighbors.append(order[i-2])
            cities[order[i-2]].neighbors.append(order[i])


class AGENT:
    def __init__(self):
        self.path = []
        self.closedSet = []
        self.openSet = [i for i in range(total_cities)]
        self.found = False
    def connect(self):
        for i in range(len(self.path) - 1):
            pygame.draw.line(screen,(0,255,0),(cities[self.path[i]].x,cities[self.path[i]].y),(cities[self.path[i+1]].x,cities[self.path[i+1]].y),2)
    def start(self):
        self.tree = Node(order[0])
        self.closedSet.append(order[0])
        self.openSet.remove(order[0])
        for n in cities[order[0]].neighbors:
            neighbor = cities[n]
            neighbor.g = np.hypot(neighbor.x-cities[order[0]].x,neighbor.y-cities[order[0]].y)
            neighbor.h = np.hypot(neighbor.x-cities[order[len(order)-1]].x,neighbor.y-cities[order[len(order)-1]].y)
            neighbor.f = neighbor.g + neighbor.h
            c = Node(neighbor.i)
            c.parent = self.tree
            self.tree.child.append(c)
    def grow(self):
        if self.spawn == None:
            return False
        else:
            self.openSet.remove(self.spawn.val)
            self.closedSet.append(self.spawn.val)
            for neighbor in cities[self.spawn.val].neighbors:
                if neighbor not in self.closedSet:
                    cities[neighbor].g = np.hypot(cities[neighbor].x-cities[self.spawn.val].x,cities[neighbor].y-cities[self.spawn.val].y)
                    cities[neighbor].h = np.hypot(cities[neighbor].x-cities[self.spawn.val].x,cities[neighbor].y-cities[self.spawn.val].y)
                    cities[neighbor].f = cities[neighbor].g + cities[neighbor].h
                    c = Node(neighbor)
                    c.parent = self.spawn
                    self.spawn.child.append(c)
        return True

    def check(self):
        global last_child
        last_child = []
        find_extremes(self.tree)
        for i in last_child:
            if i.val == order[total_cities - 1]:
                self.spawn = i
                self.found = True
                return True
        ord_dict = {cities[ch.val].f:j for (ch,j) in zip(last_child,range(len(last_child)))}
        orde = [cities[ch.val].f for ch in last_child]
        for i in range(len(orde)):
            for j in range(len(orde) - i - 1):
                if orde[j] > orde[j+1]:
                    temp = orde[j]
                    orde[j] = orde[j+1]
                    orde[j+1] = temp
        self.spawn = None
        for o in orde:
            if last_child[ord_dict[o]].val not in self.closedSet:
                self.spawn = last_child[ord_dict[o]]
                break
        return False

    def shortest_path(self):
        if self.spawn != None:
            self.path = []
            sp = self.spawn
            while sp.parent != None:
                self.path.append(sp.val)
                sp = sp.parent
            self.path.append(sp.val)
            self.path = self.path[::-1]
        # return True




a = AGENT()
a.start()
'''
if not a.check():
    while a.grow():
        print a.closedSet,a.openSet
        if a.check():
            print "sol found"
            break
        a.shortest_path()

else:
    print "b-no sol"
    print a.openSet,a.closedSet
a.shortest_path()
print a.path
'''
# exit()
run = False
if not a.check():
    run = True

while run:
    sleep(sleep_time)
    screen.fill(background)
    for city in cities:
        city.show()
    for road in roads:
        road.show()
    a.connect()
    if not a.found:
        if a.grow():
            if a.check():
                print "solution found"
            a.shortest_path()
        else:
            print "not growing"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
