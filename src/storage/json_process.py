import os
import json
from datetime import datetime

class JsonProcessor:
    def __init__(self, output_dir="data/raw"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_file_path(self, stock_code: str) -> str:
        return os.path.join(self.output_dir, f"{stock_code}.json")

    def _load_json(self, stock_code: str) -> dict:
        path = self._get_file_path(stock_code)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_json(self, stock_code: str, data: dict):
        path = self._get_file_path(stock_code)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_trade(self, stock_code: str, trade_time: str, trade_data: dict):
        """
        trade_data = {
            "price": "29.50",
            "volume": "200",
            "side": "B"
        }
        """
        data = self._load_json(stock_code)
        timestamp = datetime.now().strftime("%H:%M:%S.%f")

        if timestamp not in data:
            data[timestamp] = {
                "Khớp": "",
                "Giá": "",
                "KL": "",
                "M/B": "",
                "zone": [
                    {"KL_mua 1": "", "Gia_mua 1": "", "Gia_ban 1": "", "KL_ban 1": ""},
                    {"KL_mua 2": "", "Gia_mua 2": "", "Gia_ban 2": "", "KL_ban 2": ""},
                    {"KL_mua 3": "", "Gia_mua 3": "", "Gia_ban 3": "", "KL_ban 3": ""}
                ]
            }

        data[timestamp]["Khớp"] = trade_time
        data[timestamp]["Giá"] = trade_data["price"] / 1000.0
        data[timestamp]["KL"] = trade_data["volume"]
        data[timestamp]["M/B"] = trade_data["side"]

        self._save_json(stock_code, data)

    def update_orderbook(self, stock_code: str, order_data: list[dict]):
        """
        order_data = {
            "bids": [
                {
                    "price": 22600,
                    "volume": 13900
                },
                {
                    "price": 22550,
                    "volume": 300
                },
                {
                    "price": 22500,
                    "volume": 107000
                }
            ],
            "asks": [
                {
                    "price": 22700,
                    "volume": 1000
                },
                {
                    "price": 22750,
                    "volume": 5000
                },
                {
                    "price": 22850,
                    "volume": 30000
                }
            ]
        }
        """
        data = self._load_json(stock_code)
        timestamp = datetime.now().strftime("%H:%M:%S.%f")

        if timestamp not in data:
            data[timestamp] = {
                "Khớp": "",
                "Giá": "",
                "KL": "",
                "M/B": "",
                "zone": []
            }

        new_zone=[]
        for i in range(3):
            new_zone.append({
                f"KL_mua {i+1}": order_data['bids'][i]['volume'] ,
                f"Gia_mua {i+1}": order_data['bids'][i]['price'] / 1000.0,
                f"Gia_ban {i+1}": order_data['asks'][i]['price'] / 1000.0,
                f"KL_ban {i+1}": order_data['asks'][i]['volume'],
            })
        data[timestamp]["zone"] = new_zone
        
        self._save_json(stock_code, data)
