# Bài Tập Lớn Trí Tuệ Nhân Tạo: Caro (Gomoku) AI

Dự án này cài đặt trò chơi Cờ Caro (Gomoku) giữa Người và Máy (AI) sử dụng thuật toán Minimax kết hợp Alpha-Beta Pruning.

## 1. Thông Tin Nhóm
*   **Ngô Thị Thảo Linh** - 23020620
*   **Nguyễn Hà Linh** - 22024505
*   **Lã Minh Đức** - 23020526

## 2. Mô Tả Dự Án
*   **Ngôn ngữ**: Python
*   **Luật chơi**: Bàn cờ 9x9 (hoặc tùy chỉnh). Người thắng là người có 4 quân liên tiếp theo hàng ngang, dọc, hoặc chéo (không áp dụng luật chặn 2 đầu).
*   **Thuật toán AI**: Minimax & Alpha-Beta Pruning. Hàm Heuristic đánh giá trạng thái dựa trên các chuỗi quân cờ mở và bị chặn.

## 3. Cấu Trúc Thư Mục
*   `source_code/`: Thư mục chứa mã nguồn chính.
    *   `game_logic.py`: Quản lý bàn cờ và luật chơi.
    *   `ai_engine.py`: Chứa thuật toán tìm kiếm Minimax & Alpha-Beta Pruning.
    *   `evaluation.py`: Hàm đánh giá Heuristic.
    *   `main.py`: Vòng lặp trò chơi và giao diện (Console/Pygame).
    *   `utils.py`: Các hàm tiện ích (đo thời gian, đếm trạng thái duyệt).
*   `requirements.txt`: Các thư viện phụ thuộc.
*   `README.md`: Hướng dẫn cài đặt và chạy chương trình.

## 4. Yêu Cầu Cài Đặt (Prerequisites)
Yêu cầu Python 3.8 trở lên. Cài đặt các thư viện cần thiết bằng lệnh:
```bash
pip install -r requirements.txt
```

## 5. Hướng Dẫn Chạy Chương Trình
Để bắt đầu trò chơi, hãy chạy file `main.py` từ thư mục gốc:
```bash
python source_code/main.py
```

## 6. Tham Khảo và Học Hỏi Từ Mã Nguồn Mẫu

Trong quá trình nghiên cứu, thiết kế hệ thống và phát triển thuật toán, nhóm đã bám sát các tài liệu khoa học nền tảng kết hợp với việc phân tích, học hỏi có chọn lọc từ các kho tài nguyên mã nguồn mở được giảng viên cung cấp:

### 6.1. Tài Liệu Lý Thuyết Học Thuật Nền Tảng

1. **Slide bài giảng môn Trí tuệ Nhân tạo** - Hệ thống lý thuyết cốt lõi về không gian trạng thái và tìm kiếm có đối thủ (Lecture 5: Adversarial Search), Khoa Công nghệ Thông tin.
2. Stuart Russell và Peter Norvig, **Artificial Intelligence: A Modern Approach**, Fourth Edition, Pearson, 2020 - Chương 5: Adversarial Search and Games (Cơ sở toán học của cây quyết định Minimax và các định lý cắt nhánh Alpha-Beta).

### 6.2. Khai Báo Minh Bạch Các Phân Đoạn Tham Khảo Từ Repository Mẫu

Nhóm cam kết tuân thủ nghiêm ngặt quy định liêm chính học thuật, tự lực hiện thực hóa các thuật toán lõi và thực hiện khai báo minh bạch các thành phần đã kế thừa ý tưởng từ hai repository mẫu:

*   **Đối với Repository `gomokuAI-py`:**
    *   *Thành phần học hỏi:* Kế thừa giải pháp thiết lập cấu trúc đồ họa và bắt sự kiện chuột (Mouse Click Event) cơ bản bằng thư viện `pygame`. Kế thừa tư duy module hóa, tách biệt hoàn toàn giữa tầng xử lý đồ họa (Frontend) và logic tính toán (Backend).
    *   *Sự cải tiến tự lực của nhóm:* Do mã nguồn mẫu vận hành trên luật Gomoku bàn cờ 15x15 thắng bằng 5 quân liên tiếp, nhóm đã tiến hành viết lại toàn bộ logic trong file `game_logic.py` để thu hẹp không gian ma trận về chuẩn 9x9 và áp dụng luật thắng đúng 4 quân liên tiếp, bỏ qua ràng buộc chặn hai đầu theo đúng yêu cầu đề bài.
    
*   **Đối với Repository `Caro_AI`:**
    *   *Thành phần học hỏi:* Tham khảo ý tưởng lượng hóa thế trận bằng cách trượt để đếm số lượng tổ hợp quân X và O xuất hiện trong các cửa sổ liên tiếp. Học hỏi phương pháp tối ưu hóa không gian tìm kiếm bằng cách giới hạn tập nước đi khả thi xung quanh chiến sự để triệt tiêu các nhánh trống vô ích.
    *   *Sự cải tiến tự lực của nhóm:* Nhóm hoàn toàn tự cô đọng logic thành thuật toán **Cửa sổ trượt 4 ô cố định** trong file `evaluation.py` để tính toán điểm số chính xác cho luật 4 quân, đồng thời tăng vọt trọng số phòng ngự chống chuỗi 3 (-50,000) để ép AI phản xạ chặn. Nhóm tự tay viết mới 100% logic đệ quy cho hai hàm biệt lập là Minimax thuần túy (`minimax`) và Cắt nhánh Alpha-Beta (`alpha_beta`), đồng thời tự tích hợp bộ đếm `counter.increment()` cùng bộ đo `GameTimer` xuyên suốt cây tìm kiếm để phục vụ lấy số liệu thực nghiệm khoa học.
