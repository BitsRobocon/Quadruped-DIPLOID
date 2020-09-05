# -*- coding: utf-8 -*-
"""
@author: Deep
leg no.s 1,2,3,4 form a Z from ForwardLeft leg
"""
import time
import math
import numpy as np
import plotView3d as view3d
import fourLegSimulator as fls
# from dxl_control.Ax12 import Ax12
#----------variables---------------------------------------------

# # create motor object
# femur = Ax12(2)
# tibia = Ax12(1)

# # connecting
# Ax12.open_port()
# Ax12.set_baudrate()


t_elapse_ref = 0 #variable initialised

TD = False

clr_height=4 # clearance height in cm
L_span = 8 #centimetres
v_d = 0.7 #10/11 #m/s

T_st = 2*L_span/(100*v_d) #0.18
T_sw = 0.15 #sec

T_stride = T_st + T_sw #0.33
precision=0.01
legNum=1
S_st_i=0
S_sw_i=0

phase=[0,0,0,0]
phase=np.array(phase)
loopStart=0
loopEnd=0
loopTime=0

dS_gallop=[0,0.2,0.55,0.75]#gallop
dS_trot=[0,0.5,0.5,0]#trot
dS_walk=[0,0.5,0.75,0.25]#walk- 0.5 and 0.75 flipped, looks correct
dS_bound=[0,0,0.5,0.5]# bound
dS_pace=[0,0.5,0,0.5] # pace
dS = []
dS = dS_trot
# print(dS_trot)

t1=0
t2=0
t3=0
t4=0
t_elapse_ref=0.0 #change this value between 0 and 0.33(stride time)

t_i=[t1,t2,t3,t4]
t_i=np.array(t_i)

x=0 #coordinates initialized
y=0
z=0

lateral_fraction=0
bodyHeight=18
delta=-0.85

t_gt = 0.02 #transition starting time
dT_gt = 0.10 #duration of gait transition

bezierControlPoints=[[-L_span,0.0-bodyHeight],
                     [-L_span*1.4,0.0-bodyHeight],
                     [-L_span*1.5,clr_height*0.9-bodyHeight],
                     [-L_span*1.5,clr_height*0.9-bodyHeight],
                     [-L_span*1.5,clr_height*0.9-bodyHeight],
                     [0.0,clr_height*0.9-bodyHeight],
                     [0.0,clr_height*0.9-bodyHeight],
                     [0.0,clr_height*1.157-bodyHeight],
                     [L_span*1.5,clr_height*1.157-bodyHeight],
                     [L_span*1.5,clr_height*1.157-bodyHeight],
                     [L_span*1.4,0.0-bodyHeight],
                     [L_span,0.0-bodyHeight]]
bezierControlPoints=np.array(bezierControlPoints)
# k belongs to 0,1,2...11 for 12 bezier contol points

femur=12
tibia=11.5
hip=0
angles=[]
alpha_list=[]
beta_list=[]
gamma_list=[]
alpha_list2=[]
beta_list2=[]
gamma_list2=[]
alpha_list3=[]
beta_list3=[]
gamma_list3=[]
alpha_list4=[]
beta_list4=[]
gamma_list4=[]
x_list1 = []
z_list1 = []
x_list2 = []
z_list2 = []
x_list3 = []
z_list3 = []
x_list4 = []
z_list4 = []
# helix=0.1

