# This file is executed on every boot (including wake-boot from deepsleep)
### #import esp
### #esp.osdebug(None)
### import uos, machine
### #uos.dupterm(None, 1) # disable REPL on UART(0)
### import gc
### #import webrepl
### #webrepl.start()
### gc.collect()

try:
  ##############################################################################
  #
  # Load and execute our main config if config.INIT set in config.py
  #
  ##############################################################################
  print('Checking config.INIT')
  import config
  if (config.INIT):
    print('Executing init.py')
    exec(open('init.py').read())
  del config
except Exception as e:
  None
finally:
  ##############################################################################
  #
  # Clean everything up
  #
  ##############################################################################
  print('Cleaning up')
  from gc import collect
  collect()
  del collect

class t:
  def a():
      exec(open('trya.py').read())
  
  def b():
      exec(open('tryb.py').read())
  
  def c():
      exec(open('tryc.py').read())

import sensor
mySensor = sensor.Sensor()
mySensor.run()
