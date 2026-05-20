# Logic Analysis: STAX Safe-Update Pattern

## 1. Mục đích (Purpose)
- **Vấn đề:** Hiện tại, nhiều Drizzle Repository đang truyền toàn bộ đối tượng dữ liệu (bao gồm cả trường Khóa chính `id`) vào phương thức `.set()` của lệnh `.update()`. Điều này vi phạm ràng buộc bảo vệ Khóa chính của PostgreSQL, gây ra lỗi `500 Internal Server Error`.
- **Giải pháp:** Xây dựng một cơ chế tập trung (Centralized) để tự động lọc bỏ các trường không được phép cập nhật (`id`, `createdAt`) trước khi gửi lệnh xuống Database.
- **Vị trí Tier:** Tier 0 - Infrastructure Foundation (Lớp hạ tầng cốt lõi).

## 2. Yêu cầu phi chức năng (NFR)
- **Tính nhất quán:** Áp dụng đồng bộ cho tất cả các Repository kế thừa từ `DrizzleBaseRepository`.
- **Hiệu năng:** Việc lọc dữ liệu phải diễn ra cực nhanh bằng native JavaScript/TypeScript, không gây overhead cho DB.
- **Type Safety:** Dữ liệu sau khi lọc vẫn phải đảm bảo đúng kiểu dữ liệu (`Partial<InsertModel>`) mà Drizzle yêu cầu để tránh lỗi biên dịch.

## 3. Tác động (Impact)
- **Core Layer:** Thay đổi `DrizzleBaseRepository` trong `@core/shared`.
- **Infrastructure Layer:** Cập nhật lại phương thức `save` của ít nhất 7 Repositories hiện có (`Lead`, `Organization`, `Contact`, `Employee`, `Finote`, `Notification`, `User`).
- **Data Integrity:** Đảm bảo `createdAt` không bao giờ bị ghi đè vô tình khi thực hiện các tác vụ cập nhật thông tin.

## 4. Open Questions
1. Ngoài `id` và `createdAt`, chúng ta có muốn bảo vệ thêm các trường "Tenant-Isolation" như `organizationId` khỏi lệnh update thông thường không? (Khuyến nghị: **CÓ**, để tăng cường bảo mật dữ liệu).
2. Chúng ta nên đặt tên phương thức helper là gì để vừa ngắn gọn vừa tường minh? (Gợi ý: `mapToUpdate` hoặc `omitImmutableFields`).

---
👉 *Phân tích này đã chính xác ý đồ của bạn chưa? Hãy xác nhận để tôi lên thiết kế chi tiết (Bước 2).*
