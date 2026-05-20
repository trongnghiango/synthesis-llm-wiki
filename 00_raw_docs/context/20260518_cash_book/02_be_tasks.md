# Checklist Thực thi Backend: Cash Book (Sổ Quỹ)

Trình tự các bước thực thi tính năng:

- [ ] 1. Định nghĩa Zod Contract cho `CashFund` (tạo mới `shared/contracts/accounting/cash-fund.ts`) và đăng ký vào contract chính.
- [ ] 2. Tạo file schema Drizzle mới `cash-funds.schema.ts` trong `backend/src/database/schema/accounting/`.
- [ ] 3. Sửa đổi `finotes.schema.ts` để thêm `fundId` vào bảng `cash_transactions` và cập nhật quan hệ (Relations).
- [ ] 4. Đăng ký `cash-funds.schema.ts` vào index schema chung `backend/src/database/schema/index.ts`.
- [ ] 5. Chạy lệnh sinh Migration: `pnpm --filter rbac-nest-project db:generate` (hoặc `pnpm db:push` trong môi trường dev).
- [ ] 6. Tạo Domain Entity `CashFund` (`src/modules/accounting/domain/entities/cash-fund.entity.ts`).
- [ ] 7. Định nghĩa Port `ICashFundRepository` (`src/modules/accounting/domain/repositories/cash-fund.repository.ts`).
- [ ] 8. Tạo Mapper `CashFundMapper` (`src/modules/accounting/infrastructure/mappers/cash-fund.mapper.ts`).
- [ ] 9. Implement Repository `DrizzleCashFundRepository` (`src/modules/accounting/infrastructure/persistence/drizzle-cash-fund.repository.ts`).
- [ ] 10. Tạo Application Service `CashFundService` (`src/modules/accounting/application/services/cash-fund.service.ts`).
- [ ] 11. Cập nhật `FinotePaymentService` để tự động chọn Quỹ mặc định nếu giao dịch ghi nhận thanh toán chưa chọn quỹ cụ thể.
- [ ] 12. Tạo DTOs cho các request tạo quỹ, chuyển tiền nội bộ.
- [ ] 13. Tạo Controller `CashFundController` và `CashTransactionController`.
- [ ] 14. Kết nối Module và xuất Port trong `accounting.module.ts` và `index.ts`.
- [ ] 15. Tạo 1 seeder/migration script để cập nhật toàn bộ dữ liệu lịch sử (tạo Quỹ Tiền Mặt mặc định cho mọi Org hiện có và gán mọi `cash_transactions` cũ vào đó).
- [ ] 16. Viết Unit Test cho `CashFundService` để test chức năng chuyển khoản nội bộ (Transfer) và tạo quỹ.
- [ ] 17. Chạy `pnpm run build` để đảm bảo 0 lỗi TypeScript compile.
