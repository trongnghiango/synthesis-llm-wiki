# 03 Walkthrough: CRM Naming Migration (Stage 1 - Backend)

## 📌 Tổng quan
Đã thực hiện chuẩn hóa toàn bộ hệ thống Backend để chuyển đổi từ `companyName` sang `organizationName`. Đây là bước chuẩn bị quan trọng để đồng nhất dữ liệu với Module Leads và hỗ trợ team Frontend trong Đợt 2.

## 🛠️ Các thay đổi chính

### 1. Database & Schema
- **Rename Column**: Cột `company_name` trong bảng `organizations` đã được đổi tên thành `organization_name`.
- **Enum Expansion**: Cập nhật `lead_source` với các giá trị mới (`SOCIAL`, `ZALO`, `FACEBOOK`, ...).
- **Leads Table**: Thêm cột `contact_id` và xóa các cột thông tin liên hệ cũ (`contact_name`, `contact_email`, `contact_phone`) để chuyển sang dùng quan hệ 1-1 với bảng `contacts`.

### 2. Domain & Application Layer
- **Organization Entity**: Refactor toàn bộ thuộc tính và getter/setter.
- **Backward Compatibility**: API trả về cả `organizationName` và `companyName` (deprecated) để đảm bảo các client cũ không bị lỗi.
- **Affected Services**: 
    - `LeadIntakeService`: Cập nhật logic tạo Organization mới.
    - `IncomeTargetStrategy` (Accounting): Cập nhật hiển thị tên đối tượng.
    - `CrmLegacyMigrationService`: Cập nhật logic import dữ liệu lịch sử.

### 3. Kiểm thử (Testing)
- Đã cập nhật `test-db.helper.ts` (SQL hardcoded) để khớp với Schema mới.
- Chạy toàn bộ 32 Unit Tests của module CRM: **Tất cả đều vượt qua (100% PASS)**.

## ⚠️ Lưu ý kỹ thuật (Troubleshooting)
Trong quá trình migration, `drizzle-kit` gặp lỗi không in ra log (silent error) do xung đột giữa `ALTER TYPE` và `RENAME COLUMN`. Chúng ta đã xử lý bằng script **Manual Migration** để đảm bảo an toàn dữ liệu.

## 🔜 Bước tiếp theo
- **Đợt 2 (Frontend)**: Team Frontend có thể bắt đầu chuyển sang dùng `organizationName`.
- **Stage 2 (Backend)**: Sau khi Frontend hoàn tất, chúng ta sẽ thực hiện xóa hoàn toàn trường `companyName` khỏi DTO để làm sạch API.
