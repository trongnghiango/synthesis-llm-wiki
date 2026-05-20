# Audit Report: CRM & Accounting Modules

**Date:** 2026-05-09
**Auditor:** STAX Architecture Auditor
**Status:** 🔴 CRITICAL VIOLATIONS FOUND

---

## 1. Summary of Findings

Cuộc kiểm toán đã phát hiện 2 lỗi logic nghiêm trọng ảnh hưởng đến tính toàn vẹn của dữ liệu và sự an toàn của hệ thống đa thuê bao (Multi-tenancy), cùng với một số vi phạm về kiến trúc.

---

## 2. Critical Violations (Vi phạm Nghiêm trọng)

### 🚨 V01: Organization Theft (Ăn cắp Tổ chức) - CRM Module
- **File:** `src/modules/crm/application/services/lead-intake.service.ts`
- **Mô tả:** Logic `intelligentIntake` tự động liên kết Lead mới với một Organization cũ chỉ dựa trên số điện thoại (Contact Phone) mà không kiểm tra tính nhất quán của tên tổ chức (`organizationName`).
- **Rủi ro:** Một khách hàng mới sử dụng số điện thoại của một người đã từng làm việc cho công ty khác sẽ bị gán nhầm vào công ty cũ đó. Dữ liệu kinh doanh bị rò rỉ hoặc bị lẫn lộn giữa các pháp nhân.
- **Hiến pháp STAX:** Vi phạm nguyên tắc "Identity Integrity".

### 🚨 V02: Tenancy Leak (Rò rỉ Đa thuê bao) - Accounting Module
- **File:** `src/modules/accounting/infrastructure/controllers/finote.controller.ts`
- **Mô tả:** API `GET /accounting/finotes` cho phép người dùng truyền `orgId` qua Query String và ưu tiên giá trị này hơn `user.organizationId` từ Session.
- **Rủi ro:** Một người dùng có quyền `finote:read` ở Tổ chức A có thể xem toàn bộ dữ liệu tài chính của Tổ chức B bằng cách thay đổi tham số `orgId`.
- **Hiến pháp STAX:** Vi phạm nguyên tắc "Strict Tenancy Enforcement" (ADR 002).

---

## 3. Architecture Leaks (Rò rỉ Kiến trúc)

### ⚠️ L01: Framework Leak in Controller
- **File:** `src/modules/accounting/infrastructure/controllers/finote.controller.ts`
- **Mô tả:** Sử dụng `BadRequestException` trực tiếp từ `@nestjs/common` tại Controller để xử lý logic nghiệp vụ (kiểm tra Employee Profile).
- **Quy chuẩn:** Phải ném `BusinessRuleValidationException` ở tầng Application/Service và để Exception Filter xử lý.

---

## 4. Test Coverage Gap

- **LeadIntakeService:** Các case kiểm tra trùng SĐT nhưng khác tên Org chưa được bao phủ trong Unit Test, dẫn đến việc không phát hiện ra lỗi logic "ăn cắp" tổ chức.
- **FinoteController:** Thiếu các bài test về "Cross-tenant access" (truy cập chéo tổ chức).

---

## 5. Đề xuất Hiến pháp mới

Cần bổ sung điều khoản:
> **"Dữ liệu định danh tổ chức (Tenant ID) phải được trích xuất từ Authentication Context và áp đặt tại tầng Application/Infrastructure của Backend. Tuyệt đối không được tin tưởng vào Tenant ID do Frontend gửi lên trong các tác vụ truy vấn dữ liệu nhạy cảm."**

---

👉 **Câu hỏi cho User:** Tôi đã hoàn tất báo cáo kiểm toán sơ bộ. Bạn có muốn tôi lên kế hoạch sửa chữa (Refactoring Plan) chi tiết cho các lỗi này không?
