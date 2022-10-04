BASEDIR = $(shell pwd)

test:
	qemu-system-x86_64 -boot n -m 512M -enable-kvm -device virtio-net,netdev=n1 -netdev user,id=n1,tftp=$(BASEDIR)/netboot/,bootfile=/menu/boot.ipxe
