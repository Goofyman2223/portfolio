import os
import pygame
from sys import exit
import time
import random

pygame.init()
pygame.mixer.init()

#Game states
main = True

info_screen = False

settings_screen = False

gamemode_1 = False
gamemode_1_weapon_menu = False
gamemode_1_character_menu = False

gamemode_2 = False
gamemode_2_weapon_menu = False
gamemode_2_character_menu = False
gamemode_2_show_character = False
gamemode_2_show_weapon = False

hit_count = 0
crit_count = 0
miss_count = 0

end_screen = False

character_choice = None
weapon_choice = None
Dead = False
Fight = False
RUN = True
action = False

#music settings
music_loops = 100000
volume = .2
sfx_volume = .1

#background music
background_song = pygame.mixer.music.load("SFX/Background_song.wav")

#Sound effects for the game
bomb_explode = pygame.mixer.Sound("SFX/Bomb_sfx.mp3")

grenade_explode = pygame.mixer.Sound("SFX/Grenade_sfx.mp3")

holy_sfx = pygame.mixer.Sound("SFX/Holy_sfx.mp3")

pistol_shot = pygame.mixer.Sound("SFX/Pistol_sfx.mp3")

spikey_swing = pygame.mixer.Sound("SFX/Spikey_sfx.mp3")

info_sfx = pygame.mixer.Sound("SFX/Idea_sfx.mp3")

settings_sfx = pygame.mixer.Sound("SFX/Settings_sfx.mp3")




#Fonts/title info
pygame.display.set_caption("Dummy Demolisher")
screen = pygame.display.set_mode((900,600))
title_font = pygame.font.Font("Thinkpad.otf",60)
name_font = pygame.font.Font("Thinkpad.otf",40)
clock = pygame.time.Clock()
TITLE = "DUMMY DEMOLISHER"

#weapon damage numbers
bomb_damage = random.randint(60,150)
grenade_damage = random.randint(30,55)
holy_damage = random.randint(420,690)
pistol_damage = random.randint(5,15)
spikey_damage = random.randint(30,70)

#weapon images
bomb = pygame.image.load("Side_view_weapons/Bomb.png").convert_alpha()
bomb_hover = pygame.image.load("Mouse_hover_weapons/Bomb_hover.png").convert_alpha()
bomb_text = name_font.render(f"DAMAGE: {bomb_damage}",False,(0,255,0))

grenade = pygame.image.load("Side_view_weapons/Grenade.png").convert_alpha()
grenade_hover = pygame.image.load("Mouse_hover_weapons/Grenade_hover.png").convert_alpha()

holy_hand_grenade = pygame.image.load("Side_view_weapons/Holy_Hand_Grenade.png").convert_alpha()
holy_hover = pygame.image.load("Mouse_hover_weapons/Holy_Hand_Grenade_hover.png").convert_alpha()

pistol = pygame.image.load("Side_view_weapons/Pistol.png").convert_alpha()
pistol_hover = pygame.image.load("Mouse_hover_weapons/Pistol_hover.png").convert_alpha()

spikey_mace = pygame.image.load("Side_view_weapons/Spikey_Mace.png").convert_alpha()
spikey_hover = pygame.image.load("Mouse_hover_weapons/Spikey_Mace_hover.png").convert_alpha()

#character images
big_boss = pygame.image.load("Characters/Big_Boss.png")
big_hover = pygame.image.load("Character_hover/Big_hover.png")

cyborg = pygame.image.load("Characters/Cyborg.png")
cyborg_hover = pygame.image.load("Character_hover/Cyborg_hover.png")

small_fry = pygame.image.load("Characters/Small_fry.png")
small_hover = pygame.image.load("Character_hover/Small_hover.png")

zombie = pygame.image.load("Characters/Zombie.png")
zombie_hover = pygame.image.load("Character_hover/Zombie_hover.png")


#Character health numbers
big_health = random.randint(300,500)
cyborg_health = random.randint(600, 800)
small_health = random.randint(50, 100)
zombie_health = random.randint(150, 600)


