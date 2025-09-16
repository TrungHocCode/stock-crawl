from app import run_app

def main():
    stock_codes = input("Nhập danh sách mã chứng khoán (phân cách bằng dấu phẩy): ") \
        .strip().upper().split(",")
    stock_codes = [code.strip() for code in stock_codes if code.strip()]
    run_app(stock_codes)

if __name__ == "__main__":
    main()
