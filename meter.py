#! /usr/bin/python3

import tkinter as tk
from decimal import Decimal
import cmath
import sys
import logging
import math
import time

################################### Initialize #################################
class Initialize(tk.Frame):
    def __init__(self, parent, size=100):
        tk.Frame.__init__(self, parent)
        self.size = size

    def to_absolute(self, x, y):
        return x + self.size/2, y + self.size/2

################################### Dial #######################################
def draw_dial(canv,x0,y0,degree, t,r):
    xr=x0
    yr=y0
    angle = math.radians(degree)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    dy=r*sin_val
    dx=r*cos_val
    dx2=t*sin_val
    dy2=t*cos_val
    mlx=xr+dx
    mly=yr-dy
    mrx=xr-dx
    mry=yr+dy
    px=xr+dx2
    py=yr+dy2
    xy = x0-r,y0-r,x0+1*r,y0+1*r
    xyz = mlx,mly,px,py,mrx,mry
    canv.delete('dial')
    canv.create_arc(xy,start=degree,extent=180,fill="#00A2E8",
                    tags=('dial', 'one', 'two', 'three', 'four'))
    canv.create_polygon(xyz, fill="#00A2E8",tags=('dial', 'two'))
    canv.create_oval(xr-5,yr-5,xr+5,yr+5,fil="#00A2E8",tags=('dial', 'three'))
    canv.create_line(xr,yr,px,py,fill="light gray",tags=('dial', 'four'))

############################### Position Meter #################################
class PositionMeter(Initialize):
    def __init__(self, parent,max_value, min_value, size,**options):
        super().__init__(parent, size=size, **options)

        self.max_value = float(max_value)
        self.min_value = float(min_value)
        self.size = size
        self.canvas = tk.Canvas(self, width=self.size, height=self.size-self.size/12,
                                bg='white',highlightthickness=0)
        self.canvas.grid(row=0)
        self.draw_PosMeter()
        self.draw_tick()
        initial_value = 0.0
        self.set_value(initial_value)

    def draw_PosMeter(self, divisions=100):
        self.canvas.create_arc(self.size/5, self.size/6, self.size-self.size/6,
                               self.size-self.size/6, style="arc", outline = "red",
                               start=-61, extent=61,width=self.size/10)
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6,
                               self.size-self.size/6,outline = "orange",start=0,
                               width=self.size/10,style="arc", extent=60)
                               
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6,
                               self.size-self.size/6,width=self.size/10,style="arc",
                               start=60, extent=60, outline = "yellow")
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6,
                               self.size-self.size/6,width=self.size/10,style="arc",
                               start=120, extent=60, outline = "light green")
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6,
                               self.size-self.size/6,width=self.size/10,style="arc",
                               start=180, extent=60,outline = "green")
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5,
                                               font=("Arial",int(self.size/18),'bold'),
                                               fill="black", text='')
        
    def draw_tick(self,divisions=100):
        inner_tick_radius = int((self.size-self.size/9) * 0.35)
        outer_tick_radius = int((self.size-self.size/9) * 0.45)
        label = 'Position'
        self.canvas.create_text(self.size/2,2*self.size/5, font=("Arial",int(self.size/18)),
                                fill="black", text=label,angle=0)
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5,
                                               font=("Arial",int(self.size/18),'bold'),
                                               fill="black", text='')
        inner_tick_radius2 = int((self.size-self.size/9) * 0.48)
        outer_tick_radius2 = int((self.size-self.size/9) * 0.50)
        inner_tick_radius3 = int((self.size-self.size/9) * 0.35)
        outer_tick_radius3 = int((self.size-self.size/9) * 0.40)
        for tick in range(divisions+1):
            angle_in_radians = (2.0 * cmath.pi / 3.0)+tick/divisions * (5.0 * cmath.pi / 3.0)
            inner_point = cmath.rect(inner_tick_radius, angle_in_radians)
            outer_point = cmath.rect(outer_tick_radius, angle_in_radians)
            if (tick%10) == 0:
                self.canvas.create_line(
                    *self.to_absolute(inner_point.real, inner_point.imag),
                    *self.to_absolute(outer_point.real, outer_point.imag),
                    width=2,fill='blue')
            else:
                inner_point3 = cmath.rect(inner_tick_radius3, angle_in_radians)
                outer_point3 = cmath.rect(outer_tick_radius3, angle_in_radians)
                self.canvas.create_line(
                    *self.to_absolute(inner_point3.real, inner_point3.imag),
                    *self.to_absolute(outer_point3.real, outer_point3.imag),
                    width=1,fill='black')
            if (tick%10) == 0:
                inner_point2 = cmath.rect(inner_tick_radius2, angle_in_radians)
                outer_point2 = cmath.rect(outer_tick_radius2, angle_in_radians)
                x= outer_point2.real + self.size/2
                y= outer_point2.imag + self.size/2
                label = str(int(self.min_value + tick * (self.max_value-self.min_value)/100))
                self.canvas.create_text(x,y, font=("Arial",int(self.size/20)),fill="black",
                                        text=label)
                
    def set_value(self, number: (float, int)):
        number = number if number <= self.max_value else self.max_value
        number = number if number > self.min_value else self.min_value
        degree = 30.0 + (number- self.min_value) / (self.max_value - self.min_value) * 300.0
        draw_dial(self.canvas,self.size/2,self.size/2,-1*degree,self.size/3,8)
        label = str(int(number))
        self.canvas.delete(self.readout)
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5,
                                               font=("Arial",int(self.size/14),'bold'),
                                               fill="black", text=label,angle=0)
        
