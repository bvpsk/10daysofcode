import numpy as np
from random import randint as r
import pygame
screen_x = 700
screen_y = 600
last_child = []
background = (51,51,51)
total_cities = 13
probability_for_second_con = 0.7
probability_for_third_con = 0.45
screen = pygame.display.set_mode((screen_x,screen_y))
class Node:
    def __init__(self,val):
        self.val = val
        self.child = []
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
# print order
# print cities_dict
order = [cities_dict[o] for o in order]
# roads = [ROAD(cities[r(0,total_cities-1)],cities[r(0,total_cities-1)]) for i in range(total_roads)]
roads = []
# print len(cities)
for i in range(total_cities-1):
    roads.append(ROAD(cities[order[i]],cities[order[i+1]]))
    cities[order[i]].neighbors.append(i+1)
    cities[order[i+1]].neighbors.append(i)
    if i > 1 and i < total_cities-2:
        if np.random.random() <= probability_for_second_con:
            roads.append(ROAD(cities[order[i]],cities[order[i+2]]))
            cities[order[i]].neighbors.append(i+2)
            cities[order[i+2]].neighbors.append(i)
        if np.random.random() <= probability_for_third_con:
            roads.append(ROAD(cities[order[i]],cities[order[i-2]]))
            cities[order[i]].neighbors.append(i-2)
            cities[order[i-2]].neighbors.append(i)
run = True


class AGENT:
    def __init__(self):
        self.cities = []
        self.closedSet = []
        self.openSet = [i for i in range(total_cities)]
    def connect(self):
        for i in range(total_cities - 1):
            pygame.draw.line(screen,(0,255,0),(cities[i].x,cities[i].y),(cities[i+1].x,cities[i+1].y),2)
    def start(self):
        self.tree = Node(order[0])
        self.closedSet.append(order[0])
        self.openSet.remove(order[0])
        for n in cities[order[0]].neighbors:
            neighbor = cities[n]
            neighbor.g = np.hypot(neighbor.x-cities[order[0]].x,neighbor.y-cities[order[0]].y)
            neighbor.h = np.hypot(neighbor.x-cities[order[len(order)-1]].x,neighbor.y-cities[order[len(order)-1]].y)
            neighbor.f = neighbor.g + neighbor.h
            self.tree.child.append(Node(neighbor.i))
            self.closedSet.append(neighbor.i)
            self.openSet.remove(neighbor.i)
    def grow(self):
        global last_child
        last_child = []
        find_extremes(self.tree)
        ord_dict = {cities[ch.val].f:j for (ch,j) in zip(last_child,range(len(last_child)))}
        orde = [cities[ch.val].f for ch in last_child]
        for i in range(len(orde)):
            for j in range(len(orde) - i - 1):
                if orde[j] > orde[j+1]:
                    temp = orde[j]
                    orde[j] = orde[j+1]
                    orde[j+1] = temp
        spawn = None
        for o in orde:
            if last_child[ord_dict[o]].val not in self.closedSet:
                spawn = last_child[ord_dict[o]]
                break
        if spawn == None:
            return False
        else:
            self.openSet.remove(spawn.val)
            self.closedSet.append(spawn.val)
            for neighbor in cities[spawn.val].neighbors:
                if neighbor.i not in self.closedSet:
                    neighbor.g = np.hypot(neighbor.x-cities[spawn.val].x,neighbor.y-cities[spawn.val].y)
                    neighbor.h = np.hypot(neighbor.x-cities[spawn.val].x,neighbor.y-cities[spawn.val].y)
                    neighbor.f = neighbor.g + neighbor.h
                    spawn.child.append(Node(neighbor.i))
                    self.closedSet.append(neighbor.i)
                    self.openSet.remove(neighbor.i)
        return True

    def check(self):
        global last_child
        last_child = []
        find_extremes(self.tree)
        for i in last_child:
            if i.val == order[total_cities - 1]:
                return True
        return False








a = AGENT()
a.start()
while run:
    screen.fill(background)
    for city in cities:
        city.show()
    for road in roads:
        road.show()
    if not a.check():
        if not a.grow():
            print "no solution"
            run = False
    else:
        print "done"
        run = False
    # a.connect()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
