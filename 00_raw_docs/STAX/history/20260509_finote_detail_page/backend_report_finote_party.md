# Báo cáo Yêu cầu API: Bổ sung thông tin Đối tượng liên quan trong Finote

**Vấn đề**: Giao diện danh sách Phiếu Thu/Chi (Finotes) hiện đang hiển thị tất cả các đối tượng dưới dạng **Cá nhân** (Icon User) và tên là **"Khách hàng lẻ"**. Nguyên nhân là do API `GET /accounting/finotes` hiện không trả về thông tin tên và loại hình của Tổ chức/Cá nhân liên quan (`sourceOrgId`).

**Yêu cầu thay đổi Backend**:

1. **FinoteResponseDto**: Bổ sung các trường sau:
   - `organizationName?: string`: Tên của tổ chức/khách hàng.
   - `organizationType?: 'INDIVIDUAL' | 'ENTERPRISE'`: Loại hình đối tượng để hiển thị Icon tương ứng.

2. **DrizzleFinoteRepository**: Cập nhật phương thức `findAll` để thực hiện `leftJoin` với bảng `organizations`.

3. **FinoteResponseDto.fromDomain**: Cập nhật mapper để điền thông tin từ bảng `organizations` vào DTO trả về.

**Ví dụ dữ liệu mong muốn**:
```json
{
  "id": 1,
  "code": "INC-2026-0001",
  "organizationName": "Công ty TNHH STAX",
  "organizationType": "ENTERPRISE", 
  ...
}
```
