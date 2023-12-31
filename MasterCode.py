import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
from scipy import integrate
from scipy import interpolate
import math
import pandas as pd
import os
font={'fontname':'Times New Roman'}
sg.theme('SandyBeach')

#Grafical interface
layout1 = [
 [sg.Text('Please enter the required parameters')],
 [sg.Text('Project name', size=(20,1)), sg.Input(key='-
IN-')],
 [sg.Text('Please enter the drag polar (Mach number vs Drag coeff as  .csv
file)', size =(50, 1)), sg.Input(key='-IN1-'),
sg.FileBrowse(file_types=(('Excel Files','*csv'),))],
 [sg.Text('Motor parameters',size=(100,1), justification='c')],
 [sg.Text('Motor impuls [Ns]', size=(20,1)), sg.Input(key='-
IN2-', size=(10,1)),sg.Text('Gross mass of motor [kg]'),
sg.Input(key='-IN3-',size=(10,1)), sg.Text('Mass of propopelent[kg]'),
sg.Input(key='-IN4-',size=(10,1))],
 [sg.Text('Please enter thrust curve (seconds vs Newtons as a  .cvs
file)', size =(50, 1)), sg.Input(key='-IN5-'),
sg.FileBrowse(file_types=(('Excel Files','*csv'),))],
 [sg.Text('Rocket parameters',size=(100,1), justification='c')],
 [sg.Text('Mass of rocket WITHOUT motor [kg]',size=(40,1)), sg.Input
(key='-IN6-', size=(10,1)),sg.Text('Rocket caliber [m]', size =(20,
1)), sg.Input(key='-IN7-', size=(10,1)) ],
 [sg.Text('Starting conditions', size=(100,1), justification='c')],
 [sg.Text('Start elevation angle [deg]', size=(30,1)),
sg.Input(key='-IN8-', size=(10,1))],
 [sg.Submit(), sg.Cancel()]
]
# Memory alocation
Memory_Allocation = 30000
window1 = sg.Window('Calculating the rocket trijectory', layout1)
event, values1 = window1.read()
window1.close()

#Storing the drag polar
DragCVS=pd.read_csv(values1['-IN1-'])
M_DragCVS_1=pd.DataFrame(DragCVS).to_numpy()
M_DragCVS=M_DragCVS_1[:,0]
Cd_DragCVS=M_DragCVS_1[:,1]
#Storing the thust curve
ThrustCVS=pd.read_csv(values1['-IN5-'])
t_ThrustCVS_1=pd.DataFrame(ThrustCVS).to_numpy()
time_thrust=t_ThrustCVS_1[:,0]
Thrust=t_ThrustCVS_1[:,1]
#Storing other parameters 
Mass_Rocket_Dry=float(values1['-IN6-'])
A=(float(values1['-IN7-'])**2)*np.pi/4
Propelent_Weight=float(values1['-IN4-'])
Engine_Initial_Mass=float(values1['-IN3-'])
Total_Impuls=float(values1['-IN2-'])
#Starting conditions 
Theta_0=float(values1['-IN8-'])
Delta = 0.02
Memory_Allocation = 30000
t = np.zeros(Memory_Allocation)
Mass = np.zeros(Memory_Allocation)
Theta = np.zeros(Memory_Allocation)
Alpha = np.zeros(Memory_Allocation)
Fn = np.zeros(Memory_Allocation)
Temp = np.zeros(Memory_Allocation)
Temp0=300
Temp[0]=Temp0
Rho=np.zeros(Memory_Allocation)
rho0=1.2
Rho[0]=rho0
M = np.zeros(Memory_Allocation)
Cd = np.zeros(Memory_Allocation)
Drag = np.zeros(Memory_Allocation)
Fx = np.zeros(Memory_Allocation)
Fy = np.zeros(Memory_Allocation)
Fz = np.zeros(Memory_Allocation)
Ax = np.zeros(Memory_Allocation)
Ay = np.zeros(Memory_Allocation)
Az = np.zeros(Memory_Allocation)
Acc = np.zeros(Memory_Allocation)
Vx = np.zeros(Memory_Allocation)
Vy = np.zeros(Memory_Allocation)
Vz = np.zeros(Memory_Allocation)
34
V = np.zeros(Memory_Allocation)
x = np.zeros(Memory_Allocation)
y = np.zeros(Memory_Allocation)
z = np.zeros(Memory_Allocation)
Distance_x = np.zeros(Memory_Allocation)
Distance_y = np.zeros(Memory_Allocation)
Distance_z = np.zeros(Memory_Allocation)
Distance = np.zeros(Memory_Allocation)
kappa = 1.4
R = 287
A=(float(values1['-IN7-'])**2)*np.pi/4
Launch_Rod_Length = 6
Mass[0]=Engine_Initial_Mass+Mass_Rocket_Dry
slices=np.linspace(0,0,num=Memory_Allocation)
Theta[0] = Theta_0
Alpha[0] = 0
Vx[0] = 0
Vy[0] = 0
Vz[0] = 0
V[0] = 0
x[0] = 0
y[0] = 0
z[0] = 0.1
Distance_x[0] = 0
Distance_y[0] = 0
Distance_z[0] = 0
Distance[0] = 0
n = 0
while z[n] > 0:
 n += 1
 t[n] = n * Delta
 new_Thrust=np.interp(t,time_thrust,Thrust)
 Temp[n]=Temp0-0.0065*z[n]
 M[n]=V[n-1]/np.sqrt(kappa*R*Temp[n])
 new_Cd=np.interp(M,M_DragCVS,Cd_DragCVS)
 slices[n]=integrate.trapz(new_Thrust,t,dx=0.01)
 Mass[n]=-
(slices[n]/Total_Impuls*Propelent_Weight)+Engine_Initial_Mass+Mass_
Rocket_Dry
 Rho[n]=rho0*(1-z[n]/44300)**(4.25588)
 Drag[n]=0.5*new_Cd[n]*Rho[n]*A*(V[n-1])**2
 if Distance[n - 1] <= Launch_Rod_Length:
35
 Fn[n] = Mass[n] * 9.81 * np.cos(np.deg2rad(Theta[0])) *
np.cos(np.deg2rad(Alpha[0]))
 else:
 Fn[n] = 0
 Fx[n] = new_Thrust[n] * np.cos(np.deg2rad(Theta[n - 1])) *
np.sin(np.deg2rad(Alpha[n - 1])) - Drag[n] * np.cos(
 np.deg2rad(Theta[n - 1])) * np.sin(np.deg2rad(Alpha[n -
1])) - Fn[n] * np.sin(
 np.deg2rad(Theta[n - 1])) * np.sin(np.deg2rad(Alpha[n -
1]))
 Fy[n] = new_Thrust[n] * np.cos(np.deg2rad(Theta[n - 1])) *
np.cos(np.deg2rad(Alpha[n - 1])) - Drag[n] * np.cos(
 np.deg2rad(Theta[n - 1])) * np.cos(np.deg2rad(Alpha[n -
1])) - Fn[n] * np.sin(
 np.deg2rad(Theta[n - 1])) * np.cos(np.deg2rad(Alpha[n -
1]))
 Fz[n] = new_Thrust[n] * np.sin(np.deg2rad(Theta[n - 1])) -
Mass[n] * 9.81 - Drag[n] * np.sin(
 np.deg2rad(Theta[n - 1])) + Fn[n] *
np.cos(np.deg2rad(Theta[n - 1]))
 Ax[n] = Fx[n] / Mass[n]
 Ay[n] = Fy[n] / Mass[n]
 Az[n] = Fz[n] / Mass[n]
 Acc[n] = np.sqrt(Ax[n]**2 + Ay[n]**2 + Az[n]**2)
 Vx[n] = Vx[n - 1] + Ax[n] * Delta
 Vy[n] = Vy[n - 1] + Ay[n] * Delta
 Vz[n] = Vz[n - 1] + Az[n] * Delta
 V[n] = np.sqrt(Vx[n]**2 + Vy[n]**2 + Vz[n]**2)

 x[n] = x[n - 1] + Vx[n] * Delta
 y[n] = y[n - 1] + Vy[n] * Delta
 z[n] = z[n - 1] + Vz[n] * Delta
 Distance_x[n] = Distance_x[n - 1] + np.abs(Vx[n] * Delta)
 Distance_y[n] = Distance_y[n - 1] + np.abs(Vy[n] * Delta)
 Distance_z[n] = Distance_z[n - 1] + np.abs(Vz[n] * Delta)
 Distance[n] = np.sqrt(Distance_x[n]**2 + Distance_y[n]**2 +
Distance_z[n]**2)
 Theta[n] = np.rad2deg(np.arcsin(Vz[n] / V[n]))
 Alpha[n] = np.rad2deg(np.arctan(Vx[n] / Vy[n]))
#Graphical interface for saving results 
layout1 = [
36
 [sg.Text('Please enter the folder in which you want to results to be stored')],
 [sg.Text('Adress', size =(50, 1)),
sg.Input(key='-IN9-'), sg.FolderBrowse(size=(10,1))],
 [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Data saving', layout1)
event, values = window.read()
window.close()
pl.figure (1)
pl.plot(y[:n], z[:n])
pl.grid()
pl.title('Rocket trijectorz?', **font, fontsize=16,
style='italic')
pl.xlabel('Distance [m]', **font, fontsize=14, style='italic')
pl.ylabel('Height [m]', **font, fontsize=14, style='italic')
pl.xticks(**font, fontsize=12)
pl.yticks(**font, fontsize=12)
pl.savefig(values['-IN9-']+"/Rocket trijectory (Distance vs Height)")
pl.figure(2)
pl.plot(t[1:n], Vz[1:n])
pl.grid()
pl.title('Vertical velocity', **font, fontsize=16, style='italic')
pl.xlabel('Seconds[s]', **font, fontsize=14, style='italic')
pl.ylabel('Vz [m/s]', **font, fontsize=14, style='italic')
pl.xticks(**font, fontsize=12)
pl.yticks(**font, fontsize=12)
pl.savefig(values['-IN9-']+"/Vertical velocity")
pl.figure(3)
pl.plot(t[1:n], Vy[1:n])
pl.grid()
pl.title('Horizontal velocity', **font, fontsize=16,
style='italic')
pl.xlabel('Seconds [s]', **font, fontsize=14, style='italic')
pl.ylabel('Vx [m/s]', **font, fontsize=14, style='italic')
pl.xticks(**font, fontsize=12)
pl.yticks(**font, fontsize=12)
pl.savefig(values['-IN9-']+"/Horzontal velocity")
pl.figure(4)
pl.plot(t[1:n], Theta[1:n])
pl.grid()

pl.title('Elevation angle', **font, fontsize=16, style='italic')
pl.xlabel('Seconds [s]', **font, fontsize=14, style='italic')
pl.ylabel(' Theta [m/s]', **font, fontsize=14, style='italic')
pl.xticks(**font, fontsize=12)
pl.yticks(**font, fontsize=12)
pl.savefig(values['-IN9-']+"/Elevation angle")
pl.figure (5)
pl.plot(t[1:n], z[1:n])
pl.grid()
pl.title('Rocket trijectory', **font, fontsize=16,
style='italic')
pl.xlabel('Seconds[s]', **font, fontsize=14, style='italic')
pl.ylabel('Height[m]', **font, fontsize=14, style='italic')
pl.xticks(**font, fontsize=12)
pl.yticks(**font, fontsize=12)
pl.savefig(values['-IN9-']+"/Rocket trijectory")
pl.figure(6)
pl.plot(t[1:n], Drag[1:n])
pl.grid()
pl.title('Drag Force', **font, fontsize=16, style='italic')
pl.xlabel('Seconds [s]', **font, fontsize=14, style='italic')
pl.ylabel('Drag force [N]', **font, fontsize=14, style='italic')
pl.xticks(**font, fontsize=12)
pl.yticks(**font, fontsize=12)
pl.savefig(values['-IN9-']+"/Drag force ")
inforesults=pd.DataFrame({"Project name" : values1['-IN-'],"Motor impuls
[Ns]": values1['-IN2-'],'GRocket mass [kg]': values1
['-IN3-'], ' Propelent mass  [kg]': values1['-IN4-'], 'Mass rocket without motor [kg]': values1['-IN6-'], 'Rocket caliber [m]': values1 ['-
IN7-'], 'Starting angle [in deg]': values1['-IN8-']},
dtype="string", index=[0])
trueresults=pd.DataFrame({'Time  [s]':t, 'Height [m]':z, 'Distance
[m]':y, 'Vertical speed? [m/s]':Vz, 'Horizontal speed
[m/s]':Vx, ' Total speed [m/s]':V, 'Vertical acceloration
[m/s^2]':Az, ' Horzontal accerelation? [m/s^2]':Ax, ' Total acceleration
[m/s^2]':Acc, 'Elecation angle [deg]':Theta, 'Masa [kg]': Mass,
'Drag coefficent  [/]':new_Cd, 'Drag force[N]':Drag, 'Thrust [N]':new_Thrust})
results=pd.concat([inforesults,trueresults])
results.to_excel(values['-IN9-']+"\Results.xlsx", index=False)
