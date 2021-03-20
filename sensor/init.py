##############################################################################
#
# bootstrap.py
#
# Initialise micropython after new firmware.
# Namely:
#   Setup basic logger
#   Setup wifi
#   Setup date via ntp
#
##############################################################################
import config
from gc import collect

##############################################################################
#
# Set up logging
#
##############################################################################
from logging import basicConfig, DEBUG, getLogger
basicConfig(level=DEBUG)
log = getLogger(__name__)
del basicConfig
del DEBUG
del getLogger
collect()
log.debug ('logging initilised')

try:
  ##############################################################################
  #
  # 
  #
  ##############################################################################
  from gc import collect
  from machine import deepsleep, reset_cause, DEEPSLEEP_RESET, I2C, Pin
  from time import sleep

  ##############################################################################
  #
  # Init Wifi
  #
  ##############################################################################
  log.info('Raising the semaphore flags.')
  from network import AP_IF, STA_IF, WLAN
  from ubinascii import hexlify
  # turn off the WiFi Access Point
  ap_if = WLAN(AP_IF)
  ap_if.active(False)
  # connect the device to the WiFi network
  wifi = WLAN(STA_IF)
  active = wifi.active(True)
  log.info('WIFI_SSID={}'.format(config.WIFI_SSID))
  log.info('WIFI_PASS={}'.format(config.WIFI_PASS))
  connect = wifi.connect(config.WIFI_SSID,config.WIFI_PASS)
  # wait until the device is connected to the WiFi network
  MAX_ATTEMPTS = 20
  attempt_count = 0
  while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    log.info('z.')
    sleep(1)
  if attempt_count == MAX_ATTEMPTS:
    log.error('The flag pole is broken.')
  log.info('connect={}'.format(connect))
  # Get mac address
  mac = hexlify(wifi.config('mac'),':').decode()
  log.info('mac={}'.format(mac))
  # clean up this mess
  del hexlify
  del WLAN
  del AP_IF
  del STA_IF
  del ap_if
  del active
  del connect
  del MAX_ATTEMPTS
  del attempt_count
  del wifi
  collect()
  
  ##############################################################################
  #
  # Init date/time
  #
  ##############################################################################
  log.info('Synchronizing time pieces.')
  from ntptime import settime
  gottime = settime()
  log.info('gottime={}'.format(gottime))
  del settime
  del gottime
  collect()

except Exception as e:
  log ('ERROR: e={}'.format(e))

