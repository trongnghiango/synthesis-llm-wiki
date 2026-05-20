# Nợ Kỹ Thuật: Đồng Bộ Hóa Trạng Thái Lead (Database vs Domain)
**ID:** STAX-DEBT-001  
**Module:** CRM  
**Severity:** Medium (Dễ gây nhầm lẫn khi truy vấn SQL trực tiếp)  
**Date Created:** 2026-05-20  

---

## 1. Hiện trạng & Vấn đề (Current State & Issue)
Hiện tại có sự bất đối xứng giữa **Domain Enum (`LeadStage`)** và **Database pgEnum (`lead_status`)** của bảng `leads`:

*   **Domain Enums (`LeadStage`):**
    ```typescript
    export enum LeadStage {
        NEW = 'NEW',
        CONSULTING = 'CONSULTING',
        NEGOTIATING = 'NEGOTIATING',
        WON = 'WON',
        LOST = 'LOST',
    }
    ```
*   **Database pgEnum (`lead_status`):**
    ```typescript
    export const leadStatusEnum = pgEnum('lead_status', [
        'NEW', 
        'CONTACTED', 
        'QUALIFIED', 
        'PROPOSAL', 
        'NEGOTIATION', 
        'WON', 
        'LOST', 
        'ARCHIVED', 
        'DISQUALIFIED'
    ]);
    ```

### Giải pháp tạm thời hiện tại (Workaround)
Để tránh lỗi `INTERNAL_SERVER_ERROR` khi lưu dữ liệu, một bộ Helper chuyển đổi hai chiều đã được thêm vào lớp `LeadMapper` (`lead.mapper.ts`):
*   Database $\rightarrow$ Domain: `CONTACTED`/`QUALIFIED`/`PROPOSAL` gộp thành `CONSULTING`; `NEGOTIATION` đổi thành `NEGOTIATING`.
*   Domain $\rightarrow$ Database: `CONSULTING` chuyển ngược thành `CONTACTED`; `NEGOTIATING` chuyển ngược thành `NEGOTIATION`.

### Hệ quả (Consequences)
1.  **Code Boilerplate:** Mapper phải gánh thêm logic dịch chuyển trạng thái không đáng có.
2.  **Khó khăn khi thống kê:** Viết các câu lệnh SQL thuần (Raw SQL) hoặc báo cáo trực tiếp từ Database sẽ gặp khó khăn vì tên cột trong DB không trùng khớp với khái niệm nghiệp vụ trên giao diện (ví dụ: tìm kiếm lead "Đang tư vấn" thì phải tìm theo `status IN ('CONTACTED', 'QUALIFIED', 'PROPOSAL')` thay vì chỉ tìm `CONSULTING`).

---

## 2. Kế hoạch Tái cấu trúc (Refactoring Plan)

### Bước 1: Tạo file Migration cập nhật pgEnum & Data
Bổ sung một migration script để:
1.  Thêm các giá trị enum mới (`CONSULTING`, `NEGOTIATING`) vào type `lead_status` trong PostgreSQL.
2.  Chạy script SQL cập nhật dữ liệu lịch sử:
    ```sql
    -- Chuyển đổi dữ liệu cũ sang enum chuẩn của Domain
    UPDATE leads SET status = 'CONSULTING' WHERE status IN ('CONTACTED', 'QUALIFIED', 'PROPOSAL');
    UPDATE leads SET status = 'NEGOTIATING' WHERE status = 'NEGOTIATION';
    UPDATE leads SET status = 'LOST' WHERE status IN ('ARCHIVED', 'DISQUALIFIED');
    ```
3.  Loại bỏ các giá trị enum cũ (`CONTACTED`, `QUALIFIED`, `PROPOSAL`, `NEGOTIATION`, `ARCHIVED`, `DISQUALIFIED`) khỏi type `lead_status` (sử dụng câu lệnh `ALTER TYPE` hoặc tạo type mới rồi cast).

### Bước 2: Cập nhật Schema định nghĩa Drizzle
Cập nhật file `/backend/src/database/schema/crm/leads.schema.ts`:
```typescript
export const leadStatusEnum = pgEnum('lead_status', ['NEW', 'CONSULTING', 'NEGOTIATING', 'WON', 'LOST']);
```

### Bước 3: Đơn giản hóa Mapper (LeadMapper)
Xóa bỏ các hàm `mapStatusToStage` và `mapStageToStatus` trong `LeadMapper`, thực hiện cast trực tiếp 1:1:
```typescript
stage: raw.status as LeadStage,
```

---

## 3. Lợi ích sau khi tối ưu (Expected Benefits)
*   **Thống nhất Ubiquitous Language:** Cả UI, Domain, BFF, Backend và Database đều sử dụng chung một tập hợp trạng thái (`NEW`, `CONSULTING`, `NEGOTIATING`, `WON`, `LOST`).
*   **Đơn giản hóa báo cáo:** Các câu lệnh query thống kê theo nhóm trạng thái sẽ ngắn gọn và rõ ràng hơn.
*   **Hiệu năng:** Loại bỏ bước xử lý/mapping ở CPU phía ứng dụng.
