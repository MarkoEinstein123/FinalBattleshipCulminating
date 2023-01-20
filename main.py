import random
from random import randint
import time
import os
import pygame, sys
from button import Button
import database


#Basic Grid Setup and System
pygame.init()
bounds = (400,450)
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
font_one = pygame.font.SysFont('comicsans',60, True)
shots_left = 60

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

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
  
        
def shotsleft():
  global shots_left
  window.fill(LIGHT_BLUE, rect=(0,400,400,50))
  SHOTS_LEFT_TEXT = get_font(10).render(str(shots_left) + "/60 Shots Left", True, BLACK)
  window.blit(SHOTS_LEFT_TEXT, [100,425])

def ship_location():
  x,y= 0,0
  #window.fill(LIGHT_BLUE, rect=(0,400,400,50))
  #SHOTS_LEFT_TEXT = get_font(10).render(str(shots_left) + "/60 Shots Left", True, BLACK)
  #SHOTS_LEFT_RECT = SHOTS_LEFT_TEXT.get_rect(center=(100, 425))
  for row in grid:
    for col in row:
      #if col == 1:
        #pygame.draw.rect(window, BLACK, pygame.Rect(x, y, 40, 40),  2)
        #pygame.draw.rect(window, BLACK, pygame.Rect(x+1, y+1, 38, 38))
      if col == 3:
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
  global shots_left
  mouse = pygame.mouse.get_pos()
  left_click = pygame.mouse.get_pressed()[0]
  
  if left_click == True and mouse[1]<=399: 
    a,b = int(mouse[0]/40), int(mouse[1]/40)
    if grid[b][a] == 1:
      grid[b][a] = 3
      shots_left -= 1
      game_over_check()
    elif grid[b][a] == 0:
      grid[b][a] = 4
      shots_left -= 1
      game_over_check()

  return shots_left
def respawn():
  grid = [[0]*10 for n in range(10)]
  print(grid)
  ship_positions = []
  count = 0
  shots_left = 0
  print(shots_left)
  start_function()
  main_game()
  return grid, ship_positions, count, shots_left

def game_over_screen(win_screen):
  global shot_left
  global database

  if 60 - shots_left < int(database_highscore[0][0]):
    database.write_table(shots_left)
  while True:
      window.fill(LIGHT_BLUE)

      MENU_MOUSE_POS = pygame.mouse.get_pos()

      if win_screen == True:
        MENU_TEXT = get_font(32).render("You Win", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 50))

      if win_screen == False:
        MENU_TEXT = get_font(32).render("You Lose", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 50))

      if 60 - shots_left < int(database_highscore[0][0]):
        HIGHSCORE_TEXT = get_font(10).render("NEW HIGHSCORE!", True, RED)
        HIGHSCORE_RECT = HIGHSCORE_TEXT.get_rect(center=(200, 80))
        window.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)

      RESTART_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 130), 
                          text_input="RESTART", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      MENU_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 230), 
                          text_input="MENU", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      QUIT_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 330), 
                          text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

      window.blit(MENU_TEXT, MENU_RECT)
      for button in [RESTART_BUTTON, MENU_BUTTON, QUIT_BUTTON]:
          button.changeColor(MENU_MOUSE_POS)
          button.update(window)
      
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN:
              if RESTART_BUTTON.checkForInput(MENU_MOUSE_POS):
                  respawn()
              if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                  main_menu()
              if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                  pygame.quit()
                  sys.exit()

      pygame.display.update()
  
def game_over_check():
  global shots_left
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
    win_screen = True
    game_over_screen(win_screen)
    return count
  elif shots_left == 0:
    win_screen = False
    game_over_screen(win_screen)

def info():
  while True:
    instructions_background = pygame.image.load("instructions.png").convert()
    window.blit(instructions_background, (0, 0))
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    BACK_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 390), 
                          text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
    
    for button in [BACK_BUTTON]:
          button.changeColor(MENU_MOUSE_POS)
          button.update(window)

    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN:
              if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                  main_menu()
    pygame.display.update()

def pause():
  while True:
      window.fill(LIGHT_BLUE)
  
      MENU_MOUSE_POS = pygame.mouse.get_pos()
  
      BACK_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 330), 
                            text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      
      for button in [BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
  
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_game()
      pygame.display.update()



def main_menu():
  database_highscore = database.read_file()
  while True:
      window.fill(LIGHT_BLUE)

      MENU_MOUSE_POS = pygame.mouse.get_pos()

      MENU_TEXT = get_font(32).render("Battleships", True, BLACK)
      MENU_RECT = MENU_TEXT.get_rect(center=(200, 50))

      HIGHSCORE_TEXT = get_font(10).render("Highscore:" + database_highscore[0][0], True, RED)
      HIGHSCORE_RECT = HIGHSCORE_TEXT.get_rect(center=(200,75))
      
      PLAY_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 130), 
                          text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      INFO_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 230), 
                          text_input="INFO", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
      QUIT_BUTTON = Button(image=pygame.image.load("rsz_2play_rect.png"), pos=(200, 330), 
                          text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

      window.blit(MENU_TEXT, MENU_RECT)
      window.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)

      for button in [PLAY_BUTTON, INFO_BUTTON, QUIT_BUTTON]:
          button.changeColor(MENU_MOUSE_POS)
          button.update(window)
      
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN:
              if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                  start_function()
                  main_game()
              if INFO_BUTTON.checkForInput(MENU_MOUSE_POS):
                  info()
              if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                  pygame.quit()
                  sys.exit()

      pygame.display.update()

def start_function():
  background()
  draw_grid()

def main_game():
  run = True
  background()
  while run:
      timer.tick(60)
      ship_location()
      shotsleft()
      shoot()
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            pause()
        if event.type == pygame.QUIT:
          run = False
  
  
  
  
      
      pygame.display.flip()
  pygame.quit()

database_highscore = database.read_file()
print(database_highscore)
main_menu()
  