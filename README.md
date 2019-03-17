# upy-esp8266-gpiod
這個專案啟發來自於 http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro
以及它的函式庫 https://github.com/micropython/micropython-lib/tree/master/umqtt.robust

首先要確定你的USB轉TTL運作是否正常,刪除flash 
esptool.py --port /dev/ttyUSB0 erase_flash
