#Cd to views folder (where html page is stored)
cd /home/deployer/apps/cau/current/app/views

#Remove old pages folder
rm -rf pages

#Clone git hub with new information
git clone https://github.com/oriolxi/pages

#give execution permission to update.sh
chmod +x pages/update.sh

#Remove old sc2018 folder
rm -rf /home/deployer/apps/cau/current/public/sc2018

#Copy new sc2018 directory
cp -r pages/sc2018 /home/deployer/apps/cau/current/public/sc2018

#We finally reboot the system to make changes online
reboot
