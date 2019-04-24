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
SCREEN_SIZE = 500,500
SUN_POS = 125,125
WATER_POS = 300,100
STEP_TIME = 0.25 # time between updates 
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

# load images from pygame files
#plant1 = pygame.image.load("../plant_pygame.bmp")
#plant2 = pygame.image.load("../plant_pygame2.bmp")

# define plant preferences
plant_1_pref = {'opt_sun':100, 'opt_h2o':50, 'h2o_loss_rate':5}
plant_2_pref = {'opt_sun':300, 'opt_h2o':25, 'h2o_loss_rate':1}

# construct plants
for i in range(NUM_AGENTS): 
    if(i%2 == 0): # PLANT A
        sprite_1 = pygame.image.load("../assets/plant_1.bmp")
        agents.append(Plant(plant_1_pref, randint(0,SCREEN_SIZE[0]), randint(0,SCREEN_SIZE[1]), mode.LIGHT, sprite_1))
    else: # PLANT B
        sprite_2 = pygame.image.load("../assets/plant_2.bmp")
        agents.append(Plant(plant_2_pref, randint(0,SCREEN_SIZE[0]), randint(0,SCREEN_SIZE[1]), mode.LIGHT, sprite_2))

# Update loop
running = True
while(running):
    time.sleep(STEP_TIME)
    # clear screen
    screen.fill(WHITE)
    #update all agents
    for i in range(NUM_AGENTS):

        #update water health
        agents[i].lose_water(SUN_POS[0], SUN_POS[1], WATER_POS[0], WATER_POS[1])

        # move if not dead
        if(not(agents[i].dead)):

            # check plant's mode
            # LIGHT
            if(agents[i].mode == mode.LIGHT and not(agents[i].is_sun_optimal(SUN_POS[0], SUN_POS[1]))):
			    # check collisions
                for j in range(NUM_AGENTS):
                    if(j != i and (dist(agents[i].rect.centerx, agents[i].rect.centery, agents[j].rect.centerx, agents[j].rect.centery) < 30)):
                        print("colliding " + str(i) + " and " + str(j))
                        if(agents[i].is_sun_optimal(SUN_POS[0], SUN_POS[1])):
                            agents[i].move_toward_x(VEL, SUN_POS[0], agents[i].pref['opt_sun'])
                        if(agents[j].is_sun_optimal(SUN_POS[0], SUN_POS[1])):
                            agents[j].move_toward_y(VEL, SUN_POS[1], agents[j].pref['opt_sun'])			

                agents[i].move_toward(VEL, SUN_POS[0], SUN_POS[1], agents[i].pref['opt_sun'])

            # WATER
            elif(agents[i].mode == mode.WATER and not(agents[i].is_water_optimal(WATER_POS[0], WATER_POS[1], 1))):
                # check collisions
                for j in range(NUM_AGENTS):
                    if(j != i and (dist(agents[i].rect.centerx, agents[i].rect.centery, agents[j].rect.centerx, agents[j].rect.centery) < 30)):
                        if(agents[i].is_water_optimal()):
                            agents[i].move_toward_x(VEL, WATER_POS[0], agents[i].pref['opt_h2o'])
                        if(agents[j].is_water_optimal()):
                            agents[j].move_toward_y(VEL, WATER_POS[1], agents[j].pref['opt_h2o'])			

                agents[i].move_toward(VEL, WATER_POS[0], WATER_POS[1], agents[i].pref['opt_h2o'])

            # VOC 
            #else:

            #update sun health
            if(agents[i].is_sun_optimal(SUN_POS[0], SUN_POS[1])):
                if(agents[i].sun_health < 60):
                    agents[i].sun_health += 1
                else:
                    agents[i].sun_health -= 1

            #update water health
            if(agents[i].is_water_optimal(WATER_POS[0], WATER_POS[1], 1)):
                if(agents[i].water_health < 60):
                    agents[i].water_health += 1

            # agent plays the game of survival
            if(agents[i].death_roll(randint(1,100))):
                death_count += 1
                print("Plant " + str(i) + " died")

        color = agents[i].resolve_color(SUN_POS, WATER_POS)
        screen.blit(tint(agents[i].sprite, color), agents[i].rect)

    # flip to the screen   
    pygame.display.flip()

    # exit game if player tries
    for event in pygame.event.get():
        if(event.type == pygame.QUIT): running = False
        
# PyGame cleanup
pygame.quit()  
