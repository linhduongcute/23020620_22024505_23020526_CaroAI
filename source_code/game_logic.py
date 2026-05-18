import numpy as np

class CaroGame:
    def __init__(self, board_size=9):
        """
        Khởi tạo trò chơi Caro sử dụng numpy array.
        :param board_size: Kích thước bàn cờ (mặc định 9x9 theo yêu cầu Level 1).
        """
        self.board_size = board_size
        # Bàn cờ được khởi tạo bằng ma trận numpy kích thước 9x9 với toàn giá trị 0 (ô trống)
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = 1 # 1: Người (X), 2: Máy (O)
        self.is_game_over = False

    def is_valid_move(self, row, col):
        """
        Kiểm tra nước đi có hợp lệ không.
        Nước đi hợp lệ khi nằm trong giới hạn bàn cờ và ô đó chưa có quân cờ nào (giá trị 0).
        """
        return 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row, col] == 0

    def make_move(self, row, col, player):
        """
        Thực hiện đặt quân cờ vào vị trí (row, col) trên bàn cờ.
        """
        if self.is_valid_move(row, col):
            self.board[row, col] = player
            return True
        return False

    def check_winner(self):
        """
        Kiểm tra trạng thái thắng/thua/hòa của trò chơi.
        Luật Level 1: Yêu cầu đúng 4 quân liên tiếp (ngang, dọc, chéo) là thắng.
        Ràng buộc: KHÔNG xét luật chặn 2 đầu.
        :return: 1 (Người thắng), 2 (Máy thắng), 0 (Hòa), hoặc None (Chưa kết thúc)
        """
        # 4 hướng cần kiểm tra: ngang (phải), dọc (xuống), chéo chính (xuống-phải), chéo phụ (lên-phải)
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        
        # Duyệt toàn bộ các ô trên bàn cờ
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r, c] == 0:
                    continue # Bỏ qua các ô trống
                
                player = self.board[r, c]
                
                # Kiểm tra cả 4 hướng từ ô hiện tại
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4): # Chỉ cần kiểm tra thêm 3 ô liên tiếp nữa để đạt 4 quân
                        nr, nc = r + dr * i, c + dc * i
                        # Nếu ô tiếp theo nằm trong bàn cờ và cùng màu với người chơi hiện tại
                        if 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr, nc] == player:
                            count += 1
                        else:
                            break # Chuỗi bị đứt đoạn
                    
                    # Nếu đếm đủ 4 quân liên tiếp thì người đó giành chiến thắng
                    if count == 4:
                        return player
        
        # Nếu không ai thắng, kiểm tra trạng thái hòa (bàn cờ không còn ô trống)
        if not np.any(self.board == 0):
            return 0 
            
        return None # Trò chơi vẫn đang tiếp diễn

    def get_board_state(self):
        """
        Lấy trạng thái bàn cờ hiện tại.
        """
        return self.board
