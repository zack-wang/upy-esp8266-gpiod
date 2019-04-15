import time
from robustr import MQTTClientr
from machine import Pin
import ubinascii
import machine
import micropython
import os
import network
import gc

#IO初始化,燈全暗
p2=Pin(2, Pin.OUT,value=0)
Pin(4, Pin.OUT,value=1)
Pin(5, Pin.OUT,value=1)
Pin(12, Pin.OUT, value=0)
Pin(13, Pin.OUT, value=0)
Pin(14, Pin.OUT, value=1)
Pin(15, Pin.OUT, value=0)
p16=Pin(16, Pin.OUT, value=1)
adc=machine.ADC(0)

#回呼函式
def sub_cb(topic,msg):
	print((topic,msg))
	global IOPWD
	try:
		pin=int(msg[0:2])
		sts=int(msg[2:3])
		iopass=str(msg[3:],"utf-8")
		if iopass!=IOPWD:
			print('Wrong password')
			return
	except ValueError:
		pin=-1
		sts=-1

	if pin==2 or pin==4 or pin==5 or pin==12 or pin==13 or pin==14 or pin==15 or pin==16 :
		p=Pin(pin,Pin.OUT)
    		if sts == 3:
        		p.off()
        		time.sleep(1)
        		p.on()
		elif sts == 2:
			p.on()
			time.sleep(1)
			p.off()
		elif sts == 1:
    			p.on()
		elif sts == 0:
			p.off()
		else:
			time.sleep(1)

#讀設定檔
def read_config():
	try:
		f=open('config.txt')
		global ESSID,WIFIPWD,SERVER,PORT,USR,PWD,CID,IOPWD
		ESSID=f.readline().replace("\r","").replace("\n","")
		WIFIPWD=f.readline().replace("\r","").replace("\n","")
		SERVER=f.readline().replace("\r","").replace("\n","")
		PORT=int(f.readline())
		USR=f.readline().replace("\r","").replace("\n","")
		PWD=f.readline().replace("\r","").replace("\n","")
		CID=f.readline().replace("\r","").replace("\n","")
		f.close()
		f=open('password.txt')
		IOPWD=f.readline().replace("\r","").replace("\n","")
		f.close()
	except OSError:
		print('No Config or File IO Error')

#每個人的服務器地址都不同哦
SERVER=''
#這個連接埠是未加密
PORT=0
#這是帳號
USR=''
#這是密碼
PWD=''
#keep-alive=3 minutes
KEEPALV=60
#這是client id
CID='0'
#等daemon完成
ESSID=''
WIFIPWD=''
IOPWD=''
read_config()
sta=network.WLAN(network.STA_IF)
sta.connect(ESSID,WIFIPWD)
isc=sta.isconnected()
while isc==False:
	print('Wait for WiFi Connected...')
	time.sleep(5)
	isc=sta.isconnected()
#啟用函式
c=MQTTClientr(CID,SERVER,PORT,USR,PWD,KEEPALV)
c.DEBUG=True
c.set_callback(sub_cb)
try:
	c.connect(True)
	c.publish('online',CID)
	print("New session being set up")
	print(CID+'/gpio')
	c.subscribe(CID+'/gpio')
except:
	print('mqtt error')
	machine.reset()

cnt=0
while 1 :
	try:
		c.check_msg()
		print(cnt)
		cnt+=1
		if cnt%60==0:
			c.ping()
		if cnt%2 == 0:
			p2.off()
		if cnt%2 == 1:
			p2.on()
		if cnt%10==0:
			c.publish(CID+'/adc','{"cds":"'+str(adc.read())+'"}')
		if cnt>60000:
			cnt=0
		time.sleep(1)
		gc.collect()
	except OSError as e:
		p16.on()
		c.reconnect()
