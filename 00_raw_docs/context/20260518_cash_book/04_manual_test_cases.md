# Kịch bản Kiểm thử Thủ công (Manual Test Cases) — Phân hệ Sổ Quỹ STAX

Tài liệu này hướng dẫn chi tiết từng bước kiểm thử thủ công (manual test cases) toàn bộ luồng nghiệp vụ **Sổ Quỹ (Cash Book)** dòng tiền thực tế tại cả Frontend và Backend.

---

## 🛠️ Trạng thái & Chuẩn bị (Pre-conditions)
1.  **Backend & Frontend đang chạy:**
    *   Backend NestJS đang chạy cổng mặc định.
    *   Frontend Client đang chạy (thường là `http://localhost:5173`).
2.  **Tài khoản đăng nhập:** Tài khoản Admin hoặc Kế toán có đầy đủ quyền thao tác trong phân hệ `Accounting`.

---

## 📋 Danh sách các Kịch bản Kiểm thử (Test Cases)

### 🧪 Test Case 01: Khởi tạo Dữ liệu Tự động & Giao diện Bento Grid
*   **Mục tiêu:** Kiểm tra khả năng tự động tạo Quỹ mặc định cho tổ chức và hiển thị Bento Grid trực quan.
*   **Các bước thực hiện:**
    1.  Đăng nhập vào hệ thống STAX -> Click mục **Sổ Quỹ (Cash Book)** trên thanh Sidebar trái.
    2.  Quan sát màn hình chính ở chế độ **Modern (Bento Grid)**.
*   **Kết quả kỳ vọng (Expected Results):**
    *   [ ] Xuất hiện 3 thẻ thống kê Bento ở trên cùng: **Tổng số dư dòng tiền** (màu xanh lá gradient), **Tiền mặt thực tế** (màu xanh dương) và **Tiền gửi ngân hàng** (màu chàm).
    *   [ ] Hệ thống seeder tự động kích hoạt tạo ngay 1 Quỹ mặc định có tên: **Tiền mặt mặc định** (hoặc tương tự) với Badge **Default** lấp lánh (nếu tổ chức chưa có quỹ nào).
    *   [ ] Số dư của quỹ mặc định phản ánh chính xác tổng số tiền từ các giao dịch thu/chi lịch sử (nếu có).

---

### 🧪 Test Case 02: Tạo Sổ Quỹ Mới (Tiền mặt / Tài khoản Ngân hàng)
*   **Mục tiêu:** Kiểm tra Dialog thêm quỹ mới và logic hiển thị động các trường dữ liệu.
*   **Các bước thực hiện:**
    1.  Tại trang Sổ Quỹ, click nút **Tạo Sổ Quỹ** (nút màu xanh lá góc trên bên phải).
    2.  **Thử nghiệm 1 (Lỗi Validation):** Để trống trường *Tên Sổ Quỹ* -> Click *Xác nhận*.
    3.  **Thử nghiệm 2 (Quỹ Tiền mặt):** 
        *   Nhập tên: `Quỹ tiền mặt văn phòng`.
        *   Chọn Loại: `Tiền mặt (Cash)`.
        *   Click *Xác nhận*.
    4.  **Thử nghiệm 3 (Quỹ Ngân hàng):**
        *   Click lại nút *Tạo Sổ Quỹ*.
        *   Nhập tên: `Tài khoản ACB công ty`.
        *   Chọn Loại: `Tài khoản Ngân hàng (Bank Account)`.
        *   *Quan sát màn hình: Trường "Số tài khoản / Số Ví" xuất hiện.*
        *   Nhập Số tài khoản: `190288888`.
        *   Click *Xác nhận*.
*   **Kết quả kỳ vọng (Expected Results):**
    *   [ ] Ở Thử nghiệm 1: Form báo lỗi đỏ *"Tên quỹ không được để trống"* và chặn submit.
    *   [ ] Ở Thử nghiệm 2: Quỹ tiền mặt mới xuất hiện trên Bento Grid với số dư ban đầu là `0 ₫`.
    *   [ ] Ở Thử nghiệm 3: Trường số tài khoản hiển thị mượt mà. Quỹ ACB xuất hiện trên Bento Grid, hiển thị rõ số tài khoản ngân hàng bên dưới tên quỹ.

---

### 🧪 Test Case 03: Thiết lập Sổ Quỹ Mặc định (Set Default Fund)
*   **Mục tiêu:** Kiểm tra khả năng đổi quỹ mặc định hệ thống.
*   **Các bước thực hiện:**
    1.  Tại Bento Grid, tìm thẻ quỹ vừa tạo `Tài khoản ACB công ty` (hiện tại chưa có badge Default).
    2.  Click nút **Thiết lập mặc định** ở góc dưới thẻ quỹ.
*   **Kết quả kỳ vọng (Expected Results):**
    *   [ ] Thẻ quỹ ACB lập tức nhận Badge **Default** lấp lánh màu xanh lá.
    *   [ ] Thẻ quỹ cũ mất Badge Default và xuất hiện lại nút *Thiết lập mặc định*.
    *   [ ] Hiển thị Toast thông báo thành công ở góc phải màn hình.

---

