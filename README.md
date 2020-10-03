# Python version

This is a simple logger for Bamberg Bambados. It could easily adapter for every organization backed by ticos-systems.cloud. It does not offer any scheduling and simply writes to STDOUT. Thereofre this crontab would be useful:

```
* * * * * /home/debuglevel/bambados-visitor-logger/venv/bin/python3 /home/debuglevel/bambados-visitor-logger/main.py > /home/debuglevel/bambados-visitor-logger/log.csv
```

Afterwards this CSV could be fed into a graph visualizer like Grafana to generate something beautiful. (Althogh feeding it directly into a time series database would be better.)

# Golang version

Although probably a really bad piece of golang code, it works. But unfortunately it is not really smaller than the Python venv 🤔, which was the intention.

## Development cheat sheet

Run with `go run main.go` or build binary with `go build -o logger` or cross compile with `GOOS=windows go build -o logger.exe`. Format with `gofmt -s -w main.go`.
