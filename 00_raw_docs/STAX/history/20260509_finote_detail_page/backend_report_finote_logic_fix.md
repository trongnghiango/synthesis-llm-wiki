# Báo cáo Lỗi Logic Backend: Nhầm lẫn giữa Chủ thể (Owner) và Đối tượng (Partner) trong Finote

**Vấn đề**: Hiện tại, bảng `finotes` đang sử dụng trường `sourceOrgId` để lưu trữ **Chủ thể sở hữu phiếu** (Tenancy - ví dụ: STAX ENTERPRISE). Khi Backend thực hiện JOIN với bảng `organizations` qua trường này, kết quả trả về luôn là thông ty chủ quản.

**Để hiển thị đúng "Đối tượng" (Người nộp/Người nhận), hệ thống cần phân biệt rõ**:

1. **Chủ thể (Owner/Tenant)**: Là STAX (đã có trường `sourceOrgId`).
2. **Đối tượng (Partner/Related Party)**: Là Khách hàng/Nhà cung cấp. **Trường này đang thiếu trong Schema.**

**Đề xuất giải pháp cho Backend**:

1. **Cập nhật Schema (`finotes.schema.ts`)**: 
   - Bổ sung trường `partnerOrgId: bigint` (hoặc `clientId`) để lưu trữ ID của đối tượng liên quan.
2. **Cập nhật Service (`finote.service.ts`)**:
   - Khi tạo Finote từ Lead/Contract, hãy gán `lead.organizationId` vào trường `partnerOrgId` mới này.
3. **Cập nhật Repository**:
   - Thực hiện `leftJoin` bảng `organizations` qua trường `partnerOrgId` (thay vì `sourceOrgId`) để lấy tên đối tượng.
4. **Cập nhật DTO**:
   - Trả về `organizationName` và `organizationType` của **Partner** chứ không phải của **Owner**.

**Hệ quả hiện tại**: Nếu không có trường `partnerOrgId`, chúng ta sẽ không thể biết phiếu thu này là thu của ai, phiếu chi này là chi cho ai ở cấp độ dữ liệu.
