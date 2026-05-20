# 🚨 STAX Audit Report: Audit Log System (Logic & Architecture)

**Ngày kiểm toán:** 2026-05-09
**Module:** Logging / Audit Log
**Trạng thái:** Rà soát thiết kế (Design Audit)

---

## 1. Vi phạm Kiến trúc (Architecture Violations & Risks)

Dựa trên "Hiến pháp STAX" và Ma trận Cảnh báo Đỏ, tôi phát hiện các điểm cần lưu ý sau trong bản đề xuất:

### 🚨 Rủi ro Framework Leak (ADR 001)
- **Vấn đề:** Bản phân tích đề cập đến việc "Service sẽ lấy `userId` từ JWT". 
- **Cảnh báo:** Domain Service **KHÔNG ĐƯỢC PHÉP** biết về JWT hay Request Object. Thông tin `userId` hoặc `actor` phải được truyền vào từ Controller/Interface Layer dưới dạng tham số đơn thuần.

### 🚨 Rủi ro Audit Log Blocking (ADR 005)
- **Vấn đề:** Chưa mô tả cơ chế *ghi* log (Capture). 
- **Cảnh báo:** Việc ghi log phải là "Fire-and-forget". Nếu Service đợi `await db.insert(auditLogs)` xong mới trả kết quả cho Client thì sẽ vi phạm ADR 005, gây chậm hệ thống (Blocking).

### 🚨 Nợ kỹ thuật: Data Scoping Complexity
- **Vấn đề:** "Truy vấn Employee -> Position -> OrgUnit... thêm điều kiện WHERE actor_id IN (subordinate_ids)".
- **Cảnh báo:** Việc tính toán `subordinate_ids` đệ quy mỗi khi query Log là một thảm họa hiệu năng. 
- **Giải pháp:** Cần sử dụng **Path-based enumeration** (Materialized Path) trong bảng OrgUnit để query nhánh con chỉ bằng một câu lệnh `LIKE 'path/%'` thay vì đệ quy.

---

## 2. Code Smells & Cải thiện (Proposed Improvements)

### 👃 Smell: Resource Hardcoding
- Frontend không nên tự hardcode list resource (leads, contracts...). Backend nên trả về một Metadata API để Frontend render dropdown filter linh hoạt.

### 👃 Smell: Real-time Polling
- Việc dùng `refetchInterval` (Polling) là giải pháp tạm thời. Nếu hệ thống lớn, hàng trăm user cùng polling sẽ gây tải cực lớn cho DB. 
- **Đề xuất:** Chỉ cho phép polling ở trang "Live Dashboard" với tần suất thấp, hoặc dùng Server-Sent Events (SSE) cho module hệ thống.

---

## 3. Ma trận Cảnh báo Đỏ (Red Flags Matrix Check)

| Red Flag | Status | Ghi chú |
| :--- | :---: | :--- |
| **Framework Leak** | 🟡 | Cần tách biệt JWT khỏi Application Service. |
| **Response Leak** | 🔴 | Cần DTO Mapper cho AuditLog để che giấu các thông tin nhạy cảm trong `before/after` JSON. |
| **Audit Log Blocking** | 🔴 | Phải đảm bảo dùng `setImmediate` hoặc Event Bus để ghi log. |
| **Missing Tests** | 🔴 | Cần kế hoạch Unit Test cho bộ lọc phân quyền (Data Scope Filter). |

---

## 4. Kết luận sơ bộ
Bản thiết kế logic của bạn rất tốt về mặt nghiệp vụ, đặc biệt là phần phân quyền theo sơ đồ tổ chức. Tuy nhiên, cần chỉnh sửa lại cách triển khai ở tầng Backend để đảm bảo **Độ thuần khiết (Purity)** và **Hiệu suất (Performance)**.

👉 **Tôi đã hoàn tất báo cáo kiểm toán. Bạn có muốn tôi lên kế hoạch sửa chữa & thực hiện (Refactoring & Implementation Plan) cho tính năng này theo đúng chuẩn STAX không?**
