import websocket 
import json
from logger import get_logger

logger=get_logger(__name__)

class WebsocketClient:
    def __init__(self, url, stock_codes, on_message_callback=None):
        self.url=url
        self.stock_codes=stock_codes
        self.on_message_callback=on_message_callback
        self.ws=None
        self.is_running=False

    def on_open(self,ws):
        for code in self.stock_codes:
            msg_matchedTrades={"type":"sub","topic":"leTableAddV2","variables":[code],"component":"matchedPriceHistoriesTable"} 
            msg_priceDepth={"type":"sub","topic":"stockRealtimeBySymbolsAndBoards","variables":{"symbols":[code],"boardIds":["MAIN"]},"component":"priceDepth"}
            ws.send(json.dumps(msg_matchedTrades))
            ws.send(json.dumps(msg_priceDepth))
            logger.info(f"Subscribed to {code}")

    def on_message(self, ws, message):
        if self.on_message_callback:
            self.on_message_callback(message)

    def on_error(self,ws, error):
        logger.error(f"Websocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.warning("Websocket connection closed")
    def run_forever(self):
        self.is_running=True
        self.ws=websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
        )
        self.ws.run_forever()