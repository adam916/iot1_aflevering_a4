from math import radians, cos, sin, asin, sqrt
#import umqtt_robust2 as mqtt
from machine import UART
from micropyGPS import MicropyGPS
import _thread
from machine import Pin
import time
from machine import Timer
start = time.time()
distance_samlet = 0
def distance(lat1, lat2, lon1, lon2):
     
    
    # grader til radianer
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formel
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # jordens radius i km
    r = 6371
      
    # calculate the result
    return(c * r)

total_distance_koordinater = [] # liste oprettet til at holde koordinater
total_distance = [] # liste til at holde afstanden man har bevæget si
# denne variabel opdateres til at holde gps data
gps_to_adafruit = None

# instans af gps klassen opdateres her
gps = None
def gps_main():
    
    uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
    global gps
    gps = MicropyGPS()
    global total_distance_koordinater   #global variabel , så listen kan ændres udenfor funktionen
    global total_distance   #global variabel, så listen kan ændres udenfor funktionen
    global start
    while True:
        buf = uart.readline()
        if buf:
            for char in buf:
                gps.update(chr(char)) # Note the conversion to to chr, UART outputs ints normally
        
        #different gps methods that can be used:
        
        #print('UTC Timestamp:', gps.timestamp)
        #print('Date:', gps.date_string('long'))
        #print('Satellites:', gps.satellites_in_use)
        #print('Altitude:', gps.altitude)
        #print('Latitude:', gps.latitude_string())
        #print('Longitude:', gps.longitude_string())
        #print('Horizontal Dilution of Precision:', gps.hdop)
        #print('Compas direction: ', gps.compass_direction())
        
        formattedLat = gps.latitude_string()
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]
        formattedAlt = str(gps.altitude)
        formattedSpd = gps.speed_string()
        formattedSpd = formattedSpd[:-5]
        #print(gps.speed_string())
        gps_ada = formattedSpd+","+formattedLat+","+formattedLon+","+formattedAlt
        
        lon = float(gps.longitude_string()[:-3])  #stringslice her, negativt, så der kun kommer tal i vores variabler
        lat = float(gps.latitude_string()[:-3])  
        if lat != 0.0 and lon != 0.0: #denne kondition sørger for jeg ikke gemmer de 0.0 koordinater man får ved opstart af forbindelse
            
            lat_lon_tuple = (lat, lon)           #touple til at holde 2 koordinat positioner                        
            total_distance_koordinater.append(lat_lon_tuple) #her kommes de 2 koordinater fra ovenfor i listen total_distance1
          
        else:
            print("No reading yet")
        
        
        if len(total_distance_koordinater)>2:
            global distance_samlet
            total_distance.append(distance(total_distance_koordinater[-2][-2],total_distance_koordinater[-1][-2],total_distance_koordinater[-2][-1],total_distance_koordinater[-1][-1])) #her kommer de 2 nyeste lat og lon koordinater fra listen "total_distance1" ind i funktionen "distance"
            distance_samlet = sum(total_distance)# her kommer summen af distancen i en ny variabel
            
            
            #----------- sender til adafruit hvert 10 sek ----------#
            """
            if time.time () > start + 40: #det her venter noget til mellem hver sending til adafruit
                print("sender til ada")
                mqtt.web_print(f"{total_distance_samlet}Km tilbagelagt", 'adam8143/feeds/iotfeed')
                start = time.time()
            else:
                pass
            """
             
            #mqtt.web_print(f"{total_distance_samlet}Km tilbagelagt", 'adam8143/feeds/iotfeed')
                
            #print(sum(total_distance),"km")
            
            #if total_distance_samlet != 0: #hvis samlet distance ikke er 0, print den
                #print(total_distance_samlet, "km")
                
            total_distance_koordinater.pop(0)
            if 0.0 in total_distance:
                total_distance.remove(0.0)
            
        if len(total_distance) ==  5:
            temp_sum = sum(total_distance)
            total_distance.clear()
            total_distance.append(temp_sum)
        time.sleep(0.2)
        
        
        
        
        
        if formattedLat != "0.0" and formattedLon != "0.0":
            #print("gps_ada: ",gps_ada)
            global gps_to_adafruit
            gps_to_adafruit = gps_ada
            
def send_til_ada():
    global distance_samlet
    return round(distance_samlet,3)

#_thread.start_new_thread(gps_main, ())


