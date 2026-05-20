# Phân tích Kỹ thuật: Finote Payment Integration

**A. Phân loại module:**
- Thuộc Tier 3 (Accounting) — Phân hệ quản lý dòng chảy tài chính.
- Phụ thuộc vào: `cash_transactions`, `finote_payments`, `finotes`. Bắn sự kiện lên EventBus (Tier 1).

**B. Bounded Context & Ubiquitous Language:**
- Domain: Payment Reconciliation (Ghi nhận thanh toán / Gạch nợ).
- Nghiệp vụ: Thu tiền mặt/chuyển khoản và gán vào một Yêu cầu thanh toán (Finote).
- Code: `RecordFinotePayment`.

**C. Data Flow & API Design:**
- Flow: Client -> Controller -> Service (TxManager) -> Domain Entity -> Repo -> DB.
- Endpoint: `POST /api/accounting/finotes/:finoteId/payments`.
- Quyền: Admin (MVP).

**D. Cross-module dependencies:**
- Gọi Port `IEventBus` để publish `FinotePaymentRecordedEvent`.
- `IAuditLogService` (fire-and-forget).

**E. Multi-tenancy:**
- Truy vấn Finote phải kèm `.where(eq(finotes.tenantId, orgId))`.

**F. Security (_actions):**
- Trả về `_actions.recordPayment.allowed` nếu Finote `status` khác `PAID`.
