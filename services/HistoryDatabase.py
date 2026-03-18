from collections import Counter


class HistoryDatabase:
    def __init__(self, borrow_history_path):
        self.borrow_history_path = borrow_history_path

    def add_borrow_history(self, isbn, borrow_amount):
        with open(self.borrow_history_path, 'a+') as file:
            file.seek(0)
            tempo = file.readlines()
            if len(tempo) == 0:
                borrow_id = 1
            else:
                previous_id = int(tempo[-1].strip('\n').split(',')[0])
                borrow_id = previous_id + 1
                return_status = False
            new_record = f'{borrow_id}, {isbn}, {borrow_amount}, {return_status}\n'
            file.writelines(new_record)
    
    def update_return_status(self, borrow_id) -> str: #Trả về isbn để cập nhập database
        updated_records = []
        is_updated = False
        isbn = None
        borrow_amount = 0

        # Bước 1: Đọc toàn bộ dữ liệu hiện có
        try:
            with open(self.borrow_history_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                for line in lines:
                    # Tách dòng thành các cột (giả sử bạn dùng ", " làm phân tách)
                    data = line.strip('\n').split(', ')
                    
                    # data[1] là ISBN, data[3] là return_status
                    # Kiểm tra nếu đúng ISBN và sách đó chưa được trả (False)
                    if data[0] == borrow_id and data[3] == 'False':
                        data[3] = 'True'  # Cập nhật trạng thái
                        is_updated = True
                        isbn = data[1]
                        borrow_amount = int(data[2])
                    
                    # Ghép lại thành dòng hoàn chỉnh và lưu vào list tạm
                    updated_line = ", ".join(data) + "\n"
                    updated_records.append(updated_line)

            # Bước 2: Chỉ ghi đè lại file nếu có sự thay đổi
            if is_updated:
                with open(self.borrow_history_path, 'w', encoding='utf-8') as file:
                    file.writelines(updated_records)
            else:
                raise ValueError("Không tìm thấy bản ghi mượn sách chưa trả cho ISBN {isbn} hoặc bạn đã trả sách.")
            
            return isbn, borrow_amount

        except FileNotFoundError:
            print("File lịch sử mượn không tồn tại.")

    def top_book_stat(self, top_n = 5):
         # Đọc ISBN từ history file
        all_isbns = []
        with open(self.borrow_history_path, 'r') as f:
            for line in f:
                all_isbns.append(line.split(', ')[1])
    
        # Đếm tần suất
        counts = Counter(all_isbns)
        top_ns = counts.most_common(top_n)
        return top_ns