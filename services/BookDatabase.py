from collections import defaultdict
from models.book import Book

class BookDatabase:
    def __init__(self, data_path):
        self._hashtable = defaultdict(list)
        self.__data_path = data_path
        self.categories = set()

        with open(data_path, 'r', encoding='utf-8') as file:
            for row in file.readlines():
                row = [item.strip() for item in row.strip('\n').split(',')]
                isbn, title, author, category, p_year, amount = row
                isbn, title, author, category = isbn.lower(), title.lower(), author.lower(), category.lower()
                self.categories.add(category)
                new_book = Book(isbn, title, author, category, int(p_year), int(amount))
                BookDatabase.initialize_book(self, new_book)

    def add_database(self, book: Book):
        with open(self.__data_path, 'a', encoding='utf-8') as file:
            row = f'{book.isbn}, {book.title}, {book.author}, {book.category}, {book.p_year}, {book.amount}\n'
            file.writelines(row)

    def isbn_hash_function(self, isbn : str, table_size=10007) -> int:
        """
        Hàm băm cho ISBN sử dụng thuật toán Polynomial Rolling Hash.
        table_size nên là một số nguyên tố lớn để giảm thiểu xung đột.
        """
        hash_val = 0
        p = 31  # Một số nguyên tố nhỏ
        
        # Loại bỏ dấu gạch ngang nếu có
        clean_isbn = isbn.replace("-", "").strip()
        
        for char in clean_isbn:
            # Chuyển ký tự thành số (ISBN có thể có chữ 'X' ở cuối)
            char_val = ord(char)
            hash_val = (hash_val * p + char_val) % table_size
            
        return hash_val

    def save_all_to_database(self):
        """
        Ghi đè toàn bộ nội dung từ Hashtable trong RAM vào file database.txt.
        Dùng khi có sự thay đổi lớn như Update hoặc Remove book.
        """
        try:
            # Mở file ở chế độ 'w' để xóa sạch nội dung cũ và ghi mới hoàn toàn
            with open(self.__data_path, 'w', encoding='utf-8') as file:
                # Duyệt qua từng danh sách các đối tượng Book trong values của hashtable
                for book_list in self._hashtable.values():
                    for book in book_list:
                        # Tạo dòng dữ liệu chuẩn CSV từ các thuộc tính của object Book
                        row = f'{book.isbn}, {book.title}, {book.author}, {book.category}, {book.p_year}, {book.amount}\n'
                        file.writelines(row)
            # print("Đã cập nhật dữ liệu từ RAM vào database.txt thành công.")
        except Exception as e:
            print(f"Lỗi khi lưu database: {e}")
    
    def initialize_book(self, book):
        isbn = book.isbn
        hash_key = self.isbn_hash_function(isbn)
        if self.is_exist(hash_key, isbn):
            self._hashtable[hash_key].append(book)
        else:
            raise AssertionError('Đã có cuốn sách này trong thư viện')

    def add_book(self, book : Book):
        isbn = book.isbn
        hash_key = self.isbn_hash_function(isbn)
        if self.is_exist(hash_key, isbn):
            self._hashtable[hash_key].append(book)
            self.add_database(book)
            self.save_all_to_database()
        else:
            raise AssertionError('Đã có cuốn sách này trong thư viện')

    def is_exist(self, hashkey, isbn) -> bool:
        for book_in_data in self._hashtable[hashkey]:
            if book_in_data.isbn == isbn:
                return False
        return True
    
    def remove_book(self, isbn):
        hashkey = self.isbn_hash_function(isbn)
        for index, book in enumerate(self._hashtable[hashkey], 0):
            if book.isbn == isbn:
                self._hashtable[hashkey].pop(index)
                self.save_all_to_database()
                return
        raise AssertionError('Không có cuốn sách này trong thư viện')


    def update_book(self, isbn, title = None, author = None, category = None, p_year = None, change_amount = None):
        hashkey = self.isbn_hash_function(isbn)
        if self.is_exist(hashkey, isbn) is False:
            for index, book in enumerate(self._hashtable[hashkey], 0):
                if book.isbn == isbn:
                    book.title = title if title is not None else book.title
                    book.author = author if author is not None else book.author
                    book.category = category if category is not None else book.category
                    book.p_year = p_year if p_year is not None else book.p_year
                    book.amount += change_amount if change_amount is not None else 0
                    self.save_all_to_database()
        else:
            raise AssertionError('Không có cuốn sách này trong thư viện')