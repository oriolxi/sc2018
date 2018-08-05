#Cd to views folder (where html page is stored)
cd /home/deployer/apps/cau/current/app/views

#Remove old pages folder
sudo rm -rf pages

#Clone git hub with new information
git clone https://github.com/oriolxi/sc2018 pages

#give execution permission to update.sh
sudo chmod +x pages/update.sh

#Remove old sc2018 folder
sudo rm -rf /home/deployer/apps/cau/current/public/sc2018_files

#Copy new sc2018 directory
sudo cp -r pages/sc2018_files /home/deployer/apps/cau/current/public/sc2018_files

#We finally reboot the system to make changes online
sudo reboot
