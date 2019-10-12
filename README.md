# Slowloris attack & defend implementation

## Attacker

```

1) specify host variable in the `.env` file

2) docker build -t slowloris .

3) docker-compose up -d

```


The goal of Attacker is to exhaust server thread pool via making a lot of HTTP requests and sending headers periodically every 15 seconds, without breaking connection.


## Defender

```
1) docker build -t defender .

2) docker-compose up -d

```

### Tuning nginx performance

Custom settings for `nginx.conf`

1) Set `worker_processes` to `auto` for using maximum CPU cores.
2) Increasing amount of `worker_connections` form `1024` to `2048`.
3) Specify `worker_rlimit_nofile` to 4096. For Changing the limit on the maximum number of open files for worker processes.
4) Reduce `keepalive_timeout` for closing connection faster.
