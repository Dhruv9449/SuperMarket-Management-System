#importing libraries and modules
from os import *
from setup import *

#checks if the file with basic necessary info exists
#opens set up if it doesn't
if path.exists("SMMS.txt")==False or path.getsize("SMMS.txt")==0:
    setup()

#the main menu and program
from menus import *
main()
