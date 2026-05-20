# Đề xuất Thiết kế Kỹ thuật (Technical Implementation Plan)

## A. API Contracts & Shared Schemas

Chúng ta sử dụng chính xác các Zod Schemas đã được đồng bộ hóa từ Backend sang Frontend trong contract `@shared/contracts/accounting.ts`:

1.  **Lập Phiếu thu/chi (Finote):**
    *   API Endpoint: `POST /api/accounting/finotes`
    *   Schema: `createFinoteSchema`
2.  **Lập Bút toán thủ công (Manual Journal Entry):**
    *   API Endpoint: `POST /api/accounting/journal-entries`
    *   Schema: `createJournalEntrySchema`

---

## B. Thiết kế Frontend & Components

### 1. `CreateFinoteDialog` (Tạo mới)
*   **Vị trí:** [create-finote-dialog.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/components/create-finote-dialog.tsx)
*   **Chức năng:** Form Dialog bọc bằng `@/components/ui/dialog`.
    *   Nhận prop `type: "INCOME" | "EXPENSE"` để tự cấu hình giao diện (màu sắc, icon, tiêu đề).
    *   Sử dụng `@hookform/resolvers/zod` kết hợp với `zod` để validate form cục bộ trước khi submit.
    *   Tự động đổi định dạng ngày `yyyy-MM-dd` từ ô input sang ISO 8601 string để gửi lên backend.

### 2. `FinotesPage` (Tích hợp)
*   **Vị trí:** [finotes.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/finotes.tsx)
*   **Chức năng:**
    *   Thay thế các nút bấm tĩnh bằng `<CreateFinoteDialog type="INCOME" />` và `<CreateFinoteDialog type="EXPENSE" />`.
    *   Khi tạo thành công, tự động thực hiện invalidate cache `["accounting", "finotes"]` để bảng dữ liệu cập nhật ngay lập tức.

### 3. `JournalEntriesPage` (Tích hợp)
*   **Vị trí:** [journal-entries.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/journal-entries.tsx)
*   **Chức năng:**
    *   Bọc nút `"Thêm Bút toán mới"` trong Dialog và render [JournalEntryForm](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/accounting/components/JournalEntryForm.tsx).
    *   Khai báo React Query Mutation `createMutation` gọi tới `accountingApi.createJournalEntry`.
    *   Tự động làm mới cache `journalEntries` để cập nhật bảng Nhật ký chung ngay tức khắc.

---

## C. Chiến lược Kiểm thử (Testing Strategy)

Do đây là các nâng cấp trực tiếp trên phân hệ giao diện người dùng (UI/UX Pages), chiến lược kiểm thử tập trung vào **Kiểm thử thủ công (Manual End-to-End Testing)** dựa trên kịch bản nghiệp vụ thực tế của một Kế toán viên:
1.  **Luồng tự động:** Lập phiếu chi -> Phê duyệt chi -> Ghi nhận thanh toán qua Sổ Quỹ -> Kiểm tra xem Sổ quỹ có giảm số dư không và Nhật ký chung có tự động sinh bút toán DRAFT không.
2.  **Luồng thủ công:** Lập bút toán thủ công -> Chọn tài khoản định khoản -> Đảm bảo tổng Nợ bằng tổng Có -> Lưu bút toán DRAFT thành công.
