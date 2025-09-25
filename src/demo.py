import json
from storage.excel_process import ExcelProcessor

excel_processor=ExcelProcessor("./data/raw/VRE(1).json")
excel_processor.run()
print("✅ Đã chuyển đổi xong và lưu")


