class Book:
    def __init__(self, isbn, title, author, category, p_year, amount):
        self.__isbn = isbn
        self.__title = title
        self.__author = author
        self.__category = category
        self.__p_year = p_year
        self.__amount = amount 
    

    @property
    def isbn(self):
        return self.__isbn
    
    @isbn.setter
    def isbn(self, value):
        # Kiểm tra tính hợp lệ trước khi cho phép sửa
        if len(value) < 10:
            raise ValueError("ISBN không hợp lệ!")
        self.__isbn = value
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value : str):
        # Kiểm tra tính hợp lệ trước khi cho phép sửa
        self.__title = value

    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, value : str):
        # Kiểm tra tính hợp lệ trước khi cho phép sửa
        self.__author = value
    
    @property
    def category(self):
        return self.__category
    
    @category.setter                                                        
    def category(self, value : str):
        # Kiểm tra tính hợp lệ trước khi cho phép sửa
        self.__category = value
    
    @property
    def p_year(self):
        return self.__p_year
    
    @p_year.setter
    def p_year(self, value):
        # Kiểm tra tính hợp lệ trước khi cho phép sửa
        self.__p_year = value
    
    @property
    def amount(self):
        return self.__amount
    
    @amount.setter
    def amount(self, value):
        # Kiểm tra tính hợp lệ trước khi cho phép sửa
        self.__amount = value
    
    def __str__(self):
        return f'ISBN: {self.__isbn } | Tên sách: {self.__title} | Tác giả: {self.__author} | Thể loại: {self.__category} | Năm xuất bản: {self.__p_year} | Số cuốn: {self.__amount} cuốn'
    
    def is_available(self):
        return True if self.__amount > 0 else False