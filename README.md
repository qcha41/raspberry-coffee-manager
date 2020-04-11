# Raspberry Coffee Manager [DEV AND DOCS IN PROGRESS]

This is a raspberry project to manage a shared coffee caps stock in a group in an original way, using in particular a user-friendly touchscreen graphical interface, and a RFID tag reader.

## Features

- **User accounts**: The basic principle of this system is that users notify the system each time they take a coffee caps from the group stock. This is done simply by passing their personal RFID tags near an integrated reader, or by selecting their name on the main panel. The corresponding caps price is then deducted from their own virtual account. The users can recharge their accounts by putting some money in a common group box (or any other method decided in the group), and notify themselves this recharge in the account panel of the graphical interface. In this panel, they can also review the activity of their account day by day, change their name, link their account with another RFID tag, etc.. Finally, to avoid negative accounts, a warning is sent automatically by email to the users whose the account's balance is negative, and their name are listed in the main panel of the graphical interface.

- **Admin panel**: The person in charge of managing the coffee in the group has access to a private admin panel, either by using its admin RFID tag, or by entering a password in the graphical interface. From that panel, the admin can review users operations (ex : account recharges), notify a group caps purchase, a supply purchase, or that some caps are missing in the stock, etc...

- **Dynamical caps price**: The system thus know how many caps have been added in the stock by the admin, and how many were taken by the users. The caps price that is deducted from the virtual accounts is then dynamic, and is simply calculated by dividing the remaining system charges by the remaining number of caps.

- **Charities donations**: More than just managing a caps stock, this project also represents a tool to raise money for charities in a group easily. In their account panel, users can indeed configure an optional automatic donation (a few cents), which is then deducted on their virtual account in addition of the caps price, each time they take a caps from the stock. In parallel, users can also proceed in their account panel to a one-shot donation of the amount of their choice, which is then deducted from their virtual account. The global amount of money raised by all users is they donated by the admin to a real charity (defined by the group), and notified in the admin panel.

- **Shares**: In order to keep a sufficient working capital for the admin of the group, each user is invited to add shares to the system at the creation of its virtual account. These shares are a refoundable amount of money, that does not appear in the account balance. They help the admin of the system to buy caps in advance and maintain a sufficiently large caps stock. The users without shares are listed in the main panel of the graphical interface.

- **Secondary features**: The system integrates a LED strip whose the color is changing dynamically depending on the scenario (idle, green for positive balance, blinking red for negative balance..). Using a PIR sensor, the system automatically wakes up (turn on screen + led strip) when someone approaches the system and go back to sleep after 1 minute of inactivity.


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

#### Assembling and wiring

### Raspberry configuration

## Python dependencies
## System configuration
## Installation
## Configuration
