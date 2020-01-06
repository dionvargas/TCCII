echo "## Atualizando sistema ##"
sudo apt-get update
sudo apt-get upgrade

echo "## Instalando dependencias ##"
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran

echo "## Instalando Python3 ##"
sudo apt-get install python3-dev
sudo apt-get install python3-pip

echo "## Instalando Opencv e outas bibliotecas##"
pip3 install numpy
pip3 install opencv-python
pip3 install picamera	
pip3 install Pillow
pip3 install matplotlib

echo "## Instalando dependencias da camera ##"
sudo apt-get install libqtgui4
sudo modprobe bcm2835-v4l2
sudo apt-get install libqt4-test

echo "## Instalando MP4Box"
sudo apt-get install gpac

echo "## Instalando Samba ##"
sudo apt-get install samba
mkdir /home/pi/Compartilhada
chmod 777 /home/pi/Compartilhada