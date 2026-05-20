# 📄 Hướng dẫn Cập nhật Giao diện: Chuẩn hóa Đối tượng Kế toán (Accounting Party)

Chào team Frontend, Backend đã hoàn thành việc chuẩn hóa dữ liệu cho module Accounting. Dưới đây là các thay đổi quan trọng mà team cần cập nhật để hiển thị đúng thông tin đối tượng (Khách hàng/Nhân viên) trên giao diện.

## 1. Thay đổi cấu trúc API Response

Trong các API của Finotes (Danh sách và Chi tiết), các trường cũ như `organizationName` hoặc `partner` đã được thay thế bằng một object `party` duy nhất.

### Cấu trúc mới:
```json
{
  "id": 123,
  "code": "INC-2026-0001",
  ...
  "party": {
    "id": 101,          // ID của Tổ chức hoặc Nhân viên (nếu có)
    "name": "Công ty ABC", // Tên hiển thị (Đã được Backend xử lý sẵn)
    "type": "ORGANIZATION" // Loại đối tượng: ORGANIZATION | EMPLOYEE | INCIDENTAL
  }
}
```

## 2. Hướng dẫn Hiển thị trên UI

### 2.1. Hiển thị Tên
Team không cần phải thực hiện logic nối tên hay kiểm tra null phức tạp nữa. Hãy sử dụng trực tiếp:
👉 `finote.party.name`

### 2.2. Hiển thị Icon (Phân loại đối tượng)
Dựa vào trường `party.type` để hiển thị Icon tương ứng:

| `party.type` | Ý nghĩa | Icon đề xuất (Lucide/Shadcn) |
| :--- | :--- | :--- |
| `ORGANIZATION` | Khách hàng Doanh nghiệp / Đối tác | `Building2` |
| `EMPLOYEE` | Nhân viên (Chi lương, tạm ứng...) | `UserCheck` |
| `INCIDENTAL` | Khách vãng lai / Đối tượng lẻ | `User` |

## 3. API Tạo mới (Create Finote)

Khi gửi dữ liệu tạo phiếu, team hãy cập nhật các field tương ứng:

- Nếu là Tổ chức/Khách hàng: Gửi `organizationId`.
- Nếu là Nhân viên: Gửi `employeeId`.
- Nếu là Khách lẻ: Gửi `partyName`.

**Lưu ý**: Backend sẽ tự động lấy thông tin Tên và Loại từ DB dựa trên ID bạn gửi lên để đảm bảo tính chính xác, bạn không cần gửi kèm `partyType`.

---
*Mọi thắc mắc về cấu trúc dữ liệu mới, vui lòng liên hệ team Backend.*
