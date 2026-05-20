# 🏛️ TÀI LIỆU KIẾN TRÚC: MÔ HÌNH BẢO MẬT LAI THỰC DỤNG (PRAGMATIC HYBRID SECURITY)
**Cấp độ:** Cốt lõi hệ thống (Core Architecture Standard)
**Nguyên tắc:** RBAC Guard + SQL Filtering + DTO `_actions`

---

## 1. TẠI SAO PHẢI DÙNG MÔ HÌNH LAI (HYBRID)?

Trong các hệ thống ERP/CRM phức tạp như STAX, việc chỉ dùng RBAC (Role-based) hay ABAC (Attribute-based) đơn thuần đều dẫn đến thất bại:
*   **Chỉ dùng RBAC:** Dẫn đến bùng nổ vai trò (Role Explosion). Bạn không thể tạo ra hàng ngàn Role như `SỬA_LEAD_MIỀN_BẮC`, `SỬA_LEAD_MIỀN_NAM`.
*   **Chỉ dùng ABAC:** Dẫn đến thảm họa hiệu năng (N+1 Query). DB không thể lọc nhanh nếu logic quyền hạn nằm ở một cỗ máy Policy độc lập trên RAM.

**Giải pháp của STAX:** Kết hợp sức mạnh của 3 lớp bảo vệ để tối ưu cả **Bảo mật - Hiệu năng - Độ linh hoạt**.

---

## 2. CẤU TRÚC 3 LỚP (THE 3-LAYER DEFENSE)

Đây là "Kiến trúc Vàng" mà STAX áp dụng trên toàn bộ hệ thống:

### 🛡️ Lớp 1: Cổng bảo vệ (RBAC Guard)
*   **Vị trí:** Controller / API Gateway.
*   **Công cụ:** Decorators như `@Permissions('crm:leads:edit')`.
*   **Tác dụng (Lọc thô):** Trả lời câu hỏi: *"Bạn có chìa khóa để vào tòa nhà này không?"*. Nếu User không có quyền cơ bản, hệ thống đá văng ngay (403 Forbidden) mà không cần truy vấn Database. Cực nhanh và an toàn.

### 🔍 Lớp 2: Lọc dữ liệu (Data-Level Security/SQL Filter)
*   **Vị trí:** Repository (Drizzle ORM / SQL Level).
*   **Công cũ:** Mệnh đề `WHERE` tự động gắn kèm `organization_id` hoặc `department_path`.
*   **Tác dụng (Lọc sâu):** Trả lời câu hỏi: *"Trong hàng triệu bản ghi, cái nào thuộc quyền sở hữu của doanh nghiệp bạn?"*. 
    *   Việc lọc này diễn ra trực tiếp tại Database bằng Index. 
    *   Đảm bảo User chỉ lấy lên RAM đúng những data họ được phép thấy. 
    *   Ngăn chặn hoàn toàn việc rò rỉ dữ liệu giữa các Tenant (SaaS Isolation).

### ⚡ Lớp 3: Điều khiển tương tác (Lightweight ABAC via DTO `_actions`)
*   **Vị trí:** Tầng Application Service / Response DTO Mapper.
*   **Công cụ:** Pattern `_actions` trong các Object trả về.
*   **Tác dụng (Lọc tinh):** Trả lời câu hỏi chi tiết nhất: *"Bản ghi này đang ở trạng thái WON, bạn có được bấm nút SỬA không?"*.
    *   Logic kiểm tra trạng thái (`isClosed`, `isOwner`) được đặt trong DTO.
    *   Kết quả trả về cho Frontend là các tín hiệu `allow: true/false` kèm lý do `reason`.
    *   **Backend-Driven UI:** Frontend chỉ việc "nhắm mắt" làm theo lệnh Backend trả về để hiện/ẩn nút bấm.

---

## 3. CÁCH TRIỂN KHAI THỰC CHIẾN

### Bước 1: Định nghĩa logic DTO (Mẫu chuẩn)
Thay vì dùng Policy Engine cồng kềnh, ta dùng các helper function đơn giản ngay trong DTO của module.

```typescript
// lead-action.util.ts
export const calculateLeadActions = (user, lead) => {
  return {
    edit: {
      allowed: lead.stage !== 'WON' && (user.id === lead.ownerId || user.role === 'ADMIN'),
      reason: lead.stage === 'WON' ? 'Hợp đồng đã chốt, không thể sửa' : 'Bạn không phụ trách khách hàng này'
    },
    delete: {
      allowed: user.role === 'ADMIN',
      reason: 'Chỉ Admin mới có quyền xóa dữ liệu lõi'
    }
  };
};
```

### Bước 2: Nhúng vào Response
Trong Service/Controller, sau khi lấy dữ liệu, ta "map" thêm field `_actions`.

```typescript
// lead.service.ts
async getDetail(id, currentUser) {
  const lead = await this.repo.findById(id); // Đã qua Lớp 2 (SQL Filter)
  return {
    ...lead,
    _actions: calculateLeadActions(currentUser, lead) // Lớp 3 (Lightweight ABAC)
  };
}
```

---

## 4. TẠI SAO ĐÂY LÀ BEST PRACTICE?

1.  **Clean Code:** Logic quyền hạn không bị vấy bẩn vào Business Service. Nó nằm riêng ở DTO và Guard.
2.  **Hiệu năng tuyệt đối:** Không có độ trễ của Policy Engine. Mọi thứ là logic so sánh cơ bản trên RAM sau khi đã lọc dữ liệu tinh gọn từ DB.
3.  **Trải nghiệm người dùng:** Frontend luôn biết chính xác tại sao một nút bấm bị khóa nhờ field `reason` từ Backend.
4.  **Dễ bảo trì:** Khi Sếp thay đổi luật: *"Lead trên 1 tỷ chỉ Admin được xóa"*, bạn chỉ cần vào duy nhất 1 file `calculateActions` để sửa.

---

## 5. KHI NÀO CẦN NÂNG CẤP LÊN POLICY ENGINE ĐỘC LẬP?

Chúng ta **CHỈ** nâng cấp khi hệ thống cho phép **Người dùng cuối (End-user)** tự vào màn hình Cài đặt để tự định nghĩa các luật (Custom Rules) như Salesforce hay Jira. 

Với mọi kịch bản ERP/CRM thông thường, mô hình **3 Lớp Lai** này là **KIẾN TRÚC VÀNG**.

---
*Tài liệu được cập nhật ngày 03/05/2026 dựa trên tư duy kiến trúc STAX đột phá.*