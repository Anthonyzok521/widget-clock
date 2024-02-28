#Modules of clock.py for initialize the clock with the widget
from clock.clock import Clock, os
from diagnostics.diagnostics import Diagnostics
from tkinter import messagebox, mainloop
from PIL import Image
Image.CUBIC = Image.BICUBIC
from ttkbootstrap import Frame, Label, Menu, Meter, Separator, Window, Style
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
        self.sizeW :    int = 270
        self.sizeH :    int = 180
        self.fontFamily:str = 'Console'
        self.fontSize : str = '28'

        self.clock : Clock = Clock()
        self.diagnostics = Diagnostics()
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

        self.frame_time : Frame = Frame(self.widget, width=270, height=60)
        self.frame_diagnostic : Frame = Frame(self.widget, width=270, height=60)
        
        self.text_time : Label = Label(self.frame_time, text='', font=f'{self.fontFamily} {self.fontSize}')
        self.separator: Separator = Separator(self.frame_diagnostic, bootstyle="info")
        self.text_ram : Label = Label(self.frame_diagnostic, text='RAM', font='Verdana 8 bold')
        self.text_cpu : Label = Label(self.frame_diagnostic, text='CPU', font='Verdana 8 bold')
        self.text_temperature : Label = Label(self.frame_diagnostic, text='TMP', font='Verdana 8 bold')
        self.text_space : Label = Label(self.frame_diagnostic, text='SPC', font='Verdana 8 bold')
        self.text_porcent_ram : Label = Label(self.frame_diagnostic, text='', font='Verdana 8 bold')
        self.text_porcent_cpu : Label = Label(self.frame_diagnostic, text='', font='Verdana 8 bold')        
        self.text_porcent_space : Label = Label(self.frame_diagnostic, text='', font='Verdana 8 bold')
        self.text_porcent_temperature : Label = Label(self.frame_diagnostic, text='', font='Verdana 8 bold')

        self.ram: Meter = Meter(self.frame_diagnostic, metersize=40, meterthickness=3, stripethickness=3, padding=0,amountused=0 ,metertype="full", bootstyle="info", showtext=False)
        self.cpu: Meter = Meter(self.frame_diagnostic, metersize=40, meterthickness=3, stripethickness=3, padding=0,amountused=0 ,metertype="full", bootstyle="info", showtext=False)
        self.temperature: Meter = Meter(self.frame_diagnostic, metersize=40, meterthickness=3, stripethickness=3, padding=0,amountused=0 ,metertype="full", bootstyle="info", showtext=False)
        self.space: Meter = Meter(self.frame_diagnostic, metersize=40, meterthickness=3, stripethickness=3, padding=0,amountused=0 ,metertype="full", bootstyle="info", showtext=False)

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

    def bootstyle(self, ram, cpu, space, temperature) -> None:
        if ram > 0 and ram < 50:
            self.ram.configure(bootstyle="info")
        elif ram >= 50 and ram < 80:
            self.ram.configure(bootstyle="warning")
        else:
            self.ram.configure(bootstyle="danger")
        
        if cpu > 0 and cpu < 50:
            self.cpu.configure(bootstyle="info")
        elif cpu >= 50 and cpu < 80:
            self.cpu.configure(bootstyle="warning")
        else:
            self.cpu.configure(bootstyle="danger")

        if space > 0 and space < 50:
            self.space.configure(bootstyle="info")
        elif space >=50 and space < 80:
            self.space.configure(bootstyle="warning")
        else:
            self.space.configure(bootstyle="danger")
        
        if temperature > 0 and temperature < 50:
            self.temperature.configure(bootstyle="info")
        elif temperature >= 50 and temperature < 80:
            self.temperature.configure(bootstyle="warning")
        else:
            self.temperature.configure(bootstyle="danger")

    #Uppdate times
    def update(self) -> None:
        h = self.clock.show_time()['hours']
        m = self.clock.show_time()['minutes']
        s = self.clock.show_time()['seconds']
        ap = self.clock.show_time()['ap']

        ram = self.diagnostics.ram()
        cpu = self.diagnostics.cpu()
        space = self.diagnostics.space()
        temperature = self.diagnostics.temperature()

        self.bootstyle(ram, cpu, space, temperature)

        self.time = h + ':' + m + ':' + s + ap
        self.text_time.configure(text=self.time) 

        self.ram.configure(amountused=ram)
        self.text_porcent_ram.configure(text=f'{ram}%')

        self.cpu.configure(amountused=cpu)
        self.text_porcent_cpu.configure(text=f'{cpu}%')

        self.space.configure(amountused=space)
        self.text_porcent_space.configure(text=f'{space}%')

        self.temperature.configure(amountused=temperature)
        self.text_porcent_temperature.configure(text=f'{temperature}%')

        self.widget.after(900,self.update)

    #Initializer
    def init(self) -> None:
        self.frame_time.pack()
        self.frame_diagnostic.pack()
        self.text_time.pack(expand=True)
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
