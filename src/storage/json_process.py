# import json
# import os
# from logger import get_logger

# logger = get_logger(__name__)

# class JsonProcessor:
#     def __init__(self, output_dir="data/raw"):
#         self.output_dir = output_dir
#         os.makedirs(self.output_dir, exist_ok=True)  # Tạo thư mục nếu chưa có

#     def _get_file_path(self, stock_code: str) -> str:
#         """Trả về đường dẫn file JSON theo stock_code."""
#         return os.path.join(self.output_dir, f"{stock_code}.json")

#     def _load_json(self, stock_code: str) -> dict:
#         file_path = self._get_file_path(stock_code)
#         if os.path.exists(file_path):
#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     return json.load(f)
#             except json.JSONDecodeError:
#                 logger.warning(f"File JSON {file_path} lỗi, khởi tạo dữ liệu rỗng")
#                 return {}
#         return {}

#     def _save_json(self, stock_code: str, data: dict):
#         file_path = self._get_file_path(stock_code)
#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)

#     def update_trade(self, stock_code: str, timestamp: str, trade_data: dict):
#         data = self._load_json(stock_code)
#         record = data.setdefault(timestamp, {"matched_trade": {}, "order_book": {}})
#         record["matched_trade"].update(trade_data)
#         self._save_json(stock_code, data)

#     def update_orderbook(self, stock_code: str, timestamp: str, book_data: dict):
#         data = self._load_json(stock_code)

#         if timestamp not in data:
#             # Tìm timestamp gần nhất trước đó
#             last_trade = {}
#             if data:
#                 last_time = sorted(data.keys())[-1]
#                 last_trade = data[last_time].get("matched_trade", {})

#             data[timestamp] = {
#                 "matched_trade": last_trade.copy(),  # giữ nguyên trade cũ
#                 "order_book": {}
#             }

#         data[timestamp]["order_book"].update(book_data)
#         self._save_json(stock_code, data)

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
                    {"KL_mua": "", "Gia_mua": "", "Gia_ban": "", "KL_ban": ""},
                    {"KL_mua": "", "Gia_mua": "", "Gia_ban": "", "KL_ban": ""},
                    {"KL_mua": "", "Gia_mua": "", "Gia_ban": "", "KL_ban": ""}
                ]
            }

        data[timestamp]["Khớp"] = trade_time
        data[timestamp]["Giá"] = trade_data["price"]
        data[timestamp]["KL"] = trade_data["volume"]
        data[timestamp]["M/B"] = trade_data["side"]

        self._save_json(stock_code, data)

    def update_orderbook(self, stock_code: str, order_data: list[dict]):
        """
        order_data = [
            {"KL_mua": "100", "Gia_mua": "29.50", "Gia_ban": "29.55", "KL_ban": "200"},
            ...
        ]
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

        data[timestamp]["zone"] = order_data
        self._save_json(stock_code, data)
