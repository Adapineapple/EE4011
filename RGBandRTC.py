from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import ntptime
import i2c_bus
from m5mqtt import M5mqtt
import time
from easyIO import *
import unit
import ds1307


rgb.set_screen([0,0,0,0,0,0,0xfaf205,0,0xfaf205,0,0,0,0,0,0,0xfaf205,0,0,0,0xfaf205,0,0xfaf205,0xfaf205,0xfaf205,0])
env_0 = unit.get(unit.ENV, unit.PORTA)


RGB = None
x = None
type2 = None
r = None
g = None
b = None






def fun_SuiSui1101_feeds_RGB_(topic_data):
  global RGB, x, type2, r, g, b, i2c0
  RGB = topic_data
  x = len(RGB)
  type2 = (str(((str(RGB[1]) + str(RGB[2])))) + str(RGB[3]))
  r = int(type2)
  r = float(r)
  r = (r / 255) * 100
  type2 = (str(((str(RGB[5]) + str(RGB[6])))) + str(RGB[7]))
  g = int(type2)
  g = float(g)
  g = (g / 255) * 100
  type2 = (str(((str(RGB[9]) + str(RGB[10])))) + str(RGB[11]))
  b = int(type2)
  b = float(b)
  b = (b / 255) * 100
  wait(1)
  pass


    

wifiCfg.doConnect('Sui', '00000000')
ntp = ntptime.client(host='cn.pool.ntp.org', timezone=8)
i2c0 = i2c_bus.easyI2C((25, 21), 0x00, freq=400000)
i2c0.addr=(0x68)
r = 0
g = 0
b = 0
m5mqtt = M5mqtt('Atom_control', 'io.adafruit.com', 1883, '<Your ID>', '<Your KEY>', 300)
m5mqtt.subscribe(str('SuiSui1101/feeds/RGB'), fun_SuiSui1101_feeds_RGB_)
m5mqtt.start()

i2c = I2C(1, I2C.MASTER, sda = 21, scl = 25)
ds = ds1307.DS1307(i2c)

#enable the osscilator
ds.halt(False)
ds.datetime()

#enter the current time (year, month, date, weekday, hour, minute, second, microsecond)
now = (2024, 04, 20, 5, 16, 20, 22, 0)
ds.datetime(now)

while(True):
  time = ds.datetime()
  
  m5mqtt.publish(str('SuiSui1101/feeds/tempature'), str((env_0.temperature)), 0)
  m5mqtt.publish(str('SuiSui1101/feeds/humidity'), str((env_0.humidity)), 0)
  m5mqtt.publish(str('SuiSui1101/feeds/pressure'), str((env_0.pressure)), 0)
  m5mqtt.publish(str('SuiSui1101/feeds/Hour'), str((ntp.hour())), 0)
  m5mqtt.publish(str('SuiSui1101/feeds/Minute'), str((ntp.minute())), 0)
  m5mqtt.publish(str('SuiSui1101/feeds/Second'), str((ntp.second())), 0)
  analogWrite(22, r)
  analogWrite(19, g)
  analogWrite(23, b)
  wait(7)
  wait_ms(2)
