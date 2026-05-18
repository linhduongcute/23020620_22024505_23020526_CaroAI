import sys
#pyrefly: ignore [missing-import]
import pygame
import threading
from game_logic import CaroGame
from ai_engine import CaroAI

# Các thông số thiết lập giao diện đồ họa
CELL_SIZE = 50
BOARD_SIZE = 9
WIDTH = BOARD_SIZE * CELL_SIZE
HEIGHT = BOARD_SIZE * CELL_SIZE + 100 # Mở rộng khung cửa sổ thêm phần dưới cho trạng thái

# Định nghĩa bảng màu sắc
BG_COLOR = (245, 245, 245)
LINE_COLOR = (100, 100, 100)
X_COLOR = (220, 20, 60) # Màu đỏ (Người)
O_COLOR = (30, 144, 255) # Màu xanh (Máy)
MENU_BG = (40, 44, 52)
BTN_COLOR = (97, 175, 239)
BTN_HOVER = (86, 156, 214)
BTN_SELECTED = (152, 195, 121)
TEXT_COLOR = (255, 255, 255)

class Button:
    """Lớp hỗ trợ tạo và vẽ các nút bấm Menu"""
    def __init__(self, x, y, w, h, text, selected=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.selected = selected
        
    def draw(self, screen, font):
        color = BTN_SELECTED if self.selected else BTN_COLOR
        mouse_pos = pygame.mouse.get_pos()
        if not self.selected and self.rect.collidepoint(mouse_pos):
            color = BTN_HOVER
            
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
class CaroApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Minimax vs Alpha-Beta")
        
        self.font_large = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 22, bold=True)
        
        # Quản lý luồng hiển thị
        self.state = "MENU" # Bắt đầu bằng giao diện MENU
        
        # Biến cấu hình AI (mặc định)
        self.algorithm = 'minimax'
        self.depth = 2
        self.first_player = 1 # 1: Người, 2: Máy
        
        self.init_menu_buttons()
        self.ai_thinking = False

    def init_menu_buttons(self):
        """Khởi tạo danh sách các nút bấm trên Menu"""
        self.btn_minimax = Button(50, 100, 160, 40, "Minimax", selected=True)
        self.btn_alphabeta = Button(240, 100, 160, 40, "Alpha-Beta")
        
        self.btn_human_first = Button(50, 200, 160, 40, "you first", selected=True)
        self.btn_ai_first = Button(240, 200, 160, 40, "AI first")
        
        self.btn_depth2 = Button(50, 300, 100, 40, "Depth 2", selected=True)
        self.btn_depth3 = Button(170, 300, 100, 40, "Depth 3")
        self.btn_depth4 = Button(290, 300, 100, 40, "Depth 4")
        
        self.btn_start = Button(125, 400, 200, 60, "START GAME")
        
    def draw_menu(self):
        """Vẽ giao diện Menu lên màn hình"""
        self.screen.fill(MENU_BG)
        title = self.font_large.render("CARO AI MENU", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        lbl_algo = self.font_medium.render("Algorithm:", True, TEXT_COLOR)
        self.screen.blit(lbl_algo, (50, 70))
        self.btn_minimax.draw(self.screen, self.font_medium)
        self.btn_alphabeta.draw(self.screen, self.font_medium)
        
        lbl_first = self.font_medium.render("First Player:", True, TEXT_COLOR)
        self.screen.blit(lbl_first, (50, 170))
        self.btn_human_first.draw(self.screen, self.font_medium)
        self.btn_ai_first.draw(self.screen, self.font_medium)
        
        lbl_depth = self.font_medium.render("Depth:", True, TEXT_COLOR)
        self.screen.blit(lbl_depth, (50, 270))
        self.btn_depth2.draw(self.screen, self.font_medium)
        self.btn_depth3.draw(self.screen, self.font_medium)
        self.btn_depth4.draw(self.screen, self.font_medium)
        
        self.btn_start.draw(self.screen, self.font_large)
        pygame.display.flip()

    def handle_menu_click(self, pos):
        """Xử lý sự kiện click trên Menu"""
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
        """Khởi tạo Game loop sau khi bấm BẮT ĐẦU"""
        self.state = "GAME"
        self.game = CaroGame(board_size=BOARD_SIZE)
        self.ai = CaroAI(depth=self.depth)
        self.game.current_player = self.first_player
        
        print(f"\n=====================================")
        print(f"BẮT ĐẦU GAME VỚI CẤU HÌNH:")
        print(f"- Thuật toán: {self.algorithm.upper()}")
        print(f"- Lượt đi đầu: {'Người (X)' if self.first_player == 1 else 'Máy (O)'}")
        print(f"- Độ sâu Minimax: {self.depth}")
        print(f"=====================================")
        
        # Nếu máy đi trước, gọi AI đánh tự động lượt đầu
        if self.first_player == 2:
            threading.Thread(target=self.handle_ai_turn).start()

    def draw_board(self):
        """Vẽ lại toàn bộ bàn cờ và thông tin trạng thái"""
        self.screen.fill(BG_COLOR)
        
        # Lưới caro
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, LINE_COLOR, rect, 1)
                
                player = self.game.board[r][c]
                if player == 1:
                    text = self.font_large.render("X", True, X_COLOR)
                    self.screen.blit(text, text.get_rect(center=rect.center))
                elif player == 2:
                    text = self.font_large.render("O", True, O_COLOR)
                    self.screen.blit(text, text.get_rect(center=rect.center))
        
        # Vùng trạng thái bên dưới
        status_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
        pygame.draw.rect(self.screen, MENU_BG, status_rect)
        
        algo_text = f"Mode: {'Alpha-Beta' if self.algorithm == 'alpha_beta' else 'Minimax'} (d={self.depth})"
        surf_algo = self.font_medium.render(algo_text, True, TEXT_COLOR)
        self.screen.blit(surf_algo, (10, HEIGHT - 90))
        
        # Hiển thị thông báo trạng thái
        if self.game.is_game_over:
            winner = self.game.check_winner()
            if winner == 1:
                status = "Người (X) THẮNG!"
                color = X_COLOR
            elif winner == 2:
                status = "Máy (O) THẮNG!"
                color = O_COLOR
            else:
                status = "HÒA!"
                color = TEXT_COLOR
            surf_status = self.font_large.render(status, True, color)
            self.screen.blit(surf_status, (WIDTH//2 - surf_status.get_width()//2, HEIGHT - 50))
        else:
            turn_text = "Máy (O) đang tính toán..." if self.ai_thinking else "Lượt của Người (X)"
            color = O_COLOR if self.ai_thinking else X_COLOR
            surf_turn = self.font_medium.render(turn_text, True, color)
            self.screen.blit(surf_turn, (10, HEIGHT - 50))
            
        pygame.display.flip()

    def handle_ai_turn(self):
        """Chạy AI trên một luồng phụ để không treo giao diện"""
        self.ai_thinking = True
        self.draw_board() 
        print(f"\n[AI] Máy đang chạy thuật toán {self.algorithm} (d={self.depth})...")
        
        # Gọi hàm get_best_move truyền vào thuật toán đã chọn
        best_move, score, elapsed_time, total_states = self.ai.get_best_move(self.game, self.algorithm)
        
        if best_move:
            r, c = best_move
            self.game.make_move(r, c, self.ai.ai_player)
            
            # YÊU CẦU: In ra Console thông số cho việc so sánh hiệu năng
            print(f"[AI INFO] Nước đi chọn: Hàng {r}, Cột {c}")
            print(f"[AI INFO] Giá trị đánh giá: {score}")
            print(f"[AI INFO] Số trạng thái duyệt: {total_states} nodes")
            print(f"[AI INFO] Thời gian chạy: {elapsed_time:.4f}s")
            
            if self.game.check_winner() is not None:
                self.game.is_game_over = True
            
            self.game.current_player = 1
            
        self.ai_thinking = False

    def run(self):
        """Vòng lặp sự kiện chính"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_menu_click(pygame.mouse.get_pos())
                        
                elif self.state == "GAME":
                    if not self.game.is_game_over and not self.ai_thinking:
                        if self.game.current_player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = pygame.mouse.get_pos()
                            # Kiểm tra click vào vùng bàn cờ (không dính vào thanh status bên dưới)
                            if my < HEIGHT - 100:
                                c = mx // CELL_SIZE
                                r = my // CELL_SIZE
                                
                                if self.game.make_move(r, c, 1):
                                    if self.game.check_winner() is not None:
                                        self.game.is_game_over = True
                                    else:
                                        self.game.current_player = 2
                                        threading.Thread(target=self.handle_ai_turn).start()

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "GAME":
                self.draw_board()

if __name__ == "__main__":
    app = CaroApp()
    app.run()
