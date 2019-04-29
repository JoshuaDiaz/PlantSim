from random import randint
from plant_utilities import *
from math import exp

class Plant:


    def __init__(self, pref, x_init, y_init, mode, sprite):
        self.pref = pref # 'opt_sun' 'opt_h2o' 'h2o_loss_rate'	
        self.sun_health = 60
        self.water_health = 60
        self.health = self.sun_health + self.water_health
        self.sprite = pygame.transform.scale(sprite, (20, 20))
        self.rect = self.sprite.get_rect()
        self.rect.centerx = x_init
        self.rect.centery = y_init
        self.dead = False
        self.mode = mode	# 0=light, 1=water, 2=VOC 
        self.stress = 0 # ranges 0 - 100

    # def move_toward_x(self, vel, pos_x, opt):
    #     """
    #     Update the x_pos of this agent to move toward the resource by vel

    #     Args:
    #         vel: absolute value of amount to increment x_pos
    #         pos_x: x position of the resource
    #         opt: the optimal distance to the resource
    #     """
    #     #don't move when agent is close to light source
    #     if(abs(self.rect.centerx - pos_x) <= opt): return         
    #     # move away if opt_sun distance greater than current position
    #     self.rect.centerx += (vel if ((pos_x - self.rect.centerx) > opt) else -vel)
    
    # def move_toward_y(self, vel, pos_y, opt):
    #     """
    #     Update the y_pos of this agent to move toward the resource by vel

    #     Args:
    #         vel: absolute value of amount to increment x_pos
    #         pos_y: y position of the resource
    #         opt: the optimal distance to the resource
    #     """
    #     #don't move when agent is close to light source
    #     if(abs(self.rect.centery - pos_y) <= opt): return         
    #     # move away if opt_sun distance greater than current position
    #     self.rect.centery += (vel if ((pos_y - self.rect.centery) > opt) else -vel)

    def death_roll(self):
        """
        Roll the die to see if this agent will live or pay the eternal price

        Returns:
            bool: True if dies, false otherwise
        """
        self.health = self.water_health + self.sun_health
        if(self.health <= 100): 
            self.dead = (randint(0,1000) < (100 - self.health)) #too likely to die rn, change!
        return self.dead


    def is_sun_optimal(self, light_pos_x, light_pos_y):
        """
        Returns whether this agent is optimally placed by distance to the sun

        Args:
            light_pos_x: x position of the light
            light_pos_y: y position of the light

        Returns:
            bool: True if optimally placed, false otherwise
        """
        r = abs(self.pref['opt_sun'] - dist(self.rect.centerx, self.rect.centery, light_pos_x, light_pos_y))
        return r <= 10  


    def is_water_optimal(self, water_pos_x, water_pos_y):
        """
        Returns whether this agent is optimally placed by distance to water

        Args:
            water_pos_x: x position of the water
            water_pos_y: y position of the water
            water_max: maximum water distance that can be considered optimal
        Returns:
            bool: True if optimally placed, false otherwise
        """
        return dist(self.rect.centerx, self.rect.centery, water_pos_x, water_pos_y) <= self.pref["opt_h2o"] 
            

    def move_toward(self, vel, pos_x, pos_y, opt):
        """
        Update the coordinates of this agent to move toward the sun by vel

        Args:
            vel: absolute value of amount to increment x_pos
            pos_x: x position of the resource
            pos_y: y position of the resource
            opt: the optimal value for the resource
        """
        dx_vect = pos_x - self.rect.centerx
        dy_vect = pos_y - self.rect.centery
        mag = dist(pos_x, pos_y, self.rect.centerx, self.rect.centery)

        self.rect.centerx += (dx_vect/mag)*vel if (mag>opt) else -(dx_vect/mag)*vel
        self.rect.centery += (dy_vect/mag)*vel if (mag>opt) else -(dy_vect/mag)*vel
    

    def check_collision(self, plant):
        return self.rect.colliderect(plant.rect)
        # col_dist = 25 #collision distance
        #return (dist(self.rect.centerx, self.rect.centery, plant.rect.centerx, plant.rect.centery) < col_dist)


    def update_health(self, light_pos_x, light_pos_y, water_pos_x, water_pos_y):
        """
        Update water health of agent, water health increases if near water source,
	    water health decreases by h2o_loss_rate if away

        Args:
            light_pos_x: x position of the light
            light_pos_y: y position of the light
            water_pos_x: x position of water
            water_pos_y: y position of water
        """
        #SUN
        # distance to the circle of optimal sun 
        dist_to_opt = abs(dist(self.rect.centerx, self.rect.centery, light_pos_x, light_pos_y) - self.pref['opt_sun'])
        p = 2 # amount gained if plant is right at the optimal sun amount
        b = 0.01 # time constant of exponential decay
        q = 1 # max loss an agent will face when away from optimal sun distance
        self.sun_health += (p+q)*exp(-(b*dist_to_opt**2)) - q 

        # WATER
        # if agent is within distance 1 of water source, add water
        if( self.is_water_optimal(water_pos_x, water_pos_y) and self.water_health < 60):	
            self.water_health += 2
	    # decrease water if not near water source
        else:
            self.water_health -= .25 #self.pref['h2o_loss_rate']


    def resolve_color(self, sun_pos, water_pos):
        # dead agent
        if(self.dead):
            return GRAY 
        # optimal agent
        elif(self.is_sun_optimal(sun_pos[0], sun_pos[1])): 
            if(self.is_water_optimal(water_pos[0], water_pos[1])):
                return PURPLE
            return RED
        elif(self.is_water_optimal(water_pos[0], water_pos[1])):
            return CYAN
        # default
        return BLACK

