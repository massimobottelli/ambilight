# ambilight

Software in Python to capture image via webcam, extract dominant color and control a RGB LED strip via Raspberry Pi GPIO ports.

gpiod must be installed and running on RPi

```
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
```

Connections

RPi PIN: R = 17; G = 22; B = 24; 5V = 2; GND = 6

3x MOSFET IRLZ44N: PIN 1 (L) = to RPi (R/G/B); PIN 2 (M) = to LED (R/B/B); PIN 3 (R)  = to GND


More info on https://massimobottelli.it/coding/diy-ambilight/
