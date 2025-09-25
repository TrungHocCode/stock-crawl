# Stock Data Collector

This project collects **real-time stock trading data** (including order book and matched trades) from **SSI WebSocket API** and stores it as JSON files for further analysis.  
The system is designed to ensure each stock object always contains both parts:
- `matched_trade`
- `order_book`  

If one part changes, it is updated while the other part remains unchanged.

---

## Features
- Subscribe to stock tickers via **WebSocket**.
- Collect both **order book** and **matched trades**.
- Automatically create a JSON file for each stock code under `data/raw/`.
- Ensure JSON objects always have both fields (`matched_trade`, `order_book`).
- Easy to extend for Excel or database export.
- Easily crawl many stocks that we need
---
## Installation
Clone the repository:
```bash
git clone https://github.com/TrungHocCode/stock-crawl.git
cd stock-crawl
