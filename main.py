#!/usr/bin/env python2
# -*- coding: latin-1 -*-

import hid

import kivy
kivy.require('1.0.9')
from kivy.app import App
from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window

from constants import *


class MainScreen(TabbedPanel):

    def __init__(self):
        TabbedPanel.__init__(self)

        self.device=hid.device()
        self.device.open(6000,65280) #MSI keyboard

        self.region_colors=[1,4,6]
        self.region_intensity=[1,1,1]

    def key_handler(self,window,key,*largs):
        pass

    def next_color(self,region,button):
        self.region_colors[region]+=1
        if self.region_colors[region]>=len(COLORS):
            self.region_colors[region]=0
        button.background_color=COLORS[self.region_colors[region]]

    def upd_intensity(self,region,slider):
        self.region_intensity[region]=int(slider.value)

    def calculate_speed(self,color,period):
        if color==0:
            return 0
        return int(period*250/color)

    def set_normal(self,device,colors,intensity):
        device.send_feature_report((0x01,0x02,0x42,1,colors[0],intensity[0],0,0xec)) #Region 1
        device.send_feature_report((0x01,0x02,0x42,2,colors[1],intensity[1],0,0xec)) #Region 2
        device.send_feature_report((0x01,0x02,0x42,3,colors[2],intensity[2],0,0xec)) #Region 3
        device.send_feature_report((0x01,0x02,0x41,MODES["NORMAL"],0,0,0,0xec))

    def set_gaming(self,device,color,intensity):
        device.send_feature_report((0x01,0x02,0x42,1,color,intensity,0,0xec)) #Region 1
        device.send_feature_report((0x01,0x02,0x41,MODES["GAMING"],0,0,0,0xec))


    def set_breathe(self,device,colors,intensity,period):
        speeds=[[0,0,0] for i in range(3)]
        for region in range(3):
            for rgb in range(3):
                speeds[region][rgb]=self.calculate_speed(REAL_COLORS[colors[region]][rgb],period)

        device.send_feature_report((0x01,0x02,0x43,1,colors[0],intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,2,0,intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,3,speeds[0][0],speeds[0][1],speeds[0][2],0xec)) 

        device.send_feature_report((0x01,0x02,0x43,4,colors[1],intensity[1],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,5,0,intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,3,speeds[1][0],speeds[1][1],speeds[1][2],0xec)) 

        device.send_feature_report((0x01,0x02,0x43,7,colors[2],intensity[2],0,0xec))
        device.send_feature_report((0x01,0x02,0x43,8,0,intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,3,speeds[1][0],speeds[1][1],speeds[1][2],0xec)) 

        device.send_feature_report((0x01,0x02,0x41,MODES["BREATHE"],0,0,0,0xec))


    def set_wave(self,device,colors,intensity,period):
        speeds=[[0,0,0] for i in range(3)]
        for region in range(3):
            for rgb in range(3):
                speeds[region][rgb]=self.calculate_speed(REAL_COLORS[colors[region]][rgb],period)

        device.send_feature_report((0x01,0x02,0x43,1,colors[0],intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,2,0,intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,3,speeds[0][0],speeds[0][1],speeds[0][2],0xec)) 

        device.send_feature_report((0x01,0x02,0x43,4,colors[1],intensity[1],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,5,0,intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,3,speeds[1][0],speeds[1][1],speeds[1][2],0xec)) 

        device.send_feature_report((0x01,0x02,0x43,7,colors[2],intensity[2],0,0xec))
        device.send_feature_report((0x01,0x02,0x43,8,0,intensity[0],0,0xec)) 
        device.send_feature_report((0x01,0x02,0x43,3,speeds[1][0],speeds[1][1],speeds[1][2],0xec)) 

        device.send_feature_report((0x01,0x02,0x41,MODES["WAVE"],0,0,0,0xec))

    def apply(self,mode):
        if mode==MODES["NORMAL"]:
            self.set_normal(self.device,self.region_colors,self.region_intensity)
        elif mode==MODES["GAMING"]:
            self.set_gaming(self.device,self.region_colors[0],self.region_intensity[0])
        elif mode==MODES["BREATHE"]:
            period=self.ids.slider_period.value
            self.set_breathe(self.device,self.region_colors,self.region_intensity,period)
        elif mode==MODES["WAVE"]:
            period=3**self.ids.slider_period_wave.value
            self.set_wave(self.device,self.region_colors,self.region_intensity,period)

class MsiKbManager(App):

    def __init__(self):
        App.__init__(self)

        Window.bind(on_keyboard=self.key_handler)

    
    def key_handler(self,window,key,*largs):
        if key == 27: #Escape
            try:
                self.settings_screen.on_close()
                return True
            except:
                return False
        return False

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    MsiKbManager().run()

