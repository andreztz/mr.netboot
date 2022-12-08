#!/bin/sh
# https://www.puppeteers.net/blog/creating-pxe-bootable-virtualbox-vms/
# https://www.virtualbox.org/manual/ch08.html#vboxmanage-modifyvm
vboxmanage controlvm pxetest poweroff
sleep 2
vboxmanage unregistervm pxetest --delete
sleep 2
vboxmanage closemedium pxeboot-disk.vdi --delete
