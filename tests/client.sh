#!/bin/sh
# https://www.puppeteers.net/blog/creating-pxe-bootable-virtualbox-vms/
# https://www.virtualbox.org/manual/ch08.html#vboxmanage-modifyvm
vboxmanage createvm --name "pxetest" --ostype RedHat_64 --register
vboxmanage modifyvm pxetest --description "PXEboot test (CentOS 7)" \
    --memory 2048 --cpus 1 --boot1 net --nic1=bridged \
    --bridge-adapter1=bridge0 --macaddress1 080027fbad17
vboxmanage createmedium disk --filename pxeboot-disk.vdi --size 8192
vboxmanage storagectl pxetest --name "SATA" --add sata --bootable on
vboxmanage storageattach pxetest --storagectl "SATA" --port 1 --type hdd \
    --medium pxeboot-disk.vdi
vboxmanage startvm pxetest
