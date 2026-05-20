# Kế hoạch Phủ Unit Test Toàn diện cho STAX ERP

Bạn đã đưa ra một yêu cầu mang tính bước ngoặt để biến STAX thành một hệ thống chuẩn Enterprise: **Phủ Unit Test cho toàn bộ Services, Use Cases và Repositories**. Vì đây là một khối lượng công việc khổng lồ (hàng chục file, hàng ngàn dòng code test), chúng ta cần một chiến lược tiếp cận khoa học để đảm bảo chất lượng và không bị vỡ vụn.

## ⚠️ Đánh giá Hiện trạng & Phân tích
- **Hiện tại:** Có khoảng 13 file `.spec.ts`, chủ yếu tập trung vào các luồng khó như `PaymentReconciliation`, `LeadWorkflow`, và `AuditLog`.
- **Còn thiếu:** Hàng loạt Service cốt lõi (AuthService, UserService, ContractService, QuoteService...) và **Toàn bộ 100% Repository** (Drizzle).

> [!WARNING]
> **Vấn đề khó khăn nhất: Test các Drizzle Repositories**
> Khác với TypeORM có thể dễ dàng mock repository, Drizzle ORM sử dụng Fluent API (chaining method như `db.select().from().where()`). Việc viết Unit Test dùng Jest để mock từng hàm `.select()`, `.from()` của Drizzle là **vô cùng cực nhọc, dễ hỏng và không mang lại nhiều giá trị thực tế** (vì bản chất ta đang test cách viết Drizzle chứ không test SQL sinh ra có đúng hay không).

## 🤔 Các Câu Hỏi Mở (Open Questions)

> [!IMPORTANT]
> **Chiến lược Test Repository:** Bạn muốn tôi áp dụng phương pháp nào để test các `drizzle-*.repository.ts`?
> 
> **Lựa chọn 1: Mocking Cực đoan (Thuần Unit Test)**
> - Mock đối tượng `db` của Drizzle. 
> - *Ưu điểm:* Chạy cực nhanh, không cần setup DB thật.
> - *Nhược điểm:* Rất khó maintain, test case sẽ rất cồng kềnh vì phải mock từng chuỗi `.select().from().leftJoin()`.
> 
> **Lựa chọn 2: Integration Test với In-Memory DB (Khuyến nghị)**
> - Sử dụng `pg-mem` (Postgres in-memory) hoặc Docker `Testcontainers`.
> - *Ưu điểm:* Test được SQL thật, đảm bảo Query đúng, dễ viết test.
> - *Nhược điểm:* Cần setup môi trường, chạy chậm hơn Unit Test thông thường một chút.

## 📋 Đề xuất Lộ trình Thực thi (Phased Approach)

Do giới hạn về một lần xử lý, chúng ta sẽ chia chiến dịch này thành các Phase (Giai đoạn) nối tiếp nhau. Bạn duyệt kế hoạch này, tôi sẽ bắt tay vào **Phase 1** ngay lập tức.

### Phase 1: Hoàn thiện Unit Test cho Foundation Services (ĐÃ HOÀN THÀNH ✅)
Tập trung vào các Service ở Tier 1 (Auth, User, OrgStructure) vì chúng là nền tảng cho mọi module khác.
- [x] `UserService` (Tạo user, đổi mật khẩu)
- [x] `AuthService` (Login, JWT, Refresh Token)
- [x] `OrgStructureService` (Cây phòng ban)
- [x] `PermissionService` (Cây quyền hạn)

### Phase 2: Phủ Test cho CRM & Accounting Services (ĐÃ HOÀN THÀNH ✅)
Tập trung vào các Service nghiệp vụ phức tạp.
- [x] `LeadQueryService` & `OrganizationQueryService`
- [x] `ContractService` & `QuoteService`
- [x] `FinoteDocumentService`

> **Kết quả Phase 2:** 20 test cases mới, tổng cộng **43/43 tests PASS** (Phase 1 + 2 gộp lại). Đồng thời refactor `QuoteService` loại bỏ nốt các `ForbiddenException`/`BadRequestException` còn sót.

### Phase 3: Repository Test (Chiến lược: Integration Test với In-Memory DB 🛠️)
Tập trung vào tầng Data Access sử dụng `pg-mem`.
- [ ] Cài đặt `pg-mem` và cấu hình Jest environment riêng cho integration tests.
- [ ] Viết test cho `DrizzleLeadRepository` (findAll, findById, save).
- [ ] Viết test cho `DrizzleOrganizationRepository`.
- [ ] Viết test cho `DrizzleUserRepository`.

---

## Kế hoạch Kiểm chứng (Verification Plan)
- Chạy `npm run test` để đảm bảo toàn bộ suite test passed.
- Chạy `npm run test:cov` (Coverage) và mục tiêu nâng tỷ lệ Coverage của thư mục `src/modules/` lên trên 80%.

👉 **Xin hãy cho tôi biết ý kiến của bạn về "Lựa chọn chiến lược Test Repository", và tôi sẽ bắt đầu ngay với Phase 1!**
