from logger import get_logger
logger = get_logger(__name__)

class DataHandler:
    def __init__(self):
        pass

    def parse_message(self, raw_message: str) -> dict:
        """
        Parse raw WebSocket message thành dict.
        """
        try:
            parts = raw_message.strip().split("|")

            if len(parts) < 3:
                logger.warning(f"Invalid message: {raw_message}")
                return {}

            # Loại message: matched trade hay order book?
            if parts[1].startswith("L#"):
                return self._parse_matched_trade(parts)
            elif parts[1].startswith("S#"):
                return self._parse_order_book(parts)
            else:
                logger.debug(f"Unknown message type: {raw_message}")
                return {}

        except Exception as e:
            logger.error(f"Parse error: {e} | Message: {raw_message}")
            return {}

    def _parse_matched_trade(self, parts: list) -> dict:
        """
        Parse matched trade message (L#).
        Ví dụ:
        MAIN|L#HPG|30550|19400|668900|09:15:00|30350|bu|200|0.66|U|MAIN|1757988900021
        """
        return {
            "type": "matched_trade",
            "stock_code": parts[1].replace("L#", ""),
            "price": int(parts[2]),
            "volume": int(parts[3]),
            "time": parts[5],
            "side": "B" if parts[7] =="bu" else "M",   # "bu" = buy, "se" = sell
        }

    def _parse_order_book(self, parts: list) -> dict:
        """
        Parse order book message (S#).
        Do message quá dài, tách riêng BID / ASK book.
        """
        stock_code = parts[1].replace("S#", "")

        bids = []
        asks = []

        try:
            for i in range(2, 20, 2):
                if parts[i] and parts[i+1]:
                    bids.append({
                        "price": int(parts[i]),
                        "volume": int(parts[i+1])
                    })

            for i in range(20, 40, 2):
                if parts[i] and parts[i+1]:
                    asks.append({
                        "price": int(parts[i]),
                        "volume": int(parts[i+1])
                    })
        except Exception as e:
            logger.error(f"Error parsing order book: {e}")

        return {
            "type": "order_book",
            "stock_code": stock_code,
            "bids": bids,
            "asks": asks,
            "raw": parts 
        }