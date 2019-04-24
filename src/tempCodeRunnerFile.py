        # decode agent's draw color 
        color = BLACK
        # dead agent
        if(agents[i].dead):
            color = GRAY 
        # optimal agent
        elif(agents[i].is_sun_optimal(SUN_POS[0], SUN_POS[1])):  
            color = CYAN # PLANT B