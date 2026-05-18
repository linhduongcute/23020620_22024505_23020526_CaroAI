import numpy as np
import sys
import os
# Đảm bảo terminal hiển thị đúng font tiếng Việt
sys.stdout.reconfigure(encoding='utf-8')

from game_logic import CaroGame
from ai_engine import CaroAI

def run_experiment_state_1(depth):
    print(f"\n" + "="*15 + f" STATE 1: KHAI CUỘC (MÁY ĐI TRƯỚC - DEPTH {depth}) " + "="*15)
    game = CaroGame(board_size=9)
    # Bàn cờ hoàn toàn trống, Máy (Player 1) sẽ thực hiện nước khai cuộc đầu tiên
    
    ai = CaroAI(depth=depth)
    ai.ai_player = 1       # Máy tính đóng vai trò Người chơi 1 (X)
    ai.human_player = 2    # Con người đóng vai trò Người chơi 2 (O)

    print("[Đang chạy] Minimax thuần túy...")
    move_mm, score_mm, time_mm, nodes_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {nodes_mm}, Thời gian: {time_mm:.4f}s")

    print("\n[Đang chạy] Alpha-Beta Pruning...")
    move_ab, score_ab, time_ab, nodes_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {nodes_ab}, Thời gian: {time_ab:.4f}s")

def run_experiment_state_2(depth):
    print(f"\n" + "="*15 + f" STATE 2: GIỮA VÁN CHIẾN THUẬT (DEPTH {depth}) " + "="*15)
    # Cấu hình 12 quân cờ, Máy tính (1) đã đi 6 nước, Người (2) đã đi 6 nước. Lượt kế tiếp là của Máy (1).
    state_2_matrix = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 1, 1, 2, 0, 0],
        [0, 0, 0, 0, 0, 2, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    game = CaroGame(board_size=9)
    game.board = state_2_matrix.copy()

    ai = CaroAI(depth=depth)
    ai.ai_player = 1
    ai.human_player = 2

    print("[Đang chạy] Minimax thuần túy...")
    move_mm, score_mm, time_mm, nodes_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {nodes_mm}, Thời gian: {time_mm:.4f}s")

    print("\n[Đang chạy] Alpha-Beta Pruning...")
    move_ab, score_ab, time_ab, nodes_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {nodes_ab}, Thời gian: {time_ab:.4f}s")

def run_experiment_state_3(depth):
    print(f"\n" + "="*15 + f" STATE 3: MÁY TẤN CÔNG SẮP THẮNG (DEPTH {depth}) " + "="*15)
    # Máy (1) có chuỗi 3 tại hàng 4: (4,3), (4,4), (4,5) và trống hai đầu. Lượt Máy đi để giành chiến thắng.
    game = CaroGame(board_size=9)
    game.board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],  # MÁY (1) CÓ CHUỖI 3 THOÁNG
        [0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    ai = CaroAI(depth=depth)
    ai.ai_player = 1
    ai.human_player = 2
    
    print("[Đang chạy] Minimax thuần túy...")
    move_mm, score_mm, time_mm, nodes_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {states_mm if 'states_mm' in locals() else nodes_mm}, Thời gian: {time_mm:.4f}s")
    
    print("\n[Đang chạy] Alpha-Beta Pruning...")
    move_ab, score_ab, time_ab, nodes_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {nodes_ab}, Thời gian: {time_ab:.4f}s")
    
    reduction = ((nodes_mm - nodes_ab) / nodes_mm) * 100
    print(f"-> Hiệu suất cắt tỉa: Alpha-Beta giảm được {reduction:.2f}% số trạng thái duyệt. Nước đi dứt điểm: {move_ab}")

def run_experiment_state_4(depth):
    print(f"\n" + "="*15 + f" STATE 4: MÁY PHÒNG THỦ BẮT BUỘC (DEPTH {depth}) " + "="*15)
    # Người chơi (2) đang có chuỗi 3 thoáng tại hàng 5: (5,3), (5,4), (5,5). Đến lượt Máy (1) bắt buộc phải chặn.
    game = CaroGame(board_size=9)
    game.board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0],  # NGƯỜI CHƠI (2) CÓ CHUỖI 3 THOÁNG
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    ai = CaroAI(depth=depth)
    ai.ai_player = 1
    ai.human_player = 2
    
    print("[Đang chạy] Minimax thuần túy...")
    move_mm, score_mm, time_mm, nodes_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {nodes_mm}, Thời gian: {time_mm:.4f}s")
    
    print("\n[Đang chạy] Alpha-Beta Pruning...")
    move_ab, score_ab, time_ab, nodes_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {nodes_ab}, Thời gian: {time_ab:.4f}s")
    
    reduction = ((nodes_mm - nodes_ab) / nodes_mm) * 100
    print(f"-> Hiệu suất cắt tỉa: Alpha-Beta giảm được {reduction:.2f}% số trạng thái duyệt. Nước đi phòng thủ: {move_ab}")

