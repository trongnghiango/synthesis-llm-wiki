# Phân tích Logic: Truy vấn đệ quy và Tổng hợp dữ liệu Org Structure

## 1. Nguyên tắc "Chân lý đơn nhất" (Single Point of Truth)
- **Vị trí (Position)**: Chỉ được gắn vào **duy nhất một ID** đơn vị (`orgUnitId`).
- **Nhân sự (Employee)**: Chỉ được gắn vào **duy nhất một vị trí** (`positionId`) tại một thời điểm.

## 2. Cơ chế đường dẫn (Path-based Mechanism)
Cột `path` trong bảng `org_units` lưu trữ toàn bộ phả hệ của một đơn vị.
- *Ví dụ*: Đơn vị "Nhóm Kế toán" (ID 530) là con của "Khối Tài chính" (ID 526).
- `path` của 526: `/526/`
- `path` của 530: `/526/530/`

### A. Truy vấn trực tiếp (Direct Query)
Lấy dữ liệu thuộc về chính đơn vị đó.
- SQL: `SELECT * FROM positions WHERE org_unit_id = 530`
- Kết quả: Chỉ những chức danh nằm trực tiếp trong Nhóm Kế toán.

### B. Truy vấn tổng hợp (Recursive/Aggregated Query)
Lấy dữ liệu của đơn vị đó VÀ tất cả các đơn vị con bên dưới nó.
- Logic: Tìm tất cả đơn vị có `path` bắt đầu bằng `path` của ông cha.
- SQL: `SELECT p.* FROM positions p JOIN org_units u ON p.org_unit_id = u.id WHERE u.path LIKE '/526/%'`
- Kết quả: Tất cả chức danh thuộc Khối Tài chính, Nhóm Kế toán, Nhóm Thuế...

## 3. Ứng dụng vào Giao diện (UI UX)
- **Org Chart Node**: Hiển thị 2 loại số liệu:
    1. **Direct Count**: Số nhân sự làm việc tại văn phòng/ban quản lý cấp đó.
    2. **Total Count**: Tổng quy mô nhân sự của toàn bộ nhánh cây bên dưới.
- **Staffing Board**: Hiển thị theo từng cột (Direct) để tránh trùng lặp dữ liệu khi nhìn tổng thể.
