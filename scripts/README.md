# 🤖 HƯỚNG DẪN CHẠY SCRIPTS QUA CỔNG 9ROUTER (LLM PROXY)

Tài liệu này hướng dẫn cách chạy các công cụ tự động hóa trong thư mục `scripts/` (e.g. `sync_stax_docs.py`, `process_vault.py`) thông qua cổng **9router (Local LLM Proxy)** chạy ở máy cá nhân của bạn.

---

## ⚙️ CẤU HÌNH THAM CHIẾU (FROM CLAUDE CODE)

Dựa trên cấu hình Claude Code của bạn tại `.claude/settings.json`, các thông số kết nối 9router gồm:
*   **Base URL (Proxy):** `http://localhost:20128`
*   **API Key:** `sk-5638d38bced51efe-k98d75-a4b55eba`
*   **Model:** `ag/gemini-3-flash`

---

## 🚀 CÁC CÁCH CHẠY SCRIPTS

Bạn có thể chạy các kịch bản đồng bộ hoặc phân tích theo 2 cách dưới đây tùy thuộc vào thói quen sử dụng:

### Cách 1: Thiết lập Biến môi trường tạm thời (Khuyên dùng)
Cách này giúp bạn chỉ cần thiết lập biến môi trường 1 lần trong phiên terminal hiện tại, sau đó có thể chạy thoải mái các script khác nhau:

```bash
# 1. Khai báo các biến môi trường trỏ đến 9router
export ANTHROPIC_BASE_URL="http://localhost:20128"
export ANTHROPIC_API_KEY="sk-5638d38bced51efe-k98d75-a4b55eba"
export ANTHROPIC_MODEL="ag/gemini-3-flash"

# 2. Chạy lệnh đồng bộ tri thức STAX_ASP sang Wiki
python3 scripts/sync_stax_docs.py

# 3. (Tùy chọn) Chạy lệnh nạp dữ liệu Vault
python3 scripts/process_vault.py
```

### Cách 2: Chạy lệnh nội dòng (Inline Command)
Cách này phù hợp khi bạn muốn chạy nhanh một câu lệnh duy nhất mà không làm ảnh hưởng đến cấu hình biến môi trường toàn cục của Terminal:

```bash
# Đồng bộ tri thức STAX
ANTHROPIC_BASE_URL="http://localhost:20128" ANTHROPIC_API_KEY="sk-5638d38bced51efe-k98d75-a4b55eba" ANTHROPIC_MODEL="ag/gemini-3-flash" python3 scripts/sync_stax_docs.py

# Nạp dữ liệu Vault
ANTHROPIC_BASE_URL="http://localhost:20128" ANTHROPIC_API_KEY="sk-5638d38bced51efe-k98d75-a4b55eba" ANTHROPIC_MODEL="ag/gemini-3-flash" python3 scripts/process_vault.py
```

---

## 🛠️ CƠ CHẾ HOẠT ĐỘNG DƯỚI HẠ TẦNG

Cả hai file `sync_stax_docs.py` và `process_vault.py` đều sử dụng thư viện `urllib.request` để gửi yêu cầu HTTP POST:
1.  **URL Định tuyến:** Script sẽ đọc biến `ANTHROPIC_BASE_URL` từ môi trường (mặc định trỏ đến `https://api.anthropic.com` nếu thiếu) và ghép nối thành đường dẫn `/v1/messages`. Khi chạy qua 9router, nó sẽ gửi đến: `http://localhost:20128/v1/messages`.
2.  **API Key & Version Headers:** Đính kèm API key của 9router qua header `x-api-key`.
3.  **Hỗ trợ Stream Proxy:** Script tự động xử lý định dạng Server-Sent Events (SSE) `text/event-stream` do 9router trả về, đảm bảo phân tích văn bản mượt mà, không bị gián đoạn.

---
*Tài liệu hướng dẫn tối ưu cho môi trường làm việc cá nhân của bạn.*
