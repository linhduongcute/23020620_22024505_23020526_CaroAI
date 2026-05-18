import time

class GameTimer:
    """
    Công cụ đo đạc thời gian chạy (Execution Time) của thuật toán AI.
    Yêu cầu tích hợp vào engine để đánh giá hiệu suất của Minimax.
    """
    def __init__(self):
        self.start_time = None

    def start(self):
        """Bắt đầu đo thời gian."""
        self.start_time = time.time()

    def get_elapsed_time(self):
        """Lấy thời gian đã trôi qua kể từ lúc gọi hàm start() (tính bằng giây)."""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

class StateCounter:
    """
    Công cụ đếm số lượng trạng thái (Node) mà thuật toán đã duyệt qua trên cây không gian trạng thái.
    Yêu cầu tích hợp để đo lường mức độ mở rộng của thuật toán Minimax.
    """
    def __init__(self):
        self.count = 0

    def increment(self):
        """Tăng tổng số trạng thái đã duyệt lên 1 khi đi vào một node mới."""
        self.count += 1

    def reset(self):
        """Đặt lại bộ đếm về 0 cho lượt tính toán tiếp theo."""
        self.count = 0

    def get_count(self):
        """Trả về tổng số trạng thái đã được ghi nhận."""
        return self.count
