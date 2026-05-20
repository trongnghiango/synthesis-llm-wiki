# Cross-Check Report: Backend Fixes Verification

**Date:** 2026-05-09
**Subject:** Kiểm tra chéo các bản vá lỗi từ Team Backend

---

## 1. CRM: LeadIntakeService (V01)
- **Trạng thái:** ✅ **ĐÃ SỬA ĐÚNG (VERIFIED)**
- **Chi tiết:** Backend đã áp dụng "CHIẾN LƯỢC MỚI" tại dòng 66-76. 
    - Logic hiện tại: Chỉ link với Org cũ nếu `organizationName` khớp hoặc không có tên mới. 
    - Nếu tên công ty mới khác công ty cũ (dù trùng SĐT) -> Hệ thống sẽ tạo Org mới và Contact mới.
- **Đánh giá:** Đáp ứng hoàn hảo yêu cầu bảo vệ danh tính pháp nhân.

---

## 2. Accounting: Finote Tenancy (V02)
- **Trạng thái:** ❌ **CHƯA SỬA TRIỆT ĐỂ (FAIL)**
- **Chi tiết:** 
    - **Create Finote:** ✅ Đã sửa. Logic tại `FinoteService.createFinote` (dòng 76) đã ép `sourceOrgId` từ Context.
    - **Get List Finotes:** ❌ **VẪN CÒN LỖI.** Tại `FinoteController.getFinotes` (dòng 31):
      ```typescript
      const filterOrgId = orgId || user?.organizationId;
      ```
      Lỗ hổng này cho phép Frontend truyền `?orgId=...` để "vượt rào" xem dữ liệu của tổ chức khác nếu có quyền `finote:read`.
- **Đề xuất fix gấp:** Phải ép buộc `user.organizationId` là filter bắt buộc, hoặc kiểm tra quyền sở hữu nếu cho phép xem hộ.

---

## 3. Architecture Leaks (L01)
- **Trạng thái:** ❌ **CHƯA SỬA**
- **Chi tiết:** `BadRequestException` vẫn đang được sử dụng tại `FinoteController` (dòng 51, 71) thay vì ném từ Domain/Application.

---

## 4. Kết luận & Hành động kế tiếp
- Team Backend đã xử lý tốt phần logic tạo dữ liệu (CRM và Finote Create).
- Tuy nhiên, **phần truy vấn dữ liệu (Get List Finotes)** vẫn đang hở sườn, có nguy cơ lộ thông tin tài chính giữa các công ty.
- **Hành động của tôi (Frontend):** Tôi sẽ điều chỉnh code Frontend để luôn truyền đúng ID, nhưng Backend BẮT BUỘC phải vá lỗ hổng tại Controller để đảm bảo an toàn tuyệt đối (Security by Design).

---

👉 **Câu hỏi cho User:** Bạn có muốn tôi thực hiện luôn việc vá lỗi "vượt rào" này cho Backend không, hay để tôi tập trung hoàn thiện các tính năng Frontend?
