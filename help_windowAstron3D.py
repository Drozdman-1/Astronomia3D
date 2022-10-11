from tkinter import *
from tkinter import ttk 
from tkinter import font
import keyboard

PAGE_BG = "#134752"
BUTT_BG = "#095161"

FONT_BT = ("Segoe UI", 8, "bold")
FONT_BT2 = ("Segoe UI", 10, "bold")

FONT_TIT = ("Tahoma", 10, "bold")
COLOR_TIT = "#E1E1E1"
COLOR_T = "#DCDABE"
FONT_T = ("Times New Roman", 11, "normal")
FONT_BT = ("Times New Roman", 13, "normal")
FONT_BT_B =("Times New Roman", 11, "bold")



class helpWindow_3D:
    def __init__(self, parent, **kwargs):
        self.parent = parent        
        x = self.parent.winfo_rootx()
        y = self.parent.winfo_rooty()
        screenWidth = self.parent.winfo_screenwidth()
        screenHeight = self.parent.winfo_screenheight()
        w = 900 ; h = 700
        title = kwargs.get('title')  
        self.elem = kwargs.get('elem')   
        x1 = int(screenWidth/2 - w/2) - 40; 
        y1 = int(screenHeight/2 - h/2)- 40; 
        self.parent.wm_attributes("-disabled", True)
        self.dialog = Toplevel(self.parent,bg=PAGE_BG)
        self.dialog.resizable(False, False)
        self.dialog.title(title)

        self.dialog.geometry("{}x{}+{}+{}".format(w,h,x1,y1,))
        self.dialog.transient(self.parent)
        self.dialog.protocol("WM_DELETE_WINDOW", self.close_dialog)

        self.lbl = Label(self.dialog, text="Help", justify='center',bg=PAGE_BG, fg=COLOR_TIT, font=FONT_T,relief = GROOVE)
        TXT_BG="#00252D"
       
        self.frame2 = Frame(self.dialog,bg=PAGE_BG,borderwidth=1,relief=RIDGE)
        self.frame2.pack(side="left",fill="both",expand=True,anchor="nw",ipadx=0, ipady=0)

        self.scrollbar = ttk.Scrollbar(self.frame2, orient="vertical")
        self.txt =Text(self.frame2, bg=TXT_BG,fg=COLOR_T,font=FONT_T,relief = GROOVE,yscrollcommand=self.scrollbar.set,cursor="arrow")
        self.txt.config(wrap="word",width=120,height=30,spacing1=5,pady=10,padx=10,selectforeground =TXT_BG)
        self.scrollbar.config(command= self.txt.yview)
        self.scrollbar.pack(side="right", fill="y",pady=(10,10))        
        self.txt.pack(side=TOP,padx=(6,0),pady=(10,10),ipadx=0,ipady=10) 

        self.f = font.Font(self.txt, self.txt.cget("font"))
        self.f.configure(weight="bold")
        self.txt.tag_config("bold", foreground="#B0AA5B", font=self.f) 
        self.ft = font.Font(self.txt, self.txt.cget("font"))
        self.ft.configure(weight="bold",size=16)
        self.txt.tag_config("title", foreground="#C1BB64", font=self.ft)
        self.txt.tag_config("hilight", foreground="#9F1B1B")   
        self.txt.tag_config("test", foreground="#3DABAF") 
        
        i=1
        for el in help_obj:
            ind=self.txt.index("end")
            ind= "{}-1 line".format(ind)
            if i==1:
                self.txt.insert("end", "{:>76}".format(help_obj["title"]))
                self.txt.tag_add("title", ind,"{}+1char lineend".format(ind))
                pass
            else:
                self.txt.insert("end", el.upper()  +"\n")
                self.txt.tag_add(el, ind,"{} + 1char lineend".format(ind))
                self.txt.tag_add("bold", ind,"{} + 1char lineend".format(ind))
                self.txt.insert("end", help_obj[el])

            self.txt.insert("end", "\n\n" )
                    
            i+=1

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar", gripcount=0,background=TXT_BG, troughcolor=PAGE_BG, lightcolor=PAGE_BG, arrowcolor="#DDDDDD", highlightcolor=TXT_BG)
        self.txt.config(state=DISABLED)       





    def addTagBold(self, ind1,ind2):
            self.txt.tag_add("bold", ind1,ind2)
            self.txt.tag_config("bold", font=self.f)


    def addTagTest(self, tag,ind1,ind2):
            self.txt.tag_add(tag, ind1,ind2)
            self.txt.tag_config(tag, foreground="#AA0000") 

    def KeyPressed(self, event):
        key = event.keysym
        if event.state == 12 and key == "g":
            pass  

    def on_click(self, event):
        pass
    def close_dialog(self):
        self.parent.wm_attributes("-disabled", False)
        self.dialog.destroy()
        self.parent.deiconify() 


    def dblclick(self,event): 
        self.select_item()


#====================================================


