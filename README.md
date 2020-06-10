# Raspberry Coffee Manager [DEV AND DOCS IN PROGRESS]

This is a raspberry project dedicated to the management of a shared coffee caps stock in a group, using in particular a user-friendly touchscreen interface, and a RFID tag reader.

## Features

- **User accounts**: The basic idea of this system is that users notify the raspberry manager each time they take a coffee caps from the group stock. This is done simply by passing their personal RFID tags near an integrated reader, or by selecting their name on the main screen. The corresponding caps price is then deducted from their personal virtual account. The users can recharge their accounts by putting some money in a common group box (or any other method decided in the group), and notify themselves this recharge in the account panel of the graphical interface. In this panel, they can also review the activity of their account day by day, change their name, link their account with another RFID tag, etc. Users also receive email notifications when their accounts are negative.

- **Admin panel**: The person in charge of managing the coffee in the group has access to a private admin panel, either by using its admin RFID tag, or by entering a password in the graphical interface. From that panel, the admin can review system operations (users recharges, ...), notify a group caps purchase, a supply purchase, or that a few caps are missing in the stock, etc.

- **Dynamical caps price**: The system thus know how many caps have been added in the stock by the admin, and how many were taken by the users. The caps price deducted from the virtual accounts is then dynamic, and is simply calculated by dividing the remaining system charges by the remaining number of caps.

- **Charities donations**: More than just managing a caps stock, this project is also a tool to raise money for charities in a group easily. In their account panel, users can indeed configure an optional automatic donation (a few cents), which is then deducted on their virtual account in addition of the caps price, each time they take a caps from the stock. In parallel, users can also proceed to manual donations in their account panel. The global amount of money raised by all users is they donated by the admin to a real charity (defined by the group), and notified in the admin panel.

- **Shares**: After having created their accounts, users are invited to add a certain amount of money in the system, as shares, in order to keep a sufficient working capital that will help the admin of the group to buy caps in advance, and to maintain a sufficiently large caps stock. Unlike the recharges, the shares do not impact in the account balance : they just act as a hidden offsets, and are refundable at any time (for instance when a user leave the group).

- **Secondary features**: The system integrates a LED strip whose the color is changing dynamically depending on the scenario (idle, green for positive balance, blinking red for negative balance..). Using a PIR sensor, the system automatically wakes up (turn on screen + led strip) when someone approaches the system, and goes back to sleep after 1 minute of inactivity.

## Technical stuf

- The graphical interface opens at Pi startup using cron.
- The system requires an internet connection (Ethernet/Wifi) to sync date and time (the raspberry doesn't include an RTC module).
- 

## Fabrication

### Electronic circuit

#### Parts used

- Raspberry Pi 3B+ (https://www.raspberrypi.org/)
<p align="center"><img src="/docs_ressources/raspberry.jpg" width="300"/></p>

- EYEWINK 7" Touchscreen 1024x600 HDMI (https://fr.aliexpress.com/item/32805673182.html)
<p align="center"><img src="/docs_ressources/touchscreen.jpg" width="300"/></p>

- Buzzer piezo 5V (https://fr.aliexpress.com/item/32322485389.html)
<p align="center"><img src="/docs_ressources/buzzer.jpg" width="300"/></p>

- RFID module RC522 13.56 Mhz (https://fr.aliexpress.com/item/2026446641.html)
<p align="center"><img src="/docs_ressources/rfid.jpg" width="300"/></p>

- RBG LED strip SMD 5050 5V (https://fr.aliexpress.com/item/32812049944.html)
<p align="center"><img src="/docs_ressources/led.jpg" width="300"/></p>

- 3 TIP120 power transistors (https://fr.aliexpress.com/item/32264482219.html)
<p align="center"><img src="/docs_ressources/tip120.jpg" width="300"/></p>

- PIR motion sensor HC-SR501 (https://fr.aliexpress.com/item/1874954952.html)
<p align="center"><img src="/docs_ressources/pir.jpg" width="300"/></p>

- 5V / 3A DC power adaptor (https://www.amazon.fr/BERLS-dalimentation-Adaptateur-connecteurs-r%C3%A9sidentielle/dp/B076Y23T5Z)
<p align="center"><img src="/docs_ressources/power_adaptor.jpg" width="300"/></p>

- Female DC power connector (https://fr.aliexpress.com/item/32822006069.html)
<p align="center"><img src="/docs_ressources/power_jack.jpg" width="300"/></p>

- Wires

#### Assembling and wiring

### Raspberry configuration

1. Install Python >= 3.6 (https://liftcodeplay.wordpress.com/2017/06/30/how-to-install-python-3-6-on-raspbian-linux-for-raspberry-pi/)
2. Create an alias python3 for python3.6 (https://debian-facile.org/doc:programmation:bash:alias)
2. Install this project
```
mkdir coffee_manager        # Create main folder
git clone https://github.com/qcha41/raspberry-coffee-manager.git     # Clone GitHub project
git clone https://github.com/richardghirst/PiBits.git                # Clone PiBits

```
3. 

## Python dependencies
## System configuration
## Installation
## Configuration
