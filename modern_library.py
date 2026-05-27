import json
import os

class Book:
    """代表單一書籍的資料結構"""
    def __init__(self, title: str, isbn: str, status: str = "in"):
        self.title = title
        self.isbn = isbn
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "isbn": self.isbn,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["title"], data["isbn"], data["status"])


class LibraryManager:
    """負責圖書館的核心邏輯與檔案 I/O"""
    def __init__(self, storage_file: str = "books.json"):
        self.storage_file = storage_file
        self.books = {}  # 使用 dict 以 ISBN 作為 Key，加速查詢效率
        self.load_books()

    def load_books(self):
        """從 JSON 檔案讀取書籍資料"""
        if not os.path.exists(self.storage_file):
            return

        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data_list = json.load(f)
                for item in data_list:
                    book = Book.from_dict(item)
                    self.books[book.isbn] = book
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[警告] 預載檔案 {self.storage_file} 格式損毀，將初始化新資料庫。錯誤: {e}")
            self.books = {}
        except Exception as e:
            print(f"[錯誤] 讀取檔案時發生未知錯誤: {e}")

    def save_books(self):
        """將書籍資料一次性寫入 JSON 檔案"""
        try:
            data_list = [book.to_dict() for book in self.books.values()]
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[錯誤] 儲存檔案失敗: {e}")

    def is_isbn_exists(self, isbn: str) -> bool:
        return isbn in self.books

    def add_book(self, title: str, isbn: str, status: str) -> bool:
        """新增書籍，若 ISBN 已存在則拒絕"""
        if self.is_isbn_exists(isbn):
            return False
        self.books[isbn] = Book(title, isbn, status)
        return True

    def get_all_books(self):
        return self.books.values()

    def borrow_book(self, isbn: str) -> bool:
        """借閱書籍，將狀態改為 borrowed"""
        if self.is_isbn_exists(isbn):
            self.books[isbn].status = "borrowed"
            return True
        return False


def main():
    manager = LibraryManager("books.json")
    print("=== 圖書管理系統 v1.0 (Modern) ===")
    
    while True:
        try:
            op = input("> ").strip()
            if not op:
                continue
            
            if op == "exit":
                manager.save_books()
                print("系統關閉")
                break
                
            elif op.startswith("add "):
                # 擷取 add 後面的參數並依 '/' 分割
                raw_data = op[4:].strip().split("/")
                if len(raw_data) == 3 and all(raw_data):
                    title, isbn, status = raw_data[0].strip(), raw_data[1].strip(), raw_data[2].strip()
                    if manager.add_book(title, isbn, status):
                        print("Success")
                    else:
                        print("ISBN Exist")
                else:
                    print("Format Error")
                    
            elif op == "show":
                books = manager.get_all_books()
                if not books:
                    print("(目前圖書館內無書籍)")
                for book in books:
                    print(f"書名: {book.title}, ISBN: {book.isbn}, 狀態: {book.status}")
                    
            elif op.startswith("borrow "):
                target_isbn = op[7:].strip()
                if manager.borrow_book(target_isbn):
                    print("Updated")
                else:
                    print("ISBN Not Found")
            else:
                print("Unknown Command")
                
        except Exception as e:
            print(f"[異常] 系統執行時發生非預期錯誤: {e}")

if __name__ == "__main__":
    main()