//Installer of widget clock

//Headers
#include <stdio.h>
#include <stdlib.h>

//Constants
#define PATH "\"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"
#define VERSION "1.1.1v"
#define PROGRAM "widget-clock-" VERSION ".exe\""
#define COMMAND_MOVE "move widget-clock-1.1.1v.exe " PATH "\""
#define COMMAND_START PATH "\\" PROGRAM

void main(){
    system(COMMAND_MOVE);
    system(COMMAND_START);
}