def run_experiment_state_5(depth):
    print(f"\n" + "="*15 + f" STATE 5: THẾ TRẬN GIẰNG CO CHIẾN THUẬT (DEPTH {depth}) " + "="*15)
    # Thế trận đối công cân bằng, cả hai bên đều mở ra các đường tạo chuỗi đôi.
    game = CaroGame(board_size=9)
    game.board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0],  # Máy (1) có chuỗi 2 nằm ngang
        [0, 0, 0, 2, 2, 0, 0, 0, 0],  # Người (2) có chuỗi 2 nằm ngang
        [0, 1, 1, 0, 0, 0, 0, 0, 0],  # Máy (1) có chuỗi 2 nằm ngang
        [0, 0, 0, 0, 0, 2, 0, 0, 0],  # Người (2) có chuỗi 2 dọc
        [0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    ai = CaroAI(depth=depth)
    ai.ai_player = 1
    ai.human_player = 2
    
    print("[Đang chạy] Minimax thuần túy...")
    move_mm, score_mm, time_mm, nodes_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {nodes_mm}, Thời gian: {time_mm:.4f}s")
    
    print("\n[Đang chạy] Alpha-Beta Pruning...")
    move_ab, score_ab, time_ab, nodes_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {nodes_ab}, Thời gian: {time_ab:.4f}s")
    
    reduction = ((nodes_mm - nodes_ab) / nodes_mm) * 100
    print(f"-> Hiệu suất cắt tỉa: Alpha-Beta giảm được {reduction:.2f}% số trạng thái duyệt. Nước tối ưu: {move_ab}")


if __name__ == "__main__":
    target_depth = 2
    if len(sys.argv) > 1:
        try:
            target_depth = int(sys.argv[1])
        except ValueError:
            print("[Lỗi] Vui lòng truyền độ sâu depth là một số nguyên hợp lệ!")
            sys.exit(1)
    print(f"=== BẮT ĐẦU CHẠY TOÀN BỘ THỰC NGHIỆM MÁY ĐI TRƯỚC VỚI DEPTH = {target_depth} ===")
    
    # Kích hoạt chạy toàn bộ 5 States
    run_experiment_state_1(target_depth)
    run_experiment_state_2(target_depth)
    run_experiment_state_3(target_depth)
    run_experiment_state_4(target_depth)
    run_experiment_state_5(target_depth)
    
    target_depth = 3
    print(f"=== BẮT ĐẦU CHẠY TOÀN BỘ THỰC NGHIỆM MÁY ĐI TRƯỚC VỚI DEPTH = {target_depth} ===")
    
    run_experiment_state_1(target_depth)
    run_experiment_state_2(target_depth)
    run_experiment_state_3(target_depth)
    run_experiment_state_4(target_depth)
    run_experiment_state_5(target_depth)

    print("\n=== THỰC NGHIỆM HOÀN TẤT ===")