def nCr(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

def bernstein(S,N,K,v):
    return nCr(N,K) * (1-S)**(N-K) * S**K * v

def legIK(x,y,z):
    R = math.sqrt(x**2+y**2+z**2)
    R1 = math.sqrt(z**2 + y**2)
    theta1=math.atan2(-z,y)
    theta2=math.acos(hip/R1)
    alpha = (theta2-theta1)*180/math.pi
    
    R2=math.sqrt(R**2-hip**2)
    phi1=math.asin(x/R2)
    # print(phi1*180/math.pi)
    temp=(femur**2+R2**2-tibia**2)/(2*femur*R2)
    # print(temp)
    if temp>1:
        temp=1
        print('_______breach on positive side')
    if temp<-1:
        temp=-1
        print('_______breach on negative side')
    phi2=math.acos(temp)
    # print(phi2*180/math.pi)
    beta = (phi1-phi2)*180/math.pi
    
    temp2=(femur**2+tibia**2-R2**2)/(2*femur*tibia)
    if temp2>1:
        temp2=1
        print('_______breach on positive side')
    if temp2<-1:
        temp2=-1
        print('_______breach on negative side')
    psi=math.acos(temp2)
    # print(psi*180/math.pi)
    gamma = (math.pi-psi)*180/math.pi
    return np.array([alpha,beta,gamma])

def lateralMotion(lateral_fraction, x):
    X_POLAR = np.cos(lateral_fraction*(math.pi/2))
    Y_POLAR = np.sin(lateral_fraction*(math.pi/2))
    
    stepX = x * X_POLAR
    stepY = x * Y_POLAR
    
    return stepX, stepY

def gaitTransition(t, t_gt, dT_gt, current_gait, target_gait):
    current_gait = np.array(current_gait)
    target_gait = np.array(target_gait)
    branch1 = (t - t_gt)/dT_gt
    branch2 = 1
    # pro tip- make a lambda func for SAT(x,y)
    if branch1 <= branch2 and t >= t_gt:
        dS = current_gait + (target_gait - current_gait)*(branch1)
    elif branch1 <= branch2 and t < t_gt:
        dS = current_gait
    else:
        dS = current_gait + (target_gait - current_gait)*(branch2)
    print('PHASE MATRIX RIGHT NOW : ',end='')
    print(dS)
    return dS

#------------------------------------------------------------------

view3d.drawPoints3d([0,0,0])
view3d.drawCurve3d([[22,15,0],[-22,15,0],[-22,-15,0],[22,-15,0],[22,15,0]])
t = 0.0 #clock started
t_TD_ref = t #initialized from TouchDown
start=time.perf_counter()

for i in range(0,1): #no. of cycles
    S_st_i=0
    S_sw_i=0
    print('Cycle no: ' + str(i+1))
    TD=False
    while(not TD):
        # if precision<loopTime:
        #     precision=loopTime
        # time.sleep(precision-(0.75*loopTime))
        loopStart=time.perf_counter()
        t_elapse_ref = t - t_TD_ref
        print(t_elapse_ref)
        TD=False
        # -------------------------------------------------
        # dS = gaitTransition(t, t_gt, dT_gt, dS_trot, dS_pace)
        
        # ---------------------------------------------------
        if t_elapse_ref >= T_stride:
            t_elapse_ref = 0
            TD = True
        
        if TD:
            t_TD_ref = t
            print('\nTouchDown\n')
        
        # print(t_elapse_ref)
        t_i = t_elapse_ref - T_stride * np.array(dS)
        # print(t_i)
        
        for legTime in t_i:
            print('Leg no: ' + str(legNum))
            
            """NOTE: PAPER WAS MISSING THIS LOGIC!!
            This is to avoid a phase discontinuity if the user selects a Step Length and Velocity combination that causes Tstance > Tswing.
            """
            if legTime < -T_sw: #old stance phase active
                legTime += T_stride
                print('slow stance case')
                #time updated to current stance phase, triggers next 'if'
            
            if legTime>0 and legTime<T_st: #current stance phase active
                x=0
                y=0
                z=0
                S_st_i = legTime/T_st
                phase[legNum-1]=S_st_i
                x=L_span*(1-2*S_st_i)+0
                z=delta*(math.cos(math.pi*x/(2*L_span))+0 )- bodyHeight #this 0 is Pox and 18 Poy
                x,y=lateralMotion(lateral_fraction,x)
                # y+=helix
                print('in current stance: '+ str(S_st_i))
                print('Coords :'+'('+str(x)+', '+str(y)+', '+str(z)+')')
                print('Angles :', end="")
                angles=legIK(x, y, z)
                print(angles)
                
                
            if legTime>= -T_sw and legTime<=0: #old swing phase active
                x=0
                y=0
                z=0
                S_sw_i = (legTime+T_sw)/T_sw
                phase[legNum-1]=S_sw_i
                for index in range(0,12):
                    x+=bernstein(S_sw_i, 11, index, bezierControlPoints[index][0])
                    z+=bernstein(S_sw_i, 11, index, bezierControlPoints[index][1])
                x,y=lateralMotion(lateral_fraction,x)
                # y+=helix
                print('in old swing: '+ str(S_sw_i))
                print('Coords :'+'('+str(x)+', '+str(y)+', '+str(z)+')')
                print('Angles :', end="")
                angles=legIK(x, y, z)
                print(angles)
                
            elif legTime>= T_st and legTime<=T_stride: #current swing phase active
                x=0
                y=0
                z=0
                S_sw_i = (legTime-T_st)/T_sw
                phase[legNum-1]=S_sw_i
                for index in range(0,12):
                    x+=bernstein(S_sw_i, 11, index, bezierControlPoints[index][0])
                    z+=bernstein(S_sw_i, 11, index, bezierControlPoints[index][1])
                x,y=lateralMotion(lateral_fraction,x)
                # y+=helix
                print('in current swing: '+ str(S_sw_i))
                print('Coords :'+'('+str(x)+', '+str(y)+', '+str(z)+')')
                print('Angles :', end="")
                angles=legIK(x, y, z)
                print(angles)
            
            if legNum==1: #change this no. to change leg
                view3d.drawPoints3d([x+20,y+15,z])
                val0=angles[0]*math.pi/180
                val1=angles[1]*math.pi/180
                val2=angles[2]*math.pi/180
                alpha_list.append(val0)
                beta_list.append(val1)
                gamma_list.append(val2)
                x_list1.append(x)
                z_list1.append(z)
                # M1.set_position(val1)
                # M2.set_position(val2)
                        
            if legNum==2: #change this no. to change leg
                view3d.drawPoints3d([x+20,y-15,z])
                val0=angles[0]*math.pi/180
                val1=angles[1]*math.pi/180
                val2=angles[2]*math.pi/180
                alpha_list2.append(val0)
                beta_list2.append(val1)
                gamma_list2.append(val2)
                x_list2.append(x)
                z_list2.append(z)
                
                
            if legNum==3: #change this no. to change leg
                view3d.drawPoints3d([x-20,y+15,z])
                val0=angles[0]*math.pi/180
                val1=angles[1]*math.pi/180
                val2=angles[2]*math.pi/180
                alpha_list3.append(val0)
                beta_list3.append(val1)
                gamma_list3.append(val2)
                x_list3.append((float(x) + 40))
                z_list3.append(z)
            
            
            if legNum==4: #change this no. to change leg
                view3d.drawPoints3d([x-20,y-15,z])
                val0=angles[0]*math.pi/180
                val1=angles[1]*math.pi/180
                val2=angles[2]*math.pi/180
                alpha_list4.append(val0)
                beta_list4.append(val1)
                gamma_list4.append(val2)
                x_list4.append((float(x)+40))
                z_list4.append(z)
                
            legNum+=1
            print('----this leg done----\n')
        legNum=1
        print('********this time instant done for all legs**********')
        t_elapse_ref +=precision
        t +=precision
        loopEnd=time.perf_counter()
        loopTime=loopEnd-loopStart
        # helix+=0.1
    print('\n========================this cycle done============================\n')


print('\n\nTotal time taken: '+str(time.perf_counter()-start)+' sec')

fls.fourLegSimulator(beta_list, gamma_list, beta_list2, gamma_list2, beta_list3, gamma_list3, beta_list4, gamma_list4, bodyHeight, femur, tibia)
# sf.One_Leg_Simulation(beta_list, gamma_list)
# sf.One_Leg_Simulation(beta_list2, gamma_list2)

# # disconnect
# femur.disable_torque()
# tibia.disable_torque()
# Ax12.close_port()