#weapon class
class weapon_buttons():
  
  def __init__(self,x,y,image_1,image_2,scale,scale_2):
    width_1 = image_1.get_width()
    height_1 = image_1.get_height()
    width_2 = image_2.get_width()
    height_2 = image_2.get_height()
    self.image_1 = pygame.transform.scale(image_1,(int(width_1 * scale), int(height_1 * scale)))
    self.image_2 = pygame.transform.scale(image_2,(int(width_2 *scale_2), int(height_2 * scale_2)))
    self.rect_1 = self.image_1.get_rect()
    self.rect_1.topleft = (x,y)
    self.rect_2 = self.image_2.get_rect()
    self.rect_2.topleft = (x,y)
    self.menu_status = True
    self.character_status = False
    self.click = True
  
  #Draws weapon to screen and tests for clicks
  def draw(self,image_1,image_2):
    action = False

    if self.rect_1.collidepoint(pygame.mouse.get_pos()):
      screen.blit(self.image_2,(self.rect_2.x,self.rect_2.y))
    
    else:
      screen.blit(self.image_1,(self.rect_1.x,self.rect_1.y))
    
    if self.rect_2.collidepoint(pygame.mouse.get_pos()):
      if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
        action = True
    if pygame.mouse.get_pressed()[0] == 0:
      self.click = False
    return action
    
  #Displays weapon name and damage to screen     
  def text(self,x_damage,x_text,y,damage,name):
    self.damage = int(damage)
    self.name = name
    number = name_font.render(f"DAMAGE: {self.damage}", False,(0,0,255))
    name = name_font.render(name,False,(0,0,255))
    screen.blit(number,(x_damage,y))
    screen.blit(name,(x_text,y))



#Character class
class character_buttons():
  def __init__(self,image_1,image_2,scale,scale_2):
    width_1 = image_1.get_width()
    height_1 = image_1.get_height()
    width_2 = image_2.get_width()
    height_2 = image_2.get_height()
    self.image_1 = pygame.transform.scale(image_1,(int(width_1 * scale), int(height_1 * scale)))
    self.image_2 = pygame.transform.scale(image_2,(int(width_2 *scale_2), int(height_2 * scale_2)))
    self.rect_1 = self.image_1.get_rect()
    self.rect_2 = self.image_2.get_rect()
    self.click = True

  #Draws character to screen
  def draw(self,action,x,y):
    self.rect_1.topleft = (x,y)
    self.rect_2.topleft = (x,y)
    
    action = False
    if self.rect_1.collidepoint(pygame.mouse.get_pos()):
      screen.blit(self.image_2,(self.rect_2.x,self.rect_2.y))
    else:
      screen.blit(self.image_1,(self.rect_1.x,self.rect_1.y))

    if self.rect_2.collidepoint(pygame.mouse.get_pos()):
      if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
        action = True
      
    if pygame.mouse.get_pressed()[0] == 0:
      self.click = False
    return action
    
  #Displays character name and health to the screen
  def text(self,x_health,x_text,y,health,name):
    self.health = int(health)
    self.name = name
    number = name_font.render(f"HEALTH: {self.health}", False,(0,0,255))
    name = name_font.render(name,False,(0,0,255))
    screen.blit(number,(x_health,y))
    screen.blit(name,(x_text,y))
    
  
    
class characters():
  def __init__(self,image,image_click,scale,scale_click):
    width = image.get_width()
    height = image.get_height()
    
    width_2 = image_click.get_width()
    height_2 = image_click.get_height()

    self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
    self.rect = self.image.get_rect()

    self.image_click = pygame.transform.scale(image_click,(int(width_2*scale),int(height_2*scale)))
    self.rect_2 = self.image_click.get_rect()
    
    self.click = False

  def draw(self,x,y,health):
    self.health = health
    self.rect.topleft = x,y
    self.rect_2.topleft = x,y
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
        screen.blit(self.image_click,(self.rect_2.x,self.rect_2.y))
        self.click = True
    
    elif self.rect.collidepoint(pygame.mouse.get_pos()): 
      if pygame.mouse.get_pressed()[0] == 1 and self.click == True:
        screen.blit(self.image,(self.rect.x,self.rect.y))
    
    elif pygame.mouse.get_pressed()[0] == 0:
      screen.blit(self.image,(self.rect.x,self.rect.y))
      self.click = False
    
    screen.blit(self.image,(self.rect.x,self.rect.y))
    number = name_font.render(f"HEALTH: {self.health}",False,(0,0,255))
    screen.blit(number,(x+150,y))
    

  

