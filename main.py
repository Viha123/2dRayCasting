import pygame
import math
import random
pygame.init()

WIN_HEIGHT = 600
WIN_WIDTH = 600

WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
run = True
#class Boundary, class Ray
#general notes:
#https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
#first you need to check if a particular ray will intersect. 
#ONLY if it does, then you can calculate the intersection point
#There will be an intersection if 0 ≤ t ≤ 1 and 0 ≤ u -> according to wiki page

class Boundary:
  def __init__(self, p1, p2):
    self.p1 = p1 #wall pt 1
    self.p2 = p2 #wall pt 2
  def drawBoundary(self):
    pygame.draw.line(WINDOW, WHITE, self.p1.vector(), self.p2.vector(),3)
  

class Ray:
  def __init__(self, pt,walls):
    self.pt3 = pt #pt 1 of line segment 1 (ray pt 1)
    self.dir = []
    self.unit = 15
    self.walls = walls
    for deg in range(0,360,1):
      self.dir.append(Point(self.unit*math.cos(deg)+self.pt3.x,self.unit*math.sin(deg)+self.pt3.y))  
    #self.dir = Point(self.pt3.x + 15, self.pt3.y + 8.5)
    # self.p1 = p1
    # self.p2 = p2
    
  def drawRay(self):
    pygame.draw.circle(WINDOW, WHITE, self.pt3.vector(), 10) 
    #works! but I need to make the ray cast code before I let these loose
    for element in self.dir:
      endPoint = self.compute(element)
      if(endPoint):    
        pygame.draw.line(WINDOW, WHITE, self.pt3.vector(),endPoint.vector())
      # else:
      #   pygame.draw.line(WINDOW, WHITE, self.pt3.vector(), element.vector())
    for wall in walls:
      wall.drawBoundary()
    
  def compute(self, pt4):
    #x1 = self.wall.
    closest = self.pt3
    min = 10000
    
    for wall in self.walls:
      
      den = ((wall.p1.x - wall.p2.x)*(self.pt3.y - pt4.y)) - ((wall.p1.y-wall.p2.y)*(self.pt3.x-pt4.x))
      if(den != 0):
        
        t = (((wall.p1.x - self.pt3.x)*(self.pt3.y - pt4.y)) - ((wall.p1.y - self.pt3.y)*(self.pt3.x-pt4.x))) / den
        u = (((wall.p1.x - self.pt3.x) * (wall.p1.y - wall.p2.y)) - ((wall.p1.y - self.pt3.y)*(wall.p1.x-wall.p2.x))) / den
        if(t > 0 and t < 1 and u > 0):
          intX = wall.p1.x + t*(wall.p2.x - wall.p1.x)
          intY =  wall.p1.y + t*(wall.p2.y - wall.p1.y)
          intersect = Point(intX, intY)
          distance = math.sqrt((((self.pt3.x - intX) * (self.pt3.x - intX))+ ((self.pt3.y - intY) * (self.pt3.y - intY))))
          if(distance<=min):
            min = distance
            closest = intersect
            
    return closest

class Point:
  def __init__(self, x, y):
      self.x = x
      self.y = y
  def vector(self):
      return (self.x,self.y)
pygame.time.Clock().tick(10)

def creatingBoundaries():
  walls = []
  pTopLeft = Point(0,0)
  pTopRight = Point(600,0)
  pBottomLeft = Point(0,600)
  pBottomRight = Point(600,600)
  topWall = Boundary(pTopLeft, pTopRight)
  rightWall = Boundary(pTopRight,pBottomRight)
  bottomWall = Boundary(pBottomLeft, pBottomRight)
  leftWall = Boundary(pTopLeft, pBottomLeft)
  walls = walls + [topWall,rightWall, bottomWall ,leftWall]
  for i in range(0,4):
      p1 = Point(random.randint(0,600), random.randint(0,600))
      p2 = Point(random.randint(0,600), random.randint(0,600))
    
      wall = Boundary(p1,p2)
      wall.drawBoundary()
      walls.append(wall)

  return walls

def main():
  
  p3 = Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
  #creating boundaries at the corner
  
  ray = Ray(p3,walls)

  ray.drawRay()
  pygame.display.update()

  
global walls
walls = creatingBoundaries()
while run:
  pygame.Surface.fill(WINDOW, BLACK)
  isCurrent = True
  
  main()
  #min = 

  for event in pygame.event.get():
      if event.type==pygame.QUIT:
          pygame.quit()
  #pygame.time.delay(6000)
  pygame.display.update()
