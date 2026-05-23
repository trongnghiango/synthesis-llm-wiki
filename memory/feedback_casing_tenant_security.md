---
name: feedback-casing-tenant-security
description: Ràng buộc kiểm tra hoa/thường cho Roles, loại bỏ fallback organizationId || 1 không an toàn và tích hợp applyTenantIsolation tự động ở tầng Repository.
metadata:
  type: feedback
---

Khi phát triển hoặc rà soát tính năng trên Backend NestJS của dự án STAX:
1. **Kiểm tra Casing cho Roles**: Role được lưu trữ trong CSDL và phân quyền luôn là CHỮ IN HOA (`ADMIN`, `SUPER_ADMIN`, `MANAGER`). Mọi điều kiện so sánh, bao gồm cả trong `VisibilityResolverService`, bắt buộc phải chuyển mảng `roles` về chữ in hoa (`toUpperCase()`) trước khi đối chiếu để tránh tê liệt phân quyền.
2. **Triệt tiêu Fallback `|| 1` tại Controllers**: 
   - Tuyệt đối KHÔNG sử dụng `user.organizationId || 1` cho người dùng bên ngoài (EXTERNAL) vì sẽ tự động gán họ vào Tổ chức `1` (Platform Owner - STAX), vi phạm bảo mật đa thuê.
   - Nếu `organizationId` của người dùng bên ngoài bị thiếu, bắt buộc ném `ForbiddenException` ngay từ tầng Controller.
   - Chỉ cho phép nhân sự nội bộ (`user.isInternal === true`) được phép fallback về `1` (thư mục hệ thống của STAX) đối với các tác vụ lưu trữ tệp tin.
3. **Kích hoạt `applyTenantIsolation` tự động**:
   - Các Repository kế thừa `DrizzleBaseRepository` phải tích hợp `this.applyTenantIsolation(conditions, table)` vào mệnh đề `where` thay vì lọc `orgId > 1` thủ công.
   - Cơ chế này sẽ tự động giải phóng bộ lọc nếu người dùng có `scope: 'ALL'` (Platform Owner), cho phép họ quản lý chéo khách hàng một cách an toàn.

**Why:**
- Khắc phục lỗ hổng phân quyền nghiêm trọng khóa chặt Admin khỏi hệ thống do so sánh lowercase role.
- Ngăn ngừa nguy cơ rò rỉ dữ liệu nhạy cảm của Platform Owner (STAX) cho người dùng bên ngoài thông qua fallback `|| 1` mặc định.
- Tự động hóa chốt chặn bảo mật đa thuê ở tầng dữ liệu thông qua AsyncLocalStorage (ALS), triệt tiêu rủi ro lập trình viên quên chèn điều kiện lọc thủ công.

**How to apply:**
- Áp dụng khi phân tích thiết kế hệ thống và rà soát code tại các module nghiệp vụ Tier 2 & Tier 3 (CRM, HRM, Kế toán).