class weapons():
  def __init__(self,image,image_hover,scale,scale_hover):
    
    width = image.get_width()
    height = image.get_height()
    
    width_hover = image_hover.get_width()
    height_hover = image_hover.get_height()

    self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
    self.image_hover = pygame.transform.scale(image_hover, (int(width_hover*scale_hover),int(height_hover*scale_hover)))

    self.rect = self.image.get_rect()
    self.rect_hover = self.image_hover.get_rect()
    self.click = False
    self.press = False

    self.second = 120
    self.second_2 = 120

    self.play_sfx = 0

    


  def draw(self,sfx):
    self.mouse = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)
    
    self.rect.bottomright = self.mouse
    self.rect_hover.bottomright = self.mouse
    
    if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
      
      if self.second >0:
        screen.blit(self.image_hover,(self.rect_hover.center))
        self.second -=1 
        
      if self.play_sfx == 0:
        sfx.play()
        sfx.set_volume(sfx_volume)
        self.play_sfx += 1

      if self.second == 0:
        self.click = True
      
    elif pygame.mouse.get_pressed()[0] == 1 and self.click == True:
      screen.blit(self.image,self.rect.center)
    
    
    elif pygame.mouse.get_pressed()[0] == 0:
      screen.blit(self.image,self.rect.center)
      self.click = False
      self.second = 60
      self.play_sfx = 0

 
  def damage(self,character,health,damage): 
    global hit_count,crit_count,miss_count
    miss_message = name_font.render("YOU MISSED",False,(0,0,255))
    hit_message = name_font.render("HIT",False,(0,0,255))
    critical_message = name_font.render("CRITICAL HIT",False,(0,0,255))
    
    
    if pygame.mouse.get_pressed()[0] == 1 and self.press == False: 
      if self.rect_hover.colliderect(character):
        
        critical = random.randint(1,20)
        
        damage_multiplier = random.randint(2,4)
        
        miss = random.randint(1,15)
        
        if health>0:
          
          if critical == 20:
            health = health - (damage*damage_multiplier)
            screen.blit(critical_message,(100,100))
            crit_count += 1
        
          if miss == 15:
            screen.blit(miss_message,(100,100))
            miss_count += 1

          else:
            health = health - damage
            screen.blit(hit_message,(100,100))
            hit_count += 1
            
        
        else:
          health = 0
          
        self.press = True
    
    elif pygame.mouse.get_pressed()[0] == 0 and self.press == True:
      self.press = False
    return health 
      





    
#Main Menu Screen
def main_menu():
  global character_show_time
  global weapon_show_time
  global timer 
  global hit_count,crit_count,miss_count

  #Resets counters
  hit_count = 0
  crit_count = 0
  miss_count = 0
  
  #Resets values to original number
  character_show_time = 300
  weapon_show_time = 300
  timer = 600
  
  #Choice button rects
  global gamemode_1_rect, gamemode_2_rect,info_rect,settings_rect
  
  #Gamemode 1 button
  main_text = title_font.render(TITLE,False,(0,0,255))
  gamemode_1 = title_font.render("GAMEMODE 1",False,(0,0,255))
  gamemode_1_rect = gamemode_1.get_rect(center = (120,150))

  #Gamemode 2 button
  gamemode_2 = title_font.render("GAMEMODE 2",False,(0,0,255))
  gamemode_2_rect = gamemode_2.get_rect(center = (120,250))
  
  #Information button
  info = pygame.image.load("info_icon.png")
  info = pygame.transform.scale(info,(info.get_width() * 5,info.get_height()*5))
  info_rect = info.get_rect(center = (800,50))
  
  #Settings button
  settings = pygame.image.load("settings_icon.png")
  settings = pygame.transform.scale(settings, (settings.get_width() *6 , settings.get_height()*6 ))
  settings_rect = settings.get_rect(topleft = (50,20))

  #Shows character in the middle of the screen
  character_transform = pygame.transform.scale(big_boss,(200,275))
  transform_rect = character_transform.get_rect(topleft = (300,75))
  character_hover = pygame.transform.scale(big_hover, (187,275))
  hover_rect = character_hover.get_rect(topleft = (299,75))
 
  screen.fill((199,18,24))
  screen.blit(main_text,(320,25))
  screen.blit(gamemode_1,gamemode_1_rect)
  screen.blit(gamemode_2,gamemode_2_rect)
  screen.blit(info,info_rect)
  screen.blit(settings,settings_rect)
  if transform_rect.collidepoint(pygame.mouse.get_pos()):
    screen.blit(character_hover,hover_rect)
  else:
    screen.blit(character_transform,transform_rect)

