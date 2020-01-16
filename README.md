# Honeypot-Project

## Execute

1. Copy the file controller.py in the directory: ~/pox/ext
2. In the directory ~/pox execute the command: ```./pox.py controller```
3. In te directory where you have the file topo.py execute: ```sudo mn --custom topo.py --topo topo --mac --switch ovsk --controller remote --nat --ipbase 192.168.1.0/24```
4. In the mininet terminal run the command: ```source setup.sh```
5. Run commands from the mininet terminal or from an external terminal. You can also enter to the webpage running in the host 'hd1'
