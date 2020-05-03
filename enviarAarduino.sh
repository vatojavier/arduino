#!/usr/bin/bash

stty -F /dev/ttyACM0 9600 raw -clocal -echo icrnl

a=200
echo $a

for (( ; ; ))
do
	echo $a > /dev/ttyACM0
done
