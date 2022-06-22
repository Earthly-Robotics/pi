import os
# Compile
os.system('arduino-cli compile -b arduino:avr:nano ServoController')

# Upload
command_str = f'arduino-cli -v upload -p /dev/ttyUSB1 --fqbn arduino:avr:nano:cpu=atmega328old ServoController'
os.system(command_str)