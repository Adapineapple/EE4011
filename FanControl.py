from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import machine
from m5mqtt import M5mqtt
import time


setScreenColor(0x111111)


x = None
y = None



label0 = M5TextBox(7, 7, "EE4011", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(38, 42, "Stop", lcd.FONT_Default, 0xFFFFFF, rotate=0)
circle0 = M5Circle(19, 46, 12, 0xf91010, 0xFFFFFF)
label2 = M5TextBox(7, 94, "T:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label4 = M5TextBox(101, 225, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label5 = M5TextBox(68, 225, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label3 = M5TextBox(7, 131, "H:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label6 = M5TextBox(7, 169, "P:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label7 = M5TextBox(28, 94, "label7", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label8 = M5TextBox(28, 131, "label8", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label9 = M5TextBox(28, 169, "label9", lcd.FONT_Default, 0xFFFFFF, rotate=0)



def fun_SuiSui1101_feeds_tempature_(topic_data):
  global x, y, i2c0, pin0, pin1
  label7.setText(str(topic_data))
  pass

def fun_SuiSui1101_feeds_humidity_(topic_data):
  global x, y, i2c0, pin0, pin1
  label8.setText(str(topic_data))
  pass

def fun_SuiSui1101_feeds_pressure_(topic_data):
  global x, y, i2c0, pin0, pin1
  label9.setText(str(topic_data))
  pass

def fun_SuiSui1101_feeds_ee4011_(topic_data):
  global x, y, i2c0, pin0, pin1
  x = topic_data
  label4.setText(str(x))
  pass

def fun_SuiSui1101_feeds_ee401_(topic_data):
  global x, y, i2c0, pin0, pin1
  y = topic_data
  label5.setText(str(y))
  pass


wifiCfg.doConnect('Sui', '00000000')
pin0 = machine.Pin(25, mode=machine.Pin.OUT, pull=machine.Pin.PULL_DOWN)
pin1 = machine.Pin(26, mode=machine.Pin.OUT, pull=machine.Pin.PULL_DOWN)
x = 0
pin0.off()
pin1.off()
m5mqtt = M5mqtt('', 'io.adafruit.com', 1883, 'SuiSui1101', '<Your Key>', 300)
m5mqtt.subscribe(str('SuiSui1101/feeds/tempature'), fun_SuiSui1101_feeds_tempature_)
m5mqtt.subscribe(str('SuiSui1101/feeds/humidity'), fun_SuiSui1101_feeds_humidity_)
m5mqtt.subscribe(str('SuiSui1101/feeds/pressure'), fun_SuiSui1101_feeds_pressure_)
m5mqtt.subscribe(str('SuiSui1101/feeds/ee4011'), fun_SuiSui1101_feeds_ee4011_)
m5mqtt.subscribe(str('SuiSui1101/feeds/ee401'), fun_SuiSui1101_feeds_ee401_)
m5mqtt.start()
while True:
  if x == '1' and y == '1':
    pin1.on()
    pin0.off()
    label1.setText('clockwise')
    M5Led.on()
    circle0.setBgColor(0x33ff33)
    wait(0.5)
  elif x == '1' and y == '0':
    pin0.on()
    pin1.off()
    circle0.setBgColor(0x33ff33)
    M5Led.on()
    label1.setText('Anticlockwise')
    wait(0.5)
  elif x == '0':
    pin0.off()
    pin1.off()
    circle0.setBgColor(0xff0000)
    label1.setText('Stop')
    M5Led.off()
    wait(0.5)
  wait_ms(2)
