def fourLegSimulator(beta_list, gamma_list, beta_list2, gamma_list2, beta_list3, gamma_list3, beta_list4, gamma_list4, bodyHeight, femur, tibia):
    """" This function takes eight lists containing beta(shoulder) and gamma(knee) angles and body height four Leg Simulator code animated in 2D by Hritik Gupta date = 25/07/2020 """
    
    #import necessary packages
    import numpy as np 
    import itertools # This package is specifically used for having multiple variable "for" loop using zip function
    from numpy import pi, sin, cos, sqrt
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    get_ipython().run_line_magic('matplotlib', 'qt')



    # input parameters
    Femur_one_leg = femur # Length of femur (upper bone)
    Tibia_one_leg = tibia # Length of Tibia (lower bone)


    # Making arrays for containing value of respective coordinates
    X1 = np.zeros(len(beta_list)) # array for x_coordinates of moving point of femur
    Y1 = np.zeros(len(beta_list)) # array for y_coordinates of moving point of femur
    X2 = np.zeros(len(gamma_list)) # array for x_coordinates of moving point of tibia i.e end effector in our case
    Y2 = np.zeros(len(gamma_list))  # array for y_coordinates of moving point of tibia i.e end effector in our case
 
    X1_2 = np.zeros(len(beta_list2)) # array for x_coordinates of moving point of femur
    Y1_2 = np.zeros(len(beta_list2)) # array for y_coordinates of moving point of femur
    X2_2 = np.zeros(len(gamma_list2)) # array for x_coordinates of moving point of tibia i.e end effector in our case
    Y2_2 = np.zeros(len(gamma_list2))  # array for y_coordinates of moving point of tibia i.e end effector in our case

    X1_3 = np.zeros(len(beta_list3)) # array for x_coordinates of moving point of femur
    Y1_3 = np.zeros(len(beta_list3)) # array for y_coordinates of moving point of femur
    X2_3 = np.zeros(len(gamma_list3)) # array for x_coordinates of moving point of tibia i.e end effector in our case
    Y2_3 = np.zeros(len(gamma_list3))  # array for y_coordinates of moving point of tibia i.e end effector in our case  
    
    
    X1_4 = np.zeros(len(beta_list4)) # array for x_coordinates of moving point of femur
    Y1_4 = np.zeros(len(beta_list4)) # array for y_coordinates of moving point of femur
    X2_4 = np.zeros(len(gamma_list4)) # array for x_coordinates of moving point of tibia i.e end effector in our case
    Y2_4 = np.zeros(len(gamma_list4))  # array for y_coordinates of moving point of tibia i.e end effector in our case
    
    
    #Populating the above defined arrays currently filled with zeros to respective coordinates
    #Here in the for loop zip function is used to iterate two variales simultaneously and enumerate function to return index numbers

    for index,(beta,gamma) in enumerate(zip(beta_list,gamma_list)):
        x1 = Femur_one_leg*cos(-beta - (pi/2)) # x-cooridnate of femur
        y1 = Femur_one_leg*sin(-beta - (pi/2)) # y-cooridnate of femur
        x2 = x1 + Tibia_one_leg*cos(-pi/2 - (beta + gamma)) # x-coordinate of tibia
        y2 = y1 + Tibia_one_leg*sin(-pi/2 - (beta + gamma)) # y-coordinate of tibia
      

        # using above used flag variables to replace zeros with respective corrdinates
        X1[index] = x1 
        Y1[index] = y1 
        X2[index] = x2 
        Y2[index] = y2 
  
    for index2,(beta2,gamma2) in enumerate(zip(beta_list2,gamma_list2)):
        x1_2 = Femur_one_leg*cos(-beta2 - (pi/2)) # x-cooridnate of femur
        y1_2 = Femur_one_leg*sin(-beta2 - (pi/2)) # y-cooridnate of femur
        x2_2 = x1_2 + Tibia_one_leg*cos(-pi/2 - (beta2 + gamma2)) # x-coordinate of tibia
        y2_2 = y1_2 + Tibia_one_leg*sin(-pi/2 - (beta2 + gamma2)) # y-coordinate of tibia
       

        # using above used flag variables to replace zeros with respective corrdinates
        X1_2[index2] = x1_2 
        Y1_2[index2] = y1_2 
        X2_2[index2] = x2_2 
        Y2_2[index2] = y2_2 

    for index3,(beta3,gamma3) in enumerate(zip(beta_list3,gamma_list3)):
        x1_3 = 40 + Femur_one_leg*cos(-beta3 - (pi/2)) # x-cooridnate of femur
        y1_3 = Femur_one_leg*sin(-beta3 - (pi/2)) # y-cooridnate of femur
        x2_3 = x1_3 + Tibia_one_leg*cos(-pi/2 - (beta3 + gamma3)) # x-coordinate of tibia
        y2_3 = y1_3 + Tibia_one_leg*sin(-pi/2 - (beta3 + gamma3)) # y-coordinate of tibia
       

        # using above used flag variables to replace zeros with respective corrdinates
        X1_3[index3] = x1_3 
        Y1_3[index3] = y1_3 
        X2_3[index3] = x2_3 
        Y2_3[index3] = y2_3
        
    for index4,(beta4,gamma4) in enumerate(zip(beta_list4,gamma_list4)):
        x1_4 = 40 + Femur_one_leg*cos(-beta4 - (pi/2)) # x-cooridnate of femur
        y1_4 = Femur_one_leg*sin(-beta4 - (pi/2)) # y-cooridnate of femur
        x2_4 = x1_4 + Tibia_one_leg*cos(-pi/2 - (beta4 + gamma4)) # x-coordinate of tibia
        y2_4 = y1_4 + Tibia_one_leg*sin(-pi/2 - (beta4 + gamma4)) # y-coordinate of tibia
       

        # using above used flag variables to replace zeros with respective corrdinates
        X1_4[index4] = x1_4 
        Y1_4[index4] = y1_4 
        X2_4[index4] = x2_4 
        Y2_4[index4] = y2_4 

    # Setting up figure and subplot

    fig = plt.figure()
    fig.canvas.set_window_title('One Leg trajectory Planning')
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-30,70), ylim=(-50,50))
    ax.grid()
    ax.set_title('Leg Trajectory')
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    
    line, = ax.plot([], [], 'o-', lw=5, color='#05143b')
    line2, = ax.plot([], [], 'o-', lw=5, color='#37acf0')
    line3, = ax.plot([], [], 'o-', lw=5, color='#05143b')
    line4, = ax.plot([], [], 'o-', lw=5, color='#37acf0')
    


    # initialization function
    def init():
        line.set_data([], [])
        line2.set_data([], [])
        line3.set_data([], [])
        line4.set_data([], [])
        return line,line2,line3,line4,

    # animation function
    def animate(i):
        x_points = [0, X1[i], X2[i]]
        y_points = [0, Y1[i], Y2[i]]
        
        x2_points = [0, X1_2[i], X2_2[i]]
        y2_points = [0, Y1_2[i], Y2_2[i]]
        
        x3_points = [40, X1_3[i], X2_3[i]]
        y3_points = [0, Y1_3[i], Y2_3[i]]
        
        x4_points = [40, X1_4[i], X2_4[i]]
        y4_points = [0, Y1_4[i], Y2_4[i]]
      

        line.set_data(x_points, y_points)
        line2.set_data(x2_points, y2_points)
        line3.set_data(x3_points, y3_points)
        line4.set_data(x4_points, y4_points)
        
        return line, line2, line3, line4

    # call the animation
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(X1), interval=100, blit=True, repeat=True)
 

 # plotting respective movement trajectories in the same plot
    plt.plot(X2,Y2, '#05143b')
#     plt.plot(X1,Y1)
    
    plt.plot(X2_2,Y2_2,'#37acf0')
#     plt.plot(X1_2,Y1_2)
    
    plt.plot(X2_3,Y2_3,'#05143b')
#     plt.plot(X1_3,Y1_3)
    
    plt.plot(X2_4,Y2_4,'#37acf0')
#     plt.plot(X1_4,Y1_4)
   
    
  
    plt.plot([-20,60],[-bodyHeight,-bodyHeight],'brown')
    plt.plot([-4,44],[0,0],'#010b24')
    plt.plot([-4,-4],[0,5],'#010b24')
    plt.plot([44,44],[0,5],'#010b24')
    plt.plot([-4,44],[5,5],'#010b24')
    
    for ind in range(100):
        plt.plot([-4,44],[ind*5/100,ind*5/100],'black')
    
    return None
