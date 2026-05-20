# 🧠 SYNTHESIS LLM WIKI — STAX PROJECT KNOWLEDGE BRAIN

Dự án này là một **Personal Knowledge Management (PKM)** vault được thiết kế theo mô hình **Đường ống Tri thức Đa tầng (Multi-layered Knowledge Pipeline)** tối ưu hóa cho cả Con người (Developer) và Trí tuệ Nhân tạo (AI Agent). 

Hệ thống được thiết kế đặc biệt nhằm giải quyết nút thắt cổ chai về Ngữ cảnh (Context Window) và chi phí Token, giúp AI định tuyến và truy xuất chính xác thông tin chỉ trong vòng 1-2 bước.

---

## 🌳 KIẾN TRÚC ĐƯỜNG ỐNG TRI THỨC ĐA TẦNG (KNOWLEDGE PIPELINE)

```
[Layer 1: Raw] (00_raw_docs/) ──► Gốc đối chiếu, đóng băng tri thức gốc.
       │
       ▼
[Layer 2: Canonical] (01_structured_docs/) ──► Hợp nhất chuyên đề lớn cho Con người đọc.
       │
       ▼
[Layer 3: Atomic] (02_atomic_nodes/) ──► Mảnh ghép tri thức cực nhỏ (<50 lines) cho AI.
       │
       ▼
[Layer 4: Neural Map] (03_neural_map/) ──► Bản đồ định tuyến AI siêu nhẹ (<500 tokens).
```

### 📁 Chi tiết các Phân tầng Folder:

1.  **Layer 1: Raw (00_raw_docs/)**
    *   *Mục đích:* Bản copy nguyên trạng, bất biến tài liệu gốc từ dự án `STAX_ASP`.
    *   *Đường dẫn:* [00_raw_docs/](00_raw_docs/)
2.  **Layer 2: Canonical (01_structured_docs/)**
    *   *Mục đích:* Hợp nhất và hệ thống hóa tri thức thành 4 chuyên đề lớn rõ ràng cho lập trình viên nghiên cứu.
    *   *Đường dẫn:* [01_structured_docs/INDEX.md](01_structured_docs/INDEX.md)
3.  **Layer 3: Atomic Nodes (02_atomic_nodes/)**
    *   *Mục đích:* Bẻ nhỏ Layer 2 thành 16 nốt nguyên tử cực kỳ tinh gọn, có YAML frontmatter chuẩn và liên kết chéo.
    *   *Đường dẫn:* [02_atomic_nodes/INDEX.md](02_atomic_nodes/INDEX.md)
4.  **Layer 4: Neural Map (03_neural_map/)**
    *   *Mục đích:* File chỉ mục nơ-ron định tuyến, hướng dẫn AI Agent tìm đúng nốt cần đọc dựa trên loại hành động nghiệp vụ.
    *   *Đường dẫn:* [03_neural_map/AI_ROUTING_TABLE.md](03_neural_map/AI_ROUTING_TABLE.md)

---

## 🚦 HƯỚNG DẪN DÀNH CHO AI AGENTS & DEVELOPER KHI TIẾP CẬN

1.  **Muốn hiểu tổng quan bức tranh lớn:** Hãy mở chuyên đề tương ứng tại **Layer 2** ([01_structured_docs/INDEX.md](01_structured_docs/INDEX.md)).
2.  **Muốn lập trình / sửa lỗi nhanh:**
    *   *Bước 1:* AI hãy mở duy nhất file **Layer 4 AI Routing Table** ([03_neural_map/AI_ROUTING_TABLE.md](03_neural_map/AI_ROUTING_TABLE.md)).
    *   *Bước 2:* Dựa theo loại Task cần làm, tìm đường dẫn đến **Layer 3 Atomic Node** tương ứng.
    *   *Bước 3:* Mở duy nhất file Atomic Node đó ra và thực thi code, không đọc lan man.

---
*Phát triển bởi Antigravity AI — Thiết kế tối ưu hóa Token & Tốc độ Phản hồi.*
