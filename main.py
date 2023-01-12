import random
from random import randint
import time
import os
import pygame, sys

#Basic Grid Setup and System
pygame.init()
bounds = (400,400)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Battleships")
timer = pygame.time.Clock()
fps = 60
grid = [[0]*10 for n in range(10)]
width = 40
LIGHT_BLUE = (173,216,230)
BlUE = (0,0,255)
BLACK = (0 , 0 , 0)
RED = (255 , 0 , 0)
GREEN = (0 , 255 , 0)
ship_positions = []
count = 0

def validate_and_place_ship(start_row, end_row, start_col, end_col):
  global grid
  global ship_positions
  
  #Checks if it is empty space: if not, returns false
  all_valid = True
  for r in range(start_row, end_row):
    for c in range(start_col, end_col):
      if grid[r][c] != 0:
        all_valid = False
        break
  
  #Will only activate once all valid is true
  if all_valid == True:
    ship_positions.append([start_row, end_row, start_col, end_col])
    for r in range(start_row, end_row):
      for c in range(start_col, end_col):
        grid[r][c] = 1
  return all_valid

def try_to_place_ship_on_grid(row, col, direction, length):
  grid_size = 10
  
  start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
  
  if direction == "left":
    if col - length < 0:
      return False
    start_col = col - length + 1
  
  elif direction == "right":
    if col + length >= grid_size:
      return False
    end_col = col + length
  
  elif direction == "up":
    if row - length < 0:
      return False
    start_row = row - length + 1
  
  elif direction == "down":
    if row + length >= grid_size:
      return False
    end_row = row + length
  
  return validate_and_place_ship(start_row, end_row, start_col, end_col)

def draw_grid():
  x,y= 0,0
  for row in grid:
    for col in row:
      pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
      x = x + width
      pygame.display.flip()
    y = y + width    
    x = 0

  num_of_ships_placed = 0
  num_of_ships = 5
  ship_positions = []
  ship_size_number = 0
  while num_of_ships_placed != num_of_ships:
    random_row = random.randint(0, 9)
    random_col = random.randint(0, 9)
    direction = random.choice(["left", "right", "up", "down"])
    size = [2,3,3,4,5]
    ship_size = size[ship_size_number]
    
    if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
      num_of_ships_placed += 1 
      ship_size_number += 1
  
        
      

def ship_location():
  x,y= 0,0
  for row in grid:
    for col in row:
      if col == 1:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
        pygame.draw.rect(window, BLACK, pygame.Rect(x+1, y+1, 38, 38))
      elif col == 3:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
        pygame.draw.rect(window, RED, pygame.Rect(x+1, y+1, 38, 38))
      elif col == 4:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
        pygame.draw.rect(window, BlUE, pygame.Rect(x+1, y+1, 38, 38))
      else:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
      x = x + width
      pygame.display.flip()
    y = y + width    
    x = 0
  
def background():
  window.fill(LIGHT_BLUE)
  pygame.display.flip()
              

def shoot():
  mouse = pygame.mouse.get_pos()
  left_click = pygame.mouse.get_pressed()[0]
  
  if left_click == True: 
    a,b = int(mouse[0]/40), int(mouse[1]/40)
    if grid[b][a] == 1:
      grid[b][a] = 3
      game_over()
    elif grid[b][a] == 0:
      grid[b][a] = 4

def game_over():
  count = 0
  x,y= 0,0
  for row in grid:
   for col in row:
    if col == 3:
      count += 1
    x = x + width
  y = y + width    
  x = 0
  if count == 17:
    quit()
def get_mouse_position():
  run = True
  while run:
    timer.tick(10)
    ship_location()
    shoot()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
  
    pygame.display.flip()
  pygame.quit()
background()
draw_grid()
get_mouse_position()




  
  