#weapon button instances
bomb_button = weapon_buttons(120,50,bomb,bomb_hover,1,3)
grenade_button = weapon_buttons(155,95,grenade,grenade_hover,1,3)
spikey_button = weapon_buttons(220,150,spikey_mace,spikey_hover,1,1)
holy_button = weapon_buttons(300,200,holy_hand_grenade,holy_hover,1,1)
pistol_button = weapon_buttons(120,250,pistol,pistol_hover,1,1.1)

#Allows the user to select a weapon
def gamemode_1_weapons():
  global weapon_choice
  screen.fill((199,18,24))
  main_text = title_font.render(TITLE,False,(0,0,255))
  screen.blit(main_text,(370,20))
  
  if bomb_button.draw(bomb,bomb_hover) == True:
    weapon_choice = "Bomb"
    return weapon_choice 
  bomb_button.text(170,10,50,bomb_damage,"BOMB")
  
  if grenade_button.draw(grenade,grenade_hover) == True:
    weapon_choice = "Grenade"
    return weapon_choice
  grenade_button.text(220,10,100,grenade_damage,"GRENADE")
  
  if spikey_button.draw(spikey_mace,spikey_hover) == True:
    weapon_choice = "Spikey Mace"
    return weapon_choice
  spikey_button.text(300,10,150,spikey_damage,"SPIKEY MACE")
  
  
  if holy_button.draw(holy_hand_grenade,holy_hover) == True:
    weapon_choice = "Holy Hand Grenade"
    return weapon_choice
   
  holy_button.text(375,10,200,holy_damage,"HOLY HAND GRENADE")
  
  if pistol_button.draw(pistol,pistol_hover) == True:
    weapon_choice = "Pistol"
    return weapon_choice
  pistol_button.text(200,10,250,pistol_damage,"PISTOL")
  
  
  


#Character button instances
big_button = character_buttons(big_boss,big_hover,1,1)
cyborg_button = character_buttons(cyborg,cyborg_hover,1,1)
small_button = character_buttons(small_fry,small_hover,1,1)
zombie_button = character_buttons(zombie,zombie_hover,1,1)



#Character selection screen for gamemode 1
def gamemode_1_characters():
  global character_choice
  global health
  screen.fill((199,18,24))
  main_text = title_font.render(TITLE,False,(0,0,255))
  screen.blit(main_text,(370,20))
  
  if big_button.draw(action,150,20) != False:
    character_choice = "Big Boss"
    health = big_health
    return character_choice
  big_button.text(220,10,70,big_health,"BIG BOSS")
  
  if cyborg_button.draw(action,140,135) != False:
    character_choice = "Cyborg"
    health = cyborg_health
    return character_choice
  cyborg_button.text(220,10,185,cyborg_health,"CYBORG")
  
  if small_button.draw(action,150,260) != False:
    character_choice = "Small Fry"
    health = small_health
    return character_choice
  small_button.text(220,10,290,small_health,"SMALL FRY")
  
  if zombie_button.draw(action,150,360) != False:
    character_choice = "Zombie"
    health = zombie_health
    return character_choice
    
  zombie_button.text(220,10,400,zombie_health,"ZOMBIE")
  
  
  
  
  
#character instances for fight sequence 
big_class = characters(big_boss,big_hover,2,2)

zombie_class = characters(zombie,zombie_hover,2,2)

cyborg_class = characters(cyborg,cyborg_hover,2,2)

small_class = characters(small_fry,small_hover,2,2)

#(self,image,image_hover,scale,scale_hover,mouse)

#weapon instances for fight sequence
bomb_class = weapons(bomb,bomb_hover,1.5,4)

grenade_class = weapons(grenade,grenade_hover,1.5,4)

spikey_class = weapons(spikey_mace,spikey_hover,1.5,2)

pistol_class = weapons(pistol,pistol_hover,1.5,2)

holy_class = weapons(holy_hand_grenade,holy_hover,1.5,2)


weapon_list = [["Bomb",bomb_damage],
               ["Grenade",grenade_damage],
               ["Spikey Mace",spikey_damage],
               ["Pistol",pistol_damage],
               ["Holy Hand Grenade",holy_damage]]

#Finds the damage value for the randomly selected weapon
def damage_search(weapon_choice):
  for row in range(len(weapon_list)):
    for item in range(len(weapon_list[row])):
      if weapon_list[row][item] == weapon_choice:
        return weapon_list[row][1]


