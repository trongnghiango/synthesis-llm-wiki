# BÁO CÁO KỸ THUẬT: PHÂN TÍCH GIỚI HẠN GOOGLE DRIVE API & HƯỚNG DẪN CẤU HÌNH BỘ NHỚ DÙNG CHUNG CHO DOANH NGHIỆP

> **Dự án**: Hệ thống quản trị doanh nghiệp STAX ERP
> **Nội dung**: Giải pháp lưu trữ tệp tin đính kèm Polymorphic trên Cloud Storage (Google Drive)
> **Đơn vị thực hiện**: Đội ngũ phát triển phần mềm STAX
> **Tài liệu tham khảo**: [google_drive_setup_report.md](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/docs/context/20260520_attachment_management/google_drive_setup_report.md)

---

## I. TỔNG QUAN & ĐẶT VẤN ĐỀ KỸ THUẬT

Để hệ thống phần mềm hoạt động trơn tru, bảo mật và đồng bộ dữ liệu tức thời giữa tất cả người dùng, phân hệ Quản lý tài liệu đính kèm (Attachments) của STAX ERP được thiết kế để đẩy trực tiếp toàn bộ tài liệu (Hợp đồng, Báo giá, File scan GPKD...) lên đám mây lưu trữ thông qua **Google Drive API v3**.

Tuy nhiên, theo cập nhật chính sách bảo mật và tài nguyên mới nhất của Google (áp dụng cho các ứng dụng kết nối API doanh nghiệp):
1. **Google Service Account** (tài khoản dịch vụ tự động dùng để kết nối backend) được Google cấu hình mặc định dung lượng lưu trữ là **0 Bytes**.
2. Khi hệ thống tự động tải file lên một thư mục thông thường của tài khoản `@gmail.com` cá nhân, Google Drive vẫn tính dung lượng đó vào Service Account (với tư cách là Owner - chủ sở hữu tệp tin). Do dung lượng là 0 Bytes, API sẽ lập tức chặn hành động tải lên và trả về mã lỗi:
   > `403 Forbidden / INTERNAL_SERVER_ERROR: Service Accounts do not have storage quota. Leverage shared drives...`

### 💡 Giải pháp tiêu chuẩn Doanh nghiệp:
Để giải quyết triệt để vấn đề này, đơn vị vận hành phần mềm (Khách hàng) **bắt buộc phải sử dụng tài khoản Google Workspace (G Suite của Doanh nghiệp)** và thiết lập một **Shared Drive (Bộ nhớ dùng chung)**. 
*   Bộ nhớ dùng chung (Shared Drive) thuộc sở hữu của tổ chức/doanh nghiệp chứ không thuộc cá nhân hay Service Account nào.
*   Khi Service Account tải file lên Shared Drive, dung lượng file sẽ được tính vào hạn mức chung của doanh nghiệp, giúp hệ thống hoạt động ổn định 100%.

---

## II. HƯỚNG DẪN THIẾT LẬP CHI TIẾT DÀNH CHO KHÁCH HÀNG (DOANH NGHIỆP)

Khách hàng cần cử quản trị viên hệ thống (IT Admin) thực hiện tuần tự theo các bước dưới đây và cung cấp lại tệp thông số bảo mật cho đội ngũ phát triển.

### BƯỚC 1: TẠO DỰ ÁN TRÊN GOOGLE CLOUD & BẬT GOOGLE DRIVE API

1. Truy cập vào cổng quản trị Google Cloud Console: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Đăng nhập bằng tài khoản Google Workspace của doanh nghiệp.
3. Ở thanh công cụ phía trên, bấm vào danh sách dự án và chọn **New Project (Dự án mới)**.
4. Đặt tên dự án (Ví dụ: `stax-erp-storage`) rồi bấm **Create (Tạo)**.
5. Tại thanh tìm kiếm ở đầu trang, gõ từ khóa **"Google Drive API"**.
6. Chọn dịch vụ **Google Drive API** từ kết quả tìm kiếm và bấm nút **Enable (Kích hoạt)**.

---

### BƯỚC 2: TẠO SERVICE ACCOUNT & TẢI XUỐNG FILE CREDENTIALS `.JSON`

