# Kế hoạch Kiến trúc Chi tiết: Đồng bộ chuyển tiền nội bộ (Internal Transfer Sync)

Đây là kế hoạch kỹ thuật chi tiết nhằm triển khai cơ chế đồng bộ hạch toán bất đồng bộ qua Domain Event khi chuyển tiền nội bộ.

---

## A. Database Schema (Drizzle ORM)
*   Không có bảng, trường dữ liệu hay pgEnum mới nào cần khởi tạo ở Cơ sở dữ liệu.
*   Chúng ta sử dụng các bảng hiện có: `cash_funds`, `cash_transactions`, `accounts`, `journal_entries`, `journal_items`.

---

## B. Domain Layer (TypeScript thuần)

### 1. Định nghĩa `MoneyTransferredEvent`
*   **Vị trí:** [NEW] `backend/src/modules/accounting/domain/events/money-transferred.event.ts`
*   **Đặc điểm:** Kế thừa `IAuditableEvent` của STAX để tự động ghi log Audit Log hệ thống một cách chuẩn mực.

```typescript
import { IAuditableEvent, AuditEntryPayload } from '@core/shared/domain/events/auditable-event.interface';

export class MoneyTransferredEvent implements IAuditableEvent {
    readonly aggregateId: string;
    readonly occurredAt: Date;
    readonly payload: Record<string, any>;

    constructor(
        public readonly fromFundId: number,
        public readonly toFundId: number,
        public readonly amount: number,
        public readonly orgId: number,
        public readonly actorId: number,
        public readonly note?: string
    ) {
        this.aggregateId = fromFundId.toString();
        this.occurredAt = new Date();
        this.payload = {
            fromFundId,
            toFundId,
            amount,
            orgId,
            actorId,
            note
        };
    }

    toAuditEntry(): AuditEntryPayload {
        return {
            action: 'CASH.TRANSFER',
            resource: 'cash_funds',
            resourceId: this.aggregateId,
            organizationId: this.orgId,
            metadata: {
                fromFundId: this.fromFundId,
                toFundId: this.toFundId,
                amount: this.amount,
                note: this.note,
                actorId: this.actorId
            },
            severity: 'INFO'
        };
    }
}
```

---

## C. Infrastructure Layer (Framework-aware)
*   Không cần Mapper hay Repository mới vì chúng ta tái sử dụng toàn bộ Repo có sẵn (`ICashFundRepository`, `IAccountRepository`, `IJournalRepository`).

---

## D. Application Layer (Orchestration only)

### 1. Nâng cấp `CashFundService`
*   **Vị trí:** [MODIFY] `backend/src/modules/accounting/application/services/cash-fund.service.ts`
*   **Thay đổi:** 
    *   Inject `IEventBus` vào constructor.
    *   Phát `MoneyTransferredEvent` ngay sau khi transaction chuyển tiền hoàn tất thành công.

### 2. Xây dựng `MoneyTransferListener`
*   **Vị trí:** [NEW] `backend/src/modules/accounting/application/listeners/money-transfer.listener.ts`
*   **Mô tả:** Đón bắt sự kiện chuyển tiền nội bộ, thực thi nghiệp vụ định khoản kép tự động sinh bút toán nháp `DRAFT`.
*   **Giải thuật hạch toán:**
    *   **Nợ (Debit) TK 1111/1121** của Quỹ Nhận (`toAccount`).
    *   **Có (Credit) TK 1111/1121** của Quỹ Chuyển (`fromAccount`).

```typescript
import { Injectable, Logger, Inject } from '@nestjs/common';
import { EventHandler } from '@core/shared/infrastructure/event-bus/decorators/event-handler.decorator';
import { MoneyTransferredEvent } from '../../domain/events/money-transferred.event';
import { ICashFundRepository } from '../../domain/repositories/cash-fund.repository';
import { IAccountRepository } from '../../domain/repositories/account.repository';
import { JournalService } from '../services/journal.service';

@Injectable()
export class MoneyTransferListener {
    private readonly logger = new Logger(MoneyTransferListener.name);

    constructor(
        @Inject(ICashFundRepository) private readonly fundRepo: ICashFundRepository,
        @Inject(IAccountRepository) private readonly accountRepo: IAccountRepository,
        private readonly journalService: JournalService
    ) {}

    @EventHandler(MoneyTransferredEvent)
    async handleMoneyTransferred(event: MoneyTransferredEvent) {
        this.logger.debug(`Đang hạch toán tự động cho chuyển khoản nội bộ từ Quỹ ${event.fromFundId} sang Quỹ ${event.toFundId}`);

        try {
            const fromFund = await this.fundRepo.findById(event.fromFundId, event.orgId);
            const toFund = await this.fundRepo.findById(event.toFundId, event.orgId);

            if (!fromFund || !toFund) return;

            const fromAccountCode = fromFund.type === 'CASH' ? '111' : '112'; // Lấy tài khoản cấp 1 hoặc 2
            const toAccountCode = toFund.type === 'CASH' ? '111' : '112';

            const fromAccount = await this.accountRepo.findByCode(event.orgId, fromAccountCode);
            const toAccount = await this.accountRepo.findByCode(event.orgId, toAccountCode);

            if (!fromAccount || !toAccount) {
                this.logger.warn(`Không tìm thấy tài khoản định khoản ${fromAccountCode} hoặc ${toAccountCode} cho Tổ chức ${event.orgId}`);
                return;
            }

            await this.journalService.createManualEntry(event.orgId, {
                description: event.note || `Hạch toán tự động: Chuyển khoản nội bộ từ ${fromFund.name} sang ${toFund.name}`,
                items: [
                    { accountId: toAccount.id!, debit: event.amount, credit: 0, description: `Nhận chuyển khoản từ ${fromFund.name}` },
                    { accountId: fromAccount.id!, debit: 0, credit: event.amount, description: `Chuyển tiền sang ${toFund.name}` }
                ]
            });

            this.logger.log(`✅ Đã tạo bút toán DRAFT thành công cho giao dịch chuyển tiền nội bộ.`);
        } catch (error) {
            this.logger.error(`❌ Lỗi khi tự động hạch toán chuyển khoản nội bộ: ${error.message}`);
        }
    }
}
```

---

## E. Presentation Layer & Contracts
*   Không thay đổi các Controller hay DTO vì tầng biên nhận API chuyển tiền của Client đã hoàn thiện 100%.

---

## F. Đấu nối NestJS Module (Module Wiring)
*   **Vị trí:** [MODIFY] `backend/src/modules/accounting/accounting.module.ts`
*   **Thay đổi:** 
    *   Đăng ký `MoneyTransferListener` vào mảng `providers` để EventBus tự động quét và map sự kiện.
