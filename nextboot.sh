#!/bin/bash

readonly BOOT_NAME="ubuntu"  # uefi entry name

/bin/efibootmgr | grep -E '^Boot[0-9]{4}(\*| ) .*'$BOOT_NAME'.*' | sed -E 's/^Boot//g' | sed -E 's/(\*| ) .*'$BOOT_NAME'.*//g' | while read num;
do
  efibootmgr --bootnext $num && reboot
done
