# Rate Limiter for Chat System

This project contains two implementations of message rate limiting algorithms for a chat system:

- **Sliding Window Rate Limiter**
- **Throttling Rate Limiter**

The goal is to prevent spam in the chat by controlling the number or frequency of messages a user can send over a given period.

---

# ⚙️ 1. SlidingWindowRateLimiter

### Description

This algorithm allows a maximum of **N messages within the last T seconds**. Each new message checks whether the sliding window already contains the allowed number of messages. If not — the message is accepted, otherwise — it's blocked.

### Parameters:

- `window_size` – size of the time window in seconds (default: `10`)
- `max_requests` – maximum number of messages allowed in the window (`1`)

### Main Methods:

- `can_send_message(user_id)` – checks if the user is allowed to send a message
- `record_message(user_id)` – records a message if allowed
- `time_until_next_allowed(user_id)` – returns the time left until the next message is allowed

### Example run:

    python sliding_window_limiter.py

---

# 🧭 2. ThrottlingRateLimiter

This algorithm enforces a fixed interval between messages from a single user. For example, no more than one message every 10 seconds. If a user sends a new message too early — it's blocked.

### Parameters:
- `min_interval` – minimum interval between messages (default: 10 seconds)

### Main Methods:
- `can_send_message(user_id)` – checks if the user is allowed to send a message
- `record_message(user_id)` – records the time if the message is allowed
- `time_until_next_allowed(user_id)` – returns the time remaining until sending is allowed

### Example run:
    python throttling_limiter.py

---

## 🧪 Testing

Both algorithms have test functions: `test_rate_limiter()` and `test_throttling_limiter()`, respectively. They simulate message sending by multiple users with random delays.

The output looks like:

    Message   1 | User 2 | ✓
    Message   6 | User 2 | × (wait 7.0s)
