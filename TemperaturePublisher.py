#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Temperature
import time
import RPi.GPIO as GPIO

sleeptime = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

base_dir = '/sys/bus/w1/devices/'

device_folder = base_dir + '28-3c01d60700ab'
device_file = device_folder + '/w1_slave'

def TemperaturMessung():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Zur Initialisierung, einmal "leer" auslesen
TemperaturMessung()

def TemperaturAuswertung():
    lines = TemperaturMessung()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = TemperaturMessung()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0
        return temp_c


def talker():

   pub = rospy.Publisher('TemperaturSensor', Temperature, queue_size=10)
   i = 0
   temperature = Temperature()
   rospy.init_node('Sensor', anonymous=True)



   temperature.variance = None
   while not rospy.is_shutdown():
        temperature.header.seq = i
        temperature.header.stamp = rospy.Time.now()
        temperature.header.frame_id = "Temperature Sensor"
        temperature.temperature = TemperaturAuswertung()
        rospy.loginfo(temperature)
        pub.publish(temperature)
        time.sleep(sleeptime)
        i = i + 1

if __name__ == '__main__':

    try:
        talker()
    except rospy.ROSInterruptException:
        pass
