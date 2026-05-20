# 03 Walkthrough: Architecture v1 Adoption (Phase 0)

Giai đoạn 0 đã hoàn tất, thiết lập nền móng cho kiến trúc chuẩn hóa và quy trình làm việc mới.

## Các thay đổi quan trọng

### 1. Quy trình làm việc (CONTRIBUTING_WORKFLOW.md)
- Đã chính thức hóa quy trình quản lý bối cảnh. 
- Mọi công việc hiện tại được lưu trữ tại `docs/STAX/context/20260505_architecture_v1_adoption/`.

### 2. Chuẩn hóa RBAC
- Đã sửa đổi `database/seeds/01_rbac_rules.csv`.
- Các resource cũ (`lead`, `finote`, `employee`) đã được quy hoạch vào các domain mới (`crm`, `accounting`, `hrm`) theo chuẩn `domain:action`.

### 3. Nâng cấp API Bootstrap
- `BootstrapService` giờ đây trả về:
  - `permissions.raw`: Mảng string các quyền (VD: `crm:read`).
  - `permissions.flags`: Các cờ boolean hỗ trợ UI.
- Đã thêm unit test tại `bootstrap.service.spec.ts` để bảo vệ cấu trúc này.

### 4. Tài liệu bối cảnh
- `architecture.md` đã được cập nhật Section 9 để ghi nhận Backend là "Domain Service".
- `changelog.md` đã cập nhật lộ trình mới.

## Hướng dẫn kiểm tra
- Chạy `npm run test src/modules/system/application/services/bootstrap.service.spec.ts`.
- Kiểm tra file `01_rbac_rules.csv` để thấy sự thay đổi về Resource naming.
