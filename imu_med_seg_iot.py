'''
Using the MPU6050 inertial unit (accelerometer + gyrometer) with a Raspberry Pi Pico.
For more info:
bekyelectronics.com/raspberry-pi-pico-and-mpu-6050-micropython/
'''

from imu import MPU6050  # https://github.com/micropython-IMU/micropython-mpu9x50
import time
from machine import Pin, I2C
import tm1637
from imu import MPU6050# https://github.com/micropython-IMU/micropython-mpu9x50

i2c = I2C(0, sda=Pin(22), scl=Pin(21), freq=400000)
imu = MPU6050(i2c)

tm = tm1637.TM1637(clk=Pin(18), dio=Pin(19))


# Temperature display
tackle_count = 0   #indsat var til at hole antal taklinger
wait_time = 0      # var til at lave noget ventetid mellem taklinger
up_count = 0 #forsøg med at se på oprejst
print("Temperature: ", round(imu.temperature,2), "°C")
def imu_proeve():
    global up_count
    global tackle_count
    while True:
        
        # reading values
        acceleration = imu.accel
        gyroscope = imu.gyro
        """ 
        print ("Acceleration x: ", round(acceleration.x,2), " y:", round(acceleration.y,2),
               "z: ", round(acceleration.z,2))


        print ("gyroscope x: ", round(gyroscope.x,2), " y:", round(gyroscope.y,2),
               "z: ", round(gyroscope.z,2))
        """
    # data interpretation (accelerometer)

        if abs(acceleration.x) > 0.8:
            if (acceleration.x > 0):
                #print("The x axis points upwards")
                pass
            else:
                #print("The x axis points downwards")
                up_count +=1


        if abs(acceleration.y) > 0.8:
            if (acceleration.y > 0):
                #print("The y axis points upwards")
                pass
            else:
                print("The y axis points downwards")
                #pass



        if abs(acceleration.z) > 0.8:
            if (acceleration.z > 0):
              
                print("The z axis points upwards")
            else:
                if up_count>0:
                    tackle_count+=1
                    tm.number(tackle_count)
                    up_count=0
                #print("The z axis points downwards")
                #pass
        
    # data interpretation (gyroscope)
        """
        if abs(gyroscope.x) > 20:
            print("Rotation around the x axis")

        if abs(gyroscope.y) > 20:
            print("Rotation around the y axis")

        if abs(gyroscope.z) > 20:
            print("Rotation around the z axis")
        """
        time.sleep(0.2)


