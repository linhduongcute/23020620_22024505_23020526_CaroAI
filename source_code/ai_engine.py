import math
import copy
from evaluation import evaluate_board
from utils import GameTimer, StateCounter

class CaroAI:
    def __init__(self, depth=2):
        self.depth = depth
        self.ai_player = 2
        self.human_player = 1

    def get_possible_moves(self, board):
        moves = set()
        size = len(board)
        has_piece = False
        
        for r in range(size):
            for c in range(size):
                if board[r][c] != 0:
                    has_piece = True
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == 0:
                                moves.add((nr, nc))
                                
        if not has_piece:
            return [(size // 2, size // 2)]
            
        return sorted(list(moves)) 

    def get_best_move(self, game_state, algorithm='minimax'):
        """
        Tìm nước đi tốt nhất dựa trên thuật toán được chọn.
        """
        timer = GameTimer()
        timer.start()
        counter = StateCounter()
        
        possible_moves = self.get_possible_moves(game_state.board)
        best_move = None
        
        if algorithm == 'alpha_beta':
            best_score = -math.inf
            alpha = -math.inf
            beta = math.inf
            
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                
                # Gọi tầng tiếp theo là lượt của MIN (False)
                score = self.alpha_beta(game_state, self.depth - 1, alpha, beta, False, counter)
                
                game_state.board[r][c] = 0
                
                if score > best_score:
                    best_score = score
                    best_move = move
                
                # Cập nhật alpha ngay tại nút gốc
                alpha = max(alpha, best_score)
        else:
            # Thuật toán Minimax giữ nguyên logic cũ của bạn (đã đúng)
            best_score = -math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                score = self.minimax(game_state, self.depth - 1, False, counter)
                game_state.board[r][c] = 0
                
                if score > best_score:
                    best_score = score
                    best_move = move
                
        elapsed_time = timer.get_elapsed_time()
        total_states = counter.get_count()
        
        return best_move, best_score, elapsed_time, total_states

    def compare_algorithms(self, game_state):
        """
        ĐÁP ỨNG YÊU CẦU: 'Chạy hai thuật toán trên cùng một trạng thái bàn cờ'
        Hàm này giúp bạn lấy dữ liệu trực tiếp để đưa vào báo cáo.
        """
        # Copy trạng thái để đảm bảo công bằng, không ảnh hưởng lẫn nhau
        state_for_minimax = copy.deepcopy(game_state)
        state_for_ab = copy.deepcopy(game_state)
        
        print("--- ĐANG SO SÁNH HIỆU NĂNG TRÊN CÙNG TRẠNG THÁI ---")
        
        move_mm, score_mm, time_mm, states_mm = self.get_best_move(state_for_minimax, algorithm='minimax')
        print(f"[Minimax]    Nước đi: {move_mm} | Điểm: {score_mm} | Số trạng thái xét: {states_mm} | Thời gian: {time_mm:.4f}s")
        
        move_ab, score_ab, time_ab, states_ab = self.get_best_move(state_for_ab, algorithm='alpha_beta')
        print(f"[Alpha-Beta] Nước đi: {move_ab} | Điểm: {score_ab} | Số trạng thái xét: {states_ab} | Thời gian: {time_ab:.4f}s")
        
        # Kiểm tra tính đúng đắn: Điểm số thu được của 2 thuật toán BẮT BUỘC phải bằng nhau
        if score_mm == score_ab:
            print("=> Kết quả logic chính xác! (Alpha-Beta giữ nguyên được giá trị tối ưu của Minimax)")
        else:
            print("=> Cảnh báo: Có sự lệch điểm giữa 2 thuật toán!")
            
        return {
            'minimax': (move_mm, score_mm, time_mm, states_mm),
            'alpha_beta': (move_ab, score_ab, time_ab, states_ab)
        }

    def minimax(self, game_state, depth, is_maximizing_player, counter):
        counter.increment()
        winner = game_state.check_winner()
        if winner == self.ai_player: return 1000000 + depth
        if winner == self.human_player: return -1000000 - depth
        if winner == 0: return 0
            
        if depth == 0:
            return evaluate_board(game_state.board, self.ai_player, self.human_player)
            
        possible_moves = self.get_possible_moves(game_state.board)
        
        if is_maximizing_player:
            max_eval = -math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                eval = self.minimax(game_state, depth - 1, False, counter)
                game_state.board[r][c] = 0
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.human_player
                eval = self.minimax(game_state, depth - 1, True, counter)
                game_state.board[r][c] = 0
                min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, game_state, depth, alpha, beta, is_maximizing_player, counter):
        counter.increment()
        winner = game_state.check_winner()
        if winner == self.ai_player: return 1000000 + depth
        if winner == self.human_player: return -1000000 - depth
        if winner == 0: return 0
            
        if depth == 0:
            return evaluate_board(game_state.board, self.ai_player, self.human_player)
            
        possible_moves = self.get_possible_moves(game_state.board)
        
        if is_maximizing_player:
            max_eval = -math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, False, counter)
                game_state.board[r][c] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.human_player
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, True, counter)
                game_state.board[r][c] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval