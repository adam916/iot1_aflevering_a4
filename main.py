import umqtt_robust2 as mqtt
import gps_funktion2 
import batteri_til_adafruit_alternative
import imu_med_seg_iot 
import time 
import _thread

imu_med_seg_iot.tm.show("    ")
_thread.start_new_thread(batteri_til_adafruit_alternative.updateBP, ())
print(1)
_thread.start_new_thread(imu_med_seg_iot.imu_proeve, ())
print(2)
_thread.start_new_thread(gps_funktion2.gps_main, ())

while True:
    gps_data = gps_funktion2.gps_to_adafruit
    #print("Test", gps_data)
    mqtt.web_print(gps_data, 'adam8143/feeds/mapfeed/csv')
    #print("send til ada: ", gps_funktion2.send_til_ada())
    time.sleep(4)
    mqtt.web_print(f"{gps_funktion2.send_til_ada()}Km tilbagelagt", 'adam8143/feeds/iotfeed')
    time.sleep(4)
    mqtt.web_print(batteri_til_adafruit_alternative.ada_bat(), 'adam8143/feeds/iotbatteri')
    #print("ada bat",batteri_til_adafruit_alternative.ada_bat())
    time.sleep(4)