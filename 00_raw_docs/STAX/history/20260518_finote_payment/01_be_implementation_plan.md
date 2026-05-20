# Kế hoạch Kiến trúc Chi tiết Backend: Finote Payment

**A. Database Schema**
- Bảng `cash_transactions` và `finote_payments` đã tồn tại. Không cần Migration.

**B. Domain Layer**
- Sửa `Finote` Entity (`src/modules/accounting/domain/entities/finote.entity.ts`):
  - Props: Thêm `paidAmount?: number`.
  - Methods: `recordPayment(amount: number, date: Date, ref?: string)`.
  - Invariant check: `amount > (totalAmount - paidAmount)` -> Throw `BusinessRuleValidationException`.
  - Trạng thái: Cập nhật thành `PAID` hoặc `PARTIALLY_PAID`.
- Domain Event: `FinotePaymentRecordedEvent` (`src/modules/accounting/domain/events/finote-payment-recorded.event.ts`).

**C. Infrastructure Layer**
- Cập nhật Mapper `FinoteMapper.toDomain` và `FinoteMapper.toResponseDto` để tính `paidAmount` và trả về `_actions.recordPayment`.

**D. Application Layer**
- `FinotePaymentService` (`src/modules/accounting/application/services/finote-payment.service.ts`):
  - Bọc trong `txManager.runInTransaction`.
  - Lưu cash, lưu mapping, cập nhật finote.
  - Gọi `eventBus.publish`.
  - Gọi `auditLog.log` fire-and-forget.

**E. Presentation Layer & Contracts**
- Zod Schema: Sửa `backend/src/core/shared/contracts/accounting.ts`. Đã bổ sung `RecordFinotePaymentSchema`. Cần tool sync sang Frontend.
- DTO: `RecordFinotePaymentDto` tại `src/modules/accounting/application/dtos/record-finote-payment.dto.ts`.
- Controller: `POST /api/accounting/finotes/:id/payments`.

**F. Module Wiring**
- Inject `FinotePaymentService` vào `AccountingModule`.
