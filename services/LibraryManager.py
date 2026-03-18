from services.BookDatabase import BookDatabase
from services.HistoryDatabase import HistoryDatabase
from models.book import Book

class LibraryManager(BookDatabase, HistoryDatabase):
    def __init__(self, data_path, borrow_history_path):
        HistoryDatabase.__init__(self, borrow_history_path)
        BookDatabase.__init__(self, data_path)

    def add_book(self, isbn, title, author, category, p_year, amount):
        isbn, title, author, category = isbn.lower(), title.lower(), author.lower(), category.lower()
        book = Book(isbn, title, author, category, p_year, amount)
        BookDatabase.add_book(self, book)

    def display_all_books(self):
        index = 1
        for books in self._hashtable.values():
            for book in books: #Book ở đây đang là object
                print(f'{index}. {book}')
                index += 1
    
    def display_book(self, books):
        for index, book in enumerate(books, 0):
            print(f'{index+1}. {book}')
    
    def search_book(self, isbn = None, title = None, author = None, category = None, p_year = None): 
        if isbn:
            hashkey = self.isbn_hash_function(isbn)
            for book in self._hashtable[hashkey]:
                if book.isbn == isbn:
                    return [book]
                raise ValueError(f'Không tìm thấy sách với isbn là {isbn}')
        else:
            results = []
    # Duyệt qua tất cả các danh sách sách trong các ngăn băm
        for books_list in self._hashtable.values():
            for book in books_list:
                
                # Kiểm tra từng điều kiện. Nếu tham số là None -> Coi như thỏa mãn (True)
                # Dùng toán tử 'in' cho title/author để tìm kiếm gần đúng (partial match)
                check_title = (title is None or title.lower() in book.title.lower())
                check_author = (author is None or author.lower() in book.author.lower())
                check_category = (category is None or category.lower() == book.category.lower())
                check_year = (p_year is None or int(p_year) == book.p_year)

                # Chỉ thêm vào kết quả nếu thỏa mãn TẤT CẢ các điều kiện đã nhập (Logic AND)
                if check_title and check_author and check_category and check_year:
                    results.append(book)

        if len(results) == 0:
            raise ValueError(f'Không tìm thấy sách như bạn tìm')

        return results

    def find_availble_book(self, title, author, isbn = None):
        result = [] #Các đối tượng book
        if isbn is not None:
            hashkey = self.isbn_hash_function(isbn)
            for book in self._hashtable[hashkey]:
                if book.isbn == isbn and book.amount > 0:
                    result.append(book)
        else:
            for key in self._hashtable.keys():
                for book in self._hashtable[key]:
                    if book.title == title and book.author == author and book.amount > 0:
                        result.append(book)
        
        return result

    
    def borrow_book(self, isbn, borrow_amount : int):
        hashkey = self.isbn_hash_function(isbn)
        for book in self._hashtable[hashkey] :
            if book.isbn == isbn:
                if book.amount < borrow_amount:
                    raise ValueError('!! Không đủ số sách để mượn')
                self.update_book(isbn= isbn, change_amount= -borrow_amount)
                self.add_borrow_history(isbn, borrow_amount)
                self.save_all_to_database()
    
    def return_book(self, borrow_id, isbn = None):
        try:
            isbn, borrow_amount = HistoryDatabase.update_return_status(self, borrow_id)
            self.update_book(isbn, change_amount= borrow_amount)
        except Exception as e:
            print(e)

    def display_borrow_history(self):
        try:
            with open(self.borrow_history_path, 'r') as file:
                for record in file.readlines():
                    borrow_id, isbn, borrow_amount, return_status = record.strip('\n').split(',')
                    borrow_amount = int(borrow_amount)
                    return_status = bool(return_status)
                    print(f'Borrow_id: {borrow_id} | ISBN: {isbn} | Borrow amount: {borrow_amount} | Return status: {return_status}')
        except Exception as e:
            print(e)

    def top_books_stat(self, top_n = 5):
        top_ns = HistoryDatabase.top_book_stat(self, top_n= top_n)
        for isbn, freq in top_ns:
            # Dùng hàm search_book đã có để lấy tên sách từ ISBN
            book = self.search_book(isbn=isbn)[0]
            print(f"Sách: {book.title} | Số lượt mượn: {freq}")