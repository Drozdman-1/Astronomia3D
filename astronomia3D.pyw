import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.lines import Line2D
from matplotlib.widgets import TextBox,RadioButtons
from matplotlib.widgets import Button as widgets_Button
from matplotlib.offsetbox import AnchoredText
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Wedge
import mpl_toolkits.mplot3d.art3d as art3d

import matplotlib.animation as animation
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox 

from calc_pl import *
from help_windowAstron3D import *
from func_tools import *

#import keyboard



class c:
    planets={"Sun" : "☉", "Moon" : "☽", "Mercury" : "☿", "Venus" : "♀", "Mars" : "♂", "Jupiter" : "♃", "Saturn" : "♄", "Uranus" : "♅", "Neptune" : "♆", "Pluto" : "♇", "Node_N" : "☊", "Node_S" : "☋"}
    planets2=["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Node_N", "Node_S", "Asc", "MC"]

houses_names=["","I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
zodiac = ["","Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"] 
zodiac2 = ["", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]

color_ecl="#A9A54B"
color_ecl_zod="#767109"
color_oran="#F38600"
color_yel="#EFC300"
pl_colors={"Sun" : "#F2C500", "Moon" : "#FF8D00", "Mercury" : "#008CD2", "Venus" : "#098100", "Mars" : "#AA0000", "Jupiter" : "#6E8CA5", "Saturn" : "#874400", "Uranus" : "#1900D6", "Neptune" : "#006695", "Pluto" : "#6D00A0", "Node_N" : "#333", "Node_S" : "#333"} 

main_circles_clickable = True #  ecliptic, equator, horizon, prime vertical
main_circles_picker = 2 if main_circles_clickable == True else 0

data_pts=50

class astro3D():
    def __init__(self, parent,frame, planets_data, geo_latitude, data={}): #timestamp=0
        self.parent=parent
        bgr_col="#E0EFF0"
        self.fig = Figure(figsize=(11,8), dpi=100, facecolor = bgr_col)
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor = bgr_col)

        at = AnchoredText("Astronomia 3D by Popiel", loc="lower right",bbox_to_anchor=(0.9, 0.195), frameon=False,borderpad=0, prop=dict(alpha=0.2,size=13,color="#78A1A4",fontfamily="Lucida Handwriting"),bbox_transform=self.ax.transAxes)
        at.set_zorder(0)
        self.ax.add_artist(at)

        #================ 

        size900=size760=False
        screenHeight = parent.winfo_screenheight()
        if screenHeight<880:size900=True
        if screenHeight<780:size760=True;size900=False

        f_w=11;f_h=8
        if size900==True: dd=0.93;self.fig.set_size_inches(f_w*dd, f_h*dd);
        elif size760==True: dd=0.80;self.fig.set_size_inches(f_w*dd, f_h*dd);

        #================ 

        self.ids={}
        self.equat_ids=[]
        self.ecl_ids=[]
        self.pl_ids=[]
        self.leg_obj={}
        self.leg_items_ids=[]
        self.ecliptic_scale={}
        self.equator_scale={}


        #========== fix distorted circles (shown as ovals)  ======
        limits = self.ax.get_w_lims()
        self.ax.set_box_aspect((limits[1]-limits[0],limits[3]-limits[2],limits[5]-limits[4]))
        #===============

        self.fig.subplots_adjust(left=-0.2, bottom=-0.3, right=0.95, top=1.25, wspace=None, hspace=None) #margins

        self.planets_data=planets_data
        self.geo_latitude=geo_latitude
        self.data=data
        self.timestampIni = self.data["timestamp"]

        self.ε=23.44
        self.ε=self.data["obliquity"]
        self.trueNode=data["trueNode"]


        self.txt1=[0.87,0.206]
        self.prop_txt1={"color":'#333', "fontsize":8}
        self.id_text = self.ax.text2D(*self.txt1, "", **self.prop_txt1, transform=self.ax.transAxes)

        self.txt_name=[0.2,0.818]
        self.txt_time=[0.913,0.29]
        self.txt_time2=[0.911,0.26]
        self.txt1=[0.18,0.206]
        self.txt2=[0.41,0.206]
        self.txt3=[0.18,0.230]

        if size760==True:
            self.txt_time=[0.917+0.09,0.28]
            self.txt_time2=[0.915+0.09,0.25]
        elif size900==True:
            self.txt_time=[0.917+0.02,0.29]
            self.txt_time2=[0.915+0.02,0.26]

        bgr_col_bb1="#2D6266"
        bgr_col_bb3="#70ADB2"
        bgr_col_bb2="#EFE9DD" 
        PAGE_BG1 = "#134752"
        bgr_col_bb1=PAGE_BG1
        COL_2="#AA0000"
        COL_3="#AB1D00"
        bgr_col_bb3="#C4D4D5" #blue


        self.prop_txt1={"color":'#333', "fontsize":8}
        self.prop_txt2={"bbox": dict(boxstyle="round", facecolor=bgr_col_bb2, ec="#CEEFF1", pad=0.3, alpha=0.8), "color":"#333", "fontsize":9 }
        col_4="#001D4B"
        self.prop_txt3={"bbox": dict(boxstyle="round", facecolor=bgr_col_bb3, ec="#CAE2E3", pad=0.3, alpha=0.84), "color":col_4, "fontsize":10, "fontweight":400, "fontfamily":"Tahoma"}

        self.prop_txt_name={"bbox": dict(boxstyle="round", facecolor=bgr_col_bb1, ec="#CEEFF1", pad=0.4, alpha=0.9), "color":"#EEEEEE", "fontsize":10, "fontweight":800, "alpha":1}
        self.prop_txt_time={"bbox": dict(boxstyle="round", facecolor=bgr_col_bb3, ec="#CAE2E3", pad=0.5, alpha=0.84), "color":COL_3, "fontsize":10, "fontweight":600, "fontfamily":"Consolas"}
        self.prop_txt_time2={"bbox": dict(boxstyle="round", facecolor=bgr_col_bb3, ec="#CAE2E3", pad=0.4, alpha=0.74), "color":"#333", "fontsize":8, "fontweight":600, "fontfamily":"Consolas"}

        self.id_text = self.ax.text2D(*self.txt1, "", **self.prop_txt1, transform=self.ax.transAxes)
        self.id_text_2 = self.ax.text2D(*self.txt2, "", **self.prop_txt2, transform=self.ax.transAxes)
        self.id_text_3 = self.ax.text2D(*self.txt3, "", **self.prop_txt3, transform=self.ax.transAxes)

        help_x=1.036; help_y=0.2065
        if size760==True:help_x=1.036+0.126
        elif size900==True:help_x=1.036+0.035
        self.id_help_ico = self.ax.text2D(help_x, help_y, "?", c = "#F6F6F6", size = 10, fontweight = 800, picker=5, bbox = dict(boxstyle = "circle", edgecolor = "#990000",facecolor = "#800000",pad = 0.2), ha = "left", va = "center",alpha = 0.7, transform = self.ax.transAxes)

        #=============


        alpha_main=0.7
        self.alpha_main=alpha_main
        self.sw_cir_alpha=False

        self.ψ2 = np.linspace(-np.pi/2, np.pi/2, 100)
        self.w = np.array([0, -1, 0])

        #========== Horizon
        color_hor="#001440"
        color_hor="#333333"
        self.ψ = np.linspace(0, 2 * np.pi, 100)
        φ=self.ψ
        r=1
        x1=r * np.cos(φ)
        y1=r * np.sin(φ)
        z1=np.zeros(np.size(x1))
        
        '''
        #solid
        id_,=self.ax.plot(x1,y1,z1,color=color_hor,linewidth=2 ,picker=2)
        self.hor_circl=id_
        #id_=id(id_)
        self.ids[id(id_)] =[[x1[3],y1[3],z1[0]],"Horizon"]
        '''

        φ_1 = np.linspace(-np.pi/2, np.pi/2, 50)
        x1=r * np.cos(φ_1); y1=r * np.sin(φ_1); z1=np.zeros(np.size(x1));
        id_1, = self.ax.plot(x1,y1,z1 ,color=color_hor,picker=main_circles_picker, linewidth=1, linestyle = "solid", alpha=alpha_main)

        self.hor_circl_1=id_1
        self.ids[id(id_1)] =[[x1[20],y1[20],z1[0]],"Horizon"]

        φ_2 = np.linspace(np.pi/2,np.pi*3/2, 50)
        x1=r * np.cos(φ_2); y1=r * np.sin(φ_2); z1=np.zeros(np.size(x1));
        id_2, = self.ax.plot(x1,y1,z1 ,color=color_hor,picker=main_circles_picker, linewidth=1, linestyle = "dashed", alpha=alpha_main) 

        self.hor_circl_2=id_2
        self.ids[id(id_2)] =[self.ids[id(id_1)][0],"Horizon"]


        #======== Prime vertical
        
        color_vert="#050835"
        color_vert=color_hor
        θ=self.ψ

        '''
        #solid        
        z2= r * np.cos(θ) 
        x2= r * np.sin(θ)
        y2=np.zeros(np.size(x2))
        id_,=self.ax.plot(x2,y2,z2,color=color_vertlinewidth=1,picker=2 ) #"#0009BC"
        self.ids[id(id_)] =[[x2[20],y2[20],z2[20]],"Prime Vertical"] #"v_rot+π/2"
        self.prime_vert=id_
        '''
        φ_1 = np.linspace(0, np.pi, 50)
        x2=r * np.sin(φ_1); z2=r * np.cos(φ_1); y2=np.zeros(np.size(x2));
        id_1, = self.ax.plot(x2,y2,z2 ,color=color_vert, linewidth=1, linestyle = "solid", alpha=alpha_main,picker=main_circles_picker)

        self.prime_vert_1=id_1
        self.ids[id(id_1)] =[[x2[13],y2[13],z2[13]],"Prime Vertical"]

        φ_2 = np.linspace(np.pi,2*np.pi, 50)
        x2=r * np.sin(φ_2); z2=r * np.cos(φ_2); y2=np.zeros(np.size(x1));
        id_2, = self.ax.plot(x2,y2,z2 ,color=color_vert, linewidth=1, linestyle = "dashed", alpha=alpha_main,picker=main_circles_picker) 

        self.prime_vert_2=id_2
        self.ids[id(id_2)] =[self.ids[id(id_1)][0], "Prime Vertical"]

        X,Y,Z =self.draw_axes()

        id_=self.ax.scatter(1, 0, 0, marker="o",c="#265678", s=9, zorder=0); "#3B6D91"
        self.ids[id(id_)] =[[1,0,0]," φ=0, θ=0"]
        self.start_pt=id_

        self.plot_circle_scale("Horizon");
        self.plot_circle_scale("Prime vertical")


        #================

        self.date_utc = self.data["d_utc"]
        self.time_utc = self.data["t_utc"]
        self.timestamp = self.data["timestamp"]
        self.geo_longitude=float(self.data["lon"])

        name = " {} {} ".format(self.data["n"], self.data["ln"])
        time_utc = " UTC: {: >10}, {: >8} ".format(self.data["d_utc"], self.data["t_utc"])
        d_loc="{}-{}-{}".format(self.data["d"][2], self.data["d"][1], self.data["d"][0])
        t_loc="{: >2}:{:0>2}:{}".format(self.data["t"][0], self.data["t"][1], self.data["t"][2])
        time_loc = "{: >10}, {: >8}".format(d_loc, t_loc)
        time_loc= "{: ^21}".format(time_loc)
        name=""
        self.id_text_name= self.ax.text2D(*self.txt_name, name, **self.prop_txt_name, transform=self.ax.transAxes)
        self.id_text_time= self.ax.text2D(*self.txt_time, time_loc, **self.prop_txt_time, transform=self.ax.transAxes)
        self.id_text_time2= self.ax.text2D(*self.txt_time2, time_utc, **self.prop_txt_time2, transform=self.ax.transAxes)

        #================

        self.plot_Equator_Ecliptic()        
        self.draw_sphere()
        self.sphere_.set_visible(False)        
        self.draw_surface()
        self.plot_meridian()
        
        self.planets_obj={}
        self.houses_obj={}
        self.zodiac_obj={}
        self.planets_ids={}
        self.houses_ids={}
        self.zodiac_ids={}
        self.plot_planets(self.planets_data)
        self.plot_zodiac()

        style_=(0, (1, 2))
        id_axes,=self.ax.plot(X,Y,Z ,color='#999999',linestyle = style_,label='Axes', alpha=alpha_main,picker=0)
        self.leg_items_ids.append(id_axes) ;self.axes_id=id_axes

        self.azim0=20
        self.elev0=15
        self.ax.view_init(elev = self.elev0, azim = self.azim0)

 
        col_="#900000"
        self.annot = self.ax.annotate("click", xy=(0,0), fontsize=9, c=col_, xytext=(-20,20),textcoords="offset points",bbox=dict(boxstyle="round,pad=0.5", fc="#FCFF90", alpha = 0.7),arrowprops=dict(arrowstyle="->"), zorder=20)    #"offset pixels"
        self.annot.set_visible(False)

        self.click_tip_list=["North Pole", "South Pole", "Ecliptic North Pole", "Ecliptic South Pole"]


        #========== Legend ========
        leg_colPM="#333333"
        leg_colHor=color_hor
        leg_colPM=color_vert 
        add_item0 = Line2D([0], [0], marker="o", color="w", label="Sphere", markerfacecolor="#D0C7E8", markersize=10,linewidth=10)
        add_item1 = Line2D([0], [0], marker="s", color="w", label="Equator", markerfacecolor="#700000", markersize=10,linewidth=10)
        add_item2 = Line2D([0], [0], marker="s", color="w", label="Ecliptic", markerfacecolor="#A9A54B", markersize=10)#
        add_item3 = Line2D([0], [0], marker="s", color="w", label="Horizon", markerfacecolor=leg_colHor, markersize=10)
        add_item4 = Line2D([0], [0], marker="s", color="w", label="Prime Vertical", markerfacecolor=leg_colPM, markersize=10)
        add_item5 = Line2D([0], [0], marker="s", color="w", label="Meridian",markerfacecolor="#333333", markersize=10)#
        add_item6 = Line2D([0], [0], marker="s", color="w", label="Proj. Horizons",markerfacecolor="#2D305C", markersize=10)
        add_item7 = Line2D([0], [0], marker="s", color="w", label="Parallels",markerfacecolor="#333333", markersize=10)
        add_item8 = Line2D([0], [0], marker="*", color="w", label="Extra off",markerfacecolor='#543E17', markersize=10)#

        add_item9 = Line2D([0], [0], marker='o', color='#DCDCDC', label="Show half",markerfacecolor='#333333', markersize=1,linestyle="dashed")

        id_scale= Line2D([0], [0], marker='o', color='#DCDCDC', label="Scale",markerfacecolor='#333333', markersize=1,linestyle="dashed")
        #add_item24 = Line2D([0], [0], marker="o", color="w", label="Show grid", markerfacecolor='#111111', markersize=10)

        self.leg_mer_circle=add_item5

        for id_ in [add_item0, add_item1, add_item2, add_item3, add_item4, add_item5,add_item8, add_item9,id_scale]:
            self.leg_items_ids.append(id_)

        leg_x=0.99;leg_y=0.99
        self.legend = self.fig.legend(handles=self.leg_items_ids,loc="upper right",fancybox=True, shadow=True,borderpad=0.6,bbox_to_anchor=(leg_x, leg_y), prop=dict(size=10))

        for legline, line, text in zip(self.legend.get_lines(), self.leg_items_ids, self.legend.get_texts()):
            legline.set_picker(True)
            legline.set_pickradius(6)
            txt=text.get_text()
            self.leg_obj[legline] = (txt, line)


        #===============
        x001 = 0.92
        y001 = 0.58

        #Texts  "View:"
        resize = 0.58
        f_size = 9
        f_col = "#333"
        b_col = "#D3D3D3"
        e_col = "#999999"
        b_col2 = "#EEEEEE"
        font_f = "Courier New"  #"Tahoma"
        font_w = "bold"
        alpha_t = 0.9

        x00 = 0.916
        y00 = 0.58

        if size760==True:resize = 0.7; dd=0.93;x00=x00+0.1
        elif size900==True: resize = 0.625; dd=0.93;x00=x00+0.03

        x0 = x00; y0 = y00;dx = 0.0368; dx1 = 0.04  
        dx = resize * dx; x01= 0.009

        self.id_view=self.ax.text2D(x0, y0, "View:", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w, bbox = dict(boxstyle = "round", edgecolor = b_col2, facecolor = b_col2,pad = 0.3), picker = 3, ha = "left", va = "center",alpha = 1, transform = self.ax.transAxes)
        self.id_E = self.ax.text2D(x0 + x01 + 2*dx, y0, "E", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "round", edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "center", va = "center",alpha = alpha_t, transform = self.ax.transAxes)
        self.id_W = self.ax.text2D(x0 + x01 + 3*dx, y0, "W", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "round", edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "center", va = "center",alpha = alpha_t, transform = self.ax.transAxes)
        self.id_N = self.ax.text2D(x0 + x01 + 4*dx, y0, "N", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "round", edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "center", va = "center",alpha = alpha_t, transform = self.ax.transAxes)    
        self.id_S = self.ax.text2D(x0 + x01 + 5*dx, y0, "S", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "round", edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "center", va = "center",alpha = alpha_t, transform = self.ax.transAxes)

        #Texts  "Azim:"
        x0 = x00 
        dy00 = 0.04
        dy00 = resize * dy00
        y0 =  y00 - dy00;
        dy = 0.035;
        dx = 0.0449 ; dx1 = 0.024
        dx = resize * dx
        dy = resize * dy

        self.id_azim=self.ax.text2D(x0, y0 , "Azim:", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w, bbox = dict(boxstyle = "round", edgecolor = b_col2, facecolor = b_col2, pad = 0.3), picker = 3, ha = "left", va = "center",alpha = 1, transform = self.ax.transAxes) 

        self.id_A0 = self.ax.text2D(x0 + dx1 + dx, y0 , " 0", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center", alpha = alpha_t, transform = self.ax.transAxes) 
        self.id_A90 = self.ax.text2D(x0 + dx1 + 2*dx, y0 , "90", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)
        self.id_A180 = self.ax.text2D(x0 + dx1 + 3*dx, y0 , "180", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)

        self.id_elev=self.ax.text2D(x0, y0 - dy, "Elev:", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , bbox = dict(boxstyle = "round",edgecolor = b_col2, facecolor = b_col2,pad = 0.3), picker = 3, ha = "left", va = "center",alpha = 1, transform = self.ax.transAxes) 

        self.id_E0 = self.ax.text2D(x0 + dx1 + dx, y0 - dy, " 0", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)   
        self.id_E90 = self.ax.text2D(x0 + dx1 + 2*dx, y0 - dy, "90", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)
        self.id_E180 = self.ax.text2D(x0 + dx1 + 3*dx, y0 - dy, "180", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)  
        
        #Texts  "Init "

        dy = 0.05; dx = 0.04
        x0 = x00
        dy00 = 0.07
        dy00 = resize * dy00
        y0 = y00 - dy00    
        dy = 0.056; dx = 0.077
        dx = resize * dx
        dy = resize * dy

        self.id_v_start = self.ax.text2D(x0, y0 - dy, "Init ", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center", alpha = alpha_t, transform = self.ax.transAxes)
        self.id_v_chart = self.ax.text2D(x0 + dx, y0 - dy, "Chart", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center", alpha = alpha_t, transform = self.ax.transAxes)   
        self.id_v_Eq = self.ax.text2D(x0 + 2*dx, y0 - dy, "Equat", c = f_col, size = f_size, fontfamily = font_f, fontweight = font_w , picker = 5,bbox = dict(boxstyle = "round",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center", alpha = alpha_t, transform = self.ax.transAxes)       

        x0 = x00; 
        dx00 = 0.082
        dx00 = resize * dx00
        x0 = x0 + dx00
        dy00 = 0.15
        dy00 = resize * dy00
        y0 = y00 - dy00
        dx1 = 0.02; dx2=0.024
        dy1 = 0.08; dy2 = 0.14; dy3 = 0.11;
        dy1 = resize * dy1; dy2 = resize * dy2; dy3 = resize * dy3

        dx2=0.028;dx2b=0.024
        f_size2=7
        self.id_v_up = self.ax.text2D(x0 + resize * dx1, y0 - dy1, "  ", c = f_col, size = f_size2, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "rarrow",edgecolor = e_col,facecolor = b_col,pad = 0.3), rotation=90, ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)
        self.id_v_down = self.ax.text2D(x0 + resize * dx1, y0 - dy2, "  ", c = f_col, size = f_size2, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "larrow", edgecolor = e_col,facecolor = b_col,pad = 0.3), rotation=90, ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)    
        self.id_v_left = self.ax.text2D(x0 + resize * dx1 - resize * dx2, y0 - dy3, "  ", c = f_col, size = f_size2, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "larrow",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)
        self.id_v_right = self.ax.text2D(x0 + resize * dx1 + resize * dx2b, y0 - dy3, "  ", c = f_col, size = f_size2, fontfamily = font_f, fontweight = font_w , picker = 5, bbox = dict(boxstyle = "rarrow",edgecolor = e_col,facecolor = b_col,pad = 0.3), ha = "left", va = "center",alpha = alpha_t, transform = self.ax.transAxes)


        self.id_v_anim=None
        self.id_v_prev=self.id_v_next=None
        self.id_v_test=None


        self.half=0
        self.view_East=[self.hor_circl_1, self.prime_vert_1, self.eq_circl_1,  self.ecl_circl_1]
        self.view_West=[self.hor_circl_2, self.prime_vert_2, self.eq_circl_2,  self.ecl_circl_2]

        self.circles_alpha()

        self.ax.set_axis_off() 
        self.ax.axison=False

        self.ax.set_xlabel('x - axis');    self.ax.set_ylabel('y - axis');    self.ax.set_zlabel('z - axis')
        arr=[-1,0,1]
        self.ax.set_xticks(arr); self.ax.set_yticks(arr); self.ax.set_zticks(arr);

        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()
        self.zlim = self.ax.get_zlim()


        #============= Tkinter =============
        self.canvas = FigureCanvasTkAgg(self.fig, master = frame)
        self.canvas.draw()  
        self.canvas.get_tk_widget().pack(side=TOP, anchor=NW, fill=BOTH, expand=True)

        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('pick_event', self.onpick)   
        self.canvas.mpl_connect('key_release_event', self.key_)
        #self.canvas.mpl_connect('scroll_event', self.scroll_zoom)
        
        #=========== window size  

        mins_x=1000;mins_y=700
        self.parent.minsize(mins_x,mins_y)
        w,h = self.fig.get_size_inches()*self.fig.dpi
        h = h + 100 #figure plus parent window
        w = w + 50
        window=self.parent
        screenHeight = window.winfo_screenheight()
        screenWidth = window.winfo_screenwidth()
        x = int(screenWidth/2 - w/2)
        y = int(screenHeight/2 - h/2)
        window.wm_geometry("+{}+{}".format(x, y))
        window.resizable(False, False)    

    def draw_axes(self): 
        z4 = np.linspace(-1.01,1.01,50)
        y4 = np.zeros(np.size(z4))
        x4 = np.zeros(np.size(y4))

        x5 = np.linspace(-1.01,1.01,50)
        y5 = np.zeros(np.size(z4))
        z5 = np.zeros(np.size(y4))

        y6 = np.linspace(-1.01,1.01,50)
        x6 = np.zeros(np.size(z4))
        z6 = np.zeros(np.size(y4))

        #========joined data for legend - one item only to swicth off
        X=np.append(x4,np.NaN);X=np.append(X,x5) ;X=np.append(X,np.NaN); X=np.append(X,x6)
        Y=np.append(y4,np.NaN);Y=np.append(Y,y5) ;Y=np.append(Y,np.NaN); Y=np.append(Y,y6)
        Z=np.append(z4,np.NaN);Z=np.append(Z,z5) ;Z=np.append(Z,np.NaN); Z=np.append(Z,z6)

        return [X,Y,Z] 

    def circles_alpha(self):
        if self.sw_cir_alpha==False:
            self.prime_vert_1.set_alpha(0.4)
            self.prime_vert_2.set_alpha(0.2)
            self.hor_circl_2.set_alpha(0.2) 
            self.mer_circle.set_alpha(0.2)
            self.axes_id.set_alpha(0.2)

            for cir in [self.eq_circl_2, self.ecl_circl_2]:
                cir.set_alpha(0.2) 

            for el in self.ecliptic_scale:
                self.ecliptic_scale[el][0].set_alpha(0.5) 
                self.ecliptic_scale[el][1].set_alpha(0.5) 
            for el in self.equator_scale:
                self.equator_scale[el][0].set_alpha(0.5) 
                self.equator_scale[el][1].set_alpha(0.5)

            self.sw_cir_alpha=True

        elif self.sw_cir_alpha==True:
            self.prime_vert_1.set_alpha(self.alpha_main)
            self.prime_vert_2.set_alpha(self.alpha_main)
            self.hor_circl_2.set_alpha(self.alpha_main) 
            self.mer_circle.set_alpha(self.alpha_main)
            self.axes_id.set_alpha(self.alpha_main)

            for cir in [self.eq_circl_1, self.ecl_circl_1]:
                cir.set_alpha(self.alpha_main_2)
            for cir in [self.eq_circl_2, self.ecl_circl_2]:
                cir.set_alpha(self.alpha_main_2) 

            for el in self.ecliptic_scale:
                self.ecliptic_scale[el][0].set_alpha(self.alpha_main) 
                self.ecliptic_scale[el][1].set_alpha(self.alpha_main) 
            for el in self.equator_scale:
                self.equator_scale[el][0].set_alpha(self.alpha_main) 
                self.equator_scale[el][1].set_alpha(self.alpha_main)        

            self.sw_cir_alpha=False


    def plot_Equator_Ecliptic(self):
        ARMC=self.planets_data["MC"]["eq"][0]    
        ARMC=float(ARMC)
        ARMC=norm_(ARMC)
        self.ARMC=ARMC
        φ = self.ψ
        self.k = k = np.array([1, 0, 0])
        self.v = v = np.array([0, 1, 0])

        geo_latitude=self.geo_latitude
        s1 = "S" if self.geo_latitude<0 else "N"
        s2 = "W" if self.geo_longitude<0 else "E"
        txt="ARMC={:.0f}°, lat={:.0f}°{}, lon={:.0f}°{}".format(ARMC,self.geo_latitude,s1,self.geo_longitude,s2)
        self.id_text.set_text(txt)
        self.south = True if self.geo_latitude<0 else False

        alpha_main_2=0.8
        self.alpha_main_2=alpha_main_2
        
        #===== Celestial Equator
   
        self.geo_latitude = geo_latitude
        self.geo_lat = np.radians(self.geo_latitude)
        geo_lat = self.geo_lat

        rotation = np.pi/2 + geo_lat
        self.rotation=rotation
        self.eq_rot_ang=rotation

        v_rot = self.Rodrigues_rotation(v,k,rotation)
        self.equator_rot=v_rot

        x,y,z=self.equator_rot
        x2= np.sin(φ) + x * np.cos(φ)
        y2= y * np.cos(φ)
        z2= z * np.cos(φ)
        '''
        #==== solid
        id_,=self.ax.plot(x2,y2,z2 ,color="#700000", linestyle = "solid" ,picker=2) #'dashed'
        #id_=id(id_)
        self.ids[id(id_)] =[[x2[18],y2[18],z2[18]],"Celestial Equator"] #"v_rot+π/2"
        self.eq_circl=id_
        '''
        color_equat="#700000"
        id_1=id_2=0        

        φ_1 = np.linspace(0, np.pi, data_pts)
        x2, y2, z2 = self.circl_vect(self.equator_rot,k,φ_1)
        eq_1 = [x2[0],y2[0],z2[0]]
        self.eq_circl_1, = self.ax.plot(x2, y2, z2, color=color_equat, picker=main_circles_picker, linewidth=1, linestyle = "solid", alpha=self.alpha_main_2)

        φ_2 = np.linspace(np.pi,2*np.pi, data_pts)
        x2b, y2b, z2b = self.circl_vect(self.equator_rot,k,φ_2)
        eq_2 = [x2b[0],y2b[0],z2b[0]]
        self.eq_circl_2, = self.ax.plot(x2b, y2b, z2b, color=color_equat, picker=main_circles_picker, linewidth=1, linestyle = "dashed", alpha=self.alpha_main_2)


        self.ids[id(self.eq_circl_1)] =[[x2[13],y2[13],z2[13]],"Celestial Equator"]
        self.ids[id(self.eq_circl_2)] =[self.ids[id(self.eq_circl_1)][0],"Celestial Equator"]  

        self.equat_ids.append(self.eq_circl_1);  self.equat_ids.append(self.eq_circl_2)

        #====== ARMC
        ARMC_= eq_1
        ARMC_= np.multiply(1.05,ARMC_)
        self.armc_id, = self.ax.plot(*ARMC_,c="#555555",marker="$ARMC$",markersize=12,picker=4)  #point
        self.equat_ids.append(self.armc_id)
        self.ids[id(self.armc_id)] =[eq_1,"ARMC"]
        self.armc_id.set_visible(False)
        ARMC=np.radians(ARMC)
        self.v_equinox_ang=ARMC

        #------- 2nd point on rotated circle oblique
        self.v_equinox_ang=ARMC
        φ2=-ARMC
        x12, y12, z12 = self.circl_vect(self.equator_rot,k,φ2)
        self.v_equinox=[x12,y12,z12] # vernal equinox
        self.a_equinox=[-x12,-y12,-z12]
        self.equinox_id, = self.ax.plot(*self.v_equinox, c="#555", marker="o", markersize=2, zorder=3, alpha=1);
        self.ecl_ids.append(self.equinox_id)

        #====== poleN
        rot=self.rotation
        v_rot=self.equator_rot
        color_4="#444444"
        rotation = self.eq_rot_ang + np.pi/2

        v_rot1 = self.Rodrigues_rotation(v,k,rotation)
        self.poleS=v_rot1
        v_rot2=-v_rot1
        self.poleN=v_rot2

        self.poleN_id, =self.ax.plot(*self.poleN,c=color_4,marker="$N$",picker=5, zorder=2) #point
        self.ids[id(self.poleN_id)] =[self.poleN,"North Pole"] #"v_rot-π/2"
        self.equat_ids.append(self.poleN_id)

        self.poleS_id, =self.ax.plot(*self.poleS,c=color_4, marker="$S$",picker=5, zorder=2) #point
        self.ids[id(self.poleS_id)] =[self.poleS,"South Pole"] #"v_rot+π/2"
        self.equat_ids.append(self.poleS_id)

        poleN_θ_hor=np.arccos(self.poleN[2])
        self.poleN_elev=np.degrees(poleN_θ_hor)  
        

        #====== Ecliptic
        φ1 = -ARMC - np.pi/2
        x13, y13, z13 = self.circl_vect(self.equator_rot,k,φ1)
        self.v_rot4=[x13,y13,z13]

        #ε=23.43  
        k1=np.array(self.v_equinox) 
        v1=np.array(self.v_rot4)
        ε=np.radians(self.ε)
        rotation = ε
        v_rot3 = self.Rodrigues_rotation(v1,k1,rotation)
        self.ecliptic_rot=v_rot3
        v2= -self.ecliptic_rot

        φ4=np.arctan(-k1[2]/v2[2])
        x3t= v2[0] * np.sin(φ4) + k1[0] * np.cos(φ4)
        if x3t<0:
            φ4 = φ4 + np.pi

        φ4=norm_r(φ4)
        self.asc_lon=φ4

        φ3 = np.arctan(-v2[0]/k1[0]) if k1[0] != 0 else np.pi/2

        if norm_r(ARMC)< np.pi:
            φ3=np.pi/2 - φ3
            ecl_st=0 + φ3 #ecl_start
        else:
            φ3= - np.pi/2 - φ3
            ecl_st=0 + φ3
            
        self.ecl_start=np.degrees(φ3)
        φ_1 = np.linspace(ecl_st , ecl_st + np.pi, data_pts)
        x3, y3, z3 = self.circl_vect(k1, v2, φ_1)
        self.ecl_circl_1, = self.ax.plot(x3,y3,z3 ,color=color_ecl, picker=main_circles_picker, linestyle = "solid", alpha=alpha_main_2)
        self.ids[id(self.ecl_circl_1)] =[[x3[15],y3[15],z3[15]],"Ecliptic"]
        

        φ_2 = np.linspace(ecl_st + np.pi, ecl_st + 2*np.pi, data_pts)
        x3, y3, z3 = self.circl_vect(k1, v2, φ_2)
        self.ecl_circl_2, = self.ax.plot(x3,y3,z3 ,color=color_ecl, picker=main_circles_picker, linestyle = "dashed", alpha=alpha_main_2)
        self.ids[id(self.ecl_circl_2)] =[self.ids[id(self.ecl_circl_1)][0],"Ecliptic"]
   
        r1=1.07
        x3p, y3p, z3p = self.circl_vect(k1, v2, φ3, r1)
        self.v_MC=self.circl_vect(k1, v2, φ3)

        self.mc_id,= self.ax.plot(x3p,y3p,z3p,c="#444444",marker="$MC$",markersize=10,picker=4, zorder=2); #point
        x3, y3, z3 = self.circl_vect(k1, v2, φ3)
        lon_=f'Medium Coeli: lon={round(self.planets_data["MC"]["ecl"][0],2)}°'
        self.ids[id(self.mc_id)] =[[x3, y3, z3],lon_]
        self.ecl_ids.append(self.mc_id)
        self.mc_id.set_visible(False)


        #====== Asc ========
        x13, y13, z13 = self.circl_vect(k1, v2, φ4)
        self.asc_id2, =self.ax.plot(x13,y13,z13, c="#333", marker="o",  markersize=3, zorder=2, alpha=0.6);#point
        self.ecl_ids.append(self.asc_id2)
        asc=[x13,y13,z13]
        self.v_asc=asc

        r1=1.07
        x3p, y3p, z3p = self.circl_vect(k1, v2, φ4, r1)
        asc_t=[x3p,y3p,z3p-0.03]
        self.asc_id,=self.ax.plot(*asc_t, c="#555555",marker="$Asc$",markersize=10,picker=5, zorder=2) ;#point

        self.asc_id2.set_visible(False)
        self.asc_id.set_visible(False)
        self.ecl_ids.append(self.asc_id)


        self.Asc_φ_hor=np.arccos(self.v_asc[0])
        if self.v_asc[1]<0: self.Asc_φ_hor = -abs(self.Asc_φ_hor)
        self.Asc_φ_hor = norm_r(self.Asc_φ_hor)


        '''
        #=== solid
        x3= k1[0] * np.sin(φ) + self.ecliptic_rot[0] * np.cos(φ)
        y3= k1[1] * np.sin(φ) + self.ecliptic_rot[1] * np.cos(φ)
        z3= k1[2] * np.sin(φ) + self.ecliptic_rot[2] * np.cos(φ)
        id_,=self.ax.plot(x3,y3,z3 ,color = color_ecl, linestyle = "solid" ,picker=2) #'dashed'
        self.ids[id(id_)] =[[x2[18],y2[18],z2[18]],"Ecliptic"] 
        self.ecl_circle=id_
        '''

        #============= Ecliptic pole 

        rotation = -np.pi/2
        k1=np.array(self.v_equinox) 
        v1=np.array(self.ecliptic_rot)

        v_rot6 = self.Rodrigues_rotation(v1,k1,rotation)
        self.poleN_ecl = v_rot6
        self.poleN_ecl_id, =self.ax.plot(*self.poleN_ecl,c=color_ecl, marker="$n$",markersize=5,picker=5, zorder=2, alpha=0.8)
        self.poleS_ecl=-self.poleN_ecl; 
        self.poleS_ecl_id, =self.ax.plot(*self.poleS_ecl,c=color_ecl, marker="$s$",markersize=5,picker=5, zorder=2, alpha=0.8)

        self.ids[id(self.poleN_ecl_id)] =[self.poleN_ecl,"Ecliptic North Pole"]
        self.ecl_ids.append(self.poleN_ecl_id)
        self.ids[id(self.poleS_ecl_id)] =[self.poleS_ecl,"Ecliptic South Pole"]
        self.ecl_ids.append(self.poleS_ecl_id)


        poleN_ecl_θ_hor=np.arccos(self.poleN_ecl[2])
        pole_ecl_elev= np.pi/2 - poleN_ecl_θ_hor
        self.pole_ecl_elev=np.degrees(pole_ecl_elev)

        self.plot_ecliptic_scale()
        self.plot_equator_scale()


    def plot_Equator_Ecliptic_next(self):
        ARMC=self.planets_data["MC"]["eq"][0]
        ARMC=float(ARMC)
        ARMC=norm_(ARMC)
        self.ARMC=ARMC
        
        φ = self.ψ
        self.k = k = np.array([1, 0, 0])
        self.v = v = np.array([0, 1, 0])
        geo_latitude=self.geo_latitude

        s1 = "S" if self.geo_latitude<0 else "N"
        s2 = "W" if self.geo_longitude<0 else "E"
        txt="ARMC={:.0f}°, lat={:.0f}°{}, lon={:.0f}°{}".format(ARMC,self.geo_latitude,s1,self.geo_longitude,s2)
        self.id_text.set_text(txt)
        self.south = True if self.geo_latitude<0 else False
        
    #===== Celestial Equator
   
        self.geo_latitude = geo_latitude
        self.geo_lat = np.radians(self.geo_latitude)
        geo_lat = self.geo_lat

        rotation = np.pi/2 + geo_lat
        self.rotation=rotation
        self.eq_rot_ang=rotation

        v_rot = self.Rodrigues_rotation(v,k,rotation)
        self.equator_rot=v_rot

        x,y,z=self.equator_rot
        x2= np.sin(φ) + x * np.cos(φ)
        y2= y * np.cos(φ)
        z2= z * np.cos(φ)

        color_equat="#700000"
        id_1=id_2=0        

        φ_1 = np.linspace(0, np.pi, 50)
        x2, y2, z2 = self.circl_vect(self.equator_rot,k,φ_1)
        eq_1 = [x2[0],y2[0],z2[0]]
        self.eq_circl_1.set_data_3d(x2, y2, z2)

        φ_2 = np.linspace(np.pi,2*np.pi, 50)
        x2b, y2b, z2b = self.circl_vect(self.equator_rot,k,φ_2)
        eq_2 = [x2b[0],y2b[0],z2b[0]]
    
        self.eq_circl_2.set_data_3d(x2b, y2b, z2b)

        #====== ARMC
        ARMC_= eq_1
        ARMC_= np.multiply(1.05,ARMC_)
        self.armc_id.set_data_3d(*ARMC_)
        ARMC=np.radians(ARMC)
        self.v_equinox_ang=ARMC

        self.v_equinox_ang=ARMC
        φ2=-ARMC
        x12, y12, z12 = self.circl_vect(self.equator_rot,k,φ2)
        self.v_equinox=[x12,y12,z12]
        self.a_equinox=[-x12,-y12,-z12]
        self.equinox_id.set_data_3d(x12, y12, z12)

        #====== poleN
        rot=self.rotation
        v_rot=self.equator_rot
        color_4="#444444"

        rotation = self.eq_rot_ang + np.pi/2
        v_rot1 = self.Rodrigues_rotation(v,k,rotation)
        self.poleS=v_rot1
        v_rot2=-v_rot1
        self.poleN=v_rot2

        self.poleN_id.set_data_3d(*self.poleN)
        self.ids[id(self.poleN_id)] =[self.poleN,"North Pole"]

        self.poleS_id.set_data_3d(*self.poleS)
        self.ids[id(self.poleS_id)] =[self.poleS,"South Pole"]
        poleN_θ_hor=np.arccos(self.poleN[2])
        self.poleN_elev=np.degrees(poleN_θ_hor)  

        #====== Ecliptic 

        φ1 = -ARMC - np.pi/2
        x13, y13, z13 = self.circl_vect(self.equator_rot,k,φ1)
        self.v_rot4=[x13,y13,z13]
       
        k1=np.array(self.v_equinox) 
        v1=np.array(self.v_rot4)
        ε=np.radians(self.ε)
        rotation = ε
        v_rot3 = self.Rodrigues_rotation(v1,k1,rotation)
        self.ecliptic_rot=v_rot3
        v2= -self.ecliptic_rot

        φ4=np.arctan(-k1[2]/v2[2])
        x3t= v2[0] * np.sin(φ4) + k1[0] * np.cos(φ4)
        if x3t<0:
            φ4 = φ4 + np.pi

        φ4=norm_r(φ4)
        self.asc_lon=φ4

        φ3 = np.arctan(-v2[0]/k1[0]) if k1[0] != 0 else np.pi/2

        if norm_r(ARMC)< np.pi:
            φ3=np.pi/2 - φ3
            ecl_st=0 + φ3 #ecl_start
        else:
            φ3= - np.pi/2 - φ3
            ecl_st=0 + φ3

        self.ecl_start=np.degrees(φ3)
        φ_1 = np.linspace(ecl_st , ecl_st + np.pi, 50)
        x3, y3, z3 = self.circl_vect(k1, v2, φ_1)
        self.ecl_circl_1.set_data_3d(x3, y3, z3)
        φ_2 = np.linspace(ecl_st + np.pi, ecl_st + 2*np.pi, 50)
        x3, y3, z3 = self.circl_vect(k1, v2, φ_2)
        self.ecl_circl_2.set_data_3d(x3, y3, z3)


        #====== MC ========
        r1=1.07

        x3, y3, z3 = self.circl_vect(k1, v2, φ3, r1)
        self.v_MC=self.circl_vect(k1, v2, φ3)
        self.mc_id.set_data_3d(x3, y3, z3)

        x3, y3, z3 = self.circl_vect(k1, v2, φ3)
        lon_=f'Medium Coeli: lon={round(self.planets_data["MC"]["ecl"][0],2)}°'
        self.ids[id(self.mc_id)] =[[x3, y3, z3],lon_]

        #====== Asc ========
        r1=1.07

        x3p, y3p, z3p = self.circl_vect(k1, v2, φ4, r1)
        asc_t=[x3p,y3p,z3p-0.03]
        self.asc_id.set_data_3d(*asc_t)


        x13, y13, z13 = self.circl_vect(k1, v2, φ4)
        asc=[x13,y13,z13]
        self.v_asc=asc
        self.asc_id2.set_data_3d(x13, y13, z13)

        self.Asc_φ_hor=np.arccos(self.v_asc[0])
        if self.v_asc[1]<0: self.Asc_φ_hor = -abs(self.Asc_φ_hor)
        self.Asc_φ_hor = norm_r(self.Asc_φ_hor)
 
        #============= Ecliptic pole 
        rotation = -np.pi/2
        k1=np.array(self.v_equinox) 
        v1=np.array(self.ecliptic_rot)
        v_rot6 = self.Rodrigues_rotation(v1,k1,rotation)
        self.poleN_ecl = v_rot6
        self.poleS_ecl=-self.poleN_ecl; 
        self.poleN_ecl_id.set_data_3d(*self.poleN_ecl)
        self.poleS_ecl_id.set_data_3d(*self.poleS_ecl)

        poleN_ecl_θ_hor=np.arccos(self.poleN_ecl[2])
        pole_ecl_elev= np.pi/2 - poleN_ecl_θ_hor
        self.pole_ecl_elev=np.degrees(pole_ecl_elev)

        self.ids[id(self.poleN_ecl_id)] =[self.poleN_ecl,"Ecliptic North Pole"]
        self.ids[id(self.poleS_ecl_id)] =[self.poleS_ecl,"Ecliptic South Pole"]
        
        self.plot_ecliptic_scale()
        self.plot_equator_scale()


    def plot_meridian(self):  
        color_="#666666"      
        alpha_main=self.alpha_main
        θ=self.ψ
        y2=np.sin(θ)
        z2=np.cos(θ)
        x2=np.zeros(np.size(y2))
        id_,=self.ax.plot(x2,y2,z2 ,color=color_, linestyle = (0, (1, 2,1,3)), alpha=alpha_main, picker=main_circles_picker, zorder=0)
        self.ids[id(id_)] =[[x2[6],y2[6],z2[6]],"Meridian"]
        self.mer_circle=id_

    def plot_next_prev(self, seconds=0, minutes=0, hours=0):
        self.clear_ann()
        self.id_text_2.set_text("")
        tz_=self.data["tz"]
        t_obj=add_days(self.timestamp, seconds=seconds, minutes=minutes, hours=hours,tz_=tz_)
        date_t= t_obj["date_utc"];  time_t= t_obj["time_utc"]
        date_t_loc= t_obj["date_loc"];  time_t_loc= t_obj["time_loc"]  
        self.timestamp=t_obj["timestamp"]

        self.date_utc = date_t
        self.time_utc = time_t

        latitude = float(self.data["lat"])
        longitude = float(self.data["lon"])
        self.geo_latitude=latitude
        self.planets_data = calc_.get_planets_data(self.date_utc, self.time_utc, latitude, longitude)

        self.plot_Equator_Ecliptic_next()
        self.plot_zodiac_next()
        self.plot_planets_next(self.planets_data)

        time_utc = " UTC: {}, {} ".format(self.date_utc, self.time_utc)
        time_loc = "{: >10}, {: >8}".format(date_t_loc, time_t_loc)
        time_loc= "{: ^21}".format(time_loc)

        self.id_text_time.set_text(time_loc)
        self.id_text_time2.set_text(time_utc)

        self.legend_updt()


    def plot_planets(self, planets_data):
        for i, pl in enumerate(planets_data):
            if pl not in c.planets.keys():continue
            pl_RA=planets_data[pl]['eq'][0]
            pl_decl=planets_data[pl]['eq'][1]
            lon=planets_data[pl]['ecl'][0]
            lat=planets_data[pl]['ecl'][1]
            sym = "$" + c.planets[pl] + "$"
            txt="{}: RA={:.2f}°, decl={:.2f}°, lon={:.1f}°, lat={:.1f}°".format(pl, pl_RA, pl_decl, lon, lat)
            self.plot_planet_equat(pl_RA ,pl_decl, lon, lat ,rad=False,meridian=False, name=pl,sym=sym, text=txt)

    def plot_planet_equat(self, RA, decl, lon, lat, rad=False, meridian=False, parallel=False, name="",sym ="",text=""):
        pl_RA=np.radians(RA) if rad==False else RA
        pl_decl=np.radians(decl) if rad==False else decl
        rotation=pl_RA
        φ=self.ψ
        θ=self.ψ
        k=self.k
        k2 = self.poleN;
        v2 = self.equator_rot;   
   
        color_pl2=pl_colors[name]
        color_pl1=pl_colors[name]
        color_dot="#1C0367"
        color_dot=color_pl1

        rotation=rotation - self.v_equinox_ang
        v_rot5 = self.Rodrigues_rotation(v2,k2,rotation)

        v_mer = self.circl_vect(v_rot5,k2,φ)
        style_=(0, (1,4,1,6))        
        color_oran="#F38600"
        color_yel="#FFCD00"
        color_mer_par=color_pl1
        style_= (0, (1,3,)) if name in ["Sun","Moon","Jupiter"] else style_
        alpha_= 0.8 if name in ["Sun","Moon","Jupiter"] else 0.6 #fix light color contrast
        id_Mer, = self.ax.plot(*v_mer ,color=color_mer_par, linestyle=style_, linewidth=1,alpha=alpha_, picker=2)
        if meridian==False:
            id_Mer.set_visible(False)

        id_Mer_nat, = self.ax.plot(*v_mer ,color=color_mer_par, linestyle=(0, (2,4,3,4)), linewidth=1,alpha=alpha_, picker=2)
        id_Mer_nat.set_visible(False)
            
        shift=np.sin(pl_decl)
        data=self.plot_parallel(shift,color_=color_mer_par, style_=style_, alpha=alpha_) 
        id_Par=data[0]
        if parallel==False:
            id_Par.set_visible(False)

        φ2 = pl_RA  - self.v_equinox_ang
        φ2=norm_r(φ2)
        pl_φ_eq=φ2
        v_RA = self.circl_vect(self.equator_rot,k,φ2)

        id_pt_Eq, = self.ax.plot(*v_RA, c=color_dot, marker="o", markersize=2, picker=4, zorder=3)
        id_pt_Eq.set_visible(False)

        pl_declination=pl_decl
        θ2=pl_decl
        v_pl = self.circl_vect(v_RA,k2,θ2)
        pl_θ_hor=np.arccos(v_pl[2])

        #-- planet dot        
        if "Node" in name:
            id_pl, =self.ax.plot(*v_pl, c=color_pl1, marker="o", picker=5, markersize=2,zorder=6) #onpick
        else:
            id_pl, =self.ax.plot(*v_pl, c=color_pl1, marker="o", picker=5, markersize=4,zorder=6) #onpick

        arr=[-0.05,0.05]
        shift=0.07
        v_pl_t=np.add(v_pl,shift)

        if "Node" in name:
            id_t =self.ax.text(*v_pl_t,s=sym,fontsize=11,c=color_pl2, label=name, fontweight=800, picker=5,bbox=dict(boxstyle="round",edgecolor=("#FFF"),facecolor=("#FFF"),pad=0.0, alpha=0.0), alpha=1.0, zorder=2)
        elif name in ["Sun","Moon"]:
            id_t =self.ax.text(*v_pl_t,s=sym,fontsize=17,c=color_pl2, label=name, fontweight=800, picker=5,bbox=dict(boxstyle="round",edgecolor=("#FFF"),facecolor=("#FFF"),pad=0.0, alpha=0.0), alpha=1.0, zorder=4)
        else:
            id_t =self.ax.text(*v_pl_t,s=sym,fontsize=16,c=color_pl2, label=name, fontweight=800, picker=5,bbox=dict(boxstyle="round",edgecolor=("#FFF"),facecolor=("#FFF"),pad=0.0, alpha=0.0), alpha=1.0, zorder=4)

        v_hor=[v_pl[0],v_pl[1],0]
        v_hor=v_hor/np.linalg.norm(v_hor) 
        id_pt_Hor, = self.ax.plot(*v_hor,c=color_dot,marker="o", markersize=2, picker=4, zorder=7)  
        id_pt_Hor.set_visible(False)

        pl_φ_hor = np.arccos(v_hor[0]); 
        if v_hor[1] < 0:
            pl_φ_hor = 2*np.pi - pl_φ_hor

        azimuth = 2*np.pi - pl_φ_hor + np.pi/2
        azimuth = norm_r(azimuth)

        pl_θ_hor= np.arccos(v_pl[2])
        pl_alt_hor= np.pi/2 - pl_θ_hor
        #pl_alt_hor = rd(pl_alt_hor)

        #------ planet's proportionate horizon
        #tan(a)/tan(A)=sin(b) # Napier
        #np.tan(np.pi/2 - θ_pl)/np.tan(α)=np.sin(np.pi/2 - φ_pl) -> α= np.arctan(np.tan(np.pi/2 - θ_pl)/np.sin(np.pi/2 - φ_pl))
        #np.tan(np.pi/2 - θ_proj_hor)/np.tan(α)=np.sin(np.pi/2)
        #np.tan(np.pi/2 - θ_proj_hor)=np.tan(α) -> np.pi/2 - θ_proj_hor =α -> θ_proj_hor =np.pi/2 - α

        α = np.arctan(np.tan(np.pi/2 - pl_θ_hor)/np.sin(np.pi/2 - pl_φ_hor)) # α = proportionate horizon's inclination
        k=self.k
        w=self.w
        if v_pl[0]<0: α = α + np.pi
        v_rot8 = self.Rodrigues_rotation(k, w, α)        
        φ2 = self.ψ2
        x2,y2,z2 = self.circl_vect(v_rot8, w, φ2)
        id_proj_hor,=self.ax.plot(x2,y2,z2 ,color=color_mer_par, linestyle = style_, linewidth=1, alpha=alpha_, picker=1, zorder=1)
        id_proj_hor.set_visible(False)

        id_proj_hor_nat,=self.ax.plot(x2,y2,z2 ,color=color_mer_par, linestyle = (0, (2,4,3,4)), linewidth=1, alpha=alpha_, picker=1, zorder=1)
        id_proj_hor_nat.set_visible(False)
       
        k2=np.array(self.v_equinox) 
        v2= -self.ecliptic_rot 
        φ2=np.radians(lon) 
        v_ecl = self.circl_vect(k2,v2,φ2)
        id_pt_Ecl, = self.ax.plot(*v_ecl,c=color_dot,marker="o", markersize=2, picker=4, zorder=5);
        id_pt_Ecl.set_visible(False)
        pl_φ_ecl=lon

        #----- help_lines
        color_lin="#0D5022"

        ve_=self.line_vect(v_RA, v_pl)
        id_l_eq,=self.ax.plot(*ve_ ,color=color_lin, linestyle = (0, (1,2,1,3)), lw=1, alpha=0.6, picker=1)
        id_l_eq.set_visible(False)
        
        ve_=self.line_vect(v_hor, v_pl)
        id_l_ho,=self.ax.plot(*ve_ ,color=color_lin, linestyle = (0, (1,2,1,3)), lw=1, alpha=0.6, picker=1)
        id_l_ho.set_visible(False)

        ve_=self.line_vect(v_ecl, v_pl)
        id_l_ecl,=self.ax.plot(*ve_ ,color=color_lin, linestyle = (0, (1,2,1,3)), lw=1, alpha=0.6, picker=1)
        id_l_ecl.set_visible(False)

        self.planets_obj[id_t]={}         
        self.planets_obj[id_t]["id_pl"]=id_pl
        self.planets_obj[id_t]["id_Mer"]=id_Mer 
        self.planets_obj[id_t]["id_Mer_nat"]=id_Mer_nat
        self.planets_obj[id_t]["id_Par"]=id_Par 
        self.planets_obj[id_t]["id_proj_hor"]=id_proj_hor 
        self.planets_obj[id_t]["id_proj_hor_nat"]=id_proj_hor_nat 
        self.planets_obj[id_t]["name"]=name
        self.planets_obj[id_t]["txt"]=text

        self.planets_obj[id_t]["id_pt_Eq"] = (id_pt_Eq, rd(norm_r(pl_φ_eq + self.v_equinox_ang)), v_RA, rd(pl_φ_eq)) 
        self.planets_obj[id_t]["id_pt_Hor"] = (id_pt_Hor, rd(pl_φ_hor), v_hor, rd(azimuth), rd(pl_alt_hor))
        self.planets_obj[id_t]["id_pt_Ecl"] = (id_pt_Ecl, round(pl_φ_ecl,1), v_ecl)

        self.planets_obj[id_t]["id_l_eq"]=id_l_eq
        self.planets_obj[id_t]["id_l_ho"]=id_l_ho
        self.planets_obj[id_t]["id_l_ecl"]=id_l_ecl

        self.planets_obj[id_t]["show_mer_par"]=0

        
        self.planets_ids[name]={}
        self.planets_ids[name]["id_pl"]=id_pl
        self.planets_ids[name]["id_t"]=id_t
        self.planets_ids[name]["id_Mer"]=id_Mer
        self.planets_ids[name]["id_Mer_nat"]=id_Mer_nat
        self.planets_ids[name]["id_Par"]=id_Par
        self.planets_ids[name]["id_proj_hor"]=id_proj_hor 
        self.planets_ids[name]["id_proj_hor_nat"]=id_proj_hor_nat
        self.planets_ids[name]["id_pt_Eq"]=id_pt_Eq
        self.planets_ids[name]["id_pt_Hor"]=id_pt_Hor
        self.planets_ids[name]["id_pt_Ecl"]=id_pt_Ecl
        self.planets_ids[name]["id_l_eq"]=id_l_eq
        self.planets_ids[name]["id_l_ho"]=id_l_ho
        self.planets_ids[name]["id_l_ecl"]=id_l_ecl


    def plot_planets_next(self, planets_data):
        for i, pl in enumerate(planets_data):
            if pl not in c.planets.keys():continue
            pl_RA=planets_data[pl]['eq'][0]
            pl_decl=planets_data[pl]['eq'][1]
            lon=planets_data[pl]['ecl'][0]
            lat=planets_data[pl]['ecl'][1]
            txt="{}: RA={:.2f}°, decl={:.2f}°, lon={:.1f}°, lat={:.1f}°".format(pl, pl_RA, pl_decl, lon, lat)
            self.plot_planet_equat_next(pl_RA ,pl_decl, lon, lat ,rad=False,meridian=False, name=pl, text=txt) 

    def plot_planet_equat_next(self, RA, decl, lon, lat, rad=False, meridian=False, parallel=False, name="", text=""):
        pl_RA=np.radians(RA) if rad==False else RA
        pl_decl=np.radians(decl) if rad==False else decl
        rotation=pl_RA
        φ=self.ψ
        θ=self.ψ
        k=self.k
        j=np.array([0,0,1])
        k2 = self.poleN;
        v2 = self.equator_rot;   

        color_pl2=pl_colors[name]
        color_pl1=pl_colors[name]

        rotation=rotation - self.v_equinox_ang
        v_rot5 = self.Rodrigues_rotation(v2,k2,rotation)
        
        v_mer = self.circl_vect(v_rot5,k2,φ)
        style_="dashed"
        color_="#543E17"   
        self.planets_ids[name]["id_Mer"].set_data_3d(*v_mer)

        shift=np.sin(pl_decl)
        data=self.plot_parallel(shift, redraw=False) 
        id_Par=data[0]
        v_par=data[1]
        self.planets_ids[name]["id_Par"].set_data_3d(*v_par) 

        φ2 = pl_RA - self.v_equinox_ang
        φ2=norm_r(φ2)
        pl_φ_eq=φ2

        v_RA = self.circl_vect(self.equator_rot,k,φ2)

        self.planets_ids[name]["id_pt_Eq"].set_data_3d(*v_RA)
 
        pl_declination=pl_decl
        θ2=pl_decl
        v_pl = self.circl_vect(v_RA,k2,θ2)

        pl_θ_hor=np.arccos(v_pl[2])

        self.planets_ids[name]["id_pl"].set_data_3d(*v_pl) 
        arr=[-0.05,0.05]
        shift=0.07
        v_vert=np.cross(v_pl,j)
        v_vert=v_vert/np.linalg.norm(v_vert)
        v_pl_t=np.add(v_pl,shift)

        self.planets_ids[name]["id_t"].set_position_3d(v_pl_t);


        v_hor=[v_pl[0],v_pl[1],0]
        v_hor=v_hor/np.linalg.norm(v_hor) 
        self.planets_ids[name]["id_pt_Hor"].set_data_3d(*v_hor)

        pl_φ_hor= np.arccos(v_hor[0]); 

        if v_hor[1] < 0:
            pl_φ_hor = 2*np.pi - pl_φ_hor

        azimuth = 2*np.pi - pl_φ_hor + np.pi/2
        azimuth = norm_r(azimuth)

        pl_θ_hor= np.arccos(v_pl[2])
        pl_alt_hor= np.pi/2 - pl_θ_hor

        α = np.arctan(np.tan(np.pi/2 - pl_θ_hor)/np.sin(np.pi/2 - pl_φ_hor)) # α = proportionate horizon's inclination
        k=self.k
        w=self.w
        v_rot8 = self.Rodrigues_rotation(k, w, α)
        φ2 = self.ψ2
        x2,y2,z2 = self.circl_vect(v_rot8, w, φ2)
        self.planets_ids[name]["id_proj_hor"].set_data_3d(x2,y2,z2)

        k2=np.array(self.v_equinox) 
        v2= -self.ecliptic_rot 
        φ2=np.radians(lon) 
        v_ecl = self.circl_vect(k2,v2,φ2)
        self.planets_ids[name]["id_pt_Ecl"].set_data_3d(*v_ecl)
        pl_φ_ecl=lon

        #----- help_lines
        ve_=self.line_vect(v_RA, v_pl)
        self.planets_ids[name]["id_l_eq"].set_data_3d(*ve_)

        ve_=self.line_vect(v_hor, v_pl)
        self.planets_ids[name]["id_l_ho"].set_data_3d(*ve_)
        
        ve_=self.line_vect(v_ecl, v_pl)
        self.planets_ids[name]["id_l_ecl"].set_data_3d(*ve_)

        id_l_ecl=0
        id_t=self.planets_ids[name]["id_t"]
        id_pt_Eq=self.planets_obj[id_t]["id_pt_Eq"][0]
        id_pt_Hor=self.planets_obj[id_t]["id_pt_Hor"][0]
        id_pt_Ecl=self.planets_obj[id_t]["id_pt_Ecl"][0]
        self.planets_obj[id_t]["id_pt_Eq"] = (id_pt_Eq, rd(norm_r(pl_φ_eq + self.v_equinox_ang)), v_RA, rd(pl_φ_eq)) 
        self.planets_obj[id_t]["id_pt_Hor"] = (id_pt_Hor, rd(pl_φ_hor), v_hor, rd(azimuth), rd(pl_alt_hor))
        self.planets_obj[id_t]["id_pt_Ecl"] = (id_pt_Ecl, round(pl_φ_ecl,1), v_ecl)
        self.planets_obj[id_t]["txt"]=text

    def plot_zodiac(self):        
        k2=np.array(self.v_equinox) 
        v2= -self.ecliptic_rot
        ψ=0;i=1
        while ψ < 2*np.pi:
            v_ = self.circl_vect(k2,v2,ψ)
            v_1=np.multiply(v_, 1.01)
            v_2=np.multiply(v_, 0.99)
            data=np.array([v_1,v_2])
            id_1, = self.ax.plot(*v_, c=color_ecl_zod, marker="D", markersize=2, picker=3, zorder=2)

            name=zodiac[i]
            sym =zodiac2[i]
            self.zodiac_obj[id_1] = (name, sym, v_)

            sym = "$" + zodiac2[i] + "$"
            v_s = self.circl_vect(k2, v2, ψ + np.pi/12)
            v_s=np.multiply(v_s, 1.05)
            id_2, = self.ax.plot(*v_s, c="#4E4C25", marker=sym, markersize=10, picker=3, zorder=0, alpha=0.2)
            self.ecl_ids.append(id_2)

            self.zodiac_ids[i]={}
            self.zodiac_ids[i]["dot"]=id_1
            self.zodiac_ids[i]["text"]=id_2

            ψ+=np.pi/6
            i+=1

    def plot_zodiac_next(self):
        k2=np.array(self.v_equinox) 
        v2= -self.ecliptic_rot
        ψ=0;i=1
        while ψ < 2*np.pi:
            v_ = self.circl_vect(k2,v2,ψ)
            v_1=np.multiply(v_, 1.01)
            v_2=np.multiply(v_, 0.99)
            data=np.array([v_1,v_2])
            self.zodiac_ids[i]["dot"].set_data_3d(*v_)             
            tup=self.zodiac_obj[self.zodiac_ids[i]["dot"]] 
            self.zodiac_obj[self.zodiac_ids[i]["dot"]]=(tup[1],tup[0],v_)
            v_s = self.circl_vect(k2, v2, ψ + np.pi/12)
            v_s=np.multiply(v_s, 1.05)
            self.zodiac_ids[i]["text"].set_data_3d(*v_s)
            
            ψ+=np.pi/6
            i+=1

    def plot_ecliptic_scale(self): 
        k2=np.array(self.v_equinox) 
        v2= -self.ecliptic_rot
        ψ=0;i=1
        first=True if len(self.ecliptic_scale)==0 else False
        while ψ < 360:
            v_ = self.circl_vect(k2,v2,np.radians(ψ))
            if first:
                id_, = self.ax.plot(*v_, c="#333", marker="o", markersize=1)#,zorder=1
                id_t=self.ax.text(*v_,s=str(ψ),fontsize=6,c="#333", fontweight=400, picker=5, alpha=self.alpha_main, zorder=0)
                self.ecliptic_scale[i]=(id_,id_t)
                id_.set_visible(False)
                id_t.set_visible(False)
            else:
                self.ecliptic_scale[i][0].set_data_3d(*v_)
                self.ecliptic_scale[i][1].set_position_3d(v_)
            ψ+=10
            i+=1

    def plot_equator_scale(self): 
        k2=np.array(self.v_equinox) 
        v2= -self.ecliptic_rot
        ψ=0;i=1
        first=True if len(self.equator_scale)==0 else False
        while ψ < 360:
            φ2 = np.radians(ψ)  - self.v_equinox_ang
            φ2=norm_r(φ2)
            v_ = self.circl_vect(self.equator_rot,self.k,φ2)   
            if first:
                id_, = self.ax.plot(*v_, c="#333", marker="o", markersize=1)#,zorder=1
                id_t=self.ax.text(*v_,s=str(ψ),fontsize=6,c="#333", fontweight=400, picker=5, alpha=self.alpha_main, zorder=0)
                self.equator_scale[i]=(id_,id_t)
                id_.set_visible(False)
                id_t.set_visible(False)
            else:
                self.equator_scale[i][0].set_data_3d(*v_)
                self.equator_scale[i][1].set_position_3d(v_)
            ψ+=10
            i+=1


    def plot_circle_scale(self, circle):
        k2=np.array([1,0,0])
        v2=np.array([0,1,0])
        if circle=="Horizon":
            obj_scale=self.Hor_scale={}
            k2=np.array([1,0,0])
            v2=np.array([0,1,0])
        elif circle=="Prime vertical":
            obj_scale=self.PV_scale={}
            k2=np.array([1,0,0])
            v2=np.array([0,0,1])

        ψ=0;i=1
        while ψ < 360:
            v_ = self.circl_vect(k2,v2,np.radians(ψ))  
            id_, = self.ax.plot(*v_, c="#333", marker="o", markersize=1)
            id_t=self.ax.text(*v_,s=str(ψ),fontsize=6,c="#333", fontweight=400, picker=5, alpha=self.alpha_main, zorder=0)
            obj_scale[i]=(id_,id_t)
            id_.set_visible(False)
            id_t.set_visible(False)
            ψ+=10
            i+=1

    def draw_projected_horizon(self,rotation=np.pi/6, color_="#2D305C", linestyle_="dashed"):
        k=self.k
        w=np.array([0, -1, 0])
        v_rot6 = self.Rodrigues_rotation(k,w,rotation)
        φ2 = self.ψ2
        x2= w[0] * np.sin(φ2) + v_rot6[0] * np.cos(φ2)
        y2= w[1] * np.sin(φ2) + v_rot6[1] * np.cos(φ2)
        z2= w[2] * np.sin(φ2) + v_rot6[2] * np.cos(φ2)
        id_,=self.ax.plot(x2,y2,z2 ,color=color_, linestyle = linestyle_, linewidth=1)
        self.ids[id(id_)] =[[x2[3],y2[3],z2[0]],"proportionate horizon"] 
        self.proj_horizons.append(id_)
        return id_

    def plot_parallel(self,shift,color_="#CABF6B", alpha=1,style_=(0, (1, 3)), redraw=True):
        frac_poleN=np.multiply(shift,self.poleN) 
        o_=[0,0,0]; o_shift=np.add(o_,frac_poleN)
        c=o_shift
        r=shiftx=np.sqrt(1-np.square(shift))
        v_rot_shift=self.equator_rot; k_shift=self.k
        v_rot_shift= np.multiply(r,v_rot_shift); k_shift= np.multiply(r,k_shift);  
        v = k_shift ; w = v_rot_shift
        φ = self.ψ
        x =c[0] + v[0]*np.cos(φ) + w[0]*np.sin(φ)
        y =c[1] + v[1]*np.cos(φ) + w[1]*np.sin(φ)
        z =c[2] + v[2]*np.cos(φ) + w[2]*np.sin(φ)
        if redraw==True:
            circle_id, =self.ax.plot(x,y,z ,color=color_, linestyle = style_ , alpha=alpha, picker=2, lw=1)
            return (circle_id,[x,y,z]) 
        else:
            return (None,[x,y,z])

    def draw_sphere(self):
        φ = np.linspace(0, 2 * np.pi, 100)
        θ = np.linspace(0, np.pi, 100)
        x = 1 * np.outer(np.cos(φ), np.sin(θ))
        y = 1 * np.outer(np.sin(φ), np.sin(θ))
        z = 1 * np.outer(np.ones(np.size(φ)), np.cos(θ))
        col_viol="#EFE9FF"
        col_yel="#E9E4D1"
        self.sph_alf=0.3
        id_ = self.ax.plot_surface(x, y, z,  rstride=4, cstride=4, color=col_yel, linewidth=0, alpha=self.sph_alf)
        self.sphere_ = id_

    def draw_surface1(self):
        col_viol="#EFE9FF"
        col_yel="#E9E4D1"
        col_='#333'
        self.surface = Circle((0., 0.), 1, color=col_yel,alpha=0.3)
        self.ax.add_patch( self.surface)
        art3d.pathpatch_2d_to_3d( self.surface, z=0, zdir="z")

    def draw_surface(self):
        col_yel1="#E9E4D1"
        col_yel2="#D0CAB2"
        
        angle=90
        theta1, theta2 = angle, angle + 180

        self.surface1 = Wedge((0., 0.), 1, theta1, theta2, fc=col_yel2,alpha=0.3)
        self.surface2 = Wedge((0., 0.), 1, theta2, theta1, fc=col_yel1,alpha=0.3)
        self.ax.add_patch(self.surface1)
        self.ax.add_patch(self.surface2)
        art3d.pathpatch_2d_to_3d(self.surface1, z=0, zdir="z")
        art3d.pathpatch_2d_to_3d(self.surface2, z=0, zdir="z")


    def new_now(self, planets_data, geo_latitude, data):
        self.planets_data=planets_data
        self.geo_latitude=geo_latitude
        self.data=data
        self.timestampIni = self.data["timestamp"]

        self.plot_Equator_Ecliptic_next()
        self.plot_zodiac_next()
        self.plot_planets_next(self.planets_data)

        ARMC=self.planets_data["MC"]["eq"][0]
        self.date_utc = self.data["d_utc"]
        self.time_utc = self.data["t_utc"]
        self.timestamp = self.data["timestamp"]
        self.geo_longitude=float(self.data["lon"])

        s1 = "S" if self.geo_latitude<0 else "N"
        s2 = "W" if self.geo_longitude<0 else "E"
        txt="ARMC={:.0f}°, lat={:.0f}°{}, lon={:.0f}°{}".format(ARMC,self.geo_latitude,s1,self.geo_longitude,s2)
        self.id_text.set_text(txt)

        name = " {} {} ".format(self.data["n"], self.data["ln"])
        time_loc_ = " {}, {}".format(self.data["date_loc"],self.data["time_loc"])
        name = " {} {} ".format(self.data["n"], self.data["ln"])
        time_utc_ = " UTC: {}, {} ".format(self.date_utc, self.time_utc)
        self.id_text_name.set_text(name)
        self.id_text_time.set_text(time_loc_)
        self.id_text_time2.set_text(time_utc_)

        self.legend_updt()

        self.canvas.draw() 


    def Rodrigues_rotation(self, v, k, rotation): #Rodrigues' rotation formula  #rotation about k; v= vector to rotate
        v_rot = v * np.cos(rotation) + np.cross(k, v) * np.sin(rotation) + k * np.dot(k, v) * (1 - np.cos(rotation))
        return v_rot

    def circl_vect(self,k,v,φ2,r=1):       
        x = r * v[0] * np.sin(φ2) + r * k[0] * np.cos(φ2)
        y = r * v[1] * np.sin(φ2) + r * k[1] * np.cos(φ2)
        z = r * v[2] * np.sin(φ2) + r * k[2] * np.cos(φ2)
        return [x, y, z]

    def line_vect(self, k, v, n=10, col="#0D5022"):
        x = np.linspace(k[0],v[0],n)
        y = np.linspace(k[1],v[1],n)
        z = np.linspace(k[2],v[2],n)
        return [x, y, z]
         
    def legend_updt(self):
        for leg in self.leg_obj:
            lin=self.leg_obj[leg][1]
            if lin==None:continue
            if isinstance(lin,tuple):lin=lin[0]
            isVisible = lin.get_visible()
            leg.set_alpha(1.0 if isVisible else 0.2)
        self.canvas.draw_idle()

    def show_annot(self,v3d,txt, interval_=5000):
        x2, y2, _ = proj3d.proj_transform(*v3d, self.ax.get_proj())
        self.annot.xy = x2, y2
        self.annot.set_text(txt)
        self.annot.set_visible(True)
        try:self.timer.stop()
        except:pass
        self.timer = self.canvas.new_timer(interval=interval_)
        self.timer.add_callback(self.clear_ann)
        self.timer.start()

    def toggle_ecliptic_scale(self, hide=False):
        isVisible= self.ecliptic_scale[1][1].get_visible()
        if hide==True:isVisible=True
        if self.ecl_circl_1.get_visible()==False:isVisible=True
        for i in self.ecliptic_scale:
                self.ecliptic_scale[i][0].set_visible(not isVisible)
                self.ecliptic_scale[i][1].set_visible(not isVisible)

    def toggle_equator_scale(self, hide=False):
        isVisible= self.equator_scale[1][1].get_visible()
        if hide==True:isVisible=True
        if self.eq_circl_1.get_visible()==False:isVisible=True
        for i in self.equator_scale:
            self.equator_scale[i][0].set_visible(not isVisible)
            self.equator_scale[i][1].set_visible(not isVisible)    

    def toggle_horizon_scale(self, hide=False):
        isVisible= self.Hor_scale[1][1].get_visible()
        if hide==True:isVisible=True
        if self.hor_circl_1.get_visible()==False:isVisible=True
        for i in self.Hor_scale:
            self.Hor_scale[i][0].set_visible(not isVisible)
            self.Hor_scale[i][1].set_visible(not isVisible)         

    def toggle_prime_vert_scale(self, hide=False):
        isVisible= self.PV_scale[1][1].get_visible()
        if hide==True:isVisible=True
        if self.prime_vert_1.get_visible()==False:isVisible=True
        for i in self.PV_scale:
            self.PV_scale[i][0].set_visible(not isVisible)
            self.PV_scale[i][1].set_visible(not isVisible) 
            

    def key_(self,event):
        if event.key=="escape":
            exit()

        elif event.key=="left":
            azim_, elev_ = self.ax.azim, self.ax.elev
            azim_=azim_+1
            self.ax.view_init(azim = azim_, elev = elev_)   
            self.canvas.draw_idle()

        elif event.key=="right":
            azim_, elev_ = self.ax.azim, self.ax.elev  
            azim_=azim_-1
            self.ax.view_init(azim = azim_, elev = elev_)   
            self.canvas.draw_idle()

        elif event.key=="up":
            azim_, elev_ = self.ax.azim, self.ax.elev
            elev_+=1
            self.ax.view_init(azim = azim_, elev = elev_)   
            self.canvas.draw_idle()

        elif event.key=="down":
            azim_, elev_ = self.ax.azim, self.ax.elev
            elev_-=1
            self.ax.view_init(azim = azim_, elev = elev_)
            self.canvas.draw_idle()

        if event.key=="j":
            self.ax.view_init(azim = 0, elev = 0) 
            self.canvas.draw_idle()
        if event.key=="h":
            self.canvas.draw_idle()
        elif event.key=="ctrl+s":
            filename=r"3D_astro"
            filename=asksaveasfilename(parent=self.parent,title="Save file",initialdir="C:\\",initialfile = filename,filetypes=[('image, .png', '*.png'),('All Files', '*.*')])
            filename=f"{filename}.png"
            if filename=="": # cancel
                return
            else:
                self.fig.savefig(filename)

    def onpick(self,event):
        if event.mouseevent.button in [2,"up","down"]:return
        legend = event.artist
        if legend in self.legend.get_lines():
            txt=self.leg_obj[legend]
            txt=self.leg_obj[legend][0]
            if txt=="Axes":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                    dim = True if self.axes_id.get_alpha() != self.alpha_main else False
                    alfa2= self.alpha_main if dim else 0.2
                    self.axes_id.set_alpha(alfa2)
                    self.canvas.draw_idle()
                    return
                isVisible = self.axes_id.get_visible()
                self.axes_id.set_visible(not isVisible)
                legend.set_alpha(1.0 if not isVisible else 0.2)

            elif txt=="Sphere":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                    for id_ in [self.surface1, self.surface2]:#self.surface
                        isVisible = id_.get_visible()
                        id_.set_visible(not isVisible)
                    return 
                isVisible = self.sphere_.get_visible()
                self.sphere_.set_visible(not isVisible)
                legend.set_alpha(1.0 if not isVisible else 0.2) 

            elif txt=="Ecliptic":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                    dim = True if self.ecl_circl_2.get_alpha() != self.alpha_main_2 else False
                    alfa2= self.alpha_main_2 if dim else 0.3
                    for cir in [self.ecl_circl_1, self.ecl_circl_2]:
                        cir.set_alpha(alfa2)
                    self.canvas.draw_idle()
                    return
                isVisible = self.ecl_circl_1.get_visible()
                self.ecl_circl_1.set_visible(not isVisible)
                self.ecl_circl_2.set_visible(not isVisible)
                legend.set_alpha(1.0 if not isVisible else 0.2)
                for id_ in self.ecl_ids:
                    id_.set_visible(not isVisible)
                for id_ in self.houses_obj:
                    id_.set_visible(not isVisible)
                for id_ in self.zodiac_obj:
                    id_.set_visible(not isVisible)

                self.toggle_ecliptic_scale(hide= True)

            elif txt=="Equator":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                    dim = True if self.eq_circl_2.get_alpha() != self.alpha_main_2 else False
                    alfa2= self.alpha_main_2 if dim else 0.3
                    for cir in [self.eq_circl_1, self.eq_circl_2]:
                        cir.set_alpha(alfa2)
                    self.canvas.draw_idle()
                    return
                isVisible = self.eq_circl_1.get_visible()
                self.eq_circl_1.set_visible(not isVisible)
                self.eq_circl_2.set_visible(not isVisible)
                legend.set_alpha(1.0 if not isVisible else 0.2)
                for id_ in self.equat_ids:
                    id_.set_visible(not isVisible)

                self.toggle_equator_scale(hide= True) 

            elif txt=="Horizon":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                    dim = True if self.hor_circl_2.get_alpha() != self.alpha_main else False
                    alfa2= self.alpha_main if dim else 0.2
                    for cir in [self.hor_circl_1, self.hor_circl_2]:
                        cir.set_alpha(alfa2)
                    self.canvas.draw_idle()
                    return
                isVisible = self.hor_circl_1.get_visible()
                self.hor_circl_1.set_visible(not isVisible)
                self.hor_circl_2.set_visible(not isVisible)
                legend.set_alpha(1.0 if not isVisible else 0.2)

                self.toggle_horizon_scale(hide= True) 

            elif txt=="Prime Vertical":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                    dim = True if self.prime_vert_2.get_alpha() != self.alpha_main else False
                    alfa2= self.alpha_main if dim else 0.2
                    for cir in [self.prime_vert_1, self.prime_vert_2]:
                        cir.set_alpha(alfa2)
                    self.canvas.draw_idle()
                    return
                isVisible = self.prime_vert_1.get_visible()
                self.prime_vert_1.set_visible(not isVisible)
                self.prime_vert_2.set_visible(not isVisible)
                legend.set_alpha(1.0 if not isVisible else 0.2)

                self.toggle_prime_vert_scale(hide= True)

            elif txt=="Meridian":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                    dim = True if self.mer_circle.get_alpha() != self.alpha_main else False
                    alfa2= self.alpha_main if dim else 0.2
                    self.mer_circle.set_alpha(alfa2)
                    self.canvas.draw_idle()
                    return
                isVisible = self.mer_circle.get_visible()
                self.mer_circle.set_visible(not isVisible)
                legend.set_alpha(1.0 if not isVisible else 0.2)

            elif txt=="Show half":
                self.annot.set_visible(False)
                if event.mouseevent.button==3:
                   self.circles_alpha()
                   self.canvas.draw_idle()
                   return
                if self.half==0:
                    self.half=1
                    for id_ in self.view_West:
                        id_.set_visible(False)
                    for id_ in self.view_East:
                        id_.set_visible(True) 
                elif self.half==1:
                    self.half=2
                    for id_ in self.view_West:
                        id_.set_visible(True)
                    for id_ in self.view_East:
                        id_.set_visible(False)
                elif self.half==2:
                    self.half=0
                    for id_ in self.view_West:
                        id_.set_visible(True)
                    for id_ in self.view_East:
                        id_.set_visible(True)

            elif txt=="Extra off":
                for id_t in self.planets_obj:
                    obj = self.planets_obj[id_t]                
                    for el in ["id_Mer", "id_Mer_nat", "id_Par", "id_proj_hor", "id_proj_hor_nat"]:
                        obj[el].set_visible(False)
                    for el in ["id_pt_Eq", "id_pt_Hor", "id_pt_Ecl"]:
                        obj[el][0].set_visible(False)
                    for el in ["id_l_eq", "id_l_ecl","id_l_ho"]:
                        obj[el].set_visible(False)
                self.annot.set_visible(False)

                self.toggle_ecliptic_scale(hide= True) 
                self.toggle_equator_scale(hide= True) 
                self.toggle_horizon_scale(hide= True) 
                self.toggle_prime_vert_scale(hide= True)

            elif txt=="Scale":
                if event.mouseevent.button==3:
                   self.toggle_equator_scale() 
                else:
                    self.toggle_ecliptic_scale()
                    self.toggle_equator_scale()
            self.canvas.draw_idle()
            return

        if event.artist==self.id_v_start:
            if event.mouseevent.button==1:
                self.timestamp=self.timestampIni
                self.plot_next_prev(minutes=0) 
            self.ax.set_xlim(self.xlim)
            self.ax.set_ylim(self.ylim)
            self.ax.set_zlim(self.zlim)
            self.ax.view_init(azim = self.azim0, elev = self.elev0) 
            self.mer_circle.set_visible(True)
            self.prime_vert_1.set_visible(True)
            self.prime_vert_2.set_visible(True) 

        elif event.artist==self.id_v_chart:
            if event.mouseevent.button==3: 
                self.ax.view_init(azim = 90 + np.degrees(self.Asc_φ_hor), elev = self.poleN_ecl_elev+90)  

            else:
                azim_=90 + np.degrees(self.Asc_φ_hor)
                self.ax.view_init(azim = azim_, elev = self.poleN_ecl_elev) 
                self.mer_circle.set_visible(False)
                self.prime_vert_1.set_visible(False)
                self.prime_vert_2.set_visible(False)            
                if event.mouseevent.button==3:
                    azim_, elev_ = self.ax.azim, self.ax.elev
                    self.ax.view_init(azim = 30, elev = elev_)

        elif event.artist==self.id_v_Eq:
            if event.mouseevent.button == 3:
                self.ax.view_init(azim = 90, elev = self.poleN_elev-90)
            else:
                self.ax.view_init(azim = 90, elev = self.poleN_elev)

        elif event.artist==self.id_v_anim:
            s=0; m=0; h=0
            val=self.radio.value_selected
            Δt=int(self.text_box.text)
            if val=="sec":
                s=Δt
            elif val=="min":
                m=Δt
            elif val=="hour":
                h=Δt
            
            if event.mouseevent.button==3:
                s=-s ; m=-m ; h=-h
            for i in range(10):
                self.parent.after(i*500, lambda s=s, m=m, h=h: self.plot_next_prev(seconds=s, minutes=m, hours=h))
                self.canvas.draw_idle()           

        elif event.artist==self.id_v_prev:
            s=self.radio.value_selected
            Δt=int(self.text_box.text)
            if s=="sec":
                self.plot_next_prev(seconds=-Δt)
            elif s=="min":
                self.plot_next_prev(minutes=-Δt)                
            elif s=="hour":
                self.plot_next_prev(hours=-Δt)

            val=self.radio.value_selected
            Δt=int(self.text_box.text)
            if val=="sec":
                s=Δt
            elif val=="min":
                m=Δt
            elif val=="hour":
                h=Δt

        elif event.artist==self.id_v_next:
            s=self.radio.value_selected
            Δt=int(self.text_box.text)
            if s=="sec":
                self.plot_next_prev(seconds=Δt)
            elif s=="min":

                self.plot_next_prev(minutes=Δt)                
            elif s=="hour":
                self.plot_next_prev(hours=Δt)

        elif event.artist==self.id_E:
            self.ax.view_init(azim = 30,elev = 15) 

        elif event.artist==self.id_W:
            self.ax.view_init(azim = 200, elev = 15)

        elif event.artist==self.id_N:
            self.ax.view_init(azim = 180, elev = -90) 
 
        elif event.artist==self.id_S:
            self.ax.view_init(azim = 180, elev = 90)   

        elif event.artist==self.id_A0:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                self.ax.view_init(azim = 0, elev = elev_)  
            else:
                self.ax.view_init(azim = 0, elev = elev_)   

        elif event.artist==self.id_E0:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                self.ax.view_init(azim = azim_, elev = 0)  
            else:
                self.ax.view_init(azim = azim_, elev = 0)  

        elif event.artist==self.id_A90:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                self.ax.view_init(azim = -90, elev = elev_)  
            else:
                self.ax.view_init(azim = 90, elev = elev_)   

        elif event.artist==self.id_A180:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                self.ax.view_init(azim = 180, elev = elev_)  
            else:
                azim_=azim_+10
                self.ax.view_init(azim = 180, elev = elev_)   

        elif event.artist==self.id_E90:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                self.ax.view_init(azim = azim_, elev = -90)  
            else:
                self.ax.view_init(azim = azim_, elev = 90)   

        elif event.artist==self.id_E180:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                self.ax.view_init(azim = azim_, elev = 180)  
            else:
                self.ax.view_init(azim = azim_, elev = 180)   

        elif event.artist==self.id_v_left:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                azim_-=1
            else:
                azim_-=10
            self.ax.view_init(azim = azim_, elev = elev_)   

        elif event.artist==self.id_v_right:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                azim_+=1
            else:          
                azim_+=10
            self.ax.view_init(azim = azim_, elev = elev_)   

        elif event.artist==self.id_v_up:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                elev_+=1
            else:           
                elev_=elev_+10
            self.ax.view_init(azim = azim_, elev = elev_)   

        elif event.artist==self.id_v_down:
            azim_, elev_ = self.ax.azim, self.ax.elev
            if event.mouseevent.button==3:
                elev_-=1
            else:              
                elev_=elev_-10
            self.ax.view_init(azim = azim_, elev = elev_)

        elif event.artist==self.id_v_test:
            pass

        elif event.artist==self.id_help_ico:
            self.helpDialog = helpWindow_3D(self.parent,title="Help")

        if event.artist in [self.id_v_start, self.id_v_up, self.id_v_down, self.id_v_left, self.id_v_right, self.id_E, self.id_W, self.id_N, self.id_S, self.id_E0, self.id_A0, self.id_E90, self.id_E180, self.id_A90, self.id_A180,self.id_v_Eq, self.id_v_chart, self.id_v_test,self.id_view, self.id_azim, self.id_elev]:
            azim, elev = self.ax.azim, self.ax.elev
            txt=" azim={:.1f}°, elev={:.1f}° ".format(azim, elev)
            self.id_text_2.set_text(txt)
            self.canvas.draw_idle()
            self.timer_azim_elev(15000) 
            return

        if event.artist in [self.eq_circl_1, self.eq_circl_2] and self.eq_circl_1.get_visible():
            el=event.artist
            el=event.artist
            ind = event.ind
            xx, yy, zz = el.get_data_3d()
            i=ind[0]
            x,y,z=[xx[i],yy[i],zz[i]]
            φ2=np.arccos(x);
            φ2a=np.degrees(φ2)
            if y>=0:
                φ2 = φ2 + np.pi/2
            elif y<0:
                φ2 = np.pi/2 - φ2
            if φ2<0: φ2 = φ2 + 2*np.pi  
            if self.south==True: φ2=np.pi-φ2
            φ2=norm_r(φ2)              
            φ2a=np.degrees(φ2)
            RA= norm_(φ2a + self.ARMC)
            self.show_txt_tip(RA,"Equator")

        elif event.artist in [self.ecl_circl_1, self.ecl_circl_2] and self.ecl_circl_1.get_visible():
            el=event.artist
            ind = event.ind
            xx, yy, zz = el.get_data_3d()
            i=ind[0]
            x,y,z=[xx[i],yy[i],zz[i]]
            d=np.dot(self.v_equinox,[x,y,z]);
            φ2=np.arccos(d)
            lon=np.degrees(φ2)
 
            if self.south==True: φ2=np.pi-φ2
            φ2=norm_r(φ2)              
            φ2a=np.degrees(φ2)
            v=np.cross(self.v_equinox,[x,y,z])

            if self.v_MC[1]<=0 and v[2]<0:
                lon=norm_(360-lon)
            if self.v_MC[1]>0 and v[2]>0:
                lon=norm_(360-lon)

            self.show_txt_tip(lon,"Ecliptic")


        if event.mouseevent.button==3:
            for id_t in self.planets_obj.keys(): # click circles to hide
                obj = self.planets_obj[id_t]
                for key_ in ["id_Mer", "id_Par", "id_proj_hor", "id_Mer_nat", "id_proj_hor_nat"]:
                    id_=obj[key_]
                    if event.artist==id_:
                        id_.set_visible(False)
                        return


        for id_t in self.planets_obj.keys(): # click planet text
            obj = self.planets_obj[id_t]
            if event.artist==id_t:
                if event.mouseevent.button==3:
                    pass
                    '''
                    isVisible = obj["id_Mer_nat"].get_visible()
                    obj["id_Mer_nat"].set_visible(not isVisible)
                    obj["id_proj_hor_nat"].set_visible(not isVisible)
                    '''
                else:
                    pass
 
                φ_hor = obj["id_pt_Hor"][1]
                azimuth = obj["id_pt_Hor"][3]
                altitude = obj["id_pt_Hor"][4]
                txt=" {}, azim={:.1f}°(E), {:.1f}°(N), alt={:.1f}°".format(obj["txt"], φ_hor, azimuth, altitude)
                txt=txt.replace("Node_","Node ")
                self.id_text_2.set_text(txt)
                self.timer_azim_elev(15000) 
                self.canvas.draw_idle()
                return

        for id_t in self.planets_obj.keys(): # click planet dot
            obj = self.planets_obj[id_t]
            id_pl = obj["id_pl"]
            if event.artist==id_pl:
                if id_pl.get_visible()==False:return
                if event.mouseevent.button==1:
                    if self.planets_obj[id_t]["show_mer_par"]==0:
                        obj["id_Mer"].set_visible(True)
                        obj["id_Par"].set_visible(True)
                        #obj["id_proj_hor"].set_visible(True) #planet's proportionate horizon
                        self.planets_obj[id_t]["show_mer_par"]=1
                    elif self.planets_obj[id_t]["show_mer_par"]==1:
                        obj["id_Mer"].set_visible(True)
                        obj["id_Par"].set_visible(False)
                        #obj["id_proj_hor"].set_visible(False)
                        self.planets_obj[id_t]["show_mer_par"]=2
                    elif self.planets_obj[id_t]["show_mer_par"]==2:
                        obj["id_Mer"].set_visible(False)
                        obj["id_Par"].set_visible(True)
                        #obj["id_proj_hor"].set_visible(False)
                        self.planets_obj[id_t]["show_mer_par"]=3
                    elif self.planets_obj[id_t]["show_mer_par"]==3:
                        obj["id_Mer"].set_visible(False)
                        obj["id_Par"].set_visible(False)
                        #obj["id_proj_hor"].set_visible(False)
                        self.planets_obj[id_t]["show_mer_par"]=0

                elif event.mouseevent.button==3:
                    for el in ["id_pt_Eq", "id_pt_Hor", "id_pt_Ecl"]:
                        isVisible = obj[el][0].get_visible()
                        obj[el][0].set_visible(not isVisible)
                    for el in ["id_l_eq", "id_l_ecl", "id_l_ho"]:
                        isVisible = obj[el].get_visible()
                        obj[el].set_visible(not isVisible)

                φ_hor = obj["id_pt_Hor"][1]
                azimuth = obj["id_pt_Hor"][3]
                altitude = obj["id_pt_Hor"][4]
                txt=" {}, azim={:.1f}°(E), {:.1f}°(N), alt={:.1f}°".format(obj["txt"], φ_hor, azimuth, altitude)
                txt=txt.replace("Node_","Node ")
                self.id_text_2.set_text(txt)
                self.timer_azim_elev(15000)                          
                return

        for id_t in self.planets_obj.keys(): # click projection dot
            obj = self.planets_obj[id_t]
            id_pl = obj["id_pl"]
            id_dot_Eq = obj["id_pt_Eq"][0]
            id_dot_Ec = obj["id_pt_Ecl"][0]
            id_dot_H = obj["id_pt_Hor"][0]
            name = obj["name"]

            if event.artist in [id_dot_Eq, id_dot_Ec ,id_dot_H]:
                if event.mouseevent.button == 3:
                    self.clear_ann(event)
                else:
                    if event.artist ==id_dot_Eq:
                        if id_dot_Eq.get_visible()==False:return
                        txt=" {} RA={:.0f}°".format(name, obj["id_pt_Eq"][1])
                        xyz=obj["id_pt_Eq"][2]
                    elif event.artist ==id_dot_H:
                        if id_dot_H.get_visible()==False:return
                        txt=" {} azim={:.0f}°(from E) ".format(name,obj["id_pt_Hor"][1])# φ hor.
                        xyz=obj["id_pt_Hor"][2]  
                    elif event.artist ==id_dot_Ec:
                        if id_dot_Ec.get_visible()==False:return 
                        txt=" {} ecl. long={:.0f}° ".format(name, obj["id_pt_Ecl"][1])
                        xyz=obj["id_pt_Ecl"][2]                                               
                    self.show_annot(xyz,txt, interval_=2000)
                    self.canvas.draw_idle()
                return

        for id_ in self.houses_obj.keys():
            if event.artist==id_:
                obj = self.houses_obj[id_]
                txt=" {}, {} ".format(obj[0], obj[1])
                self.show_annot(obj[2],txt)

                if event.mouseevent.button == 3:
                    self.clear_ann(event)
                else:
                    self.canvas.draw_idle()
                return

        for id_ in self.zodiac_obj.keys():            
            if event.artist==id_:
                obj = self.zodiac_obj[id_]
                txt=" {}, {} ".format(obj[0], obj[1])
                self.show_annot(obj[2],txt)
                x2, y2, _ = proj3d.proj_transform(*obj[2], self.ax.get_proj())
                if event.mouseevent.button == 3:
                    self.clear_ann(event)
                else:
                    self.canvas.draw_idle()
                return


        if id(event.artist) in self.ids.keys():
            xyz=self.ids[id(event.artist)][0]
            txt=self.ids[id(event.artist)][1]
            for i in range(len(self.click_tip_list)):
                if self.click_tip_list[i] in txt:
                    s=True
                    x2, y2, _ = proj3d.proj_transform(xyz[0],xyz[1],xyz[2], self.ax.get_proj())
                    self.annot.xy = x2, y2
                    self.annot.set_text(txt)
                    self.annot.set_visible(True)

                    try:self.timer.stop()
                    except:pass
                    self.timer = self.canvas.new_timer(interval=5000)
                    self.timer.add_callback(self.clear_ann)
                    self.timer.start()
        self.canvas.draw_idle()

    def on_click(self,event):
        if event.button==3:
            self.clear_ann()

    def show_txt_tip(self,dig,which=""):
        if which=="Ecliptic":
            txt = " Click on Ecliptic: lon={:.0f}° ".format(dig)
        elif which=="Equator":
            txt = " Click on Equator: RA={:.0f}° ".format(dig)
        else:
            txt = " {} ".format(dig)
        self.id_text_3.set_text(txt)
        self.canvas.draw_idle()
        try:self.timer3.stop()
        except:pass
        self.timer3 = self.canvas.new_timer(interval=15000)
        self.timer3.add_callback(self.hide_txt_tip)
        self.timer3.start()

    def hide_txt_tip(self):
        self.id_text_3.set_text("")
        self.canvas.draw_idle()
        try:self.timer3.stop()
        except:pass

    def zoom_(self, event, r):
        l_x1, l_x2 = self.ax.get_xlim()
        l_y1, l_y2 = self.ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata
        width = l_x2 - l_x1
        height = l_y2 - l_y1
        w = r*width ; h = r*height
        dx1 = xdata - (xdata - l_x1) * r
        dx2 = xdata + (l_x2 - xdata) * r
        dy1 = ydata - (ydata - l_y1) * r
        dy2 = ydata + (l_y2 - ydata) * r
        self.ax.set_xlim(dx1, dx2)
        self.ax.set_ylim(dy1, dy2)
        self.ax.figure.canvas.draw()

    def scroll_zoom(self, event):
        r=0.20
        r=1-r
        if event.button == "up":
            self.zoom_(event,r)                 
        elif event.button == "down":
            self.zoom_(event,1/r)

    def timer_azim_elev(self, interval=15000, event=None):
        try:self.timer_az.stop()
        except:pass
        self.timer_az = self.canvas.new_timer(interval=interval)
        self.timer_az.add_callback(self.clear_azim_elev)
        self.timer_az.start()

    def clear_azim_elev(self, event=None):
        try:self.timer_az.stop()
        except:pass
        self.id_text_2.set_text("")
        self.canvas.draw_idle()
        print("clear azim_elev")  
          
    def clear_ann(self, event=None):
        self.annot.set_text("")
        self.annot.set_visible(False)
        self.canvas.draw_idle()
        try:self.timer.stop()
        except:pass

    def save_animation(self, frames=40, minutes=0, hours=0, format="gif"):
        def animate(frame_n):
            self.plot_next_prev(minutes=minutes, hours=hours)
            return 

        resp = messagebox.askquestion("Sample animation", f"Save sample animation?\nframes={frames}\nminutes={minutes}, hours={hours}") 
        if resp != "yes":
            return
        anim = animation.FuncAnimation(self.fig, animate, frames=frames, interval=200, repeat=False, blit=False)
        video_ = animation.FFMpegWriter(fps=3)
        if format=="gif":
            filename="Astronomia3D_animation"
            filename=asksaveasfilename(parent=self.parent,title="Save file",initialdir="C:\\",initialfile = filename,filetypes=[('image, .gif', '*.gif'),('All Files', '*.*')])
            filename=f"{filename}.gif"
        elif format=="mp4":
            filename="Astronomia3D_animation"
            filename=asksaveasfilename(parent=self.parent,title="Save file",initialdir="C:\\",initialfile = filename,filetypes=[('video, .mp4', '*.mp4'),('All Files', '*.*')])
            filename=f"{filename}.mp4"; 
        if filename=="": # cancel
            return
        else:
            anim.save(filename, writer=video_)

#=====================

PAGE_BG1 = "#134752"
BUTT_BG = "#095161"
PAGE_BG_2="#0F5274"
FONT_BT2 = ("Segoe UI", 10, "bold")
FONT_TIT = ("Tahoma", 10, "bold")
COLOR_TIT = "#E1E1E1"
FONT_SYM =  ("Consolas", 15, "normal")
FONT_N = ("Tahoma", 10, "bold")

class GUI_astro3D:
    def __init__(self, parent, planets_data, geo_latitude, data, title_="Astronomia 3D - Popiel"):
        self.parent = parent
        self.parent.title(title_) 
        self.parent.bind("<F1>", self.keypressed)
        self.parent.bind("<F2>", self.keypressed)
        self.parent.bind("1", self.keypressed)
        self.parent.bind("2", self.keypressed)
        self.parent.bind("<Control-a>", self.keypressed)
        self.parent.bind("<Control-d>", self.keypressed)
        
        self.page_plot = Frame(self.parent,bg=PAGE_BG1,borderwidth=1, relief="ridge")
        self.page_plot.pack(side="top",fill="both",expand=True,anchor="sw",ipadx=0, ipady=0) 

        self.page0 = Frame(self.parent,bg=PAGE_BG1,borderwidth=1, relief="ridge")
        self.page0.pack(side="left",fill="both",expand=True,anchor="nw",ipadx=0, ipady=0)
        self.page1 = Frame(self.page0,bg=PAGE_BG1,borderwidth=0, relief="ridge")
        self.page1.pack(side="top",fill="both",expand=True,anchor="nw",ipadx=0, ipady=0,pady=(0,0))
        self.page2 = Frame(self.page0,bg=PAGE_BG1,borderwidth=0, relief="ridge")  #
        self.page2.pack(side="bottom",fill="both",expand=True,anchor="nw",ipadx=0, ipady=0)

        self.page3 = Frame(self.parent,bg=PAGE_BG1,borderwidth=1, relief="ridge")
        self.page3.pack(side="right",fill="both",expand=False,anchor="ne",ipadx=0, ipady=0) 
        self.page4 = Frame(self.parent,bg=PAGE_BG1,borderwidth=1, relief="ridge")
        self.page4.pack(side="right",fill="both",expand=False,anchor="ne",ipadx=0, ipady=0) 
        self.page5 = Frame(self.parent,bg=PAGE_BG1,borderwidth=1, relief="ridge")
        self.page5.pack(side="right",fill="both",expand=False,anchor="ne",ipadx=0, ipady=0) 

        self.chkvars=[]
        chkboxes={}
        for i, el in enumerate(c.planets):
            if el=="Node_S":continue
            chkvar = IntVar(); chkvar.set(1) 
            self.chkvars.append(chkvar)
            name=el
            sym=c.planets[el]
            chkboxes[name]=chkvar
            font_f = "Lucida Console"
            font_ = (font_f, 13, "normal")
            padx_=1
            pady_=(2,0)
            if "Node_" in name:font_= (font_f, 11, "normal"); pady_=(3,0);
            if name=="Sun":padx_=0
            id_=Checkbutton(self.page1, text=sym, variable=self.chkvars[i], command = lambda name=name, chkvar=chkvar: self.planets_toggle(name,chkvar))
            id_.config(bg=PAGE_BG1, fg="#F0F0F0", offvalue = 0, onvalue=1, font=font_, activebackground=PAGE_BG_2, activeforeground="#F0F0F0", selectcolor=PAGE_BG_2, justify="center", borderwidth=3)
            id_.grid(row=0, column=i+2,sticky='nw', padx=padx_, pady=pady_)

        lbl_empt = Label(self.page1, text=" ", width=2, justify="center", bg=PAGE_BG1, font=("Tahoma", 8, "bold"))
        lbl_empt.grid(row=0, column=15,sticky="nw", padx=0, pady=(2,0))

        self.chkvar_all = IntVar() ; self.chkvar_all.set(1)
        self.chk_all = Checkbutton(self.page1, text="All", variable=self.chkvar_all, command = lambda name="All", chkvar=self.chkvar_all: self.planets_toggle(name,chkvar))
        self.chk_all.config(offvalue = 0, onvalue=1, bg=PAGE_BG1, fg="#F0F0F0", font=("Arial", 8, "bold"), activebackground=PAGE_BG_2, activeforeground="#F0F0F0", selectcolor=PAGE_BG_2,justify="center",borderwidth=3)
        self.chk_all.grid(row=0, column=1,sticky='nw', padx=(4,4), pady=(3,0))

        sel_col= "#015E70" 
        COL_1 = "#E3E3E3"
        style_ = ttk.Style()
        try:
            style_.theme_use("new_style") 
        except:
            style_ = ttk.Style()
            configure_ = dict(foreground = COL_1, selectbackground = sel_col,fieldbackground = sel_col,background = sel_col, arrowcolor = COL_1)
            style_.theme_create("new_style", parent="alt", settings = {"TCombobox":{"configure":configure_}} )   
            style_.theme_use("new_style")    

        self.combo_ = ttk.Combobox(self.page2, width = 24) 
        self.combo_.grid(row=0, column=1,sticky="w", padx=10, pady=(0,5))  
        self.combo_['values'] = ("Extra off", "Planet projection points", "Planet meridian", "Planet parallel", 
            "Planet prop. horizon", "All ecliptic points", "Zodiac ecliptic points","Zodiac symbols",
            "Ecliptic scale", "Equator scale", "Horizon scale", "Prime vertical scale")
        self.combo_.set("Hide/show")
        self.combo_["state"] = "readonly"
   
        self.combo_.bind('<<ComboboxSelected>>',self.combobox_callback) 
        self.combo_.bind('<Return>',self.combobox_callback)

        #SpinBox input range Validation
        self.vc = (self.parent.register(self.input_validate), "%P", "%d", "%W")

        self.time_shift_buttons()
        self.anim_buttons()
        self.geo_buttons()

        self.plot = astro3D(self.parent,self.page_plot, planets_data, geo_latitude, data=data) 

    def time_shift_buttons(self):   
        sel_col= "#015E70"
        COL=PAGE_BG1
        COL_F="#F6F6F6"
        FONT_ = ("Tahoma", 8, "bold")
        FONT_2 = ("Arial", 9, "bold")
        COL_1 = "#F6F6F6"

        f_args_p={"side":"top","fill":"both","expand":False,"anchor":"nw"}

        self.fr = Frame(self.page3,bg=PAGE_BG1,borderwidth=0)

        self.f0 = Frame(self.fr,bg=PAGE_BG1,borderwidth=4)
        self.f0.pack(side="left",fill="both",expand=False,anchor="nw", padx=0, pady=0)       
        self.f1 = Frame(self.fr,bg=PAGE_BG1,borderwidth=4, padx=0, pady=0)
        self.f1.pack(**f_args_p)
        self.f2 = Frame(self.fr,bg=PAGE_BG1,borderwidth=4, padx=0, pady=0)
        self.f2.pack(**f_args_p)

        self.rad_var = StringVar(None, "Days")
        
        w=6; indic=0;
        ipx=4; ipy=1; py=0;
        args={"width":w,"bg":COL,"fg":COL_F,"font":FONT_,"command":None,"variable":self.rad_var,"indicator":indic, "selectcolor":sel_col}
        args_p={"fill":None, "ipadx":ipx, "ipady":ipy, "pady":py,"side":"left","anchor":"nw"}
        self.rad_h=Radiobutton(self.f1, text = "Hours", value="Hours", **args); self.rad_h.pack(**args_p)        
        self.rad_m=Radiobutton(self.f1, text = "Minutes", value="Minutes", **args); self.rad_m.pack(**args_p) 
        self.rad_s=Radiobutton(self.f1, text = "Seconds", value="Seconds", **args); self.rad_s.pack(**args_p)

        self.spbox_var = IntVar()
        self.sp = Spinbox(self.f2, from_=1, to=60,increment=1,textvariable=self.spbox_var,bg=sel_col,width=7,fg=COL_1,font=("Tahoma", 11, "normal"),justify="center",buttonbackground=COL)
        self.sp.pack(side="left",anchor="nw" ,padx=(0,7), pady=(2,0))  
        #SpinBox range Validation
        self.sp.config(validate ="key",  validatecommand = self.vc )

        unit="Minutes"
        self.spbox_var.set(10)
        self.rad_var.set(unit)

        F_arr=("Helvetica", 14, "bold")
        ipx=4;ipy=0;py=(0,0);px=3;
        ipy=0
        arr_p={"fill":None, "ipadx":ipx, "ipady":ipy, "padx":px, "pady":py,"side":"left","anchor":"center"}        
        self.bt_arrowL = Button(self.f2,text="◄",command=lambda e=None, Δt=None:self.prev_tk(e, Δt),width=4,bg=COL,fg=COL_F,font=FONT_2)
        self.bt_arrowR = Button(self.f2,text="►",command=lambda e=None, Δt=None:self.next_tk(e, Δt),width=4,bg=COL,fg=COL_F,font=FONT_2)
        self.bt_arrowL.pack(**arr_p)
        self.bt_arrowR.pack(**arr_p)

        self.fr.grid(row=0, column=18,sticky="w", padx=10, pady=(0,0),)
        self.bt_arrowL.bind("<Button-3>", lambda e=None, Δt=1:self.prev_tk(e, r_click=Δt))
        self.bt_arrowR.bind("<Button-3>", lambda e=None, Δt=1:self.next_tk(e, r_click=Δt))  

        self.rad_h.bind("<Button-3>", lambda e=None, s="Hours":self.radio_(e, s))
        self.rad_m.bind("<Button-3>", lambda e=None, s="Minutes":self.radio_(e, s))
        self.rad_s.bind("<Button-3>", lambda e=None, s="Seconds":self.radio_(e, s))

    def anim_buttons(self):
        sel_col= "#015E70"
        COL=PAGE_BG1
        COL_F="#F6F6F6"
        FONT_ = ("Tahoma", 8, "bold")
        FONT_2 = ("Arial", 8, "bold")
        COL_1 = "#F6F6F6"

        self.bt_anim = Button(self.page4,text="Animation",command=self.anim_tk,width=12,bg=COL,fg=COL_F,font=FONT_2)#
        self.bt_anim.grid(row=0, column=0, columnspan=2, sticky="w", padx=(11, 8), pady=(3,5),ipady=0)  
        self.spbox_var_st = IntVar()
        self.sp_st = Spinbox(self.page4, from_=1, to=30,increment=1,textvariable=self.spbox_var_st, bg=sel_col,width=4,fg=COL_1,font=("Tahoma", 11, "normal"),justify="center",buttonbackground=COL)
        self.sp_st.grid(row=1, column=0,sticky="w", padx=(11, 0), pady=(6,5)) 
        self.spbox_var_st.set(10)

        self.lbl2 = Label(self.page4, text="steps", justify="center", bg=PAGE_BG1, fg="#F0F0F0", font=("Arial",8, "bold"))
        self.lbl2.grid(row=1, column=1, sticky="w", padx=(0,0), pady=4)

        #SpinBox range Validation
        self.sp_st.config(validate ="key",  validatecommand = self.vc)
        self.bt_anim.bind("<Button-3>", self.anim_back_tk)

    def geo_buttons(self):
        sel_col= "#015E70"
        COL=PAGE_BG1
        COL_F="#F6F6F6"
        FONT_ = ("Tahoma", 8, "bold")
        FONT_2 = ("Arial", 8, "bold")
        COL_1 = "#F6F6F6"
        FONT_E = ("Arial", 10, "normal")

        self.bt_ = Button(self.page5,text="New for current time",command=self.new_,width=21,bg=COL,fg=COL_F,font=FONT_2)#
        self.bt_.grid(row=0, column=0, columnspan=4, sticky="w", padx=(10, 8), pady=(3,5),ipady=0) 

        self.long_v = StringVar() ; self.lat_v = StringVar() 
        self.lat_v.set("50.07"); self.long_v.set("19.90")
        #self.lat_v.set("40.67") ; self.long_v.set("-73.95")

        self.inp_lat = Entry(self.page5, textvar = self.lat_v, width=6, font = FONT_E, justify="center", bg=sel_col, fg=COL_1, relief="sunken")
        self.inp_lat.grid(row=1, column=0, columnspan=1, sticky="w", padx=(10, 0), pady=(7,2),ipady=0) 
        self.inp_long = Entry(self.page5, textvar = self.long_v, width=7,font = FONT_E,  justify="center", bg=sel_col, fg=COL_1, relief="sunken")
        self.inp_long.grid(row=1, column=2, columnspan=1, sticky="w", padx=(5, 0), pady=(7,2),ipady=0)

        lbl3 = Label(self.page5, text="lat", justify="left", width=1, bg=PAGE_BG1, fg="#F0F0F0", font=("Arial",8, "bold"))
        lbl3.grid(row=1, column=1, sticky="w", padx=(2,0), pady=(7,2))
        lbl4 = Label(self.page5, text="lon", justify="left", width=2, bg=PAGE_BG1, fg="#F0F0F0", font=("Arial",8, "bold"))
        lbl4.grid(row=1, column=3, sticky="w", padx=(0,6), pady=(7,2))

        self.inp_lat.config(validate ="key",  validatecommand = self.vc)
        self.inp_long.config(validate ="key",  validatecommand = self.vc)

        self.bt_.bind("<Button-3>", self.reset_lat)



    def input_validate(self, input_, action, name):
        if input_:
            if input_=="-":
                return True
            elif input_=="." and "entry" in name:
                return True
            elif input_=="." and "entry" not in name:
                return False
            if "entry2" in name:
                try:
                    input_=float(input_)
                    if not self.test_float(input_, 2):
                        return False
                    return True
                except ValueError:
                    return False
            elif "entry" in name:
                try:
                    input_=float(input_)
                    if not self.test_float(input_, 1):
                        return False
                    return True
                except ValueError:
                    return False
            else:     #Spinbox      
                try:
                    int(input_)
                    if len(str(input_))>6:
                        return False
                    return True
                except ValueError:
                    return False
        elif action=="0": #validatecommand + backspace
            return True
        else:
            return False

    def test_float(self, f, inp):
        s=str(f)
        s=s.replace("-","")
        if "." in s:
            arr=s.split(".")
            if len(arr)>2: 
                return False #only 1 dot
            if len(arr[1])>2: 
                return False # only 2 decimal digits

            lim = 2 if inp==1 else 3 
            if len(arr[0])>lim:
                return False
            else:
                lim2= 90 if inp==1 else 180 
                if abs(int(arr[0]))>lim2:
                    return False
                return True            
        else:
            lim = 2 if inp==1 else 3 
            if len(s)>lim:
                return False
            else:
                lim2= 90 if inp==1 else 180 
                if abs(int(arr[0]))>lim2:
                    return False
                return True
        return True


    def input_validate0(self, input_, action):
        if input_:
            if input_=="-":
                return True

            try:
                int(input_)
                if len(input_)>4:
                    return False
                return True
            except ValueError:
                return False
        elif action=="0": #validatecommand + backspace
            return True
        else:
            return False

    def radio_(self, event=None, s=None):
        val   =self.rad_var.get()
        a1('',val   , s)
        if s=="Hours":
            self.spbox_var.set(1)
        elif s=="Minutes":
            self.spbox_var.set(10)
        elif s=="Seconds":
            self.spbox_var.set(30)
        self.rad_var.set(s)

    def planets_toggle(self,name,id_):
        if name!="All":
            obj=self.plot.planets_ids[name]
            if id_.get()==1:
                obj["id_pl"].set_visible(True)
                obj["id_t"].set_visible(True)
                if name=="Node_N":
                    self.plot.planets_ids["Node_S"]["id_pl"].set_visible(True)
                    self.plot.planets_ids["Node_S"]["id_t"].set_visible(True)
            elif id_.get()==0:
                for el_ in obj:
                    obj[el_].set_visible(False)
                if name=="Node_N":
                    for el_ in self.plot.planets_ids["Node_S"]:
                        self.plot.planets_ids["Node_S"][el_].set_visible(False)
                self.chkvar_all.set(0)

        elif name=="All":
            if id_.get()==1:
                for id__ in self.chkvars:
                    id__.set(1)
                for pl in self.plot.planets_ids:
                    obj=self.plot.planets_ids[pl]
                    obj["id_pl"].set_visible(True)
                    obj["id_t"].set_visible(True)
                    
            elif id_.get()==0:
                for id__ in self.chkvars:
                    id__.set(0)
                for pl in self.plot.planets_ids:
                    obj=self.plot.planets_ids[pl]
                    for el_ in obj:
                        obj[el_].set_visible(False)
        self.plot.canvas.draw_idle()

    def combobox_callback(self,event):
        str_ = self.combo_.get()
        if str_=="Planet projection points": 
            for name in c.planets2:
                if name in [ "Asc", "MC"]:continue
                obj=self.plot.planets_ids[name]
                isVisible=self.plot.planets_ids[name]["id_pl"].get_visible()            
                if not isVisible:continue
                for el in ["id_pt_Eq", "id_pt_Hor", "id_pt_Ecl"]:
                    obj[el].set_visible(isVisible)
 
        elif str_=="Planet meridian":
            for name in c.planets2:
                if name in [ "Asc", "MC"]:continue
                obj=self.plot.planets_ids[name]
                isVisible=obj["id_pl"].get_visible()
                if not isVisible:continue
                obj["id_Mer"].set_visible(isVisible)

        elif str_=="Planet parallel":
            for name in c.planets2:
                if name in ["Asc", "MC"]:continue
                obj=self.plot.planets_ids[name]
                isVisible=obj["id_pl"].get_visible()
                if not isVisible:continue
                obj["id_Par"].set_visible(isVisible)

        elif str_=="Planet prop. horizon":
            for name in c.planets2:
                if name in [ "Asc", "MC"]:continue
                obj=self.plot.planets_ids[name]
                isVisible=obj["id_pl"].get_visible()
                if not isVisible:continue
                obj["id_proj_hor"].set_visible(isVisible)

        elif str_=="Planet meridian natal":
            for name in c.planets2:
                if name in ["Node_N", "Node_S", "Asc", "MC"]:continue
                obj=self.plot.planets_ids[name]
                isVisible=obj["id_pl"].get_visible()
                if not isVisible:continue
                obj["id_Mer_nat"].set_visible(isVisible)

        elif str_=="Planet prop. horizon natal":
            for name in c.planets2:
                if name in ["Node_N", "Node_S", "Asc", "MC"]:continue
                obj=self.plot.planets_ids[name]
                isVisible=obj["id_pl"].get_visible()
                if not isVisible:continue  
                obj["id_proj_hor_nat"].set_visible(isVisible)

        elif str_=="Houses ecliptic points": 
            self.toggle_houses_p()

        elif str_=="Zodiac ecliptic points": 
            self.toggle_ecl_p()

        elif str_=="Zodiac symbols":
            self.toggle_ecl_sym()

        elif str_=="All ecliptic points":
            self.toggle_ecl_p()
            self.toggle_ecl_sym()
            self.toggle_houses_p()

        elif str_=="Celestial equator points":
            isVisible=self.plot.armc_id.get_visible() 
            self.plot.armc_id.set_visible(not isVisible)

        elif str_=="Asc, MC, ARMC...":
            isVisible=self.plot.asc_id.get_visible()
            for id_ in [self.plot.armc_id, self.plot.mc_id, self.plot.asc_id, self.plot.asc_id2, self.plot.poleN_id, self.plot.poleS_id]:
                id_.set_visible(not isVisible)


        elif str_=="Ecliptic scale":
            self.plot.toggle_ecliptic_scale()

        elif str_=="Equator scale":
            self.plot.toggle_equator_scale()

        elif str_=="Horizon scale":
            self.plot.toggle_horizon_scale()

        elif str_=="Prime vertical scale":
            self.plot.toggle_prime_vert_scale()

        elif str_=="Extra off":
            self.extra_off()

        self.plot.canvas.draw_idle()


    def extra_off(self):
        for id_t in self.plot.planets_obj:
            obj = self.plot.planets_obj[id_t]            
            for el in ["id_Mer", "id_Mer_nat", "id_Par", "id_proj_hor", "id_proj_hor_nat"]:
                obj[el].set_visible(False)
            for el in ["id_pt_Eq", "id_pt_Hor", "id_pt_Ecl"]:
                obj[el][0].set_visible(False)
            for el in ["id_l_eq", "id_l_ecl","id_l_ho"]:
                obj[el].set_visible(False)
        self.plot.annot.set_visible(False)

        self.plot.toggle_ecliptic_scale(hide= True) 
        self.plot.toggle_equator_scale(hide= True) 
        self.plot.toggle_horizon_scale(hide= True) 
        self.plot.toggle_prime_vert_scale(hide= True)

    def toggle_houses_p(self):
        isVisible=self.plot.houses_ids[1]["dot"].get_visible()
        for i in range(1,13):
            self.plot.houses_ids[i]["dot"].set_visible(not isVisible)

    def toggle_ecl_p(self):
        isVisible=self.plot.zodiac_ids[1]["dot"].get_visible()
        for i in range(1,13):
            self.plot.zodiac_ids[i]["dot"].set_visible(not isVisible)

    def toggle_ecl_sym(self):
        isVisible=self.plot.zodiac_ids[1]["text"].get_visible()
        for i in range(1,13):
            self.plot.zodiac_ids[i]["text"].set_visible(not isVisible)

    def prev_tk(self, event, r_click=None):
        Δt = self.spbox_var.get()
        val = self.rad_var.get()
        if r_click!=None:
            Δt=r_click
        if val   =="Seconds":
            self.plot.plot_next_prev(seconds=-Δt)
        elif val   =="Minutes":
            self.plot.plot_next_prev(minutes=-Δt)
        elif val   =="Hours":
            self.plot.plot_next_prev(hours=-Δt)

    def next_tk(self, event, r_click=None):
        Δt = self.spbox_var.get()
        val = self.rad_var.get()
        if r_click!=None:
            Δt=r_click
        if val   =="Seconds":
            self.plot.plot_next_prev(seconds=Δt)
        elif val   =="Minutes":
            self.plot.plot_next_prev(minutes=Δt)
        elif val   =="Hours":
            self.plot.plot_next_prev(hours=Δt)

    def anim_tk(self):
        s=0; m=0; h=0
        Δt=self.spbox_var.get()
        val=self.rad_var.get()
        if val=="Seconds":
            s=Δt
        elif val=="Minutes":
            m=Δt
        elif val=="Hours":
            h=Δt
        steps=self.spbox_var_st.get()
        for i in range(steps):
            self.parent.after(i*300, lambda s=s, m=m, h=h: self.plot.plot_next_prev(seconds=s, minutes=m, hours=h))
            self.plot.canvas.draw_idle()           
        return
        
    def anim_back_tk(self, event):
        s=0; m=0; h=0
        Δt=self.spbox_var.get()
        val=self.rad_var.get()
        Δt=-Δt
        if val=="Seconds":
            s=Δt
        elif val=="Minutes":
            m=Δt
        elif val=="Hours":
            h=Δt
        steps=self.spbox_var_st.get()
        for i in range(steps):
            self.parent.after(i*300, lambda s=s, m=m, h=h: self.plot.plot_next_prev(seconds=s, minutes=m, hours=h))
            self.plot.canvas.draw_idle()           
        return

    def reset_lat(self, time_):
        self.lat_v.set("0")
        self.long_v.set("0")

    def new_(self):
        Δt=self.spbox_var.get()
        lat_ = self.lat_v.get()
        lon_ = self.long_v.get()
        if lat_=="" or lon_=="":return
        lat_ = float(lat_)
        lon_ = float(lon_)
        if abs(lat_)>90 or abs(lon_)>180:
            messagebox.showwarning("Wrong value", "Values must be within intervals:\nlatitude:\n[0, 90] for North and [0, -90] for South\nlongitude:\n[0, 180] for East and [0, -180] for West")
            return
        self.extra_off()

        tz_=None
        t_obj = get_time_now(tz_=tz_)
        date_utc=t_obj["date_utc"]
        time_utc=t_obj["time_utc"]
        dataNow={'n': 'Planets', 'ln': 'positions'}
        dataNow["d_utc"]=date_utc
        dataNow["t_utc"]=time_utc
        dataNow["timestamp"]=t_obj["timestamp"]
        dataNow["lat"]=lat_
        dataNow["lon"]=lon_
        dataNow["tz"]=tz_
        dataNow["date_loc"]=t_obj["date_loc"]
        dataNow["time_loc"]=t_obj["time_loc"]
        planets_data = calc_.get_planets_data(date_utc,time_utc,lat_,lon_,trueNode=True)
        self.plot.new_now(planets_data, lat_, data=dataNow)


    def keypressed(self,event):
        if event.keysym=="F1":
            self.prev_tk(event)
        elif event.keysym=="F2":
            self.next_tk(event)
        elif event.keysym=="1":
            self.prev_tk(event)
        elif event.keysym=="2":
            self.next_tk(event)
        elif (event.state==12 and event.keysym=="a") or (event.state==12 and event.keysym=="d"): #  12=ctrl
            time_obj={"minutes":10}
            frames=self.spbox_var_st.get()
            Δt=self.spbox_var.get()
            val=self.rad_var.get()
            if val=="Hours":
                time_obj={"hours":Δt}
            elif val=="Minutes":
                time_obj={"minutes":Δt}
            if event.keysym=="a":
                time_obj.update({"format":"gif"})
            elif event.keysym=="d":
                time_obj.update({"format":"mp4"})
            self.plot.save_animation(frames=frames, **time_obj)


    def close_dialog(self):
        self.parent.wm_attributes("-disabled", False)
        self.parent.deiconify() 
        self.parent.destroy()

    def Exit(self):
        self.parent.destroy() 



def draw_chart3D_now(data=None):
    if data==None:
        latitude = 40.673
        longitude=-73.945
        tz_ = "America/New_York"
        date_=get_time_now(seconds=None) 
        date_utc = date_["date_utc"]
        time_utc = date_["time_utc"]
        dataNow={'n': 'Planets', 'ln': 'positions'}
        dataNow["d_utc"]=date_["date_utc"]
        dataNow["t_utc"]=date_["time_utc"]
        dataNow["timestamp"]=date_["timestamp"]
        dataNow["lat"]=latitude
        dataNow["lon"]=longitude
        dataNow["tz"]=tz_
        d= date_["date_loc"].split("-")
        d=list(reversed(d))
        dataNow["d"]=d    
        t= date_["time_loc"].split(":")    
        dataNow["t"]=t
        trueNode=True
        geo_latitude=latitude
        planets_data = calc_.get_planets_data(date_utc,time_utc,latitude,longitude,trueNode=trueNode)
        ε=calc_.ε
        dataNow["obliquity"]=ε 
        dataNow["trueNode"]=trueNode
    else:
        date_utc = data["d_utc"]
        time_utc = data["t_utc"]
        timestamp = data["timestamp"]
        latitude = float(data["lat"])
        longitude = float(data["lon"])
        geo_latitude=latitude
        trueNode=data["trueNode"]
        planets_data = calc_.get_planets_data(date_utc,time_utc,latitude,longitude,trueNode=trueNode)
        dataNow=data
    GUI = GUI_astro3D(root, planets_data, geo_latitude, data=dataNow)
    return GUI



if __name__ == "__main__":
    trueNode=True
    #print('sys.argv',len(sys.argv),'\n',sys.argv);
    if len(sys.argv)>1:
        if len(sys.argv)>2 and sys.argv[2]=="standalone": #standalone command line
            data=eval(sys.argv[1])
            cmd_obj={"date_utc":data["d_utc"], "time_utc": data["t_utc"], "lat" : data["lat"], "lon": data["lon"],"data":data, "trueNode" : data["trueNode"],"timestamp":data["timestamp"]}
        else:
            json_object=sys.argv[1]
            cmd_obj= json.loads(json_object) 

        date_utc=cmd_obj["date_utc"]
        time_utc=cmd_obj["time_utc"]
        latitude=float(cmd_obj["lat"])
        longitude=float(cmd_obj["lon"])
        trueNode=cmd_obj["trueNode"]        
        data=cmd_obj["data"] 
        print("command line")  
    else:
        data=None 

    root = Tk()
    calc_=calc_for_3D()
    GUI = draw_chart3D_now(data)
    #keyboard.add_hotkey('esc', GUI.Exit)
    mainloop()


