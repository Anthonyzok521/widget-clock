#Modulo for access the system and using color for the debuging
import os
import time
import datetime
from colorama import Fore, init

#Initialize colorama
init()

#Default forecolor
Fg = Fore.GREEN
Fr = Fore.RED
Fy = Fore.YELLOW


"""Class Clock for the time"""
class Clock:
    def __init__(self) -> None:
        self.path:     str  = os.path.join('C:\\Users',os.getenv('USERNAME'), 'WidgetClock')
        self.file_cfg: str  = os.path.join(self.path, 'config.cfg')    
        self.configs:  list = []
        self.active:   bool = True

    def start(self) -> None:
        """print(Fg + 'Starting...')"""
        self.get_config()
        
        """print(self.configs)"""
        
        while self.active:
            time_now = time.localtime()
            print(time_now.tm_hour, time_now.tm_min, time_now.tm_sec)

    def get_config(self) -> bool:
        """Get configurations for the clock
            Variables:
                path (str) : Is the path of Appdata Windows
                file_cfg (str) : Is the path file of configuration
        """
        folder_exist : bool = True
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            folder_exist = False

        if not os.path.exists(self.file_cfg) or not folder_exist:
            """print(Fr + 'config.cfg not is created...')"""
            with open(self.file_cfg, 'x') as config:
                """print(Fy + 'Creating...')"""
                config.write('#config WidgetClock\n')
                config.write('[hour_24] False\n')
                config.write('[seconds] False\n')
                """print(Fg + 'Created in', self.file_cfg)"""
            return False
        
        """print(Fg + 'config.cfg created...')"""
        
        configs = ''

        with open(self.file_cfg, 'r') as config:
                configs = ''.join(config.readlines()) 
        
        self.configs    = configs.split('\n') 
        h24: bool       = not(self.configs[1].endswith('False'))
        seconds: bool   = not(self.configs[2].endswith('False'))

        self.configs = [h24, seconds]
        return True
    
    def set_config(self, h24=False, seconds=False) -> bool:
        if not self.get_config():
            with open(self.file_cfg, '+w') as config:
                config.write('#config WidgetClock\n')
                config.write(f'[hour_24] {h24}\n')
                config.write(f'[seconds] {seconds}\n')
    
    def end(self):
        self.active = False

#Debuging
"""Show time now"""
if __name__ == '__main__':
    Clock().start()
    print(Fore.RESET)
    