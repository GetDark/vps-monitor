import time
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

_boot_time = psutil.boot_time()
_net_prev: tuple[float, float, float] = (time.monotonic(), 0.0, 0.0)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # warm up psutil cpu_percent (first call always returns 0)
    psutil.cpu_percent(interval=None)
    yield


app = FastAPI(title="vps-monitor", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://agent.swiftstream.ru"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/metrics")
async def metrics() -> dict:
    global _net_prev

    # CPU
    cpu_pct = psutil.cpu_percent(interval=None)
    load1, load5, _ = psutil.getloadavg()
    cpu_count = psutil.cpu_count(logical=True)

    # Memory
    mem = psutil.virtual_memory()

    # Disk /
    disk = psutil.disk_usage("/")

    # Uptime
    uptime_sec = int(time.time() - _boot_time)
    days, rem = divmod(uptime_sec, 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    uptime_str = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"

    # Network rates (bytes/s since last call)
    now = time.monotonic()
    net = psutil.net_io_counters()
    elapsed = now - _net_prev[0]
    rx_rate = (net.bytes_recv - _net_prev[1]) / elapsed if elapsed > 0 else 0
    tx_rate = (net.bytes_sent - _net_prev[2]) / elapsed if elapsed > 0 else 0
    _net_prev = (now, float(net.bytes_recv), float(net.bytes_sent))

    # Docker containers via socket API (no docker CLI needed)
    docker_running = 0
    try:
        import http.client, socket as _sock, json as _json

        class _UnixHTTPConn(http.client.HTTPConnection):
            def __init__(self, path: str) -> None:
                super().__init__("localhost")
                self._upath = path

            def connect(self) -> None:
                s = _sock.socket(_sock.AF_UNIX, _sock.SOCK_STREAM)
                s.connect(self._upath)
                self.sock = s

        conn = _UnixHTTPConn("/var/run/docker.sock")
        conn.request("GET", "/containers/json")
        resp = conn.getresponse()
        containers = _json.loads(resp.read())
        docker_running = len(containers)
        conn.close()
    except Exception:
        pass

    return {
        "cpu": {
            "percent": round(cpu_pct, 1),
            "load1": round(load1 / cpu_count * 100, 1),
            "cores": cpu_count,
        },
        "memory": {
            "used_gb": round(mem.used / 1024 ** 3, 2),
            "total_gb": round(mem.total / 1024 ** 3, 2),
            "percent": mem.percent,
        },
        "disk": {
            "used_gb": round(disk.used / 1024 ** 3, 1),
            "total_gb": round(disk.total / 1024 ** 3, 1),
            "percent": disk.percent,
        },
        "network": {
            "rx_kbps": round(rx_rate / 1024, 1),
            "tx_kbps": round(tx_rate / 1024, 1),
            "total_rx_gb": round(net.bytes_recv / 1024 ** 3, 2),
            "total_tx_gb": round(net.bytes_sent / 1024 ** 3, 2),
        },
        "uptime": uptime_str,
        "uptime_sec": uptime_sec,
        "docker_running": docker_running,
        "ts": int(time.time()),
    }