class GUI_window:
    def __init__(self, parent):
        self.parent = parent   
        self.parent.geometry("200x200+600+400")
        self.page1 = Frame(self.parent,bg=PAGE_BG,borderwidth=1, relief=RIDGE)
        self.page1.pack(side=TOP,fill=BOTH,expand=True,anchor=NW,ipadx=0, ipady=0,)
        self.open_but = Button(self.page1,command = self.open_dialog)
        self.open_but.configure(text="Open", width=10, bg= BUTT_BG, fg=COLOR_TIT, cursor="hand2", font = FONT_BT2)
        self.open_but.grid(row=1, column=1,sticky='nsew', padx=(60,10), pady=(83,8), ipady=0)
        self.parent.after(500, self.open_dialog)

    def open_dialog(self):
        self.dialog = helpWindow_3D(self.parent,title="3D chart help - Astronomia 3D - Popiel")


    def Exit(self):
        self.parent.destroy()               

#This is an offshoot of the program Astrologia.
help_obj={}
help_obj["title"]="Astronomia 3D help"

help_obj["About"]="""'Astronomia 3D' provides animated 3-dimensional visualizations of planets' positions relative to the horizon for a particular location at current time. E.g.: it shows which planet is visible in what part of the sky, when the Sun, Moon are rising, etc.
One can use a command line option to start the program with a chosen time, latitude and longitude (example of .bat file provided in GitHub repository https://github.com/Drozdman-1/Astronomia3D).

This program uses Swiss Ephemeris (authors: Dieter Koch and Alois Treindl) and Python extension for the Swiss Ephemeris, Pyswisseph (author: Stanislas Marquis)."""

help_obj[""]="""\u25cf To get a view of the 3D chart from a different perspective, use the mouse drag. Right and left mouse clicks on dots, texts or circles allow access to more features.
\u25cf Planet is represented by a larger dot and text.
\u25cf Left click on planet's text symbol - get info on RA, declination, ecliptic longitude, latitude (shown at the bottom).

\u25cf Left click on planet's dot - in sequence: first click - show planet's meridian, parallel, second click - show planet's meridian only, third click - show planet's parallel only, fourth click - hide all.
\u25cf Right click on planet's dot - get projected points on ecliptic, equator and horizon. Left click on projected dots to get more info.
\u25cf Right click on planet's meridian or parallel to hide one. Or use legend's item Extra off' to hide them all."""

help_obj["legend"]= """\u25cf Click on the patch next to text labels in the legend to switch on/off an item (i.g.: meridian, sphere, etc).
    Right click - switch opacity of "Horizon", "Celestial Equator", "Ecliptic", "Prime Vertical", "Meridian".
    Right click on the sphere's legend patch - hide horizon surface.
\u25cf 'Extra off' - hide all planets' projected dots (on ecliptic, equator, horizon), parallels, meridians...
\u25cf 'Show half' - in sequence: first click - show eastern hemisphere, second click - show western hemisphere, third click - show both. 
    Right click - switch opacity of the western hemisphere semi-circles and Prime Vertical, Meridian."""


help_obj["view"]= """\u25cf To move the whole figure in 3 dimensions and to get the view from particular azimuth end elevation, drag the mouse (left click) up, down, left or right. It can be also achieved by using buttons described below.
\u25cf Arrow buttons change azimuth and elevation (left click - by 10 degrees, right click - by 1 degree).
\u25cf 'View': 'E', 'W', 'N','S' - view from East, West, North, South.
\u25cf 'Azim': '0', '90', '180' - view from selected azimuth.
\u25cf 'Elev': '0', '90', '180' - view from selected elevation.
\u25cf 'View', 'Azim', 'Elev' - get azimuth and elevation.

\u25cf Checkboxes - hide planets and their points and circles.
\u25cf Combobox - hide or show selected items, points, circles of visible planets."""


help_obj["time shift"]="""\u25cf Go back or forth in time with selected number of seconds, minutes or hours.
\u25cf Date format: day-month-year.
\u25cf Right click on arrow buttons goes 1 unit (minute, second or hour) back or forth.
  Right click on 'Seconds', 'Minutes' or 'Hours' changes the time delta input to predetermined numbers: 30, 10, 1.
\u25cf 'Animation' - animate moving forward in time in chosen number of steps. Back in time - right click button or use negative sign in the time delta input.
\u25cf F1, F2 (or 1, 2) keys work like back and forth buttons"""

help_obj["buttons"]="""\u25cf 'Init' button - left click to go back to initial chart data and initial view. Right click to go back to initial view (azimuth, elevation).
\u25cf 'Chart' button - set azimuth, elevation to view the 3D chart from normal 2D natal chart perspective. Perpendicular to ecliptic.
\u25cf 'Equat' button - set azimuth, elevation to view the 3D chart from North Pole, perpendicular to celestial equator"""

help_obj["other"]= """\u25cf Clicks on Celestial Equator and Ecliptic give approximate coordinates: rectascension (RA) and longitude.
\u25cf Right click on Ecliptic point shows its projection on Equator
\u25cf "Ctrl S" - Save figure as an image.
\u25cf "Ctrl+A" save animation as a '.gif' file
\u25cf "Ctrl+D" save animation as a '.mp4' video file"""


if __name__ == "__main__":
    root = Tk()
    GUI = GUI_window(root)
    keyboard.add_hotkey('esc', GUI.Exit)
    mainloop()


