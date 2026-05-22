import math
from evaluation import evaluate_board
from utils import GameTimer, StateCounter

class CaroAI:
    def __init__(self, depth=2):
        self.depth = depth
        self.ai_player = 2
        self.human_player = 1
        self.root_branch_limit = 18
        self.search_branch_limit = 12
        self._cache = {}

    def get_possible_moves(self, board, player=None, limit=None):
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

        ordered_moves = sorted(
            moves,
            key=lambda move: self.score_move(board, move, player or self.ai_player),
            reverse=True
        )
        return ordered_moves[:limit] if limit else ordered_moves

    def is_winning_move(self, board, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1

            nr, nc = row + dr, col + dc
            while 0 <= nr < len(board) and 0 <= nc < len(board) and board[nr][nc] == player:
                count += 1
                nr += dr
                nc += dc

            nr, nc = row - dr, col - dc
            while 0 <= nr < len(board) and 0 <= nc < len(board) and board[nr][nc] == player:
                count += 1
                nr -= dr
                nc -= dc

            if count >= 4:
                return True

        return False

    def score_move(self, board, move, player):
        row, col = move
        opponent = self.human_player if player == self.ai_player else self.ai_player

        if self.is_winning_move(board, row, col, player):
            return 1_000_000
        if self.is_winning_move(board, row, col, opponent):
            return 900_000

        size = len(board)
        center = size // 2
        score = (size - (abs(row - center) + abs(col - center))) * 5
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            own_count, own_open = self.line_info(board, row, col, player, dr, dc)
            opp_count, opp_open = self.line_info(board, row, col, opponent, dr, dc)

            if own_count == 3:
                score += 60_000 if own_open == 2 else 20_000
            elif own_count == 2:
                score += 4_000 if own_open == 2 else 1_000
            elif own_count == 1 and own_open > 0:
                score += 100

            if opp_count == 3:
                score += 80_000 if opp_open == 2 else 30_000
            elif opp_count == 2:
                score += 5_000 if opp_open == 2 else 1_500

        return score

    def line_info(self, board, row, col, player, dr, dc):
        size = len(board)
        count = 1
        open_ends = 0

        nr, nc = row + dr, col + dc
        while 0 <= nr < size and 0 <= nc < size and board[nr][nc] == player:
            count += 1
            nr += dr
            nc += dc
        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == 0:
            open_ends += 1

        nr, nc = row - dr, col - dc
        while 0 <= nr < size and 0 <= nc < size and board[nr][nc] == player:
            count += 1
            nr -= dr
            nc -= dc
        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == 0:
            open_ends += 1

        return count, open_ends

    def find_winning_move(self, board, player, moves):
        for r, c in moves:
            if self.is_winning_move(board, r, c, player):
                return (r, c)
        return None

    def has_empty_cell(self, board):
        size = len(board)
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    return True
        return False

    def should_limit_branching(self):
        return self.depth >= 4

    def get_best_move(self, game_state, algorithm='minimax'):
        """
        Tìm nước đi tốt nhất dựa trên thuật toán được chọn.
        """
        timer = GameTimer()
        timer.start()
        counter = StateCounter()
        self._cache = {}
        
        all_moves = self.get_possible_moves(game_state.board, self.ai_player)
        best_move = self.find_winning_move(game_state.board, self.ai_player, all_moves)
        if best_move:
            counter.increment()
            return best_move, 1000000, timer.get_elapsed_time(), counter.get_count()

        best_move = self.find_winning_move(game_state.board, self.human_player, all_moves)
        if best_move:
            counter.increment()
            return best_move, 900000, timer.get_elapsed_time(), counter.get_count()

        limit = self.root_branch_limit if self.should_limit_branching() else None
        possible_moves = all_moves[:limit] if limit else all_moves
        best_move = None
        
        if algorithm == 'alpha_beta':
            best_score = -math.inf
            alpha = -math.inf
            beta = math.inf
            
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                
                score = self.alpha_beta(game_state, self.depth - 1, alpha, beta, False, counter, move, self.ai_player)
                
                game_state.board[r][c] = 0
                
                if score > best_score:
                    best_score = score
                    best_move = move
                
                alpha = max(alpha, best_score)
        else:
            # Ở depth 4, Minimax dùng danh sách nước đi đã lọc để tránh duyệt quá rộng.
            best_score = -math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                score = self.minimax(game_state, self.depth - 1, False, counter, move, self.ai_player)
                game_state.board[r][c] = 0
                
                if score > best_score:
                    best_score = score
                    best_move = move
                
        elapsed_time = timer.get_elapsed_time()
        total_states = counter.get_count()
        
        return best_move, best_score, elapsed_time, total_states

    def minimax(self, game_state, depth, is_maximizing_player, counter, last_move=None, last_player=None):
        counter.increment()
        if last_move and self.is_winning_move(game_state.board, last_move[0], last_move[1], last_player):
            if last_player == self.ai_player:
                return 1000000 + depth
            return -1000000 - depth
        if not self.has_empty_cell(game_state.board):
            return 0
            
        if depth == 0:
            return evaluate_board(game_state.board, self.ai_player, self.human_player)

        cache_key = (game_state.board.tobytes(), depth, is_maximizing_player)
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        player = self.ai_player if is_maximizing_player else self.human_player
        limit = self.search_branch_limit if self.should_limit_branching() else None
        possible_moves = self.get_possible_moves(game_state.board, player, limit)
        
        if is_maximizing_player:
            max_eval = -math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                eval = self.minimax(game_state, depth - 1, False, counter, move, self.ai_player)
                game_state.board[r][c] = 0
                max_eval = max(max_eval, eval)
            self._cache[cache_key] = max_eval
            return max_eval
        else:
            min_eval = math.inf
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.human_player
                eval = self.minimax(game_state, depth - 1, True, counter, move, self.human_player)
                game_state.board[r][c] = 0
                min_eval = min(min_eval, eval)
            self._cache[cache_key] = min_eval
            return min_eval

    def alpha_beta(self, game_state, depth, alpha, beta, is_maximizing_player, counter, last_move=None, last_player=None):
        counter.increment()
        if last_move and self.is_winning_move(game_state.board, last_move[0], last_move[1], last_player):
            if last_player == self.ai_player:
                return 1000000 + depth
            return -1000000 - depth
        if not self.has_empty_cell(game_state.board):
            return 0
            
        if depth == 0:
            return evaluate_board(game_state.board, self.ai_player, self.human_player)

        cache_key = (game_state.board.tobytes(), depth, is_maximizing_player)
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        player = self.ai_player if is_maximizing_player else self.human_player
        limit = self.search_branch_limit if self.should_limit_branching() else None
        possible_moves = self.get_possible_moves(game_state.board, player, limit)
        
        if is_maximizing_player:
            max_eval = -math.inf
            had_cutoff = False
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.ai_player
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, False, counter, move, self.ai_player)
                game_state.board[r][c] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    had_cutoff = True
                    break
            if not had_cutoff:
                self._cache[cache_key] = max_eval
            return max_eval
        else:
            min_eval = math.inf
            had_cutoff = False
            for move in possible_moves:
                r, c = move
                game_state.board[r][c] = self.human_player
                eval = self.alpha_beta(game_state, depth - 1, alpha, beta, True, counter, move, self.human_player)
                game_state.board[r][c] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    had_cutoff = True
                    break
            if not had_cutoff:
                self._cache[cache_key] = min_eval
            return min_eval
