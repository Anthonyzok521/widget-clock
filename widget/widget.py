#Modules of clock.py for initialize the clock with the widget
from clock.clock import Clock
from tkinter import messagebox, Label, Tk, Menu, mainloop
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
        self.sizeW :    int = 200
        self.sizeH :    int = 100
        self.fontFamily:str = 'Console'
        self.fontSize : str = '28'

        self.clock : Clock = Clock()
        self.clock.start()

        self.widget : Tk = Tk()
        self.wtotal : int = self.widget.winfo_screenwidth()
        self.htotal : int = self.widget.winfo_screenheight()

        self.widget.overrideredirect(True) #Hide toolbar and control bar
        

        pwidth = round(self.wtotal - self.sizeW)    #Set position
        pheight = round(self.htotal - self.sizeH)
        self.widget.geometry(f'{self.sizeW}x{self.sizeH}+{pwidth}-{pheight}')

        self.widget['bg'] = 'grey'
        self.widget.attributes(self.bgColor, 'grey')    #Apply transparent in grey
        self.widget.positionfrom()
        
        self.text : Label = Label(self.widget, text='', font=f'{self.fontFamily} {self.fontSize}', bg='grey', fg=self.fgColor, pady=20, padx=20)

        #Menu with click right
        self.menu : Menu = Menu(self.text, tearoff=0)
        self.menu.add_command(label="Configurations", command=self.open_config)
        self.menu.add_command(label="Close", command=self.widget.destroy)
        
        #Events
        self.text.bind("<Enter>", self.on_enter)    #Change bgColor Label
        self.text.bind("<Leave>", self.on_leave)

        self.text.bind("<Button-3>", self.do_popup) #Menu

    def on_enter(self, event) -> None:
        self.text.configure(bg="black")

    def on_leave(self, event) -> None:
        self.text.configure(bg="grey")
    
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
        self.text.configure(text=self.time) 
        self.widget.after(900,self.update)

    #Initializer
    def init(self) -> None:
        self.text.pack()
        self.update()
        mainloop()