#The computer randomly selects a weapon from the list above
def gamemode_2_weapon_choice():
  choice_int = random.randint(0, 4)
  global weapon_choice
  global damage
  for row in range(len(weapon_list)):
    for item in range(len(weapon_list[row])):
      if weapon_list[row][item] == weapon_list[choice_int][0]:
        weapon_choice = weapon_list[row][0]
        damage = damage_search(weapon_choice)



bomb_transform = pygame.transform.scale(bomb,(bomb.get_width()*2,bomb.get_height()*2))


grenade_transform = pygame.transform.scale(grenade,(grenade.get_width()*2,grenade.get_height()*2))


spikey_transform = pygame.transform.scale(spikey_mace,(spikey_mace.get_width()*2,spikey_mace.get_height()*2))


pistol_transform = pygame.transform.scale(pistol,(pistol.get_width()*2,pistol.get_height()*2))

holy_transform = pygame.transform.scale(holy_hand_grenade,(holy_hand_grenade.get_width()*2,holy_hand_grenade.get_height()*2))

#shows the weapon for approximately 5 seconds
weapon_show_time = 300


#Shows the user the weapon that the computer has randomly selected
def show_weapon():
  global weapon_show_time
  screen.fill((199,18,24))
  choice_message = title_font.render("THE COMPUTER HAS CHOSE",False,(0,0,255)) 
  
  
  weapon_message = title_font.render(weapon_choice.upper(),False,(0,0,255))
  
  if weapon_show_time >0:
    screen.blit(choice_message,(175,20))
    
    
    if weapon_choice == "Bomb":
      screen.blit(bomb_transform,(350,150))
      screen.blit(weapon_message,(330,400))
    
    elif weapon_choice == "Grenade":
      screen.blit(grenade_transform,(350,150))
      screen.blit(weapon_message,(300,400))
   
    elif weapon_choice == "Spikey Mace":
      screen.blit(spikey_transform,(350,150))
      screen.blit(weapon_message,(260,400))
    
    elif weapon_choice == "Pistol":
      screen.blit(pistol_transform,(350,150))
      screen.blit(weapon_message,(325,400))
    
    elif weapon_choice == "Holy Hand Grenade":
      screen.blit(holy_transform,(350,150))
      screen.blit(weapon_message,(200,400))
    weapon_show_time -=1


#Character list for randomly assigning a character and it's health value
character_list = [["Big Boss",big_health],
                  ["Zombie",zombie_health],
                  ["Cyborg",cyborg_health],
                  ["Small Fry",small_health]]



#This searches for the character's health number
def health_search(character_choice):
  for row in range(len(character_list)):
    for item in range(len(character_list[row])):
      if character_list[row][item] == character_choice:
        return character_list[row][1]


#The computer randomly chooses a character for the player
def gamemode_2_character_choice():
  choice_int = random.randint(0, 3)
  global character_choice
  global health
  for row in range(len(character_list)):
    for item in range(len(character_list[row])):
      if character_list[row][item] == character_list[choice_int][0]:
        character_choice = character_list[row][0]
        health = health_search(character_choice)
        
#Shows the character for approximately 5 seconds 
character_show_time = 300

#shows the user what character the computer has randomly selected
def show_character():
  global character_show_time
  screen.fill((199,18,24))
  choice_message = title_font.render("THE COMPUTER HAS CHOSE",False,(0,0,255)) 
  
  
  character_message = title_font.render(character_choice.upper(),False,(0,0,255))
  
  if character_show_time >0:
    screen.blit(choice_message,(175,20))
    screen.blit(character_message,(300,400))
    if character_choice == "Big Boss":
      big_class.draw(300,150,health)
    elif character_choice == "Zombie":
      zombie_class.draw(300,150,health)
    elif character_choice == "Cyborg":
      cyborg_class.draw(300,150,health)
    elif character_choice == "Small Fry":
      small_class.draw(300,150,health)
    character_show_time -=1


  
  



#Stage of game where the player deals damage to the chosen character
def fight():
  global Dead
  screen.fill((199,18,24))
  global character
  global health
  
  #Adds character to screen
  if character_choice == "Big Boss":
    character = big_class
   
  
  elif character_choice == "Zombie":
    
    character = zombie_class
    
    
    
  elif character_choice == "Cyborg":
    
    character = cyborg_class
    

  elif character_choice == "Small Fry":
    
    character = small_class
    
  
  
  #tests for weapon choices
  
  if weapon_choice == "Bomb":
    
    
    health = bomb_class.damage(character,health,bomb_damage)
    if health >= 0:
      health = health
    else:
      health = 0
      Dead = True

    character.draw(200,100,health)
    bomb_class.draw(bomb_explode)
    
    
    

    
    
  elif weapon_choice == "Grenade":
    
    health = grenade_class.damage(character,health,grenade_damage)
    if health >= 0:
      health = health
    else:
      health = 0
      Dead = True
    character.draw(200,100,health)
    grenade_class.draw(grenade_explode)
    
  
  elif weapon_choice == "Spikey Mace":
   
    health = spikey_class.damage(character,health,spikey_damage)
    if health >= 0:
      health = health
    else:
      health = 0
      Dead = True
    character.draw(200,100,health)
    spikey_class.draw(spikey_swing)
   
  
  elif weapon_choice == "Pistol":
   
    health = pistol_class.damage(character,health,pistol_damage)
    if health >= 0:
      health = health
    else:
      health = 0
      Dead = True
    character.draw(200,100,health)
    pistol_class.draw(pistol_shot)
    
  
  elif weapon_choice == "Holy Hand Grenade":

    health = holy_class.damage(character,health,holy_damage)
    if health >= 0:
      health = health
    else:
      health = 0
      Dead = True
    character.draw(200,100,health)
    holy_class.draw(holy_sfx)
    
 
timer = 180
num_timer = 120

#After-death endscreen
def end():
  screen.fill((199,18,24))
  global hit_count,crit_count,miss_count
  global end_screen
  global timer,num_timer
  pygame.mouse.set_visible(True)
  if timer > 0:

    for i in range(hit_count+1):
      hit = title_font.render(f"HITS: {i}",False,(0,0,255))
      screen.fill((199,18,24))
      screen.blit(hit,(30,50))
      
       

      

    
    miss = title_font.render(f"MISSES: {miss_count}",False,(0,0,255))
    screen.blit(miss,(30,100)) 

   
    crit = title_font.render(f"CRITICAL HITS: {crit_count}",False,(0,0,255))
    screen.blit(crit,(30,150))

    character.draw(400,100,health)
    timer -=1

  

#game information screen
def information():
  screen.fill((199,18,24))
  global back_button_rect
  info_font = pygame.font.Font("Thinkpad.otf",35)
  summary = info_font.render(("Dummy Demolisher is a game where you choose a weapon and a character to kill"),False,(0,0,255))
  
  gamemode_1_info = info_font.render("GAMEMODE 1: You get to choose your weapon and character",False,(0,0,255))
  gamemode_2_info = info_font.render("GAMEMODE 2: The computer chooses the weapon and character for you",False,(0,0,255))

  back_button = title_font.render("BACK TO MAIN MENU",False,(0,0,255))
  back_button_rect = back_button.get_rect(topleft=(200,300))

  screen.blit(summary,(0,30))
  screen.blit(gamemode_1_info,(0,100))
  screen.blit(gamemode_2_info,(0,170))
  screen.blit(back_button,back_button_rect)


#number list to display to settings screen
music_number_list = [1,2,3,4,5,6,7,8,9,10]
sfx_number_list = [1,2,3,4,5,6,7,8,9,10]

#settings menu
def settings():
  global volume,sfx_volume,back_button_rect
  
  screen.fill((199,18,24))
  music_text = title_font.render("MUSIC VOLUME:",False,(0,0,255))
  sfx_text = title_font.render("SFX VOLUME:",False,(0,0,255))
  
  back_button = title_font.render("BACK TO MAIN MENU",False,(0,0,255))
  back_button_rect = back_button.get_rect(topleft=(200,300))

  screen.blit(music_text,(30,50))
  screen.blit(sfx_text,(30,150))
  screen.blit(back_button,back_button_rect)
  
  for i in range(len(music_number_list)+1):
   
    music_number = title_font.render(str(i),False,(0,0,255))
    music_rect = music_number.get_rect(topleft = (350+(i*50),50))
    
    if volume*10 == i:
      pygame.draw.rect(screen,(150,128,128),music_rect)
   
    if pygame.mouse.get_pressed()[0] == 1:
      if music_rect.collidepoint(pygame.mouse.get_pos()):
        volume = i/10
       
    screen.blit(music_number,(350+(i*50),50))
    
  
    
  
  for i in range(len(sfx_number_list)+1):
    sfx_number = title_font.render(str(i),False,(0,0,255))
    sfx_rect = sfx_number.get_rect(topleft =(300+(i*50),150))
   
    if sfx_volume*10 == i:
      pygame.draw.rect(screen,(150,128,128),sfx_rect)
    
    if pygame.mouse.get_pressed()[0] == 1:
      if sfx_rect.collidepoint(pygame.mouse.get_pos()):
        sfx_volume = i/10
    
    screen.blit(sfx_number,(300+(i*50),150))
   