1. Tại menu điều hướng bên trái của Google Cloud Console, chọn **IAM & Admin** > **Service Accounts (Tài khoản dịch vụ)**.
2. Bấm nút **Create Service Account** ở phía trên màn hình.
3. Điền thông tin:
   * **Service account name**: Nhập tên gợi nhớ (Ví dụ: `stax-file-uploader`).
   * **Service account ID**: Hệ thống sẽ tự động sinh mã ID dựa trên tên.
4. Bấm **Create and Continue**, sau đó bấm **Done** để hoàn tất (không cần cấu hình phân quyền ở đây).
5. Trong danh sách tài khoản dịch vụ hiển thị, click vào email của tài khoản vừa tạo.
6. Chuyển sang tab **Keys (Khóa)** ở thanh menu phía trên.
7. Bấm nút **Add Key** > chọn **Create new key (Tạo khóa mới)**.
8. Chọn định dạng khóa là **JSON** và bấm **Create**.
9. Trình duyệt sẽ tự động tải xuống một tệp tin cấu hình bảo mật có định dạng `.json` (Ví dụ: `stax-erp-storage-xxxxxx.json`).
   > ⚠️ **LƯU Ý QUAN TRỌNG**: Hãy lưu trữ tệp `.json` này ở nơi tuyệt đối an toàn. Tệp này chứa khóa bảo mật cấp quyền truy cập trực tiếp của hệ thống.

---

### BƯỚC 3: TẠO SHARED DRIVE & CẤP QUYỀN TRUY CẬP CHO SERVICE ACCOUNT

1. Truy cập vào tài khoản Google Drive của doanh nghiệp: [https://drive.google.com/](https://drive.google.com/)
2. Tại menu bên trái, tìm và chọn mục **Shared Drives (Bộ nhớ dùng chung)**.
3. Click chuột phải chọn **New Shared Drive (Bộ nhớ dùng chung mới)**, đặt tên là: `STAX_Enterprise_Attachments`.
4. Mở Shared Drive vừa tạo, bấm vào nút **Manage Members (Quản lý thành viên)** ở góc trên bên phải.
5. **Cấp quyền cho Service Account**:
   * Mở tệp tin `.json` đã tải xuống ở Bước 2.
   * Tìm đến dòng `"client_email"` và sao chép địa chỉ email của tài khoản dịch vụ (dạng: `stax-file-uploader@stax-erp-storage.iam.gserviceaccount.com`).
   * Dán email này vào phần thêm thành viên của Shared Drive.
   * Cấp quyền tối thiểu là **Contributor (Người đóng góp)** hoặc **Content Manager (Người quản lý nội dung)**.
   * Bấm **Share (Chia sẻ)** để hoàn tất.

---

### BƯỚC 4: LẤY FOLDER ID ĐỂ CẤU HÌNH

1. Click vào Shared Drive `STAX_Enterprise_Attachments` của bạn trên Google Drive.
2. Nhìn lên thanh địa chỉ của trình duyệt Web (URL), đường dẫn sẽ hiển thị có định dạng như sau:
   `https://drive.google.com/drive/u/0/folders/1l5KR3hVSWzCborFtECcCpcfsN4YrMl2Z`
3. Hãy sao chép toàn bộ chuỗi ký tự đứng sau chữ `/folders/` (Trong ví dụ trên là: `1l5KR3hVSWzCborFtECcCpcfsN4YrMl2Z`). Đây chính là **Shared Folder ID**.

---

## III. THÔNG TIN BÀN GIAO CHO ĐỘI NGŨ PHÁT TRIỂN PHẦN MỀM

Sau khi hoàn tất quá trình thiết lập ở trên, Khách hàng vui lòng xuất và cung cấp cho chúng tôi hai thông số bảo mật sau để cấu hình vào hệ thống:

1. **Tệp tin thông tin xác thực**: Gửi file khóa bảo mật dạng `.json` (được tải về từ Bước 2).
2. **Mã định danh thư mục**: Cung cấp chuỗi ký tự **Shared Folder ID** (lấy ở Bước 4).

Chúng tôi sẽ cấu hình trực tiếp các thông số này vào các biến môi trường của hệ thống:
```env
SERVICE_ACCOUNT_JSON_PATH="google-credentials.json"
GOOGLE_DRIVE_FOLDER_ID="chuoi_folder_id_nhan_duoc"
```

Đội ngũ phát triển cam kết bảo mật tuyệt đối thông tin tài khoản Cloud của quý doanh nghiệp. Hệ thống sẽ ngay lập tức được kết nối đồng bộ và vận hành an toàn!
