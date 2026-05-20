---
title: "Chiến lược Dữ liệu (Data Strategy)"
summary: "Drizzle ORM, Delta Logging và Hybrid Storage Pattern"
status: current
last_updated: "2026-05-10"
tags: [database, drizzle, logging, audit]
---

# 🗄️ Chiến lược Dữ liệu (Data Strategy)

Dữ liệu là tài sản quý giá nhất của STAX. Chúng ta quản trị dữ liệu dựa trên sự kết hợp giữa tính chặt chẽ của SQL và sự linh hoạt của NoSQL.

## 1. DRIZZLE ORM (SQL-FIRST)

Tại sao STAX chọn Drizzle thay vì TypeORM hay Prisma?
*   **Performance:** Drizzle siêu nhẹ, không có overhead.
*   **Type-safety:** Tận dụng tối đa sức mạnh của TypeScript 5+.
*   **Transparency:** Bạn viết gì, Drizzle chạy nấy (SQL-First).

---

## 2. GIÁM SÁT DỮ LIỆU (DELTA LOGGING)

Thay vì lưu trữ ảnh chụp toàn bộ bản ghi (Full Snapshot), STAX sử dụng chiến lược **Delta Logging (Diff)**.

*   **Cơ chế:** Khi có thay đổi, hệ thống chỉ lưu lại những trường thực sự khác biệt giữa `before` và `after`.
*   **Lợi ích:**
    *   Tiết kiệm 80% dung lượng lưu trữ Database Log.
    *   Hiển thị Activity Feed thông minh (Ví dụ: "User A đã đổi trạng thái từ Chờ duyệt sang Đã duyệt").
*   **Tích hợp:** Tự động thực thi thông qua `ObjectDiff` utility và `AuditDomainEventHandler`.

---

## 3. LƯU TRỮ LAI (HYBRID STORAGE PATTERN)

Theo **ADR 003**, chúng ta đối phó với dữ liệu phi cấu trúc (hoặc dữ liệu legacy) bằng cột `metadata` kiểu **JSONB**.

*   **Schema Sạch:** Các cột SQL quan trọng (ID, Name, Date, Status) được định nghĩa rõ ràng để Index và Query.
*   **Metadata Linh hoạt:** Các thông tin phụ (Nick name, Ghi chú cũ, Cấu hình riêng của từng Tenant) được đẩy vào JSONB.
*   **Lợi ích:** Tránh việc phải "đục" schema liên tục mỗi khi có yêu cầu thêm trường dữ liệu nhỏ từ khách hàng.

---

## 4. GIA CỐ KIỂU DỮ LIỆU (STRICT ENUMS)

Theo **ADR 002**, mọi trường `status` và `type` phải được quản trị bằng **pgEnum**.

*   **Database Level:** Ngăn chặn việc nhập sai chính tả (Ví dụ: `Won` vs `won`).
*   **Code Level:** TypeScript Enum giúp gợi ý code và ngăn chặn lỗi runtime.
*   **Báo cáo:** Đảm bảo các con số báo cáo tài chính và hiệu suất kinh doanh luôn chính xác tuyệt đối.

---

## 5. OPTIMIZATION & INDEXING

*   **Composite Indexes:** Sử dụng index phức hợp cho các truy vấn phổ biến (Ví dụ: `(organization_id, status)`).
*   **Full-text Search:** Sẵn sàng cho việc tìm kiếm tên khách hàng, số điện thoại trên lượng dữ liệu lớn bằng `tsvector` trong tương lai.

---
*Cập nhật ngày 08/05/2026 bởi Antigravity AI.*
