# Bambados visitor logger

This is a simple logger for Bamberg Bambados. It could easily adapter for every organization backed by ticos-systems.cloud. It does not offer any scheduling and simply writes to STDOUT. Thereofre this crontab would be useful:

```
* * * * * /home/debuglevel/bambados-visitor-logger/venv/bin/python3 /home/debuglevel/bambados-visitor-logger/main.py > /home/debuglevel/bambados-visitor-logger/log.csv
```

Afterwards this CSV could be fed into a graph visualizer like Grafana to generate something beautiful. (Althogh feeding it directly into a time series database would be better.)

## Installation

Do the usual Python venv stuff:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py --help
```
