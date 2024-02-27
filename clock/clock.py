#Modulo for access the system and using color for the debuging
import os
import time
from colorama import Fore, init

#Initialize colorama
init()

#Default forecolor
Fg = Fore.GREEN
Fr = Fore.RED
Fy = Fore.YELLOW


"""Class Clock for the time"""
class Clock:
    """Initialize the attributes of clock"""
    def __init__(self) -> None:
        """Default configurations for the clock
            Attributes:
                path (str) : Is the path of User Windows
                file_cfg (str) : Is the path file of configuration
                configs (list) : All settings in list
                active (boolean) : Is active or not
                time (None) : This is for show the clock
        """
        self.path:     str  = os.path.join('C:\\Users',os.getenv('USERNAME'), 'WidgetClock')
        self.file_cfg: str  = os.path.join(self.path, 'config.cfg')    
        self.configs:  list = []
        self.active:   bool = False
        self.time: dict = None

    """Start clock"""
    def start(self) -> None:
        if self.get_config():
            self.active = True  
        else:
            self.active = False

    def get_config(self) -> bool:
        """Get configurations for the clock
            Variables:
                folder_exist (boolean) : Verify the folder
                config (str) : Setter configurations
        """
        folder_exist : bool = True
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            folder_exist = False

        if not os.path.exists(self.file_cfg) or not folder_exist:
            print(Fr + 'config.cfg not is created...')
            with open(self.file_cfg, 'x') as config:
                print(Fy + 'Creating...')
                config.write('#config WidgetClock\n')
                config.write('[hour_24] False\n')
                config.write('[seconds] False\n')
                print(Fg + 'Created in', self.file_cfg)
            return False
        
        """print(Fg + 'config.cfg created...')"""
        
        configs = ''

        with open(self.file_cfg, 'r') as config:
            configs = ''.join(config.readlines()) 
        
        self.configs    = configs.split('\n') 
        h24: bool       = not(self.configs[1].endswith('False')) #if is False change to True
        seconds: bool   = not(self.configs[2].endswith('False'))

        self.configs = [h24, seconds]
        return True
    
    def set_config(self, h24=True, seconds=True) -> bool:
        """Default is 24 hours with seconds [True, True]"""
        if self.get_config():
            with open(self.file_cfg, '+w') as config:
                config.write('#config WidgetClock\n')
                config.write(f'[hour_24] {h24}\n')
                config.write(f'[seconds] {seconds}\n')

    def show_zero_seconds(self, sec: str) -> str:
        return ':0'+ sec if int(sec) < 10 else ':' + sec

    def show_time(self):
        """How show the time with 24 hours or 12 hours, secconds o no secconds
            Variables:
                time_shape (dictionary) : Shapes of show the time
        """
        self.time = dict([
            ("h24", time.strftime("%H")), 
            ("h12", time.strftime("%I")),
            ("min", time.strftime("%M")),
            ("sec", time.strftime("%S")),
            ("locale", time.strftime("%p"))
            ])
        
        #list(map(lambda x: int(x), time.strftime("%H%I:%M:%S%p").split(':')))
        
        if self.active == True:
            time_shape = {
                'h24-sec': {
                    'hours':    self.time['h24'], 
                    'minutes':  self.time['min'], 
                    'seconds':  self.show_zero_seconds(self.time['sec']),
                    'ap' : '' 
                    },
                'h24-nosec': {
                    'hours':    self.time['h24'], 
                    'minutes':  self.time['min'], 
                    'seconds':  '',
                    'ap' : ''  
                    },
                'h12-sec': {
                    'hours':    self.time['h12'],
                    'minutes':  self.time['min'], 
                    'seconds':  self.show_zero_seconds(self.time['sec']),
                    'ap' : self.time['locale']
                    },
                'h12-nosec': {
                    'hours':    self.time['h12'],
                    'minutes':  self.time['min'], 
                    'seconds':  '',
                    'ap' : self.time['locale']
                    },
                }
            
            #Return a shape of the configuration
            match self.configs:
                case [True, True]:
                    return time_shape['h24-sec']
                case [True, False]:
                    return time_shape['h24-nosec']
                case [False, True]:
                    return time_shape['h12-sec']
                case [False, False]:
                    return time_shape['h12-nosec']

        else:
            return 'Not is active'

    def end(self):
        self.active = False

#Debuging
"""Show time now"""
if __name__ == '__main__':
    clock = Clock()
    print(Fg + 'Starting...')
    #clock.set_config(seconds=True)
    clock.start()
    print(Fore.RESET)
    print(clock.show_time())