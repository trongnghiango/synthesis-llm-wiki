# Walkthrough & Verification — Company & RBAC Seeder Upgrade

Chúng ta đã hoàn thành triển khai và kiểm thử thành công hệ thống Seeder Doanh nghiệp & RBAC nâng cấp theo cơ cấu tệp [STAFF.csv](STAFF.csv) kết hợp.

## A. Chi tiết Triển khai (Implementation Details)
1. **Dựng Cây Phòng Ban Đa tầng (Multi-level Tree)**:
   - Tạo khối `BOD` (Ban Giám đốc) độc lập và phòng `DỊCH VỤ KHÁCH HÀNG` (DIV_CS).
   - Tự động quét và phát hiện các nhóm `TEAM 01` .. `TEAM 04` để đăng ký làm nút con của `DỊCH VỤ KHÁCH HÀNG`.
   - Đồng bộ trường `path` theo sơ đồ cây B-Tree phân tầng.
2. **Quy tắc Khớp nối Nhân sự (Fuzzy Suffix Matching)**:
   - Lược bỏ dấu tiếng Việt và chuẩn hóa ký tự tiếng Anh thường cho cả hai nguồn dữ liệu.
   - So khớp tất cả từ tố của tên rút gọn trong `STAFF.csv` để đối chiếu chính xác sang họ tên đầy đủ trong `THONG TIN NHAN VIEN.csv` (xử lý hoàn hảo các trường hợp rút gọn tên hoặc đổi họ/tên như "Thủy Vũ" ➔ "Võ Thị Thu Thủy").
3. **Sinh Username theo chuẩn định dạng**:
   - Username được sinh tự động theo mẫu `[tên_chính][họ_chính]` viết liền không dấu (ví dụ: `daotran`, `siluu`, `thuynguyen`, `duyenvo`, `thuyvo`).
4. **Bảo toàn và Tự động hóa Mật khẩu**:
   - Mật khẩu mặc định hash sẵn khớp với `Company@2026` cho cả tài khoản cũ và tài khoản mới, giải quyết triệt để lỗi "Invalid credentials" khi đăng nhập.

## B. Nhật ký Thực thi CLI thực tế
```bash
> npm run db:seed:company

⏳ Bắt đầu thực thi lệnh seed:company...
🏢 Đang khởi tạo Master Organization (STAX)...
 - Master Organization exists: STAX ENTERPRISE (ID: 1)
🛡️ Đang gieo các quy tắc phân quyền RBAC (01_rbac_rules.csv)...
 - Đã nạp thành công 7 nhóm vai trò RBAC.
🔄 Đang đồng bộ hóa quyền chuyên biệt cho ADMIN, SPECIALIST, ASSISTANT...
📝 Đang đọc và phân tích tệp THONG TIN NHAN VIEN.csv làm nguồn phụ trợ...
📝 Đang đọc và phân tích tệp cơ cấu tổ chức STAFF.csv...
 - Đã nhận diện được 18 dòng cơ cấu.
🌳 Đang khởi tạo các đơn vị phòng ban cơ sở...
 - Đã đăng ký tổ chức TEAM mới: TEAM 01 (ID: 1725)
 - Đã đăng ký tổ chức TEAM mới: TEAM 02 (ID: 1726)
 - Đã đăng ký tổ chức TEAM mới: TEAM 03 (ID: 1727)
 - Đã đăng ký tổ chức TEAM mới: TEAM 04 (ID: 1728)
👑 Đang khôi phục tài khoản quản trị tối cao superadmin...
 - Đã gán quyền SUPER_ADMIN tối cao thành công!

🎉 HOÀN THÀNH SEED DOANH NGHIỆP THÀNH CÔNG!
 - Đã đồng bộ nhân sự thực tế: 8
 - Đã thiết lập số vị trí định biên: 10
 - Tổng số người dùng hoạt động trong DB: 14
 - Tổng số hồ sơ nhân sự trong DB: 23
```

## C. Exit Verification Results
* **npm run build**: ✅ 0 errors
* **Domain purity check**: ✅ Clean (chỉ dùng kiểu dữ liệu thuần túy)
* **Tenant isolation check**: ✅ Toàn bộ truy vấn được cô lập theo `organizationId = 1`
* **Mật khẩu & Phân quyền**: ✅ Đăng nhập thành công với mật khẩu mới `Company@2026`
