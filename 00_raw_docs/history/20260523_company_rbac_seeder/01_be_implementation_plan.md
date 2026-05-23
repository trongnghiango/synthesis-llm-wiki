# Detailed Architectural Implementation Plan: Corporate & Specialized RBAC Seeder

## A. Database Schema & Dependency Mapping
Không tạo thêm bảng dữ liệu mới. Thay vào đó, seeder sẽ tự động insert dữ liệu tuần tự tôn trọng các ràng buộc khóa ngoại (Foreign Key Constraints) sau:
1. **Bảng `organizations`:** Tạo Tổ chức STAX (Master).
2. **Bảng `permissions` và `roles`:** Tạo 4 nhóm vai trò (`ADMIN`, `MANAGER`, `SPECIALIST`, `ASSISTANT`) cùng danh sách phân quyền.
3. **Bảng `role_permissions`:** Thiết lập ma trận quyền của từng vai trò.
4. **Bảng `org_units`:** Tạo bộ phận `"P. DỊCH VỤ"` có parent là Tổ chức Master.
5. **Bảng `locations`, `grades`, và `job_titles`:** Đồng bộ từ dữ liệu CSV.
6. **Bảng `positions`:** Khởi tạo ma trận chức danh-phòng ban-cấp bậc.
7. **Bảng `users` và `user_metadata`:** Tạo tài khoản người dùng, tự động chuyển đổi Tình trạng sang trạng thái kích hoạt tài khoản (`isActive`).
8. **Bảng `employees`:** Nạp đầy đủ thông tin cá nhân cực kỳ chi tiết của 33 nhân sự.
9. **Bảng `user_roles`:** Cấp phát vai trò cho người dùng.

---

## B. Mapping Logic for Vietnamese Column Names (CSV to DB)
Do tệp [THONG TIN NHAN VIEN.csv](THONG TIN NHAN VIEN.csv) chứa tiêu đề cột tiếng Việt có BOM và dấu cách thừa, chúng ta sẽ viết mapper để trích xuất chuẩn xác:
- **HỌ VÀ TÊN** -> `fullName`
- **MÃ SỐ NV** -> `employeeCode`
- **PHÒNG BAN** -> `departmentName`
- **CHỨC VỤ** -> `positionName`
- **Địa điềm làm việc** -> `locationCode`
- **TÌNH TRẠNG LÀM VIỆC** -> `status` ("Working" -> ACTIVE, "Left" -> RESIGNED)
- **THỜI GIAN LÀM VIỆC (Ngày bắt đầu)** -> `joinDate`
- **SDT CÁ NHÂN** -> `phoneNumber`
- **EMAIL** -> `email`
- **GIỚI TÍNH** -> `gender`
- **TÌNH TRẠNG HÔN NHÂN** -> `maritalStatus`
- **NGÀY SINH** -> `dateOfBirth`
- **ĐỊA CHỈ THƯỜNG TRÚ** -> `permanentAddress`
- **ĐỊA CHỈ TẠM TRÚ** -> `temporaryAddress`
- **Số CCCD** / **ngày cấp** / **nơi cấp** -> Lưu vào `metadata` hoặc `remarks`
- **Số tài khoản** / **Ngân hàng** -> Lưu vào `metadata` hoặc `remarks`
- **Thành viên gia đình** -> Lưu vào `metadata` hoặc `remarks`

---

## C. Implementation Plan for `seed-company.command.ts`

Chúng ta sẽ tạo file lệnh mới: `backend/scripts/commands/seed-company.command.ts`.
File này sẽ:
1. Đọc tệp CSV bằng `csv-parse/sync`.
2. Khởi tạo và liên kết các thực thể.
3. Tự động sinh `username` từ `fullName` (Ví dụ: "Nguyễn Thị Thu Thủy" -> "thuynguyen" hoặc "nguyenthithuthuy").
4. Mã hóa password mặc định là `K@2026` hoặc `Company@2026` bằng cách sử dụng mock hashed password đã sinh sẵn để tăng tốc độ.
5. In ra báo cáo tiến độ chi tiết dạng log trực quan.

---

Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist (Bước 3).
