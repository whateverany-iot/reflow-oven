# The no-hardware-mod necessary reflow oven
This project is for a "no-hardware-mod" necessary solder reflow toaster oven. The idea is to avoid making changes to the oven hardware, by using an off the shelf wifi smart-plug running tasmoda. This might help cover your backside if things go wrong. Should the thing catch on fire - at least you didn't crack open the oven to add a cheap relay.

The smart-plug will be controlled via a service which will turn off/on the oven using MQTT. Temperature will be monitored using a separate ESP8266 microcontroller, which will simply publish the environment sensor values to MQTT over wifi.

```
+-------------------+
|+--------------+   |------+-+                        +-----+
||              | O |      | |          ****          |     |
||              |   |      +-+         (    )         |     | RPi MQTT service
||              | O |     sensor      *      *        |     |
||              |   |                  (****)         |     |
|+--------------+   |------+-+                        +-----+
+-------------------+      | | 
    Toaster oven           +-+  
                       Tasmoda plug
```

