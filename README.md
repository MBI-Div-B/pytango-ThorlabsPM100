# pytango-ThorlabsPM100

# Installation
install Thorlabs PM100 package from PyPi.org
`pip3 install ThorlabsPM100`

add special usb udev rule to `/etc/udev/rules.d/50-usbcom.rules`
```
KERNEL=="usbtmc*", ATTRS{idVendor}=="1313", ATTRS{idProduct}=="807b", ATTRS{serial}=="17102335", SYMLINK+="usbThorlab$
SUBSYSTEMS=="usb", ATTRS{manufacturer}=="Thorlabs", MODE="0666"
```

