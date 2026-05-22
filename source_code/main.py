import sys
#pyrefly: ignore [missing-import]
import pygame
import threading
import copy
from game_logic import CaroGame
from ai_engine import CaroAI

# Các thông số thiết lập giao diện đồ họa
CELL_SIZE = 55  
BOARD_SIZE = 9
WIDTH = BOARD_SIZE * CELL_SIZE
HEIGHT = BOARD_SIZE * CELL_SIZE + 120 

# ==========================================
# 🎨 BẢNG MÀU CUTE PASTEL (KOREAN AESTHETIC)
# ==========================================
BG_COLOR = (253, 251, 247)      # Màu kem sữa ấm áp (Milky White)
LINE_COLOR = (225, 218, 209)    # Đường kẻ màu be xám nhạt không bị chói
X_COLOR = (255, 111, 118)       # Màu đỏ dâu Tây pastel (Strawberry Red)
O_COLOR = (94, 164, 255)        # Màu xanh da trời pastel (Sky Blue)

MENU_BG = (244, 239, 233)       # Màu nền menu be nhạt dễ chịu
BTN_COLOR = (218, 230, 252)     # Màu nút bấm xanh sữa nhạt
BTN_HOVER = (193, 213, 250)     # Khi di chuột vào: màu xanh đậm hơn một chút
BTN_SELECTED = (255, 207, 210)  # Khi được chọn: Đổi sang màu hồng đào cực cute
TEXT_COLOR = (90, 85, 80)       # Màu chữ nâu đậm lịch sự

