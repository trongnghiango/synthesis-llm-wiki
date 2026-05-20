# Tasks: STAX Safe-Update Pattern

Danh sách các đầu việc cần thực hiện để phủ sạch lỗi Update Constraint trên toàn hệ thống.

- [x] **Infrastructure: Core Foundation**
  - [x] Cập nhật `DrizzleBaseRepository` bổ sung phương thức `mapToUpdate`.
- [x] **Infrastructure: CRM Repositories**
  - [x] Refactor `DrizzleOrganizationRepository`.
  - [x] Refactor `DrizzleLeadRepository`.
  - [x] Refactor `DrizzleContactRepository`.
  - [x] Refactor `DrizzleQuoteRepository`.
- [x] **Infrastructure: HRM & User Repositories**
  - [x] Refactor `DrizzleEmployeeRepository`.
  - [x] Refactor `DrizzleUserRepository`.
- [x] **Infrastructure: Accounting & Other Repositories**
  - [x] Refactor `DrizzleFinoteRepository`.
  - [x] Refactor `DrizzleNotificationRepository`.
- [x] **Verification**
  - [x] Chạy lại Integration Test cho `DrizzleOrganizationRepository` để confirm đã fix được lỗi reported bởi FE.
  - [x] Chạy lại toàn bộ test suite để đảm bảo không có side-effect.