### 🧪 Test Case 04: Chuyển Tiền Nội Bộ & Kiểm Soát Số Dư Real-time
*   **Mục tiêu:** Xác nhận logic chuyển tiền nguyên tử và ngăn chặn giao dịch âm quỹ.
*   **Các bước thực hiện:**
    1.  Click nút **Chuyển tiền nội bộ** (nút màu xanh dương góc trên bên phải).
    2.  **Thử nghiệm 1 (Chặn Âm Quỹ):**
        *   Chọn Quỹ gửi: `Tài khoản ACB công ty` (hiện tại số dư đang là `0 ₫`).
        *   Chọn Quỹ nhận: `Quỹ tiền mặt văn phòng`.
        *   Nhập số tiền chuyển: `1.000.000` (1 triệu VND).
        *   Click *Xác nhận*.
    3.  **Thử nghiệm 2 (Chuyển khoản thành công):**
        *   Chọn Quỹ gửi: Quỹ mặc định ban đầu (quỹ có số dư dương lớn hơn 500.000 ₫).
        *   Chọn Quỹ nhận: `Tài khoản ACB công ty`.
        *   Nhập số tiền chuyển: `500.000` (5 trăm nghìn VND).
        *   Nhập mô tả: `Rút tiền ACB nạp quỹ`.
        *   Click *Xác nhận*.
*   **Kết quả kỳ vọng (Expected Results):**
    *   [ ] Ở Thử nghiệm 1: Form báo lỗi đỏ ngay tại ô Nhập tiền: *"Số tiền chuyển không được vượt quá số dư hiện có (0 ₫)"* và chặn không cho gửi lên Backend.
    *   [ ] Ở Thử nghiệm 2: Giao dịch thành công, số dư của Quỹ gửi giảm đi 500.000 ₫, số dư của Quỹ ACB tăng lên 500.000 ₫ ngay trên màn hình.
    *   [ ] Chuyển sang Tab **Classic (Ledger Ledger)** -> Xuất hiện **2 dòng giao dịch mới tinh**: 1 dòng `Chi (OUT)` từ quỹ gửi và 1 dòng `Thu (IN)` vào quỹ ACB với cùng ghi chú và số tiền.

---

### 🧪 Test Case 05: Duyệt Hóa Đơn & Tự Động Thu/Chi Quỹ dòng tiền
*   **Mục tiêu:** Kiểm tra luồng liên kết Finote -> Ghi nhận thanh toán -> Tăng/Giảm số dư Sổ quỹ.
*   **Các bước thực hiện:**
    1.  Vào Sidebar -> Click **Finotes (Phiếu thu/chi)** -> Click **Tạo Finote** (Hóa đơn).
    2.  Tạo 1 Finote loại **EXPENSE (Chi phí)**, Số tiền: `200.000 ₫`, Trạng thái: Đã duyệt.
    3.  Tại trang chi tiết Finote vừa tạo -> Click nút **Ghi nhận thanh toán**.
    4.  Tại Dialog hiện lên:
        *   **Sổ Quỹ thanh toán:** Click chọn `Tài khoản ACB công ty` (đang có 500.000 ₫).
        *   **Số tiền:** Để mặc định `200.000`.
        *   Click *Xác nhận*.
    5.  Quay trở lại trang **Sổ Quỹ (Cash Book)** để kiểm tra dòng tiền.
*   **Kết quả kỳ vọng (Expected Results):**
    *   [ ] Tại Dialog Ghi nhận thanh toán: Trường Sổ quỹ thanh toán tự động hiển thị gợi ý quỹ mặc định lên đầu.
    *   [ ] Sau khi xác nhận: Trạng thái Finote chuyển sang `PAID` (Đã thanh toán).
    *   [ ] Tại Sổ Quỹ: Số dư của `Tài khoản ACB công ty` lập tức giảm từ 500.000 ₫ xuống còn **300.000 ₫**.
    *   [ ] Tại Tab **Classic (Ledger Ledger)**: Xuất hiện dòng giao dịch `Chi (OUT)` trị giá 200.000 ₫ kèm theo ghi chú thanh toán của Finote đó.

---

### 🧪 Test Case 06: Bộ Lọc Dòng Tiền Classic Ledger
*   **Mục tiêu:** Đảm bảo khả năng tra cứu và lọc dữ liệu Sổ Nhật ký dòng tiền chính xác.
*   **Các bước thực hiện:**
    1.  Tại trang Sổ Quỹ, chuyển sang Tab **Classic (Ledger Ledger)**.
    2.  Tại Bộ lọc:
        *   *Chọn Sổ Quỹ:* Chọn riêng `Tài khoản ACB công ty`.
        *   *Từ ngày / Đến ngày:* Chọn khoảng ngày chứa giao dịch vừa thực hiện.
    3.  Click nút **Reset Bộ lọc** để đưa về trạng thái ban đầu.
*   **Kết quả kỳ vọng (Expected Results):**
    *   [ ] Bảng dữ liệu lọc chính xác chỉ hiển thị các giao dịch liên quan đến quỹ ACB (không hiển thị các quỹ khác).
    *   [ ] Khi Reset bộ lọc: Toàn bộ giao dịch của tất cả các quỹ hiển thị đầy đủ trở lại.
