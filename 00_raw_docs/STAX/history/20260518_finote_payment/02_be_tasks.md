# Checklist Thực thi Backend: Finote Payment

Trình tự BẮT BUỘC:

[x] 1. Shared Contracts (Zod tại shared/contracts/) - Đã thêm RecordFinotePaymentSchema.
[x] 2. Database Schema (schema file + index export) - Không cần sửa.
[x] 3. pgEnum definitions - Không cần sửa.
[x] 4. Run migration (drizzle-kit generate / quick-fix) - Không cần sửa.
[ ] 5. Domain Entity + Props interface (Sửa Finote entity thêm recordPayment).
[ ] 6. Value Objects (nếu có).
[ ] 7. Repository Interface (Port + DI Token) - Sửa IFinoteRepository nếu cần.
[ ] 8. Domain Events (Tạo FinotePaymentRecordedEvent).
[ ] 9. Mapper (Cập nhật toDomain + toResponseDto tính toán _actions).
[ ] 10. Repository Implementation (Sửa DrizzleFinoteRepository nếu cần).
[ ] 11. Application Service (Tạo FinotePaymentService).
[ ] 12. Request/Response DTOs (Tạo RecordFinotePaymentDto).
[ ] 13. Controller (Sửa FinoteController thêm POST /:id/payments).
[ ] 14. Module Wiring + index.ts export (Sửa AccountingModule).
[ ] 15. Unit Test (Service — mock repositories).
[ ] 16. Integration Test (Repository — PGLite).
[ ] 17. npm run build — 0 TypeScript error.
[ ] 18. Manual API test via Swagger.
