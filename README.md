# IPpy
Parallel testing of IP addresses and domains in python.
Reads IP addresses and domains from a CSV file and gives two lists of working and not working ones.

## About
- Written in Python 3
- Testing of IPs and domains is done in parallel. 
- By default there are 4 Workers.
- All Workers work on an input Queue and a output Queue.
```
# The number of workers.
NUM_WORKERS = 4
```

## Modes
- Verbose, if true ping output will be displayed.
```
# Mode
verbose = True
```

## Support
- Currently Windows and Linux are supported.
- Supports both IPv4 and IPv6 IPs and domain names.
```
# Examples
127.0.0.1
::1
localhost
```

## Install
```
git clone https://github.com/shivammathur/IPpy.git
cd ippy
pip install -r requirements.txt
```

## Run
```
python ip.py
```
