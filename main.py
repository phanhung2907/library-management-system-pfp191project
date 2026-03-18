from interface import Interface
def main():
    interface = Interface()
    print('--- Chương trình quản lý thư viện đã mở ---')
    while True:
        print('--- MENU ---')
        print('1. Hiển thị sách trong thư viện')
        print('2. Mượn sách')
        print('3. Trả sách')
        print('4. Tìm kiếm sách')
        print('5. Thống kê lịch sử mượn sách')
        print('6. Các chức năng nâng cao')
        choice = input('Chọn chức năng: ')
        choice = interface.preprocess_string_input(choice)
        print()

        match choice:
            case '1':
                print('--- Các sách có trong thư viện ---')
                interface.display_all_book()
                input()
            case '2':
                interface.borrow_book()
                input()
            case '3':
                interface.return_book()
                input()
            case '4':
                interface.search_book()
                input()
            case '5':
                interface.show_topn_borrow_book()
                input()
            case '6':
                interface.advance_operation()
                input()
            case _:
                print('--- Kết thúc chương trình ---')
                break

main()