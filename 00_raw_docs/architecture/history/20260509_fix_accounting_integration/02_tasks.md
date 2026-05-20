# Tasks: Chuẩn hóa Tích hợp Kế toán

Dưới đây là kế hoạch chia nhỏ các thay đổi thành từng Commit để dễ dàng theo dõi và Review.

## 📦 Commit 1: Domain & Infrastructure Standardizing
- [x] **Domain:** Cập nhật `Finote` Entity để thêm validation invariants.
- [x] **Infrastructure:** Audit lại `FinoteMapper` để đảm bảo kiểu dữ liệu (Numeric/Date) chuẩn hóa.
- [x] **Infrastructure:** Đảm bảo `DrizzleFinoteRepository.findAll` hỗ trợ lọc theo Tenant (Organization) một cách nghiêm ngặt.

## 📦 Commit 2: Application Logic & ID Resolution
- [x] **Service:** Cập nhật `FinoteService.createFinote` để thực hiện Resolution: `User ID` -> `Employee ID`.
- [x] **Service:** Tự động gán `sourceOrgId` từ Session (Application context) nếu bị thiếu.
- [x] **Service:** Bổ sung phương thức `getList` chuẩn hóa.

## 📦 Commit 3: API Refactoring & DTO Compatibility
- [x] **DTO:** Refactor `CreateFinoteDto` & `CreateFinoteRequestDto`. 
    - Khôi phục strict validation.
    - Dùng `@Transform` để handle `transactionDate` và `type: RECEIPT` một cách sạch sẽ.
- [x] **Controller:** Dọn dẹp `FinoteController`. Xóa bỏ code debug, khôi phục typing chuẩn.
- [x] **Controller:** Hoàn thiện endpoint `GET /api/accounting/finotes`.

## 📦 Commit 4: Robust Testing (Mandatory)
- [x] **Unit Test:** Viết `.spec.ts` cho `FinoteService` (Mock repositories).
- [x] **Integration Test:** Viết `.spec.ts` cho `DrizzleFinoteRepository` (Sử dụng PGLite).

## 📦 Commit 5: Final Polish & Documentation
- [x] **Cleanup:** (Người dùng giữ lại các file script tạm thời để kiểm tra).
- [x] **Walkthrough:** Tạo file `03_walkthrough.md` tổng kết và Archive thư mục context.
