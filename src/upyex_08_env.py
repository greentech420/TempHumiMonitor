from machine import I2C, Pin
import i2c_lcd
import dht
import time

addr_light = 41

def measure_light():
    # ch0:赤外光、ch1:可視光
    raw_ch0 = i2c.readfrom_mem(addr_light, 0x8c, 2)
    raw_ch1 = i2c.readfrom_mem(addr_light, 0x8e, 2)

    # 16ビットデータに変換（ビッグエンディアン）
    ch0 = (raw_ch0[1] << 8) | raw_ch0[0]
    ch1 = (raw_ch1[1] << 8) | raw_ch1[1]

    # 照度を求める変換処理
    r = ch1/ch0
    if 0 <= r <= 0.5:
        lux = 0.0304*ch0 - 0.062*ch0*(r**1.4)
    elif 0.5 < r <= 0.61:
        lux = 0.0224*ch0 - 0.031*ch1
    elif 0.5 < r <= 0.61:
        lux = 0.0224*ch0 - 0.031*ch1
    elif 0.61 < r <= 0.8:
        lux = 0.0128*ch0 - 0.0153*ch1
    elif 0.8 < r <= 1.3:
        lux = 0.0146*ch0 - 0.00112*ch1
    elif r > 1.3:
        lux = 0
        
    str_lux = 'lux: ' + '{:.0f}'.format(lux) + '   '
    return str_lux

# i2cオブジェクトの生成
i2c = I2C(scl=Pin(21), sda=Pin(19), freq=400000)

# LCDオブジェクトの生成
lcd = i2c_lcd.Display(i2c)
lcd.clear()

# DHT11(温湿度)センサオブジェクトの生成
dht11 = dht.DHT11(Pin(25))

# TSL2561 LIIGHT SENSOR 初期設定
# ウェークアップ
i2c.writeto_mem(addr_light, 0x80, b'\x03')
# 初期化
i2c.writeto_mem(addr_light, 0x81, b'\x12')

while True:    
    dht11.measure() #温湿度の測定
    temp = dht11.temperature() #温度の取得
    humi = dht11.humidity()    #湿度の取得
    str_temp = 'T: ' + str(temp) + '  '
    str_humi = 'H: ' + str(humi)    

    # 照度の測定
    str_lux = measure_light()

    # LCDに表示
    lcd.move(0,0)
    lcd.write(str_temp)
    lcd.write(str_humi)
    lcd.move(0,1)
    lcd.write(str_lux)
    
    time.sleep(3) 