class Button:
    """Lớp hỗ trợ tạo và vẽ các nút bấm Menu phong cách bo tròn mềm mại"""
    def __init__(self, x, y, w, h, text, selected=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.selected = selected
        
    def draw(self, screen, font):
        color = BTN_SELECTED if self.selected else BTN_COLOR
        mouse_pos = pygame.mouse.get_pos()
        if not self.selected and self.rect.collidepoint(mouse_pos):
            color = BTN_HOVER
            
        # Vẽ bóng đổ nhẹ cho nút bấm (Drop Shadow)
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (210, 205, 195), shadow_rect, border_radius=12)
        
        # Vẽ nút chính
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        
        # In chữ tiêu chuẩn
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
class CaroApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Soft Pastel Matchup")
        
        # Sử dụng font Arial phổ thông nhất để không bao giờ lỗi chữ
        self.font_large = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        
        self.state = "MENU"
        self.algorithm = 'minimax'
        self.depth = 2
        self.first_player = 1 
        
        self.init_menu_buttons()
        self.ai_thinking = False
        self.game_lock = threading.Lock()

    def init_menu_buttons(self):
        """Cấu hình lại vị trí các nút bấm"""
        self.btn_minimax = Button(45, 110, 160, 45, "Minimax", selected=True)
        self.btn_alphabeta = Button(240, 110, 160, 45, "Alpha-Beta")
        
        self.btn_human_first = Button(45, 210, 160, 45, "You First", selected=True)
        self.btn_ai_first = Button(240, 210, 160, 45, "AI First")
        
        self.btn_depth2 = Button(45, 310, 100, 45, "Depth 2", selected=True)
        self.btn_depth3 = Button(175, 310, 100, 45, "Depth 3")
        self.btn_depth4 = Button(305, 310, 100, 45, "Depth 4")
        
        self.btn_start = Button(95, 410, 260, 65, "START GAME")
        self.btn_home = Button(WIDTH//2 - 95, HEIGHT - 47, 190, 36, "MAIN MENU")
        
    def draw_menu(self):
        """Vẽ giao diện Menu dùng ký tự thường thay cho Emoji lỗi font"""
        self.screen.fill(MENU_BG)
        
        # Tiêu đề game đổ bóng
        title_shadow = self.font_title.render("CARO AI PLAYGROUND", True, (225, 215, 205))
        title = self.font_title.render("CARO AI PLAYGROUND", True, TEXT_COLOR)
        self.screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 2, 32))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        # Thay thế emoji bằng ký tự text sạch sẽ
        lbl_algo = self.font_medium.render("> Choose Algorithm:", True, TEXT_COLOR)
        self.screen.blit(lbl_algo, (45, 85))
        self.btn_minimax.draw(self.screen, self.font_medium)
        self.btn_alphabeta.draw(self.screen, self.font_medium)
        
        lbl_first = self.font_medium.render("> Who Goes First?", True, TEXT_COLOR)
        self.screen.blit(lbl_first, (45, 185))
        self.btn_human_first.draw(self.screen, self.font_medium)
        self.btn_ai_first.draw(self.screen, self.font_medium)
        
        lbl_depth = self.font_medium.render("> Search Depth (AI Level):", True, TEXT_COLOR)
        self.screen.blit(lbl_depth, (45, 285))
        self.btn_depth2.draw(self.screen, self.font_medium)
        self.btn_depth3.draw(self.screen, self.font_medium)
        self.btn_depth4.draw(self.screen, self.font_medium)
        
        self.btn_start.draw(self.screen, self.font_large)
        pygame.display.flip()

    def handle_menu_click(self, pos):
        if self.btn_minimax.rect.collidepoint(pos):
            self.algorithm = 'minimax'
            self.btn_minimax.selected = True
            self.btn_alphabeta.selected = False
        elif self.btn_alphabeta.rect.collidepoint(pos):
            self.algorithm = 'alpha_beta'
            self.btn_minimax.selected = False
            self.btn_alphabeta.selected = True
            
        elif self.btn_human_first.rect.collidepoint(pos):
            self.first_player = 1
            self.btn_human_first.selected = True
            self.btn_ai_first.selected = False
        elif self.btn_ai_first.rect.collidepoint(pos):
            self.first_player = 2
            self.btn_human_first.selected = False
            self.btn_ai_first.selected = True
            
        elif self.btn_depth2.rect.collidepoint(pos):
            self.depth = 2
            self.btn_depth2.selected, self.btn_depth3.selected, self.btn_depth4.selected = True, False, False
        elif self.btn_depth3.rect.collidepoint(pos):
            self.depth = 3
            self.btn_depth2.selected, self.btn_depth3.selected, self.btn_depth4.selected = False, True, False
        elif self.btn_depth4.rect.collidepoint(pos):
            self.depth = 4
            self.btn_depth2.selected, self.btn_depth3.selected, self.btn_depth4.selected = False, False, True
            
        elif self.btn_start.rect.collidepoint(pos):
            self.start_game()

    def start_game(self):
        self.state = "GAME"
        self.game = CaroGame(board_size=BOARD_SIZE)
        self.ai = CaroAI(depth=self.depth)
        self.game.current_player = self.first_player
        
        print(f"\n=====================================")
        print(f"GAME STARTED WITH CONFIGURATION:")
        print(f"- Selected Mode: {self.algorithm.upper()}")
        print(f"- First Player: {'Human (X)' if self.first_player == 1 else 'AI (O)'}")
        print(f"- Max Search Depth: {self.depth}")
        print(f"=====================================")
        
        if self.first_player == 2:
            self.start_ai_turn()

    def start_ai_turn(self):
        if self.ai_thinking:
            return

        self.ai_thinking = True
        threading.Thread(target=self.handle_ai_turn, daemon=True).start()

    def draw_board(self):
        """Vẽ bàn cờ và TỰ VẼ quân cờ bằng hình học, không lo lỗi phông chữ"""
        with self.game_lock:
            board = self.game.board.copy()
            is_game_over = self.game.is_game_over
            winner = self.game.check_winner() if is_game_over else None

        self.screen.fill(BG_COLOR)
        
        # Vẽ lưới caro
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, LINE_COLOR, rect, 1)
                
                player = board[r][c]
                # Tính toán tọa độ tâm và khoảng cách đệm (padding) để vẽ quân cờ cho đẹp
                center_x, center_y = rect.centerx, rect.centery
                padding = 14
                
                if player == 1:
                    # TỰ VẼ QUÂN X: Dùng 2 đường chéo nét dày (width=5) siêu mượt
                    pygame.draw.line(self.screen, X_COLOR, (rect.left + padding, rect.top + padding), (rect.right - padding, rect.bottom - padding), 5)
                    pygame.draw.line(self.screen, X_COLOR, (rect.right - padding, rect.top + padding), (rect.left + padding, rect.bottom - padding), 5)
                elif player == 2:
                    # TỰ VẼ QUÂN O: Dùng hàm vẽ vòng tròn rỗng nét dày (width=5)
                    pygame.draw.circle(self.screen, O_COLOR, (center_x, center_y), (CELL_SIZE // 2) - padding, 5)
        
        # Vùng trạng thái bên dưới (Status Bar)
        status_rect = pygame.Rect(0, HEIGHT - 110, WIDTH, 110)
        pygame.draw.rect(self.screen, MENU_BG, status_rect)
        pygame.draw.line(self.screen, LINE_COLOR, (0, HEIGHT - 110), (WIDTH, HEIGHT - 110), 2)
        
        # Hiển thị chế độ chơi
        algo_text = f"Mode: {'Alpha-Beta' if self.algorithm == 'alpha_beta' else 'Minimax'} (d={self.depth})"
        surf_algo = self.font_medium.render(algo_text, True, TEXT_COLOR)
        self.screen.blit(surf_algo, (20, HEIGHT - 95))
        
        # Hiển thị trạng thái trận đấu
        if is_game_over:
            if winner == 1:
                status = "You (X) Win!"
                color = X_COLOR
            elif winner == 2:
                status = "AI (O) Wins!"
                color = O_COLOR
            else:
                status = "Draw Game!"
                color = TEXT_COLOR
            surf_status = self.font_large.render(status, True, color)
            self.screen.blit(surf_status, (WIDTH//2 - surf_status.get_width()//2, HEIGHT - 86))
            self.btn_home.draw(self.screen, self.font_medium)
        else:
            if self.ai_thinking:
                turn_text = "AI is thinking..."
                color = O_COLOR
            else:
                turn_text = "Your Turn (X)"
                color = X_COLOR
            surf_turn = self.font_medium.render(turn_text, True, color)
            self.screen.blit(surf_turn, (20, HEIGHT - 50))
            
        pygame.display.flip()

    def handle_ai_turn(self):
        try:
            with self.game_lock:
                ai_game = copy.deepcopy(self.game)

            best_move, score, elapsed_time, total_states = self.ai.get_best_move(ai_game, self.algorithm)
            
            print(f"\n[EXECUTION] Applying selected algorithm: {self.algorithm.upper()}")
            
            if best_move:
                r, c = best_move
                with self.game_lock:
                    self.game.make_move(r, c, self.ai.ai_player)
                    if self.game.check_winner() is not None:
                        self.game.is_game_over = True

                    self.game.current_player = 1
                
                print(f"[AI INFO] Chosen Move: Row {r}, Col {c}")
                print(f"[AI INFO] Evaluation Score: {score}")
                print(f"[AI INFO] Explored States: {total_states} nodes")
                print(f"[AI INFO] Elapsed Time: {elapsed_time:.4f}s")
                print("====================================================")
        finally:
            self.ai_thinking = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_menu_click(pygame.mouse.get_pos())
                        
                elif self.state == "GAME":
                    if self.game.is_game_over:
                        if event.type == pygame.MOUSEBUTTONDOWN and self.btn_home.rect.collidepoint(pygame.mouse.get_pos()):
                            self.state = "MENU"
                        continue

                    if not self.game.is_game_over and not self.ai_thinking:
                        if self.game.current_player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = pygame.mouse.get_pos()
                            if my < HEIGHT - 110:
                                c = mx // CELL_SIZE
                                r = my // CELL_SIZE
                                should_start_ai = False
                                
                                with self.game_lock:
                                    move_made = self.game.make_move(r, c, 1)
                                    if move_made:
                                        if self.game.check_winner() is not None:
                                            self.game.is_game_over = True
                                        else:
                                            self.game.current_player = 2
                                            should_start_ai = True

                                if should_start_ai:
                                    self.start_ai_turn()

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "GAME":
                self.draw_board()

if __name__ == "__main__":
    app = CaroApp()
    app.run()
