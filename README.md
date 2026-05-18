# Bài Tập Lớn Trí Tuệ Nhân Tạo: Caro (Gomoku) AI

Dự án này cài đặt trò chơi Cờ Caro (Gomoku) giữa Người và Máy (AI) sử dụng thuật toán Minimax kết hợp Alpha-Beta Pruning.

## 1. Thông Tin Nhóm
*   **MSSV 1** - Họ và Tên 1
*   **MSSV 2** - Họ và Tên 2
*   **MSSV 3** - Họ và Tên 3

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

## 6. Tham Khảo
*(Liệt kê các tài liệu, nguồn tham khảo nếu có)*
