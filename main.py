#调用需要使用到的库文件
from machine import UART
from Maix import GPIO
from fpioa_manager import fm
from time import sleep
import sensor, image, lcd, time
import KPU as kpu
import gc, sys

import utime
#映射UART2的两个引脚
fm.register(GPIO.GPIOHS9,fm.fpioa.UART1_TX)
fm.register(GPIO.GPIOHS10,fm.fpioa.UART1_RX)
#初始化串口，返回调用句柄
uart_A = UART(UART.UART1, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)
#定义一个要发送的字符串

"""

#主循环
while(True):
    try:
        read_str = uart_A.read(10)
        utime.sleep_ms(100)
        uart_A.write(str(code1))
        sleep(5)
        uart_A.write(str(code2))
        sleep(5)
        print("check")
        utime.sleep_ms(100)
    except:
        pass
"""


code1 = "1"
code2 = "2"
code3 = "3"
code4 = "4"

input_size = (224, 224)
labels = ['Hazardous Waste', 'Other Waste', 'Recyclable Waste', 'Kitchen Waste']

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=input_size)
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

def main(labels = None, model_addr="/sd/model-60119.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    try:
        sensor.reset()
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_framesize(sensor.QVGA)
        sensor.set_windowing(sensor_window)
        sensor.set_hmirror(sensor_hmirror)
        sensor.set_vflip(sensor_vflip)
        sensor.run(1)

        lcd.init(type=1)
        lcd.rotation(lcd_rotation)
        lcd.clear(lcd.WHITE)

        if not labels:
            with open('labels.txt','r') as f:
                exec(f.read())
        if not labels:
            print("no labels.txt")
            img = image.Image(size=(320, 240))
            img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
            lcd.display(img)
            return 1


        try:
            task = None
            task = kpu.load(model_addr)
            while(True):
                img = sensor.snapshot()
                t = time.ticks_ms()
                fmap = kpu.forward(task, img)
                t = time.ticks_ms() - t
                plist=fmap[:]
                pmax=max(plist)
                max_index=plist.index(pmax)
                img.draw_string(0,200, "%.2f : %s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 0, 0))
                result = labels[max_index].strip()
                if(result == "Recyclable Waste"):
                    uart_A.write(str(code1))
                    sleep(3)
                    uart_A.write(str(code4))
                    sleep(3)
                if(result == "Other Waste"):
                    uart_A.write(str(code2))
                    sleep(3)
                    uart_A.write(str(code3))
                    sleep(3)
                print(labels[max_index].strip())
                #img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
                lcd.display(img)
        except Exception as e:
            raise e
        finally:
            if not task is None:
                kpu.deinit(task)
    except:
        pass


if __name__ == "__main__":
    try:
        # main(labels=labels, model_addr=0x300000)
        main(labels=labels, model_addr="/sd/model-60119.kmodel")
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()

