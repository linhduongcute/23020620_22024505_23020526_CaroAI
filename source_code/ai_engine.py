import math
from evaluation import evaluate_board
from utils import GameTimer, StateCounter

class CaroAI:
    def __init__(self, depth=2):
        """
        Khởi tạo AI với độ sâu tìm kiếm.
        """
        self.depth = depth
        self.ai_player = 2
        self.human_player = 1

    def get_possible_moves(self, board):
        """
        Tối ưu sinh nước đi: Chỉ xét các ô trống nằm trong phạm vi bán kính 2 ô xung quanh các quân cờ đã có.
        """
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
                                
        # Nếu đánh nước đầu tiên, auto đánh vào giữa bàn cờ
        if not has_piece:
            return [(size // 2, size // 2)]
            
        return sorted(list(moves)) 

    def get_best_move(self, game_state, algorithm='minimax'):
        """
        Tìm nước đi tốt nhất. Hỗ trợ gọi linh hoạt cả 2 thuật toán để so sánh.
        :param algorithm: 'minimax' hoặc 'alpha_beta'
        """
        timer = GameTimer()
        timer.start()
        
        counter = StateCounter()
        
        best_score = -math.inf
        best_move = None
        
        possible_moves = self.get_possible_moves(game_state.board)
        
        for move in possible_moves:
            r, c = move
            # Đánh thử
            game_state.board[r][c] = self.ai_player
            
            # Chọn thuật toán dựa vào setting từ Menu
            if algorithm == 'alpha_beta':
                score = self.alpha_beta(game_state, self.depth - 1, -math.inf, math.inf, False, counter)
            else:
                score = self.minimax(game_state, self.depth - 1, False, counter)
            
            # Hoàn tác
            game_state.board[r][c] = 0
            
            if score > best_score:
                best_score = score
                best_move = move
                
        elapsed_time = timer.get_elapsed_time()
        total_states = counter.get_count()
        
        return best_move, best_score, elapsed_time, total_states

    def minimax(self, game_state, depth, is_maximizing_player, counter):
        """
        Thuật toán Minimax thuần túy (Không tối ưu cắt tỉa).
        """
        counter.increment()
        winner = game_state.check_winner()
        if winner == self.ai_player:
            return 1000000 + depth
        elif winner == self.human_player:
            return -1000000 - depth
        elif winner == 0:
            return 0
            
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
        """
        Thuật toán Alpha-Beta Pruning (Có tối ưu cắt tỉa nhánh thừa).
        """
        counter.increment()
        winner = game_state.check_winner()
        if winner == self.ai_player:
            return 1000000 + depth
        elif winner == self.human_player:
            return -1000000 - depth
        elif winner == 0:
            return 0
            
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
                    break # Cắt tỉa nhánh (Pruning)
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
                    break # Cắt tỉa nhánh (Pruning)
            return min_eval