pygame.mixer.music.play(music_loops)
#MAIN GAME LOOP
while RUN:
  pygame.mixer.music.set_volume(volume)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False

    #Tests for clicks on the main menu screen
    if main == True:
      if pygame.mouse.get_pressed()[0] == 1:
        if gamemode_1_rect.collidepoint(event.pos):
          main = False
          gamemode_1 = True
          
      
        elif gamemode_2_rect.collidepoint(event.pos):
          main = False
          gamemode_2 = True

        elif info_rect.collidepoint(event.pos):
          info_sfx.play()
          info_sfx.set_volume(sfx_volume)
          main = False
          info_screen = True
          
        elif settings_rect.collidepoint(event.pos):
          settings_sfx.play()
          settings_sfx.set_volume(sfx_volume)
          main = False
          settings_screen = True

    elif info_screen == True:
      if pygame.mouse.get_pressed()[0] == 1:
        if back_button_rect.collidepoint(event.pos):
          info_screen = False
          main = True

    elif settings_screen == True:
      if pygame.mouse.get_pressed()[0] == 1:
        if back_button_rect.collidepoint(event.pos):
          settings_screen = False
          main = True
      

      
    #Tests if there was a selection for the weapon menu screen
    elif gamemode_1 == True:
      
      if weapon_choice == None:
        gamemode_1_weapon_menu = True
      
      elif weapon_choice != None:
        gamemode_1_weapon_menu = False
        gamemode_1_character_menu = True
      
      if character_choice != None:
        gamemode_1_character_menu = False
        gamemode_1 = False
        Fight = True
       
        
    elif Fight == True:  
      if Dead == True:
        Fight = False
        end_screen = True
        
    elif end_screen == True:
      if timer <= 0:
        end_screen = False
        character_choice = None
        weapon_choice = None  
        Dead = False
        main = True
      

    elif gamemode_2 == True:
      
      if weapon_choice == None:
        gamemode_2_weapon_menu = True
      
      elif weapon_choice != None:
        gamemode_2_weapon_menu = False
        gamemode_2_show_weapon = True
      
      if gamemode_2_show_weapon == True:
        if weapon_show_time <= 0:
          gamemode_2_show_weapon = False
          gamemode_2_character_menu = True
     
      if character_choice != None:
        gamemode_2_character_menu = False
        gamemode_2_show_character = True
       
      if gamemode_2_show_character == True: 
          
        if character_show_time <=0 :
          gamemode_2_show_character = False
          gamemode_2 = False
          Fight = True
    
    elif Fight == True:      
      if Dead == True:
        Fight = False
        end_screen = True

    elif end_screen == True:
      if timer <= 0:
        end_screen = False
        character_choice = None
        weapon_choice = None  
        Dead = False
        main = True

  if main == True:
    main_menu()
  
  elif info_screen == True:
    information()

  elif settings_screen == True:
    settings()

  elif gamemode_1 == True:
    if gamemode_1_weapon_menu == True:
      gamemode_1_weapons()
    elif gamemode_1_character_menu == True:
      gamemode_1_characters()
  
  elif gamemode_2 == True:
    
    if gamemode_2_weapon_menu == True:
      gamemode_2_weapon_choice()
    
    elif gamemode_2_show_weapon == True:
      show_weapon()

    elif gamemode_2_character_menu == True:
      gamemode_2_character_choice()
    
    elif gamemode_2_show_character == True:
      show_character()
    
      
  elif Fight == True:
    fight()
    
  
  
  elif end_screen == True:
    end()
  
  
  FPS = title_font.render(f"FPS: {int(clock.get_fps())}",False,(0,0,255))
  screen.blit(FPS,(700,500))
  
 
  clock.tick(60)
  
  pygame.display.update()  

pygame.quit()  
  
    
 