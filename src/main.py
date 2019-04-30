# Joshua Diaz, Elena Sabinson, Jeremy Storey, Erika Yu
# jd794, es963, jks294, ejy25  @cornell.edu
# Cornell University, ECE 6970, Spring 2019

#import os
import pygame
#import RPi.GPIO as GPIO
import time
from random import randint
from plant import Plant
from plant_utilities import *

# Simulation parameters
SCREEN_SIZE = 600,300
SUN_POS = 125,125
WATER_POS = 300,100
STEP_TIME = 0.05 # time between updates 
NUM_PLANT_TYPES = 2 # number of different plant types
NUM_AGENTS = 50  # number of plants operating
VEL = 5        # movement speed of agents
agents = []      # list of all agents
death_count = 0  # amount of dead agents

# setup pygame and touchscreen
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb0')
#os.putenv('SDL_MOUSEDRV', 'TSLIB')
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((SCREEN_SIZE))

# define plant preferences
plant_1_pref = {'opt_sun':50, 'opt_h2o':20, 'h2o_loss_rate':5}
plant_2_pref = {'opt_sun':100, 'opt_h2o':20, 'h2o_loss_rate':1}
plant_prefs = [plant_1_pref, plant_2_pref]

plant_1_voc = {'strength': 3, 'emittance':50}
plant_2_voc = {'strength': 5, 'emittance':100}
plant_voc = [plant_1_voc, plant_2_voc]
# construct plants
rect_list = []
for i in range(NUM_PLANT_TYPES):
    for j in range(int(NUM_AGENTS/NUM_PLANT_TYPES)): 
        sprite = pygame.image.load("../assets/plant_" + str(i) + ".bmp")
        p = Plant(plant_prefs[i], randint(0,SCREEN_SIZE[0]), randint(0,SCREEN_SIZE[1]), mode.LIGHT, sprite, plant_voc[i])
        while(len(agents) != 0 and p.rect.collidelist(rect_list) != -1):
            p.rect.centerx = randint(0,SCREEN_SIZE[0])
            p.rect.centery = randint(0,SCREEN_SIZE[1])
        rect_list.append(p.rect)
        agents.append(p)

# Update loop
running = True
while(running):
    time.sleep(STEP_TIME)
    # clear screen
    screen.fill(WHITE)
    #update all agents
    for i in range(len(agents)):
        # update if not dead
        if(not(agents[i].dead)):

            #update sun health / water health
            agents[i].update_health(SUN_POS[0], SUN_POS[1], WATER_POS[0], WATER_POS[1])
            
            # agent plays the game of survival, did this position kill them?
            if(agents[i].death_roll()):
                death_count += 1
                #print("Plant " + str(i) + " died at health " + str(agents[i].health))
            else:
                # it didn't kill them! get a new position
                #choose mode
                if(agents[i].sun_health > agents[i].water_health):
                    agents[i].mode = mode.WATER
                else:
                    agents[i].mode = mode.LIGHT

                temp_x = agents[i].rect.centerx
                temp_y = agents[i].rect.centery
                # check plant's mode
                # LIGHT
                if(agents[i].mode == mode.LIGHT):
                    agents[i].move_toward(VEL, SUN_POS[0], SUN_POS[1], agents[i].pref['opt_sun'])
                    agents[i].resolve_vocs(VEL, agents)
                    # check collisions
                    for j in range(len(agents)):
                        if(i != j and agents[i].is_colliding(agents[j])):
                            agents[i].rect.centerx = temp_x
                            agents[i].rect.centery = temp_y

                # WATER
                elif(agents[i].mode == mode.WATER):
                    agents[i].move_toward(VEL, WATER_POS[0], WATER_POS[1], agents[i].pref['opt_h2o'])
                    agents[i].resolve_vocs(VEL, agents)
                    # check collisions
                    for j in range(len(agents)):
                        if(i != j and agents[i].is_colliding(agents[j])):
                            agents[i].rect.centerx = temp_x
                            agents[i].rect.centery = temp_y 
                # VOC 
                

                # limit to bounds
                if(agents[i].rect.centerx < 0): agents[i].rect.centerx = 0
                if(agents[i].rect.centerx > SCREEN_SIZE[0]): agents[i].rect.centerx = SCREEN_SIZE[0]
                if(agents[i].rect.centery < 0): agents[i].rect.centery = 0
                if(agents[i].rect.centery > SCREEN_SIZE[1]): agents[i].rect.centery = SCREEN_SIZE[1]

        # update screen state, in real robots this is the point where robot state is
        # finalized / set
        color = agents[i].resolve_color(SUN_POS, WATER_POS)
        screen.blit(tint(agents[i].sprite, color), agents[i].rect)

    # flip to the screen
    pygame.draw.circle(screen, ORANGE, SUN_POS, 10)  
    pygame.draw.circle(screen, BLUE, WATER_POS, 10)  
    pygame.display.flip()

    # exit sim if player tries
    for event in pygame.event.get():
        if(event.type == pygame.QUIT): running = False
        
# PyGame cleanup
pygame.quit()  