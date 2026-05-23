# Detailed Implementation Plan — Company & RBAC Seeder Upgrade

## A. Database Schema
Chúng ta không tạo thêm bảng mới mà tái sử dụng và đồng bộ hóa triệt để cấu trúc bảng sẵn có trong hệ thống STAX:
* **`organizations`**: Neo dữ liệu vào STAX (ID: 1).
* **`org_units`**: Phòng ban (`parentId` cho phân cấp đa tầng, `path` cho định danh đường dẫn cây `/parent_id/child_id/`).
* **`positions`**: Định biên vị trí (liên kết `orgUnitId`, `jobTitleId`, `gradeId`).
* **`grades`**: Cấp bậc (ví dụ: `BAC_2`, `BAC_5`, `BAC_8`, `BAC_9`).
* **`job_titles`**: Chức danh công việc chung (ví dụ: `'Tổng Giám đốc'`, `'Giám đốc'`, `'Chuyên viên B2'`).
* **`users`**: Tài khoản đăng nhập.
* **`user_metadata`**: Thông tin người dùng cơ bản.
* **`employees`**: Hồ sơ nhân viên hành chính (chứa `metadata` JSONB lưu trữ CCCD, ngân hàng, bảo hiểm, địa chỉ).

## B. Domain Layer & Algorithms
### 1. Thuật toán Xóa dấu tiếng Việt & So khớp Hậu tố không dấu (Approach A)
Sử dụng hàm helper `removeAccents` có sẵn để chuẩn hóa:
- **Chuẩn hóa Tên rút gọn (từ `STAFF.csv`)**: `"Trúc Đào"` ➔ `"truc dao"`.
- **Chuẩn hóa Họ tên đầy đủ (từ `THONG TIN NHAN VIEN.csv`)**: `"Trần Thị Trúc Đào"` ➔ `"tran thi truc dao"`.
- **Logic Fuzzy Match**:
  Tách các từ tố không dấu của tên rút gọn. Ví dụ: `"truc dao"` ➔ `['truc', 'dao']`.
  Kiểm tra xem tên đầy đủ không dấu có chứa toàn bộ các từ tố của tên rút gọn hay không. Ví dụ: `"tran thi truc dao"` chứa cả `"truc"` và `"dao"` ➔ **Khớp!**
  Điều này giải quyết triệt để vấn đề lệch hậu tố hoặc đảo họ tên (như `"Thủy Vũ"` ➔ `"vo thi thu thuy"`).

### 2. Thuật toán Sinh Username chuẩn (`[tên_chính][họ_chính]`)
```typescript
function generateStandardUsername(fullName: string): string {
  const accentFree = removeAccents(fullName);
  const cleanName = accentFree.replace(/[^a-zA-Z0-9\s]/g, '').trim();
  const parts = cleanName.split(/\s+/);
  if (parts.length === 0) return 'user';
  if (parts.length === 1) return parts[0];
  
  const firstName = parts[parts.length - 1]; // Tên chính (ví dụ: 'dao')
  const lastName = parts[0];                  // Họ chính (ví dụ: 'tran')
  return `${firstName}${lastName}`.toLowerCase();
}
```

## C. Infrastructure Layer & CLI Command Execution
* **File Command**: `backend/scripts/commands/seed-company.command.ts`
* **Flow thực thi chi tiết**:
  1. **Khởi tạo và Phân tích CSV**:
     - Đọc và phân tích `STAFF.csv` tại gốc dự án (`../STAFF.csv`).
     - Đọc và phân tích `THONG TIN NHAN VIEN.csv` tại gốc dự án (`../THONG TIN NHAN VIEN.csv`).
  2. **Dựng Cây Phòng Ban `org_units` đa tầng**:
     - Đăng ký hoặc lấy `BOD` (Khối Giám đốc, type: `'BOD'`, code: `'BOD'`).
     - Đăng ký hoặc lấy `DỊCH VỤ KHÁCH HÀNG` (Phòng ban chính, type: `'DEPARTMENT'`, code: `'DIV_CS'`).
     - Đọc các dòng định dạng `TEAM XX` trong `STAFF.csv` để tự động tạo các nhóm nghiệp vụ (type: `'TEAM'`, parent: `DIV_CS`).
     - Cập nhật trường `path` tương ứng cho mỗi phòng ban/team để tối ưu hóa truy vấn cây.
  3. **Duyệt qua danh sách nhân sự của `STAFF.csv`**:
     - Bỏ qua các dòng tiêu đề, dòng trống, hoặc dòng phân nhóm `TEAM XX`.
     - So khớp tên rút gọn từ `STAFF.csv` với tên đầy đủ từ `THONG TIN NHAN VIEN.csv` để lấy 100% dữ liệu hành chính chi tiết.
     - **Sinh Username chuẩn**: áp dụng thuật toán `generateStandardUsername` (ví dụ: `daotran`, `siluu`, `thuynguyen`).
     - **Sinh email**: `[username]@stax.dev` (hoặc dùng email thật nếu khớp được trong tệp hành chính chi tiết).
     - **Xác định Cấp bậc & Chức danh**:
       - `"Tổng Giám đốc"` ➔ Cấp bậc 2, Vai trò RBAC: `'ADMIN'`.
       - `"Giám đốc"` ➔ Cấp bậc 3, Vai trò RBAC: `'MANAGER'`.
       - `"Chuyên viên B2 / B1"` ➔ Cấp bậc 8, Vai trò RBAC: `'SPECIALIST'`.
       - `"Trợ lý A1 / A2 / A1.2"` ➔ Cấp bậc 9, Vai trò RBAC: `'ASSISTANT'`.
     - **Tạo Position**:
       - Sinh mã vị trí theo mẫu: `POS-SRV-[cấp_bậc]-[tên_vị_trí_không_dấu]` (ví dụ: `POS-SRV-9-tro-ly-a2`).
       - Nếu vị trí ghi nhận là "Tuyển mới", tạo định biên `positions` trống không có người dùng liên kết.
     - **Upsert Tài khoản `users` & `user_metadata`**:
       - Sử dụng mật khẩu mặc định được hash sẵn khớp với `"Company@2026"`: `$2b$10$owXJgdx76EwbvGiNITq7rurxUFACBnSw0JX1h9d.qviHkSQEQGSSC`.
       - **ÉP BUỘC**: Cập nhật cả `hashedPassword` cho tài khoản đã tồn tại để tránh lỗi Invalid Credentials sau khi seed lại.
     - **Gán quyền RBAC**: map tương ứng vào bảng `user_roles` (`ADMIN`, `MANAGER`, `SPECIALIST`, `ASSISTANT`).
     - **Upsert hồ sơ `employees`**: đắp toàn bộ dữ liệu hành chính chi tiết vào `metadata` JSONB.

## D. Exit Verification
- CLI chạy hoàn thành không phát sinh lỗi ngoại lệ.
- Toàn bộ nhân viên được phân cấp đúng phòng ban và TEAM con.
- TypeScript biên dịch thành công 100% (`npx tsc --noEmit` pass).
