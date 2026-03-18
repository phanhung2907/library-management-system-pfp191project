from services import LibraryManager
from models import Book

class Interface:
    def __init__(self):
        database_path = r'D:\personal_study\fptu\semes_1\PFP101\final project\utils\database.txt'
        borrow_history_path = r'D:\personal_study\fptu\semes_1\PFP101\final project\utils\borrow_history.txt'
        self.lib_manager = LibraryManager(database_path, borrow_history_path)
    
    def preprocess_string_input(self, string: str) -> str:
        if string == '':
            return None
        return string.strip().lower()
    
    def add_book(self):
        print('--- Bắt đầu chức năng thêm sách ---')
        isbn = self.preprocess_string_input( input('Mã isbn: '))
        title = self.preprocess_string_input(input('Tên sách: '))
        author = self.preprocess_string_input(input('Tên tác giả: '))
        category = self.preprocess_string_input(input('Loại sách: '))
        p_year = self.preprocess_string_input(input('Năm xuất bản: '))
        amount = self.preprocess_string_input(input('Số cuốn sách: '))

        p_year = int(p_year)
        amount = int(amount)

        if not isbn or not title or not author or not p_year or not amount:
            raise ValueError('Chưa đủ dữ liệu để thêm sách')
        
        self.lib_manager.add_book(isbn, title, author, category, p_year, amount)
        print(f'$$ Thêm sách có mã ISBN: {isbn} thành công')

    def update_book(self):
        print('--- Bắt đầu chức năng cập nhập sách ---')
        isbn = self.preprocess_string_input( input('Mã isbn: '))
        title = self.preprocess_string_input(input('Tên sách: '))
        author = self.preprocess_string_input(input('Tên tác giả: '))
        category = self.preprocess_string_input(input('Loại sách: '))
        p_year = self.preprocess_string_input(input('Năm xuất bản: '))
        amount = self.preprocess_string_input(input('Số cuốn sách: '))

        if not isbn:
            raise ValueError('Không có mã isbn')
        
        self.lib_manager.update_book(isbn, title, author, category, p_year, amount)
        print(f'$$ Sách mã isbn: {isbn} đã cập nhập thành công')

    def remove_book(self):
        print('--- Bắt đầu chức năng xóa sách ---')
        isbn = self.preprocess_string_input( input('Mã isbn: '))
        self.lib_manager.remove_book()
        if not isbn:
            raise ValueError('Thiếu thông tin mã ISBN !!')
        
        self.lib_manager.remove_book(isbn)
        print(f'$$ Sách mã isbn: {isbn} đã xóa thành công')
    
    
    def borrow_book(self):
        print('--- BẮT ĐẦU MƯỢN SÁCH ---')
        isbn = self.preprocess_string_input(input('Nhập số isbn: '))
        title = self.preprocess_string_input(input('Nhập tên sách: '))
        author = self.preprocess_string_input(input('Nhập tên tác giả: '))
        avai_books = self.lib_manager.find_availble_book(title, author, isbn)
        print('--- Danh sách cuốn sách bạn đang cần tìm ---')
        for index, book in enumerate(avai_books, 0):
            print(f'{index}. {book}')
        choice  = self.preprocess_string_input(input('Hãy chọn index cuốn sách bạn muốn mượn: '))
        borrow_amount = int(self.preprocess_string_input(input('Bạn muốn mượn bao nhiêu cuốn: ')))
        isbn = avai_books[int(choice)].isbn
        try:
            self.lib_manager.borrow_book(isbn, borrow_amount)
            print('$$ Bạn đã mượn sách thành công ')
        except Exception as e:
            print(e)
    
    def return_book(self):
        print('--- Bắt đầu trả sách ---')
        borrow_id = input('Nhập mã mượn sách: ')
        borrow_id = self.preprocess_string_input(borrow_id)
        try:
            self.lib_manager.return_book(borrow_id)
            print('$$ Trả sách thành công')
        except Exception as e:
            print(e)
    
    def search_book(self):
        print('--- Tìm kiếm sách ---')
        isbn = self.preprocess_string_input(input('ISBN sách: '))
        title = self.preprocess_string_input(input('Tiêu đề: '))
        author = self.preprocess_string_input(input('Tác giả: '))
        category = self.preprocess_string_input(input('Thể loại: '))
        p_year = self.preprocess_string_input(input('Năm xuất bản: '))

        try:
            books = self.lib_manager.search_book(isbn, title, author, category, p_year)
            print('--- Danh sách cuốn sách cần tìm ---')
            self.lib_manager.display_book(books)
        except Exception as e:
            print(e)


    def display_borrow_history(self):
        self.lib_manager.display_borrow_history()

    def display_all_book(self):
        self.lib_manager.display_all_books()

    def show_topn_borrow_book(self):
        print('--- Thống kê lịch sử mượn sách ---')
        self.display_borrow_history()
        print()
        top_n = int(self.preprocess_string_input(input('Nhập top_n cuốn sách mượn nhiều nhất: ')))
        self.lib_manager.top_books_stat(top_n)

    def advance_operation(self):
        while True:
            print('--- Chức năng nâng cao ---')
            print('1. Để thêm sách')
            print('2. Để update sách')
            print('3. Để xóa sách ')
            choice = self.preprocess_string_input( input('Chọn chức năng: ') )
            print()
            match choice:
                case '1':
                    try:
                        self.add_book()
                    except Exception as e:
                        print(f'Có lỗi: {e}')
                    input()
                case '2':
                    try:
                        self.update_book()
                    except Exception as e:
                        print(f'Có lỗi: {e}')
                    input()
                case '3':
                    try:
                        self.remove_book()
                    except Exception as e:
                        print(f'Có lỗi: {e}')
                    input()
                case _ :
                    print('--- Thoát chức năng nâng cao ---')
                    break

