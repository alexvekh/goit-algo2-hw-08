import random
from typing import Dict
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.message_history: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        if user_id in self.message_history:
            window = self.message_history[user_id]
            # Видаляємо всі старі записи, які вийшли за межі вікна
            while window and current_time - window[0] > self.window_size:
                window.popleft()
            # 3. При видаленні всіх повідомлень з вікна користувача 
            # видаляється запис про користувача зі структури даних.
            if not window:
                del self.message_history[user_id]

    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        # 2. При першому повідомленні від користувача завжди повертається True
        if user_id not in self.message_history:
            return True

        # 1. При спробі відправити повідомлення раніше ніж через 10 секунд 
        # повертається False.
        return len(self.message_history[user_id]) < self.max_requests
    
    def record_message(self, user_id: str) -> bool:
        current_time = time.time()
        if self.can_send_message(user_id):
            if user_id not in self.message_history:
                self.message_history[user_id] = deque()
            self.message_history[user_id].append(current_time)
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        if user_id not in self.message_history:
            return 0.0

        window = self.message_history[user_id]
        if len(window) < self.max_requests:
            return 0.0
        # Коли користувач досяг ліміту, рахуємо залишок часу до можливості надсилання
        # повертає час очікування в секундах
        return max(0.0, self.window_size - (current_time - window[0]))

# Демонстрація роботи
def test_rate_limiter():
    # Створюємо rate limiter: вікно 10 секунд, 1 повідомлення
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Симулюємо потік повідомлень від користувачів (послідовні ID від 1 до 20)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, 11):
        # Симулюємо різних користувачів (ID від 1 до 5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Невелика затримка між повідомленнями для реалістичності
        # Випадкова затримка від 0.1 до 1 секунди
        time.sleep(random.uniform(0.1, 1.0))

    # Чекаємо, поки вікно очиститься
    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        # Випадкова затримка від 0.1 до 1 секунди
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_rate_limiter()

# === Симуляція потоку повідомлень ===
# Повідомлення  1 | Користувач 2 | ✓
# Повідомлення  2 | Користувач 3 | ✓
# Повідомлення  3 | Користувач 4 | ✓
# Повідомлення  4 | Користувач 5 | ✓
# Повідомлення  5 | Користувач 1 | ✓
# Повідомлення  6 | Користувач 2 | × (очікування 7.0с)
# Повідомлення  7 | Користувач 3 | × (очікування 6.5с)
# Повідомлення  8 | Користувач 4 | × (очікування 7.0с)
# Повідомлення  9 | Користувач 5 | × (очікування 6.8с)
# Повідомлення 10 | Користувач 1 | × (очікування 7.4с)

# Очікуємо 4 секунди...

# === Нова серія повідомлень після очікування ===
# Повідомлення 11 | Користувач 2 | × (очікування 1.0с)
# Повідомлення 12 | Користувач 3 | × (очікування 0.7с)
# Повідомлення 13 | Користувач 4 | × (очікування 0.4с)
# Повідомлення 14 | Користувач 5 | × (очікування 0.0с)
# Повідомлення 15 | Користувач 1 | ✓
# Повідомлення 16 | Користувач 2 | ✓
# Повідомлення 17 | Користувач 3 | ✓
# Повідомлення 18 | Користувач 4 | ✓
# Повідомлення 19 | Користувач 5 | ✓
# Повідомлення 20 | Користувач 1 | × (очікування 7.0с)