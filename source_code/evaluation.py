def evaluate_board(board, ai_player, human_player):
    """
    Hàm Heuristic đánh giá trạng thái bàn cờ hiện tại sử dụng kỹ thuật "Cửa sổ trượt" (Sliding Window).
    Duyệt qua tất cả các cửa sổ 4 ô liên tiếp trên bàn cờ.
    Phương pháp này dùng chung cho cả Minimax và Alpha-Beta để đảm bảo tính công bằng khi so sánh.
    """
    score = 0
    size = len(board)
    
    def evaluate_window(window):
        ai_pieces = window.count(ai_player)
        human_pieces = window.count(human_player)
        empty_cells = window.count(0)
        
        window_score = 0
        
        # Nếu cửa sổ chứa cả quân X và O thì cửa sổ này coi như đã bị chặn ("chết"), điểm = 0
        if ai_pieces > 0 and human_pieces == 0:
            if ai_pieces == 4:
                window_score += 100000 # Máy có 4 quân (Chắc chắn thắng)
            elif ai_pieces == 3 and empty_cells == 1:
                window_score += 10000 # Máy có 3 quân mở rộng được
            elif ai_pieces == 2 and empty_cells == 2:
                window_score += 1000 # Máy có 2 quân
                
        elif human_pieces > 0 and ai_pieces == 0:
            if human_pieces == 4:
                window_score -= 100000 # Người có 4 quân (Người thắng)
            elif human_pieces == 3 and empty_cells == 1:
                # Trọng số phòng thủ cực cao: Ưu tiên chặn
                window_score -= 50000 
            elif human_pieces == 2 and empty_cells == 2:
                window_score -= 1000 # Chuỗi 2 của người
                
        return window_score

    # 1. Đánh giá tất cả các cửa sổ ngang
    for r in range(size):
        for c in range(size - 3):
            window = [board[r][c+i] for i in range(4)]
            score += evaluate_window(window)
            
    # 2. Đánh giá tất cả các cửa sổ dọc
    for c in range(size):
        for r in range(size - 3):
            window = [board[r+i][c] for i in range(4)]
            score += evaluate_window(window)
            
    # 3. Đánh giá chéo chính ( \ )
    for r in range(size - 3):
        for c in range(size - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window)
            
    # 4. Đánh giá chéo phụ ( / )
    for r in range(size - 3):
        for c in range(3, size):
            window = [board[r+i][c-i] for i in range(4)]
            score += evaluate_window(window)
            
    return score