############################### Voltage Meter ##################################
class VoltageMeter(Initialize):
    def __init__(self, parent, max_value, min_value, size, **options):
        super().__init__(parent, size=size, **options)

        self.max_value = float(max_value)
        self.min_value = float(min_value)
        self.size = size
        self.canvas = tk.Canvas(self, width=self.size, height=3*self.size/5,bg='white',
                                highlightthickness=0)
        self.canvas.grid(row=0)
        self.draw_VolMeter()
        self.draw_tick()
        initial_value = 0.0
        self.set_value(initial_value)
    
    def draw_VolMeter(self, divisions=100):
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7,
                               self.size-self.size/7, style="arc",
                               width=self.size/9,start=0, extent=60,
                               outline = "orange")
        good_color = "#00A2E8"
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7,
                               self.size-self.size/7, width=self.size/9,
                               style="arc",start=60, extent=60, outline = good_color)
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7,
                               self.size-self.size/7, width=self.size/9,style="arc",
                               start=120, extent=60,
                               outline = "light green")
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5,
                                               font=("Arial",int(self.size/18),
                                                     'bold'),fill="black", text='')

    def draw_tick(self, divisions=100):
        inner_tick_radius = int((self.size-self.size/9) * 0.35)
        outer_tick_radius = int((self.size-self.size/9) * 0.45)
        label = "Voltage"
        self.canvas.create_text(self.size/2,3*self.size/10, text=label,angle=0,
                                font=("Arial",int(self.size/20)),fill="red")
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5,
                                               font=("Arial",int(self.size/18),'bold'),
                                               fill="dark blue", text='')
        inner_tick_radius2 = int((self.size-self.size/9) * 0.48)
        outer_tick_radius2 = int((self.size-self.size/9) * 0.50)
        inner_tick_radius3 = int((self.size-self.size/9) * 0.35)
        outer_tick_radius3 = int((self.size-self.size/9) * 0.40)

        for tick in range(divisions+1):
            angle_in_radians = (cmath.pi)+ tick/divisions * cmath.pi
            inner_point = cmath.rect(inner_tick_radius, angle_in_radians)
            outer_point = cmath.rect(outer_tick_radius, angle_in_radians)
            

            if (tick%10) == 0:
                self.canvas.create_line(
                    *self.to_absolute(inner_point.real, inner_point.imag),
                    *self.to_absolute(outer_point.real, outer_point.imag),
                    width=2,fill='blue')
            else:
                inner_point3 = cmath.rect(inner_tick_radius3, angle_in_radians)
                outer_point3 = cmath.rect(outer_tick_radius3, angle_in_radians)
                self.canvas.create_line(
                    *self.to_absolute(inner_point3.real, inner_point3.imag),
                    *self.to_absolute(outer_point3.real, outer_point3.imag),
                    width=1,fill='light blue')
            if (tick%10) == 0:
                inner_point2 = cmath.rect(inner_tick_radius2, angle_in_radians)
                outer_point2 = cmath.rect(outer_tick_radius2, angle_in_radians)
                x= outer_point2.real + self.size/2
                y= outer_point2.imag + self.size/2
                label = str(int(self.min_value + tick * (self.max_value-self.min_value)/100))
                self.canvas.create_text(x,y, font=("Arial",int(self.size/20)),
                                        fill="black", text=label)
    def set_value(self, number: (float, int)):
        number = number if number <= self.max_value else self.max_value
        number = number if number > self.min_value else self.min_value
        degree = 90.0 + (number- self.min_value) / (self.max_value - self.min_value) * 180.0
        draw_dial(self.canvas,self.size/2,self.size/2,-1*degree,self.size/3,8)
        label = str(float(number))
        self.canvas.delete(self.readout)
        self.readout = self.canvas.create_text(self.size/3+35,self.size/2+15,
                                               font=("Arial",int(self.size/19),'bold'),
                                               fill="black", text=label,angle=0)
