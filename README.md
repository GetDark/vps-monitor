[English](#english) | [Русский](#русский)

---

<a name="english"></a>
# vps-monitor

Lightweight FastAPI backend that exposes real-time VPS system metrics via a single JSON endpoint. No external agents or exporters needed — reads the Docker socket directly.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/metrics` | Full system metrics JSON |

## Metrics

`GET /api/metrics` returns:

| Field | Description |
|-------|-------------|
| `cpu.percent` | CPU usage % |
| `cpu.load1` | 1-min load average (normalized by core count) |
| `cpu.cores` | Number of logical CPU cores |
| `memory.used_gb` | Used memory (GB) |
| `memory.total_gb` | Total memory (GB) |
| `memory.percent` | Memory usage % |
| `disk.used_gb` | Used disk (GB) |
| `disk.total_gb` | Total disk (GB) |
| `disk.percent` | Disk usage % |
| `network.rx_kbps` | Incoming traffic (KB/s, delta since last call) |
| `network.tx_kbps` | Outgoing traffic (KB/s, delta since last call) |
| `network.total_rx_gb` | Total received (GB) |
| `network.total_tx_gb` | Total sent (GB) |
| `uptime` | Human-readable uptime (e.g. `3d 12h 5m`) |
| `docker_running` | Number of running Docker containers |
| `ts` | Unix timestamp |

## Quick Start

```bash
git clone https://github.com/GetDark/vps-monitor.git
cd vps-monitor

docker compose up -d
```

API available at `http://localhost:8000`.

CORS is pre-configured for `agent.swiftstream.ru` — edit `app/main.py` to change.

## Tech Stack

- Python 3 / FastAPI
- psutil (CPU, memory, disk, network)
- Docker socket API (no CLI needed)
- Docker + Docker Compose

---

<a name="русский"></a>
# vps-monitor

Лёгкий FastAPI-бэкенд, отдающий актуальные системные метрики VPS через один JSON-эндпоинт. Без внешних агентов и экспортёров — читает Docker socket напрямую.

## Эндпоинты

| Эндпоинт | Описание |
|----------|----------|
| `GET /health` | Проверка здоровья |
| `GET /api/metrics` | Полный JSON с системными метриками |

## Метрики

`GET /api/metrics` возвращает:

| Поле | Описание |
|------|----------|
| `cpu.percent` | Загрузка CPU % |
| `cpu.load1` | Средняя нагрузка за 1 мин (нормализованная по числу ядер) |
| `cpu.cores` | Количество логических ядер |
| `memory.used_gb` | Используемая память (ГБ) |
| `memory.total_gb` | Общая память (ГБ) |
| `memory.percent` | Загрузка памяти % |
| `disk.used_gb` | Занято на диске (ГБ) |
| `disk.total_gb` | Всего на диске (ГБ) |
| `disk.percent` | Заполненность диска % |
| `network.rx_kbps` | Входящий трафик (КБ/с, дельта с последнего запроса) |
| `network.tx_kbps` | Исходящий трафик (КБ/с, дельта с последнего запроса) |
| `network.total_rx_gb` | Всего получено (ГБ) |
| `network.total_tx_gb` | Всего отправлено (ГБ) |
| `uptime` | Аптайм в читаемом виде (например `3d 12h 5m`) |
| `docker_running` | Количество запущенных Docker-контейнеров |
| `ts` | Unix timestamp |

## Быстрый старт

```bash
git clone https://github.com/GetDark/vps-monitor.git
cd vps-monitor

docker compose up -d
```

API доступен на `http://localhost:8000`.

CORS преднастроен для `agent.swiftstream.ru` — изменить в `app/main.py`.

## Технологический стек

- Python 3 / FastAPI
- psutil (CPU, память, диск, сеть)
- Docker socket API (без CLI)
- Docker + Docker Compose
