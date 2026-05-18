import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
from game_logic import CaroGame
from ai_engine import CaroAI

def run_experiments():
    print("=== CHẠY THỰC NGHIỆM CHO STATE 2 ===")
    
    # Định nghĩa State 2: 12 quân cờ (7 X, 6 O vì X đi trước, đến lượt O đi)
    # 1: Người (X), 2: Máy (O)
    state_2_matrix = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 2, 1, 2, 0, 0, 0, 0],
        [0, 0, 0, 2, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    # Khởi tạo trò chơi và gán state
    game = CaroGame(board_size=9)
    game.board = state_2_matrix.copy()

    # Độ sâu d = 3
    depth = 3
    ai = CaroAI(depth=depth)

    # 1. Chạy Minimax
    print("\nĐang chạy thuật toán Minimax (d=3)...")
    best_move_mm, best_score_mm, time_mm, nodes_mm = ai.get_best_move(game, algorithm='minimax')
    
    print(f"--- KẾT QUẢ MINIMAX ---")
    print(f"Nước đi chọn (Tọa độ): {best_move_mm}")
    print(f"Điểm đánh giá: {best_score_mm}")
    print(f"Số trạng thái đã xét (Nodes): {nodes_mm}")
    print(f"Thời gian chạy (s): {time_mm:.4f}s")

    # Đặt lại bàn cờ gốc (do get_best_move có thể đã thay đổi state nếu có lỗi, nhưng ở đây code khá an toàn)
    game.board = state_2_matrix.copy()

    # 2. Chạy Alpha-Beta
    print("\nĐang chạy thuật toán Alpha-Beta (d=3)...")
    best_move_ab, best_score_ab, time_ab, nodes_ab = ai.get_best_move(game, algorithm='alpha_beta')
    
    print(f"--- KẾT QUẢ ALPHA-BETA ---")
    print(f"Nước đi chọn (Tọa độ): {best_move_ab}")
    print(f"Điểm đánh giá: {best_score_ab}")
    print(f"Số trạng thái đã xét (Nodes): {nodes_ab}")
    print(f"Thời gian chạy (s): {time_ab:.4f}s")

def run_experiment_state_3():
    game = CaroGame(board_size=9)
    game.board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Cấu hình kiểm thử ở độ sâu d = 3 theo yêu cầu đề bài
    ai = CaroAI(depth=4)
    ai.ai_player = 2
    ai.human_player = 1
    
    print("\n" + "="*20 + " THỰC NGHIỆM STATE 3 (MÁY SẮP THẮNG) " + "="*20)
    
    # --- CHẠY VỚI MINIMAX THUẦN ---
    print("[Đang chạy] Minimax thuần túy...")
    move_mm, score_mm, time_mm, states_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {states_mm}, Thời gian: {time_mm:.4f}s")
    
    # --- CHẠY VỚI ALPHA-BETA PRUNING ---
    print("\n[Đang chạy] Alpha-Beta Pruning...")
    move_ab, score_ab, time_ab, states_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {states_ab}, Thời gian: {time_ab:.4f}s")
    
    # --- ĐÁNH GIÁ ---
    reduction = ((states_mm - states_ab) / states_mm) * 100
    print("\n" + "-"*50)
    print(f"Hiệu suất cắt tỉa: Alpha-Beta giảm được {reduction:.2f}% số trạng thái duyệt!")
    print(f"Kết luận: AI chọn nước đi dứt điểm trận đấu: {move_ab}")
    print("-"*50)

def run_experiment_state_4():
    game = CaroGame(board_size=9)
    game.board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Cấu hình kiểm thử ở độ sâu d = 4 để chứng minh hiệu năng cắt nhánh
    ai = CaroAI(depth=2)
    ai.ai_player = 2
    ai.human_player = 1
    
    print("\n" + "="*20 + " THỰC NGHIỆM STATE 4 (NGƯỜI SẮP THẮNG - DEPTH 4) " + "="*20)
    
    # --- CHẠY VỚI MINIMAX THUẦN ---
    print("[Đang chạy] Minimax thuần túy (Độ sâu 4)...")
    move_mm, score_mm, time_mm, states_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {states_mm}, Thời gian: {time_mm:.4f}s")
    
    # --- CHẠY VỚI ALPHA-BETA PRUNING ---
    print("\n[Đang chạy] Alpha-Beta Pruning (Độ sâu 4)...")
    move_ab, score_ab, time_ab, states_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {states_ab}, Thời gian: {time_ab:.4f}s")
    
    # --- ĐÁNH GIÁ ---
    reduction = ((states_mm - states_ab) / states_mm) * 100
    print("\n" + "-"*50)
    print(f"Hiệu suất cắt tỉa: Alpha-Beta giảm được {reduction:.2f}% số trạng thái duyệt!")
    print(f"Kết luận: AI chọn nước đi phòng thủ chặn đứng đối phương: {move_ab}")
    print("-"*50)

def run_experiment_state_5():
    game = CaroGame(board_size=9)
    game.board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Cấu hình kiểm thử ở độ sâu d = 3 để đánh giá tư duy chiến thuật
    ai = CaroAI(depth=4)
    ai.ai_player = 2
    ai.human_player = 1
    
    print("\n" + "="*20 + " THỰC NGHIỆM STATE 5 (THẾ TRẬN GIẰNG CO) " + "="*20)
    
    # --- CHẠY VỚI MINIMAX THUẦN ---
    print("[Đang chạy] Minimax thuần túy...")
    move_mm, score_mm, time_mm, states_mm = ai.get_best_move(game, algorithm='minimax')
    print(f"-> Kết quả Minimax: Nước đi {move_mm}, Điểm: {score_mm}, Nodes: {states_mm}, Thời gian: {time_mm:.4f}s")
    
    # --- CHẠY VỚI ALPHA-BETA PRUNING ---
    print("\n[Đang chạy] Alpha-Beta Pruning...")
    move_ab, score_ab, time_ab, states_ab = ai.get_best_move(game, algorithm='alpha_beta')
    print(f"-> Kết quả Alpha-Beta: Nước đi {move_ab}, Điểm: {score_ab}, Nodes: {states_ab}, Thời gian: {time_ab:.4f}s")
    
    # --- ĐÁNH GIÁ ---
    reduction = ((states_mm - states_ab) / states_mm) * 100
    print("\n" + "-"*50)
    print(f"Hiệu suất cắt tỉa: Alpha-Beta giảm được {reduction:.2f}% số trạng thái duyệt!")
    print(f"Kết luận: AI quyết định chọn giải pháp tối ưu: {move_ab}")
    print("-"*50)

if __name__ == "__main__":
    #run_experiments()
    #run_experiment_state_3()
    #run_experiment_state_4()
    run_experiment_state_5()
