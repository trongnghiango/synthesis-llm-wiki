# Corporate & Specialized RBAC Seeder Walkthrough

Chúng ta đã hoàn thành triển khai và kiểm thử thành công lệnh CLI `seed:company` đồng bộ hóa toàn bộ nhân sự thật và phân quyền dựa trên sơ đồ chức vụ.

## A. Chi tiết Triển khai (Implementation Details)

1. **Vô hiệu hóa Seeder cũ khi Boot:** `RUN_SEEDS=false` được đảm bảo để tối ưu hóa thời gian khởi động của NestJS, chuyển toàn bộ trách nhiệm đổ dữ liệu sang CLI.
2. **Bộ Parser CSV theo Chỉ số (Index-based Mapping):** Để tránh việc mất mát hoặc sai lệch thông tin do cấu trúc cột kép/trùng lặp (ngày bắt đầu/kết thúc, thông tin CCCD, bảo hiểm, ngân hàng, gia đình), bộ parser đã chuyển đổi sang ánh xạ chỉ số mảng cố định (`row[index]`), thu được 100% dữ liệu hành chính chi tiết của 16 nhân sự thật.
3. **Cấp phát Quyền và Vai trò Chuyên biệt:**
   - Tạo mới các vai trò chuyên môn (`ADMIN`, `SPECIALIST`, `ASSISTANT`) cùng `MANAGER`, `STAFF` và `SUPER_ADMIN`.
   - Sao chép kế thừa quyền tự động (`SUPER_ADMIN` -> `ADMIN`, `STAFF` -> `SPECIALIST`, `STAFF` -> `ASSISTANT`) để đảm bảo các tài khoản hoạt động có đầy đủ đặc quyền tương thích ngay lập tức.
4. **Cơ cấu phòng ban & Ma trận định biên (Positions):**
   - Đăng ký tự động phòng ban `"P. DỊCH VỤ"` và cập nhật đường dẫn cây (`path`).
   - Trích xuất tự động `locations` (HCM), `grades` (Bậc 2, 5, 8, 9) và `job_titles` (Tổng Giám đốc, Quản lý bộ phận, Chuyên viên B1/B2, Trợ lý A1/A2).
   - Thiết lập `positions` định biên liên kết phòng ban - chức danh - cấp bậc với headcount limit an toàn.
5. **Logic Đồng bộ An toàn (Non-destructive Smart Upsert):**
   - Định danh `employees` bằng `employeeCode`. Nếu đã tồn tại, giữ nguyên `userId`, `username`, và `email` để tránh làm hỏng các phiên làm việc và bảo mật.
   - Nếu chưa tồn tại, sinh `username` và `email` độc bản thông qua kiểm tra xung đột cơ sở dữ liệu (`username`, `username2`, `username3`...).
   - Lưu trữ 100% thông tin hành chính hành chính sâu (CCCD, địa chỉ thường trú/tạm trú, BHXH, tài khoản ngân hàng, thông tin người thân) vào cột `metadata` JSONB.

## B. Nhật ký Thực thi CLI (CLI Execution Output)

```bash
> npm run db:seed:company

⏳ Bắt đầu thực thi lệnh seed:company...
🏢 Đang khởi tạo Master Organization (STAX)...
 - Master Organization exists: STAX ENTERPRISE (ID: 1)
🛡️ Đang gieo các quy tắc phân quyền RBAC (01_rbac_rules.csv)...
 - Đã nạp thành công 7 nhóm vai trò RBAC.
🔄 Đang đồng bộ hóa quyền chuyên biệt cho ADMIN, SPECIALIST, ASSISTANT...
🌳 Đang tạo phòng ban "P. DỊCH VỤ"...
 - Đã tạo mới phòng ban P. DỊCH VỤ (ID: 1723)
📝 Đang đọc và phân tích tệp THONG TIN NHAN VIEN.csv tại root...
 - Đã nhận diện được 16 dòng nhân sự mẫu.
👑 Đang khôi phục tài khoản quản trị tối cao superadmin...
 - Đã gán quyền SUPER_ADMIN tối cao thành công!

🎉 HOÀN THÀNH SEED DOANH NGHIỆP THÀNH CÔNG!
 - Đã đồng bộ nhân sự thực tế: 16
 - Tổng số người dùng hoạt động trong DB: 22
 - Tổng số hồ sơ nhân sự trong DB: 31
```

## C. Dữ liệu Mẫu Thực tế trong DB sau khi Đồng bộ

Truy vấn kiểm tra thông tin chi tiết của nhân viên `Lưu Tiến Sĩ` (Quản lý) trong PostgreSQL:

```json
{
  "id": 56,
  "organizationId": 1,
  "userId": 66,
  "employeeCode": "052090004685",
  "fullName": "Lưu Tiến Sĩ",
  "dateOfBirth": "1990-10-20",
  "phoneNumber": "0772455899",
  "avatarUrl": null,
  "locationId": 2,
  "positionId": 26,
  "managerId": null,
  "status": "ACTIVE",
  "joinDate": "2025-04-01",
  "metadata": {
    "bank": {
      "bankName": "MB",
      "accountNumber": "0772455899"
    },
    "gender": "Nam",
    "idCard": {
      "number": "052090004685",
      "issueDate": "2021-06-28",
      "issuePlace": "Cục Trưởng Cục Cảnh Sát Quản Lý Hành Chính Về Trật Tự Xã Hội"
    },
    "taxCode": null,
    "insurance": {
      "hospital": "Bệnh viện đa khoa khu vực Thủ Đức \n(MÃ 79036)",
      "bookNumber": "7915235594"
    },
    "maritalStatus": "Đã lập gia đình",
    "emergencyContact": {
      "fullName": null,
      "phoneNumber": null,
      "relationship": null
    },
    "permanentAddress": "Thôn Bình Nghi 2, Xã Tây Sơn, Tỉnh Gia Lai",
    "temporaryAddress": null
  },
  "remarks": "CCCD cấp ngày 6/28/2021 tại Cục Trưởng Cục Cảnh Sát Quản Lý Hành Chính Về Trật Tự Xã Hội",
  "createdAt": "2026-05-22T19:26:59.769Z",
  "updatedAt": "2026-05-22T19:26:59.769Z"
}
```

## D. Kết quả Chạy Unit Test Suite

Toàn bộ 46 test suite với 234 test case của hệ thống đều vượt qua 100% thành công, không phát sinh bất kỳ lỗi runtime nào:

```text
Test Suites: 46 passed, 46 total
Tests:       234 passed, 234 total
Snapshots:   0 total
Time:        201.409 s, estimated 214 s
Ran all test suites.
```
