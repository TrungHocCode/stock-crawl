import time
from datetime import datetime
from crawler.data_handler import DataHandler
from crawler.ws_client import WebsocketClient
from storage.json_process import JsonProcessor
from logger import get_logger
from storage.excel_process import ExcelProcessor
logger = get_logger(__name__)

def run_app(stock_codes: list[str]):
    if not stock_codes:
        logger.error("Chưa nhập mã chứng khoán nào!")
        return

    logger.info(f"Đang subscribe các mã: {stock_codes}")

    json_processor = JsonProcessor(output_dir="data/raw")
    data_handler = DataHandler()

    def handle_message(message: str):
        parsed = data_handler.parse_message(message)
        if not parsed:
            return
        stock_code = parsed["stock_code"]
        if parsed["type"] == "matched_trade":
            timestamp = parsed["time"]  # giờ khớp lệnh
            trade_data = {
                "price": parsed["price"],
                "volume": parsed["volume"],
                "side": parsed["side"],
            }
            json_processor.update_trade(stock_code, timestamp, trade_data)

        elif parsed["type"] == "order_book":
            timestamp = datetime.now().strftime("%H:%M:%S") 
            book_data = {
                "bids": parsed["bids"],
                "asks": parsed["asks"],
            }
            json_processor.update_orderbook(stock_code, book_data)

    url = "wss://iboard-pushstream.ssi.com.vn/realtime"  
    ws_client = WebsocketClient(url, stock_codes, on_message_callback=handle_message)

    try:
        ws_client.run_forever()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Dừng chương trình (Ctrl+C).")
    except Exception as e:
        logger.error(f"Lỗi trong run_app: {e}")
