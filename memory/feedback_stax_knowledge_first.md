---
description: Bắt buộc tra cứu tri thức nội bộ STAX trước, dùng nhãn [Tham khảo ngoài]
  cho tri thức ngoại vi và Cổng Xác thực trước khi cập nhật tri thức mới.
metadata:
  node_type: memory
  originSessionId: 00325e94-edb8-4e30-9739-1d94947692ee
  type: feedback
name: feedback-stax-knowledge-first
synced_at: '2026-05-25 13:23:24'
synced_to_claudemd: true
---

Khi trả lời hoặc thảo luận về bất kỳ khía cạnh kỹ thuật hay nghiệp vụ nào của STAX (HRM, CRM, Kế toán, RBAC):
1. **Ưu tiên Tri thức Nội bộ:** Luôn luôn quét `02_atomic_nodes/` và `03_neural_map/AI_ROUTING_TABLE.md` trước để lấy tài liệu gốc và dẫn nguồn bằng link Obsidian.
2. **Tham khảo ngoài:** Nếu không tìm thấy trong hệ thống Wiki, thông báo rõ và gắn nhãn `[Tham khảo ngoài - External Reference]` khi trích xuất thông tin từ codebase STAX_ASP hoặc tài liệu Clean Architecture chuẩn ngành.
3. **Cổng Xác thực Tương tác (Interactive Siphon Gate):** Nếu phát hiện tri thức ngoài quan trọng chưa có trong Wiki, bắt buộc hỏi ý kiến người dùng: *"Tôi phát hiện tri thức về [{topic}] chưa có trong kho tri thức STAX Wiki. Bạn có muốn đồng bộ và tạo một nốt nguyên tử mới cho chuyên đề này không? (y/N)"* trước khi tạo file mới hoặc cập nhật chỉ mục.

**Why:**
- Tránh làm loãng hoặc duplicate tri thức khi không cần thiết.
- Đảm bảo tính nhất quán của tri thức nội bộ luôn là nguồn chân lý duy nhất.
- Ngăn ngừa AI tự tiện đưa các mẫu thiết kế không tương thích hoặc boilerplate thừa thãi vào kho tri thức.

**How to apply:**
- Áp dụng làm quy tắc mặc định cho mọi lượt chat, mọi câu hỏi và mọi session xử lý thiết kế.
