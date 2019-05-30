#!/usr/bin/python3
# File name   : setup.py
# Description : RaspTank Setup Script
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : Shaun Longworth
# Date        : 2019/05/30
 
import os
import time
import sys
 
autostart_dir = "/home/pi/.config/autostart"
autostart_file = autostart_dir + "/car.desktop"
install_dir = "/home/pi/Adeept_RaspTank/server"
 
# Commonly used functions
def replace_num(file,initial,new_num): 
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)
 
def run_os_command(cmd, max_runs=4):
    try:
        sys.stdout.write('###################################################\n')
        sys.stdout.write('Command: ' + cmd + '\n')
        for x in range(0,max_runs):
            if os.system(cmd) == 0:
                break
    except:
        print('AN ERROR OCCURRED RUNNING THE FOLLOWING COMMAND: ' + cmd)
        pass
 
def create_autostart():
    try:
        if (not os.path.exists(autostart_dir)):
            run_os_command("sudo mkdir '" + autostart_dir + "/'", 1)
        if (not os.path.isfile(autostart_file)):
            run_os_command("sudo touch " + autostart_file, 1)
        
        with open(autostart_file,'w') as file_to_write:
            file_to_write.write("[Desktop Entry]\n   Name=Car\n   Comment=Car\n   Exec=sudo python3 " + install_dir + "/server.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true")
    except:
        print('Autostart failed.  Please try again')
        pass
 
def upgrade_system():
    # Upgrade the existing system
    run_os_command("sudo apt-get update")
    run_os_command("sudo apt-get purge -y wolfram-engine")
    run_os_command("sudo apt-get purge -y libreoffice*")
    run_os_command("sudo apt-get -y clean")
    run_os_command("sudo apt-get -y autoremove")
    run_os_command("sudo apt-get -y upgrade")
 
def install_car():
    # Enable the interface(s)
    try:
        replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
    except:
        pass
   
    # Prepare to install.  Clean & Update the repositories
    run_os_command("sudo apt-get clean")
    run_os_command("sudo apt-get update")
    
    # Install the new software
    run_os_command("sudo apt-get install -y i2c-tools")
    run_os_command("sudo pip3 install adafruit-pca9685")
    run_os_command("sudo pip3 install rpi_ws281x")
    run_os_command("sudo pip3 install -U pip")
    run_os_command("sudo pip3 install numpy")
    run_os_command("sudo pip3 install opencv-contrib-python")
    run_os_command("sudo apt-get install -y libhdf5-dev")
    run_os_command("sudo apt-get install -y libhdf5-serial-dev")
    run_os_command("sudo apt-get install -y build-essential pkg-config")
    run_os_command("sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev")
    run_os_command("sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev")
    run_os_command("sudo apt-get install -y libgtk2.0-dev libatlas-base-dev gfortran")
    run_os_command("sudo apt-get install -y libqtgui4 python3-pyqt5 libqt4-test")
    run_os_command("sudo pip3 install imutils zmq pybase64 psutil")
 
    # Create the Access Point
    run_os_command("git clone https://github.com/oblique/create_ap.git")
    run_os_command("cd //home/pi/create_ap && sudo make install", 1)
 
    # Download, build & Install Sphinxbase & PocketSphinx
    run_os_command("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq")
     
    # Set up the autostart, move the config file accordingly
    create_autostart()
    run_os_command("sudo cp -f " + install_dir + "/config.txt /home/pi/config.txt", 1)
 
def reboot_system():
    # Reboot the server to have the changes take effect
    run_os_command("sudo reboot")
 
while True:
    try:
        selection = int(input("Select an option:\n    1 = Upgrade OS;\n    2 = Install Car;\n    3 = Reboot;\n    4 = Exit\n\nOption to select: "))
        
        if selection == 1:
            upgrade_system()
            sys.stdout.write('###################################################\n')
            sys.stdout.write('IT IS RECOMMENDED YOU REBOOT BEFORE CONTINUING.....\n')
            sys.stdout.write('###################################################\n')
        elif selection == 2:
            install_car()
        elif selection == 3:
            reboot_system()
        elif selection == 4:
            break
        else:
            print("Invalid selection.  Please try again")   
    except:
        print("Invalid selection.  Please try again")
        pass
