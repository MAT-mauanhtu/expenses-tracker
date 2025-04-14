import sqlite3
import csv
from datetime import datetime

DB_NAME = "expenses.db"

class ExpenseTracker:
    def __init__(self, db_name):
        """Khởi tạo kết nối cơ sở dữ liệu và tạo bảng nếu chưa có."""
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Tạo bảng lưu trữ dữ liệu nếu chưa tồn tại."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """)

    def add_expense(self, name, amount, category, date=None):
        """Thêm khoản chi tiêu mới vào cơ sở dữ liệu."""
        if not date:
            date = datetime.today().strftime('%Y-%m-%d')
        with self.conn:
            self.conn.execute("""
                INSERT INTO expenses (name, amount, category, date)
                VALUES (?, ?, ?, ?)
            """, (name, amount, category, date))
        print("✅ Đã thêm khoản chi tiêu.")

    def view_expenses(self):
        """Hiển thị danh sách các khoản chi tiêu."""
        print("\n📋 Danh sách chi tiêu:")
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM expenses ORDER BY date DESC")
            rows = cursor.fetchall()
            if not rows:
                print("Chưa có dữ liệu.")
            else:
                for row in rows:
                    print(f"{row[4]} | {row[1]} - {row[2]} VND | Danh mục: {row[3]}")

    def total_by_day(self, target_date):
        """Tính tổng chi tiêu theo ngày."""
        with self.conn:
            cursor = self.conn.execute("""
                SELECT SUM(amount) FROM expenses WHERE date = ?
            """, (target_date,))
            total = cursor.fetchone()[0]
            if total:
                print(f"Tổng chi ngày {target_date}: {total} VND")
            else:
                print(f"Không có khoản chi nào vào ngày {target_date}.")

    def total_by_category(self):
        """Tính tổng chi tiêu theo từng danh mục."""
        print("\n📊 Tổng chi tiêu theo danh mục:")
        with self.conn:
            cursor = self.conn.execute("""
                SELECT category, SUM(amount) FROM expenses GROUP BY category
            """)
            rows = cursor.fetchall()
            if not rows:
                print("Chưa có dữ liệu.")
            else:
                for row in rows:
                    print(f"{row[0]}: {row[1]} VND")

    def export_to_csv(self, csv_file_name):
        """Xuất dữ liệu từ cơ sở dữ liệu sang file CSV."""
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM expenses")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)  # Ghi tên cột
                writer.writerows(rows)  # Ghi dữ liệu

        print(f"✅ Dữ liệu đã được xuất ra file CSV: {csv_file_name}")

    def close(self):
        """Đóng kết nối cơ sở dữ liệu."""
        self.conn.close()

def menu():
    tracker = ExpenseTracker(DB_NAME)
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Thêm khoản chi")
        print("2. Xem danh sách chi tiêu")
        print("3. Tính tổng theo ngày")
        print("4. Tính tổng theo danh mục")
        print("5. Xuất dữ liệu ra CSV")
        print("0. Thoát")
        choice = input("Chọn: ")
        if choice == '1':
            name = input("Tên khoản chi: ")
            try:
                amount = float(input("Số tiền (VND): "))
                category = input("Danh mục (ví dụ: Ăn uống, Giải trí): ")
                date = input("Ngày (YYYY-MM-DD, bỏ trống để lấy hôm nay): ")
                tracker.add_expense(name, amount, category, date)
            except ValueError:
                print("❌ Số tiền phải là một số hợp lệ.")
        elif choice == '2':
            tracker.view_expenses()
        elif choice == '3':
            target_date = input("Nhập ngày cần tính tổng (YYYY-MM-DD): ")
            tracker.total_by_day(target_date)
        elif choice == '4':
            tracker.total_by_category()
        elif choice == '5':
            csv_file_name = input("Nhập tên file CSV (ví dụ: expenses.csv): ")
            tracker.export_to_csv(csv_file_name)
        elif choice == '0':
            tracker.close()
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    menu()