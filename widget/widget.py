#Modules of clock.py for initialize the clock with the widget
from clock.clock import Clock, os
from tkinter import messagebox, mainloop
from PIL import Image
Image.CUBIC = Image.BICUBIC
from ttkbootstrap import Label, Menu, Meter, Separator, Window, Style
from ttkbootstrap.constants import *
import subprocess   #For execute the notepad


"""Class widget for the GUI and show the clock with a Label"""
class Widget:
    def __init__(self) -> None:
        """Attributes by default
            Attributes:
                bgColor (str) : For the background color in transparent
                fgColor (str) : Foreground in color white
                sizeW (int) : Width of widget
                sizeH (int) : Height of widget
                fontFamily (str) : Font of letter
                fontSize (str) : Size
                clock (Clock object) : The object clock of class Clock module
                widget (Tkinter object): The root Tkinter for the widget
                wtotal (int) : width of screen
                htotal (int) : height of screen
        """
        self.bgColor :  str = '-transparentcolor'
        self.fgColor :  str = 'white'
        self.sizeW :    int = 250
        self.sizeH :    int = 180
        self.fontFamily:str = 'Console'
        self.fontSize : str = '28'

        self.clock : Clock = Clock()
        self.clock.start()

        self.widget : Window = Window()
        self.style = Style()
        self.style.load_user_themes(os.getcwd() + '\\widget\\theme.json')
        self.style.theme_use("nightout")
        self.wtotal : int = self.widget.winfo_screenwidth()
        self.htotal : int = self.widget.winfo_screenheight()

        self.widget.overrideredirect(True) #Hide toolbar and control bar
        

        pwidth = round(self.wtotal - self.sizeW)    #Set position
        pheight = round(self.htotal - self.sizeH)
        self.widget.geometry(f'{self.sizeW}x{self.sizeH}+{pwidth}-{pheight}')

        self.widget['bg'] = 'grey'
        self.widget.attributes(self.bgColor, 'grey')    #Apply transparent in grey
        self.widget.positionfrom()
        
        self.text_time : Label = Label(self.widget, text='', font=f'{self.fontFamily} {self.fontSize}', padding=(20, 10))
        self.separator: Separator = Separator(self.widget, bootstyle="info")
        self.text_ram : Label = Label(self.widget, text='RAM', font='Verdana 8 bold')
        self.text_cpu : Label = Label(self.widget, text='CPU', font='Verdana 8 bold')
        self.text_temperature : Label = Label(self.widget, text='TMP', font='Verdana 8 bold')
        self.text_space : Label = Label(self.widget, text='SPC', font='Verdana 8 bold')
        self.text_porcent_ram : Label = Label(self.widget, text='25%', font='Verdana 8 bold')
        self.text_porcent_cpu : Label = Label(self.widget, text='25%', font='Verdana 8 bold')        
        self.text_porcent_space : Label = Label(self.widget, text='25%', font='Verdana 8 bold')
        self.text_porcent_temperature : Label = Label(self.widget, text='25°', font='Verdana 8 bold')

        self.ram: Meter = Meter(self.widget, metersize=40, meterthickness=5, stripethickness=5, padding=0,amountused=25 ,metertype="full", bootstyle="info", showtext=False)
        self.cpu: Meter = Meter(self.widget, metersize=40, meterthickness=5, stripethickness=5, padding=0,amountused=25 ,metertype="full", bootstyle="info", showtext=False)
        self.temperature: Meter = Meter(self.widget, metersize=40, meterthickness=5, stripethickness=5, padding=0,amountused=25 ,metertype="full", bootstyle="info", showtext=False)
        self.space: Meter = Meter(self.widget, metersize=40, meterthickness=5, stripethickness=5, padding=0,amountused=25 ,metertype="full", bootstyle="info", showtext=False)

        #Menu with click right
        self.menu : Menu = Menu(self.text_time, tearoff=0)
        self.menu.add_command(label="Configurations", command=self.open_config)
        self.menu.add_command(label="Close", command=self.widget.destroy)
        
        #Events
        self.widget.bind("<Enter>", self.on_enter)    #Change bgColor Label
        self.text_time.bind("<Enter>", self.on_enter) 
        self.widget.bind("<Leave>", self.on_leave)
        self.text_time.bind("<Leave>", self.on_leave)

        self.widget.bind("<Button-3>", self.do_popup) #Menu
        self.text_time.bind("<Button-3>", self.do_popup)

    def on_enter(self, event) -> None:
        self.widget.configure(background="black")
        self.text_time.configure(background="black")

    def on_leave(self, event) -> None:
        self.widget.configure(background="grey")
        self.text_time.configure(background="grey")
    
    def do_popup(self, event) -> None:  #Show menu in the position x and y of mouse
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def open_config(self) -> None:  #Open configurations with notepad
        if self.clock.get_config():
            subprocess.call(['notepad.exe', self.clock.file_cfg])
            messagebox.showinfo(title='Information!', message='Configuration ready!!!')
            self.clock.end()
            self.clock.start()
        else:
            messagebox.showerror(title='Error', message='Not found config file: ' + self.clock.file_cfg)

    #Uppdate times
    def update(self) -> None:
        h = self.clock.show_time()['hours']
        m = '0' + str(self.clock.show_time()['minutes']) if self.clock.show_time()['minutes'] < 10 else self.clock.show_time()['minutes']
        s = self.clock.show_time()['seconds']
        ap = self.clock.show_time()['ap']
        self.time = str(h) + ':' + str(m) + s + ap
        self.text_time.configure(text=self.time) 
        self.widget.after(900,self.update)

    #Initializer
    def init(self) -> None:
        self.text_time.grid(row=0, column=0, columnspan=4)
        self.text_ram.grid(row=1, column=0)
        self.text_cpu.grid(row=1, column=1)        
        self.text_space.grid(row=1, column=2)
        self.text_temperature.grid(row=1, column=3)
        self.ram.grid(row=2, column=0)
        self.cpu.grid(row=2, column=1)
        self.space.grid(row=2, column=2)        
        self.temperature.grid(row=2, column=3)        
        self.text_porcent_ram.grid(row=3, column=0)
        self.text_porcent_cpu.grid(row=3, column=1)        
        self.text_porcent_space.grid(row=3, column=2)
        self.text_porcent_temperature.grid(row=3, column=3)
        self.update()
        mainloop()
