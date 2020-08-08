#!/usr/bin/python

import subprocess as sbp
import time

# Variables Globales
sample_num = 10
sample_time = 0.5
fan_speed = 0
hwmon_path = '/sys/devices/platform/asus-nb-wmi/hwmon/'

outLS = sbp.Popen(['ls', hwmon_path], stdout=sbp.PIPE)

fan_path = outLS.communicate()[0].decode('UTF-8').strip()
print(f'Device found {fan_path}')

fan_path = hwmon_path + fan_path
print(f'Full path {fan_path}')

temp_path = fan_path + '/temp1_input'
pwm_path = fan_path + '/pwm1'

while (True):
    i = 1
    temp_avg = 0

    while (i <= sample_num):
        outTemp = sbp.Popen(['cat', temp_path], stdout=sbp.PIPE)
        temp_fan = int(outTemp.communicate()[
                       0].decode('UTF-8').strip()) // 1000
        temp_avg += temp_fan

        print(f'#{i} temp {temp_fan}[°C] avg{temp_avg // i}')
        time.sleep(sample_time)
        i += 1

    temp_avg = int(temp_avg // sample_num)

    print(f'Setting speed in base to {temp_avg}')
    if temp_avg > 90:
        fan_speed = '250'
    elif temp_avg < 40:
        fan_speed = '100'
    else:
        fan_speed = str(temp_avg*3 - 20)

    with open(pwm_path, 'w') as fan_file:
        print(f'Writing {fan_speed} in {pwm_path}')
        fan_file.write(fan_speed)
    fan_file.close()
