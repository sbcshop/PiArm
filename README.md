# PiArm

PiArm is a Raspberry Pi based DIY robotic arm outfitted with 6-axis digital computerized servo motors and 360 degrees of rotation liberation designed and developed for kids, makers, and techies.

**Steps for PiArm software installation:**
1. Open Terminal and download the code by writing:

   ```
   git clone https://github.com/sbcshop/PiArm.git
   ```

2. Your code will be downloaded to '/home/pi' directory. Use 'ls' command to check the list of directories.

3. Go to directory 'PiArm' and run the command to change the permissions of 'configGUI' and 'controlGUI' python files:
   ```
   sudo chmod +x configGUI.py controlGUI.py
   ```
   You are now able to run these two softwares for your PiArm. The control software is to control the movements of PiArm, while the config software is to config the servo motor.

4. Click on the 'Servo Config' shortcut icon to configure your motor, or if you wish to give movements to PiArm or control it, click on the 'PiArm' shortcut icon.

5. You can also move these 2 icons to your desktop for your convinience.
<img src="https://sb-components.co.uk/assets/images/bg/desk.png" width="800">

# PiArm with LCD
One of the variants of PiArm has a LCD mounted on its chest. You can configure this screen using few simple steps.

**Steps for LCD configuration**
1. Open terminal and go to the PiArm directory and type
   ```
   cd LCD-show
   chmod +x LCD4-show LCD-hdmi
   ```

2. Now you would require to rotate your screen to the viuewing angle. Write

   ```
   ./LCD4-show 180
   ```

After you enter this command, your system will ask you for reboot. Enter 'y' and reboot your Pi.

3. While your system is rebooting, you will have to connect the HDMI and MicroUSB Cable.

Note: In case you see your screen resolutions distorted, you just have to press the on/off button the the LCD screen at its back. This will restore its resolution then.

   If you wish to return back to the HDMI, enter

   ```./LCD-hdmi```

<img src="https://sb-components.co.uk/assets/images/bg/terminal.png" width="800">

# PiArm Tutorial links

**Servo Config**

<a href="https://www.youtube.com/watch?v=leC8J0xXyqc&t=1s" target="_blank"><img src="https://cdn.shopify.com/s/files/1/1217/2104/files/piarm-banner_1024x1024.jpg?v=1556623276" alt="PiArm servo config tutorial video" width="800" /></a>


**PiArm Control Software**

<a href="https://www.youtube.com/watch?v=jwRVcIw8pus" target="_blank">
<img src="https://cdn.shopify.com/s/files/1/1217/2104/files/vlcsnap-2019-04-30-15h44m01s9_1024x1024.png?v=1556619752" alt="PiArm control tutorial video" width="800" />
</a>



# Buy Link

SB Shop <a href="https://shop.sb-components.co.uk/products/piarm-the-diy-robotic-arm-for-raspberry-pi" target="_blank">https://shop.sb-components.co.uk/products/piarm-the-diy-robotic-arm-for-raspberry-pi</a>
