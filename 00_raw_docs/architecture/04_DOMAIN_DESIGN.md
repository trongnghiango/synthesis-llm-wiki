# 🧠 THIẾT KẾ MIỀN NGHIỆP VỤ (DOMAIN DESIGN)

STAX áp dụng các mô thức thiết kế tiên tiến để giải quyết các bài toán ERP phức tạp một cách bền vững.

## 1. RICH DOMAIN MODEL (MÔ HÌNH MIỀN GIÀU CÓ)

Trái ngược với mô hình Anemic (chỉ chứa data), các thực thể (Entities) của STAX chứa đựng tri thức nghiệp vụ.

*   **Encapsulation:** Các thuộc tính trạng thái (như `status`, `balance`) là `private`.
*   **Business Methods:** Việc thay đổi dữ liệu phải thông qua các phương thức có tên mang ý nghĩa nghiệp vụ (Ví dụ: `lead.closeAsWon()`, `contract.liquidate()`).
*   **Invariants:** Entity tự chịu trách nhiệm kiểm tra tính hợp lệ của chính nó (Ví dụ: Không được duyệt một phiếu chi đã bị hủy).

---

## 2. POSITION-BASED HRM (KIẾN TRÚC "CÁI GHẾ")

Phân hệ HRM của STAX giải quyết bài toán nhân sự quy mô lớn bằng cách tách rời **Người (Employee)** và **Vị trí (Position)**.

*   **Employee:** Thông tin sinh trắc học, định danh cá nhân.
*   **Position:** Là "Cái ghế" gắn liền với:
    *   **OrgUnit:** Phòng ban trực thuộc.
    *   **JobTitle:** Chức danh (Trưởng phòng, Nhân viên).
    *   **Grade:** Ngạch lương và quyền hạn.
*   **Lợi ích:** Khi một nhân sự thăng chức hoặc chuyển phòng ban, chúng ta chỉ thay đổi liên kết `Position`. Toàn bộ quyền hạn, luồng phê duyệt và mức lương sẽ tự động cập nhật theo "Cái ghế" mới.

---

## 3. SERVER-DRIVEN UI (GIAO DIỆN HƯỚNG MÁY CHỦ)

STAX giảm thiểu việc "cứng hóa" logic trên Frontend để tăng khả năng linh hoạt.

*   **UI Flags:** API `/system/bootstrap` trả về các cờ quyền hạn (Ví dụ: `canManageHRM`).
*   **_actions Pattern:** 
    *   Trong các DTO trả về, Backend nhúng thêm object `_actions`.
    *   Ví dụ: `{ "_actions": { "edit": { "allowed": false, "reason": "Hợp đồng đã thanh lý" } } }`.
*   **Lookups:** Frontend lấy label, màu sắc, icon của các trạng thái từ API `/system/lookups`.

---

## 4. OMNICHANNEL ACTIVITY FEED

Hội tụ mọi tương tác (Chat, Email, Ghi chú, Thay đổi hệ thống) vào một dòng thời gian duy nhất.

*   **Timeline:** Giúp Sales và CS có cái nhìn 360 độ về lịch sử khách hàng.
*   **Event-Driven:** Feed được tổng hợp tự động từ các Domain Events, không cần code thủ công việc chèn bản ghi timeline ở khắp nơi.

---
*Cập nhật ngày 08/05/2026 bởi Antigravity AI.*
