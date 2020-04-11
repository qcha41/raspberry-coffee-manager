# Raspberry Coffee Manager [DEV AND DOCS IN PROGRESS]

This is a raspberry project to manage a shared coffee caps stock in a group in an original way. 

Using personal RFID tags, users can manage their own accounts (notify caps conso, add money, review their account activity, ...) through a user-friendly interface. When taking a coffee caps from the shared caps stock, users also notify it to the system, which deduct the associated price from their account. This price is dynamic, and is calculated using the number of remaining caps in the shared stock, and the costs declared to the system by the person in charge of buying caps for the group. This person can manage the system through a prviate admin panel. Users can add money in their acccount in two different way: the recharges (to pay daily coffee when notifying a conso) and the shares (to maintain a sufficient working capital for the administrator). Moreover, users can optionally configure a automatic charity donation (a few cents) that will be deducted additionally each time they notify a conso. Once a sufficient amount has been gathered from all users, the administrator can proceed to the real donation to a charity of the group's choice, and declare it in the admin panel.

From one side, the admin notify the manager when new caps are added in the stock (quantity and price). From the other side, each user has an account. Using a personal RFID tag, they notify the manager when they add money in their accounts and when they take a coffee caps from the stock, which deduct a dynamic caps price in their account. If they want, they can also configure an automatic charity donation deducted from their account each time they take a coffee caps.

## Main features
- User account panel for adding conso, recharging user account / adding shares, review account activity day by day, managing user informations (name, email, ...). Accessible through user's RFID tag or GUI buttons.
- Users email notification if their account balance goes below 0€.
- Optional automatic charity donation.
- Admin panel for caps stock and account management (add/remove caps and costs, supplies costs, charity donations, check new users recharges/shares). Accessible through admin's RFID tag or GUI buttons + password.
- System wake up when someone approchaes, using a PIR sensor.
- LED strip whose color is changing dynamically depending on the scenario.

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
