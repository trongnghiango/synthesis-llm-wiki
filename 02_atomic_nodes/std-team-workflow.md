---
id: std-team-workflow
title: Quy trình làm việc & Archive lịch sử (Team Workflow & History)
layer: 3-atomic
parent: "[[02_standards_governance]]"
depends_on: []
summary: "Quy chuẩn quy trình 4 bước lưu vết từ BA đến code, và quy trình đóng băng lịch sử công việc vào history/."
tags: [standards, workflow, history, archiving, documentation]
---

# Quy trình làm việc & Archive lịch sử (Team Workflow & History)

Hệ thống STAX yêu cầu mọi thay đổi hoặc bổ sung tính năng lớn phải được lập tài liệu và lưu vết rõ ràng để đảm bảo khả năng bàn giao hoàn hảo cho các AI Agent và Developer kế cận.

## 1. Quy trình phát triển tính năng 4 bước (The 4-Step Document Gate)
Mỗi tính năng mới bắt buộc phải đi qua 4 tài liệu chốt chặn:
1.  **Bước 1 - Phân tích nghiệp vụ (`00_analysis.md`):** Đặc tả nghiệp vụ từ khách hàng, định nghĩa từ vựng Ubiquitous Language.
2.  **Bước 2 - Bản thiết kế Kiến trúc (`01_implementation_plan.md`):** Thiết kế database schema (Drizzle), định nghĩa API contracts (Zod), và cấu trúc phân lớp code.
3.  **Bước 3 - Checklist thực thi (`02_tasks.md`):** Phân chia danh sách các tác vụ cụ thể để theo dõi tiến độ viết code.
4.  **Bước 4 - Nhật ký Bàn giao (`03_walkthrough.md`):** Ghi chép cách kiểm thử thủ công và tự động, kết quả đạt được sau khi code hoàn tất.

## 2. Quy trình Đóng băng Lịch sử (History Archiving)
*   **Khi nào làm:** Khi tính năng đã hoàn thiện, vượt qua tất cả các bài kiểm tra chất lượng và được **merged thành công vào nhánh `main`**.
*   **Hành động:** Di chuyển toàn bộ thư mục chứa 4 tệp tin trên vào thư mục:
    `docs/STAX/history/{YYYYMMDD}_{slug_ten_tinh_nang}/`
*   **Nguyên tắc đóng băng:** Thư mục `history/` là bất biến. Cấm chỉnh sửa nội dung bên trong sau khi đã đưa vào đây để giữ nguyên vết lịch sử thực tế của codebase tại thời điểm đó.
