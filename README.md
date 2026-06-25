# vps-monitor

Lightweight FastAPI service that exposes **real-time VPS metrics** via a JSON API — CPU, RAM, disk, network rates, uptime, Docker container count.

Used as the backend for the live monitoring widget on [agent.swiftstream.ru](https://agent.swiftstream.ru).

## Endpoint

```
GET /api/metrics
```

```json
{
  "cpu":     { "percent": 12.3, "load1": 8.1, "cores": 2 },
  "memory":  { "used_gb": 1.24, "total_gb": 4.0, "percent": 31.0 },
  "disk":    { "used_gb": 18.3, "total_gb": 50.0, "percent": 36.6 },
  "network": { "rx_kbps": 42.1, "tx_kbps": 18.7, "total_rx_gb": 12.4, "total_tx_gb": 5.1 },
  "uptime":  "12d 3h 42m",
  "docker_running": 4,
  "ts": 1750000000
}
```

## Run

```bash
docker compose up -d
curl http://localhost:8001/api/metrics
```

## nginx proxy

```nginx
location /monitor/ {
    proxy_pass         http://127.0.0.1:8001/;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_read_timeout 10s;
}
```

## Notes

- `pid: host` in docker-compose — required for psutil to read host process metrics
- `/var/run/docker.sock` mounted read-only — for `docker ps -q` container count
- Network rates computed between calls (delta / elapsed seconds)
- First `/api/metrics` call after start returns `rx_kbps: 0` / `tx_kbps: 0` — expected (no previous sample yet)
