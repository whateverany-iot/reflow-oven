##############################################################################
#
# Read ESP8266 ADC (for temperature) and publish to MQTT.
#
# TODO: Sub to some MQTT service to ensure connectivity.
#
# TODO: Use watchdog to reset if in doubt.
#
#
##############################################################################
import config
from gc import collect

##############################################################################
#
# Set up logging
#
##############################################################################
from logging import basicConfig, DEBUG, INFO, getLogger
if config.DEBUG:
  basicConfig(level=DEBUG)
else:
  basicConfig(level=INFO)
log = getLogger(__name__)
del basicConfig
del DEBUG
del INFO
del getLogger
collect()
log.debug ('logging initilised')

class Sensor:
  def __init__(self):
    """
    ##############################################################################
    #
    # __init__()
    #
    ##############################################################################
    """
    global client
    global wdt
    try:
      log.debug('Sensor.__init__() BEGIN')

      #from machine import WDT
      #wdt = WDT()
      #del WDT
      #collect()
      from umqtt.simple import MQTTClient
      client = MQTTClient('FIXME', config.MQTT_HOST,
        user=config.MQTT_USER_ID,
        password=config.MQTT_API_KEY, port=config.MQTT_PORT)
      del MQTTClient
      client.DEBUG = True
      client.set_callback(self.on_message)
      client.connect(clean_session=True)
      client.subscribe("#")
    except Exception as e:
      log.error('Sensor.__init__() caught e={}'.format(e))
    finally:
      log.debug('Sensor.__init__() END')
     
  def _handle_exception(self, loop, context):
    """
    ##############################################################################
    #
    # _handle_exception()
    #
    ##############################################################################
    """
    try:
      log.debug('Sensor._handle_exception() BEGIN')
      from io import StringIO
      s = StringIO()
      del StringIO
      collect()

      from sys import print_exception
      print_exception(context["exception"], s)
      del print_exception
      collect()
      log.error(s.getvalue())
    except Exception as e:
      log.error('Sensor._handle_exception() caught e={}'.format(e))
    finally:
      log.debug('Sensor._handle_exception() END')

  async def heart_beat(self):
    """
    ##############################################################################
    #
    # heart_beat()
    #
    # Feed the monkey.
    # Das Blinken Lichten
    # and poormans ping to gateway
    #
    ##############################################################################
    """
    global LED_STATE
    try:
      log.debug('Sensor.heart_beat() BEGIN')

      # Init LED Pin and set LED_STATE
      from machine import Pin
      LED = Pin(2,Pin.OUT)
      del Pin
      collect()
      LED.on()
      LED_STATE = LED.value()

      while True:
        from uasyncio import sleep
        await sleep(1)
        del sleep
        collect()

        #
        log.debug("Sensor.heart_beat() - feed the monkey...")
        #wdt.feed()

        #
        log.debug("Sensor.heart_beat() - Flick the light switch...")
        LED_STATE ^= 1
        LED.value(LED_STATE)

        #
        log.debug("Sensor.heart_beat() - Ping the gateway...")
        from socket import socket, AF_INET, SOCK_STREAM
        s = socket(AF_INET, SOCK_STREAM)
        del socket, AF_INET, SOCK_STREAM
        collect()

        s.settimeout(1.0)
        try:
          s.connect((config.WIFI_GATEWAY, 443))
        except Exception as e:
          log.error("e={}".format(e))
        finally:
          s.close()
    except Exception as e:
      log.error('Sensor.heart_beat() caught e={}'.format(e))
    finally:
      log.debug('Sensor.heart_beat() END')

  def mqtt_connect(self):
    """
    ##############################################################################
    #
    # mqtt_connect()
    #
    ##############################################################################
    """
    try:
      log.debug('Sensor.mqtt_connect() BEGIN')
      self.client.connect()
      self.client.subscribe('#')
    except Exception as e:
      log.error('Sensor.mqtt_connect() caught e={}'.format(e))
    finally:
      log.debug('Sensor.mqtt_connect() END')

  async def check_sensor(self):
    """
    ##############################################################################
    #
    # check_sensor()
    #
    ##############################################################################
    """
    global TEMP
    try:
      log.debug('Sensor.check_sensor() BEGIN')
      from machine import ADC
      adc = ADC(0)
      del ADC
      collect()

      while True:
        from uasyncio import sleep
        await sleep(1)
        del sleep
        collect()

        log.debug("Sensor.check_sensor()...")
        TEMP = adc.read()
        log.info("Sensor.check_sensor(TEMP={})".format(TEMP))
    except Exception as e:
      log.error('Sensor.check_sensor() caught e={}'.format(e))
    finally:
      log.debug('Sensor.check_sensor() END')
  
  def on_message(self,topic, msg):
    """
    ##############################################################################
    #
    # on_message()
    #
    ##############################################################################
    """
    try:
      log.debug('Sensor.on_message() BEGIN')
      log.info("Sensor.on_message(topic={},msg={})".format(topic,msg))
    except Exception as e:
      log.error('Sensor().on_message() caught e={}'.format(e))
    finally:
      log.debug('Sensor.on_message() END')

  async def check_mqtt(self):
    """
    ##############################################################################
    #
    # check_mqtt()
    #
    ##############################################################################
    """
    try:
      log.debug('Sensor.check_mqtt() BEGIN')
      while True:
        from uasyncio import sleep
        await sleep(2)
        del sleep
        collect()

        client.publish('/temp',str(TEMP))
        client.check_msg()

        log.debug("Check Sensor.check_mqtt() ...")
    except Exception as e:
      log.error('Sensor.check_mqtt() caught e={}'.format(e))
    finally:
      log.debug('Sensor.check_mqtt() END')
  
  def run(self):
    """
    ##############################################################################
    #
    # run()
    #
    ##############################################################################
    """
    try:
      log.debug('Sensor.run() BEGIN')
 
      from uasyncio import get_event_loop
      loop = get_event_loop()
      del get_event_loop
      collect()

      loop.set_exception_handler(self._handle_exception)
      loop.create_task(self.heart_beat())
      loop.create_task(self.check_sensor())
      loop.create_task(self.check_mqtt())
      loop.run_forever()
    except Exception as e:
      log.error('Sensor.run() caught e={}'.format(e))
    finally:
      log.debug('Sensor.run END')

try:
  """
  ##############################################################################
  #
  # Run if __main__
  #
  ##############################################################################
  """
  if __name__ == '__main__':
    sensor = Sensor()
    sensor.run()

except Exception as e:
  log.error('e={}'.format(e))

