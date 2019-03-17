import time
from umqtt.robust import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython

#每個人的服務器地址都不同哦
SERVER='m11.cloudmqtt.com'
#這個連接埠是未加密
PORT=16312
#這是帳號
USR='user'
#這是密碼
PWD='password'
#keep-alive=3 minutes
KEEPALV=180
#這是client id
UUID='c1234'
#IO初始化,燈全亮
p2 = Pin(2, Pin.OUT,value=0)
p4 = Pin(4, Pin.OUT,value=0)
p5 = Pin(5, Pin.OUT,value=0)
p12 = Pin(12, Pin.OUT, value=0)
p13 = Pin(13, Pin.OUT, value=0)
p14 = Pin(14, Pin.OUT, value=0)
p15 = Pin(15, Pin.OUT, value=0)
p16 = Pin(16, Pin.OUT, value=0)
c=MQTTClient(UUID,SERVER,PORT,USR,PWD,KEEPALV)
#回呼函式
def sub_cb(topic,msg):
	print((topic,msg))
	pin=int(msg[1:3])
	sts=int(msg[-1:])
	#print('pin='+msg[1:3]+' status='+msg[-1:])

        if sts < 2:
                Pin(pin, Pin.OUT,value=sts)
        elif sts == 2:
                Pin(pin,Pin.OUT,value=1)
                time.sleep(1)
                Pin(pin,Pin.OUT,value=0)
#等daemon完成
def main():
	time.sleep(10)
#啟用函式
def start():
        c=MQTTClient(UUID,SERVER,PORT,USR,PWD,KEEPALV)
        c.set_callback(sub_cb)
	tf=c.connect()
	print("New session being set up")
	print(UUID+'/gpio')
	c.subscribe(UUID+'/gpio')
	while True:
		c.check_msg()
		time.sleep(1)

