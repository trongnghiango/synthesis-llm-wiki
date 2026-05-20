# 🏗️ STAX Architectural Blueprint: Audit Log System (Advanced Decoupling)

Bản phác thảo này được thiết kế để giải quyết các trăn trở về "Rác", "Smell Code" và "Hiệu năng" mà chúng ta đã thảo luận.

---

## 1. Nguyên lý "Không chạm" (The Non-Invasive Strategy)

Để đảm bảo các module nghiệp vụ (CRM, Accounting) không bị "nhiễm rác" bởi logic của Audit Log, chúng ta sử dụng cơ chế **Event-Driven Architecture (EDA)**.

### Luồng xử lý (Workflow):
1.  **Capture (Tại module nghiệp vụ):** Thay vì viết code ghi log, ta sử dụng `@AuditLog()` Decorator trên các method quan trọng. Decorator này sẽ tự động phát ra một `Domain Event` sau khi method thực thi thành công.
2.  **Transport (Event Bus):** Event này được đẩy vào một hàng đợi (In-memory hoặc RabbitMQ).
3.  **Process (Tại Audit Module):** Module Audit Log sẽ lắng nghe Event này, lấy snapshot dữ liệu và lưu vào Database.

**=> Kết quả:** File nghiệp vụ hoàn toàn sạch bóng code logging.

---

## 2. Chiến thuật "Linh hoạt Database" (The Hybrid Interface)

Chúng ta sẽ sử dụng PostgreSQL ngay bây giờ nhưng với tâm thế của MongoDB để không gây "nứt vỡ" khi chuyển đổi sau này.

### Cấu trúc Repository:
```typescript
export interface IAuditLogRepository {
  // Nhận vào một Domain Object (không phải DB Record)
  save(log: AuditLog): Promise<void>;
  
  // Query dựa trên các tiêu chí nghiệp vụ, không dựa trên cú pháp SQL
  findWithFilters(query: AuditLogQuery): Promise<PaginatedResult<AuditLog>>;
}
```
*   **Hiện tại:** Triển khai bằng Drizzle ORM (Postgres) sử dụng cột `jsonb`.
*   **Tương lai:** Chỉ cần thay lớp thực thi bằng MongoDB Driver. Toàn bộ UI và Service vẫn giữ nguyên.

---

## 3. Giải quyết bài toán Hiệu suất (Performance Optimization)

### 🚀 Ghi (Write): Fire-and-forget
Dùng `setImmediate()` hoặc `EventBus` để tách biệt luồng ghi log. Request của người dùng sẽ kết thúc ngay khi nghiệp vụ xong, việc ghi log diễn ra "âm thầm" ở background.

### 🔍 Đọc (Read): Materialized Path cho OrgUnit
Thay vì đệ quy để tìm "Cấp dưới", chúng ta lưu OrgUnit dưới dạng đường dẫn (vd: `/Stax/Sales/HCM`). 
*   **Truy vấn:** `WHERE org_path LIKE '/Stax/Sales/%'` 
*   **Hiệu quả:** Tốc độ nhanh gấp hàng chục lần so với đệ quy truyền thống.

---

## 4. Cấu trúc Module (Isolation)

Module sẽ được đặt tại `src/modules/system/audit-log/`. 
Nó có **Database Schema riêng**, **Service riêng**, và **không phụ thuộc ngược** vào bất kỳ module nghiệp vụ nào. Nó chỉ phụ thuộc vào `CoreModule` để lấy Event Bus.

---

## 5. Danh sách "Red Flags" cần tránh (Anti-patterns)

1.  ❌ **KHÔNG** import `AuditLogService` vào `LeadService`. (Vi phạm Decoupling)
2.  ❌ **KHÔNG** dùng `await` khi phát tán Log Event. (Vi phạm Performance)
3.  ❌ **KHÔNG** lưu `before/after` bằng các trường text rời rạc. (Phải dùng `jsonb`)
4.  ❌ **KHÔNG** join trực tiếp bảng Log với bảng User khi query. (Phải Denormalize tên User vào Log)

---

### ⚖️ Đánh giá từ Auditor:
Với bản phác thảo này, hệ thống của bạn sẽ **không bao giờ bị "nứt vỡ"** do Audit Log. Thậm chí, việc xây dựng Audit Log theo cách này còn giúp bạn chuẩn hóa lại bộ Event Bus của toàn hệ thống - một bước tiến lớn về mặt kỹ thuật.

**Bạn có muốn tôi bắt đầu lập Kế hoạch triển khai chi tiết cho từng bước (Step 2 - Refactoring Plan) dựa trên bản phác thảo này không?**
