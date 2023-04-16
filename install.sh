#!/bin/bash
#ask user if they want to install dependencies, which may overwrite existing packages
echo "This script will install all dependencies for this project. This may overwrite existing packages. Do you want to continue? (y/n)"
read -r answer
if [[ "$answer" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Continuing..."
else
    echo "Exiting..."
    exit 1
fi
sudo apt install python3.8-dev python3.8 python3-pip apksigner apktool unzip openjdk-17-jdk-headless libjpeg-dev zlib1g-dev libfreetype6-dev openjdk-17-jdk docker.io -y
python3.8 -m pip install reportlab mobsfscan setuptools semgrep
sudo snap install mobsfscan

#libsast sometimes fails, do it after mobsfscan and semgrep.
python3.8 -m pip install libsast

#Checking current directory
currentdir=${PWD##*/}

if [ "$currentdir" = "IA495_MobAppSecurity" ]; then
    echo "Granting execute permissions on all repo Python scripts..."
    find . -name "*.py" -exec chmod +x {} \;
    echo "Done! You can now use kickstart.py to run the project."
else
    echo "You do not appear to be at the root of the repository."
    echo "Please navigate to the root of the repository and run `find . -name \*.py -exec chmod +x {} \\;`"
    echo "This grants all repo Python scripts execute permissions."
fi