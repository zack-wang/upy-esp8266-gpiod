# upy-esp8266-gpiod
這個專案啟發來自於 **MicroPython** http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro
以及它的函式庫 https://github.com/micropython/micropython-lib/tree/master/umqtt.robust

## 我是在ubuntu18的桌上型電腦做這些實驗,

### 首先要確定你的"USB轉TTL線"運作是否正常,刪除flash 
![uart-wiring](/images/usb_ttl_esp8266.jpg)

```
esptool.py --port /dev/ttyUSB0 erase_flash
```

### 下載最新的韌體,
```
wget http://micropython.org/resources/firmware/esp8266-20190125-v1.10.bin
```

### 燒錄韌體（又稱flashing)
```
sudo esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20190125-v1.10.bin
```

### 使用picocom連線到micropython操作系統
```
sudo picocom /dev/ttyUSB0 -b115200
```

### 啟動wifi station mode(以下是在micropython內）
```
import network
sta=network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('ESSID','WIFI_PASSWORD')
sta.ifconfig()
```
假如連線正常時,你會看到它（esp8266)的ip,gateway等資料

### 啟用WebRepl,就是用wifi與瀏覽器直接連上esp8266(在micropython內）
```
import webrepl
webrepl.start()
```
它會要求你輸入密碼,很重要,仔細做

### 用你的電腦瀏覽器連上esp8266
```
http://micropython.org/webrepl/?
```
把 ws://192.168.4.1:8266/ 換成上面拿到esp的ip地址 例如 ws://10.40.80.2:8266/
然後按下connect
這時候輸入密碼

### 上傳額外的兩個函式
![uploader](/images/file_uploader.png)
```
wget https://github.com/micropython/micropython-lib/raw/master/umqtt.simple/umqtt/simple.py
wget https://github.com/micropython/micropython-lib/raw/master/umqtt.robust/umqtt/robust.py
```
點 **選擇檔案** , 選好以後再點 **send to device**

>原本只要改main.py並且上傳就行了,但是似乎有些小bug
>下載 boot.py 以及 gpiod.py
>跟上個步驟相同,選擇檔案上傳,在micropython按 **ctrl+D** 
