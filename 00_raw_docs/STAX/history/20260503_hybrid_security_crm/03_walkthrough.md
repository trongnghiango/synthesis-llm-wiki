# 🏆 WALKTHROUGH: TRIỂN KHAI HỆ THỐNG BẢO MẬT LAI (HYBRID SECURITY MODEL)

**Ngày thực hiện:** 2026-05-03
**Mã số:** 001
**Tác giả:** Antigravity AI
**Trạng thái:** Hoàn tất (100%)

---

## 🏗️ TỔNG QUAN HÀNH ĐỘNG

Dựa trên tư duy kiến trúc **"Pragmatic Hybrid Security Model"**, chúng ta đã chuẩn hóa và triển khai mô hình bảo mật 3 lớp cho Module Leads (CRM). Đây là mô hình hình mẫu cho toàn bộ dự án STAX.

### 1. Các lớp bảo vệ đã triển khai:
*   **Lớp 1 (Guard):** Chặn thô tại Controller bằng `@Permissions`.
*   **Lớp 2 (Query):** Lọc dữ liệu tại SQL bằng `organizationId` của User (isolation).
*   **Lớp 3 (DTO):** Phán xử hành động chi tiết tại Response DTO qua field `_actions`.

---

## 🛠️ CHI TIẾT THAY ĐỔI

### A. Tầng Presentation (Layer 1)
*   Cập nhật `LeadController` để áp dụng `@Permissions` cho mọi hành động:
    *   `GET /crm/leads` -> `crm:leads:read`
    *   `GET /crm/leads/:id` -> `crm:leads:read`
    *   `PATCH /crm/leads/:id/assign` -> `crm:leads:edit`
    *   `POST /crm/leads/:id/won` -> `crm:leads:edit`
    *   `POST /crm/leads/intake` -> `crm:leads:create`

### B. Tầng Application & Query (Layer 2 & 3)
*   **Layer 2 (Isolation):** `LeadQueryService` tự động tiêm `organizationId` từ `currentUser` vào Repository để đảm bảo User chỉ nhìn thấy Leads của tổ chức mình.
*   **Layer 3 (Action Logic):** Triển khai logic tính toán `_actions` động:
    ```typescript
    _actions: {
        edit: {
            allowed: !isClosed && (isOwner || isAdmin),
            reason: isClosed ? 'Lead đã đóng, không thể sửa' : 'Bạn không phụ trách Lead này'
        },
        // ... assign, won ...
    }
    ```

### C. Tầng Infrastructure (DTO)
*   `LeadResponseDto` hiện đã kế thừa `ActionableDto`, cung cấp metadata chuẩn cho Frontend.
*   Thêm API `GET /crm/leads/:id` để trả về thông tin chi tiết kèm bộ phán xử hành động đầy đủ.

---

## 🎯 KẾT QUẢ ĐẠT ĐƯỢC

1.  **Hệ thống "An toàn từ trong ra ngoài":** Dữ liệu được lọc từ tầng Query, quyền truy cập được Guard chặn tại cổng, và giao diện được điều khiển bởi DTO.
2.  **Trải nghiệm DX tuyệt vời:** Developer Frontend không cần quan tâm đến logic Business phức tạp (khi nào được hiện nút), chỉ cần đọc field `_actions`.
3.  **Đáp ứng "Hiến pháp STAX":** Tuân thủ triến lý "Pháo đài" trong việc bảo vệ dữ liệu lõi.

---
*Tài liệu lưu trữ nội bộ STAX.*
