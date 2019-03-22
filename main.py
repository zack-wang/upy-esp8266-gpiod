import time
from umqtt.robust import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython
import network
import gc

#回呼函式
def sub_cb(topic,msg):
	print((topic,msg))
	try:
		pin=int(msg[1:3])
		sts=int(msg[-1:])
	except ValueError:
		pin=-1
	if pin > -1:
        if sts < 2:
        	Pin(pin, Pin.OUT,value=sts)
        elif sts == 2:
            Pin(pin,Pin.OUT,value=1)
            time.sleep(1)
            Pin(pin,Pin.OUT,value=0)

#每個人的服務器地址都不同哦
SERVER='m11.cloudmqtt.com'
#這個連接埠是未加密
PORT=1883
#這是帳號
#USR='superman'
USR='MQTT_USER'
#這是密碼
#PWD='1q2w3e4r'
PWD='MQTT_PASSWD'
#keep-alive=3 minutes
KEEPALV=180
#這是client id
UUID='UUID-1234-5678'
#等daemon完成

#IO初始化,燈全亮
p2 = Pin(2, Pin.OUT,value=0)
p4 = Pin(4, Pin.OUT,value=0)
p5 = Pin(5, Pin.OUT,value=0)
p12 = Pin(12, Pin.OUT, value=0)
p13 = Pin(13, Pin.OUT, value=0)
p14 = Pin(14, Pin.OUT, value=0)
p15 = Pin(15, Pin.OUT, value=0)
p16 = Pin(16, Pin.OUT, value=0)
sta=network.WLAN(network.STA_IF)
isc=sta.isconnected()
while isc==False:
	print('Wait for WiFi Connected...')
	time.sleep(3)
	isc=sta.isconnected()
#啟用函式
c=MQTTClient(UUID,SERVER,PORT,USR,PWD,KEEPALV)
c.set_callback(sub_cb)
tf=c.connect()
print("New session being set up")
print(UUID+'/gpio')
c.subscribe(UUID+'/gpio')
cnt=0
while 1:
	isc=sta.isconnected()
	if isc:
		if cnt == KEEPALV: #WIFI連線以後才檢查是否發出PINGREQ
			print('ping-pong')
			c.ping()
			cnt=0
			c.publish('online',UUID)
		else:
			cnt=cnt+1
		c.check_msg()
	else:
		print('not conntd')
	time.sleep(1)
	gc.collect()
