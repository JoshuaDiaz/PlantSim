from random import randint
from pygame.transform import scale
from plant_utilities import *

class Plant:
    def __init__(self, pref, x_init, y_init, mode, sprite):
        self.pref = pref # 'opt_sun' 'opt_h2o' 'h2o_loss_rate'
        self.health = 100	
        self.sun_health = 60
        self.water_health = 60
        self.sprite = scale(sprite, (20, 20))
        self.rect = sprite.get_rect()
        self.rect.centerx = x_init
        self.rect.centery = y_init
        self.dead = False
        self.mode = mode	# 0=light, 1=water, 2=VOC 

    def move_toward_x(self, vel, pos_x, opt):
        """
        Update the x_pos of this agent to move toward the sun by vel

        Args:
            vel: absolute value of amount to increment x_pos
            pos_x: x position of the resource in world coordinates
            opt: the optimal value for the resource
        """
        #don't move when agent is close to light source
        if(abs(self.rect.centerx - pos_x) <= opt): return         
        # move away if opt_sun distance greater than current position
        self.rect.centerx += (vel if ((pos_x - self.rect.centerx) > opt) else -vel)
    
    def move_toward_y(self, vel, pos_y, opt):
        """
        Update the y_pos of this agent to move toward the sun by vel

        Args:
            vel (float): absolute value of amount to increment y_pos
            pos_y: y position of the resource in world coordinates
            opt: the optimal value for the resource
        """
        #don't move when agent is close to light source
        if(abs(self.rect.centery - pos_y) <= opt): return         
        # move away if opt_sun distance greater than current position
        self.rect.centery += (vel if ((pos_y - self.rect.centery) > opt) else -vel)


    def death_roll(self, thresh):
        """
        Roll the die to see if this agent will live or pay the eternal price

        Args:
            thresh (float): value compared to death prob for deciding mortality

        Returns:
            bool: True if dies, false otherwise
        """
	    #see if it died	
        if(self.dead): return False

        # update health
        self.health = self.water_health + self.sun_health

	    #calculate chance of death
        if(self.health >= 100):
            return False
        else: 
            chance = 100 - self.health
            if( randint(0,100) > chance ): 
                return False
            else:
                self.dead = True
                return True



    def is_sun_optimal(self, light_pos_x, light_pos_y):
        """
        Returns whether this agent is optimally placed by distance to the sun

        Args:
            light_pos_x: x position of the light in world coordinates
            light_pos_y: y position of the light in world coordinates

        Returns:
            bool: True if optimally placed, false otherwise
        """
        r = abs(self.pref['opt_sun'] - dist(self.rect.centerx, self.rect.centery, light_pos_x, light_pos_y))
        return r <= 0.1  

    def is_water_optimal(self, water_pos_x, water_pos_y, water_max):
        """
        Returns whether this agent is optimally placed by distance to water

        Args:
            water_pos_x: x position of the water in world coordinates
            water_pos_y: y position of the water in world coordinates
            water_max: maximum water distance that can be considered optimal
        Returns:
            bool: True if optimally placed, false otherwise
        """
        return dist(self.rect.centerx, self.rect.centery, water_pos_x, water_pos_y) <= water_max 

    def move_toward(self, vel, pos_x, pos_y, opt):
        """
        Update the x_pos and y_pos of this agent to move toward the sun by vel

        Args:
            vel (float): absolute value of amount to increment x_pos
            pos_x: x position of the resource in world coordinates
            pos_y: y position of the resource in world coordinates
            opt: the optimal value for the resource
        """
        # if along the right vertical
        if((self.rect.centerx  - pos_x) == 0):
            x = 0
            y = 1
        else:
            slope = (self.rect.centery - pos_y)/(self.rect.centerx  - pos_x)
	        # slope greater than 1
            if(abs(slope) > 1):
                x = 1/abs(slope)
                y = 1
            else:
                x = 1
                y = ( 1/abs(slope) if (slope != 0) else 0)
	
	    # check positive x-position
        if((self.rect.centerx  - pos_x) >0):
            x = -x
	    # check posiive y-position
        if((self.rect.centery - pos_y) >0):
            y = -y

        # if distance is smaller than opt_sun
        if( dist(self.rect.centerx, self.rect.centery, pos_x, pos_y) < opt) :
            x = -x
            y = -y            

        self.rect.centerx  += x * vel
        self.rect.centery += y * vel

    def lose_water(self,light_pos_x, light_pos_y, water_pos_x, water_pos_y):
        """
        Update water health of agent, water health increases if near water source,
	    water health decreases by h2o_loss_rate if away

        Args:
            light_pos_x: x position of the light in world coordinates
            light_pos_y: y position of the light in world coordinates
            water_pos_x: x position of water in world coordinates
            water_pos_y: y position of water in world coordinates
        """
        # if agent is within distance 1 of water source, add water
        if( dist(self.rect.centerx, self.rect.centery, water_pos_x, water_pos_y) < 1 ):	
            self.water_health += 5
	# decrease water if not near water source
        else:
            self.water_health -= self.pref['h2o_loss_rate']

	# lose water faster if near light
        r = dist(self.rect.centerx, self.rect.centery, light_pos_x, light_pos_y)
        if(r < 100):	
            if(r > 1):
                self.water_health -= 10/r
            else:
                self.water_health -= 10	

    def resolve_color(self, sun_pos, water_pos):
        #default color (none)
        color = BLACK
        # dead agent
        if(self.dead):
                color = GRAY 
        # optimal agent
        elif(self.is_sun_optimal(sun_pos[0], sun_pos[1])): 
            color = RED
        return color	