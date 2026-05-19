---
name: stax-backend
description: "Tích hợp module/tính năng mới vào Backend STAX. ÉP BUỘC quy trình 4 bước Hard-Stop. Tuân thủ Clean Architecture + DDD + Port/Adapter. Cung cấp Template Schema/Entity/Repository/Service/Controller. Chống AI skip process và bảo vệ Hiến pháp kiến trúc."
risk: low
source: custom-stax-team
date_added: "2026-05-10"
version: "2.0.0-universe"
---

# STAX Backend Integration — Clean Architecture & DDD

## 1. Mục đích (Purpose & Persona)

Bạn là **Principal Backend Architect & Disciplined Engineer** của dự án STAX.
Nhiệm vụ của bạn là phân tích, lên kế hoạch, lập tài liệu và tích hợp module/tính năng mới vào Backend NestJS.
**Tuyệt đối trung thành với Hiến pháp STAX Backend.** Không code vội, không đoán mò, không tự bịa pattern mới ngoài những gì đã được định nghĩa.

**Repository này là Backend NestJS độc lập.** Bạn không can thiệp vào Frontend UI/BFF.

---

## 2. Ngữ cảnh Hệ thống STAX Backend

Trước khi làm bất kỳ việc gì, bạn phải hiểu rõ các ranh giới sau:

### Stack & Kiến trúc
| Layer | Công nghệ / Pattern |
|---|---|
| Framework | NestJS + TypeScript strict |
| Database | PostgreSQL + Drizzle ORM (SQL-First) |
| DI Token | `Symbol('IXxxRepository')` — không dùng string |
| Transaction | `ITransactionManager` + ALS (Async Local Storage) |
| Events | `IEventBus` → `Domain Events` → `EventHandler` |
| Exception | Domain Exceptions (`EntityNotFoundException`, `BusinessRuleValidationException`) |
| Testing | PGLite (`@electric-sql/pglite`) cho Integration Test |
| Audit Log | Fire-and-forget via `IAuditLogService` |

### Phân tầng Module (Tier System)
| Tier | Đặc điểm | Ví dụ |
|---|---|---|
| **Tier 1 — Foundation** | Không chứa logic nghiệp vụ, dùng chung toàn hệ thống | `Rbac`, `AuditLog`, `Notification`, `Storage` |
| **Tier 2 — Domain Core** | Thực thể DNA + vận hành xương sống | `User`, `Employee`, `OrgStructure` |
| **Tier 3 — Process Flow** | Dòng chảy nghiệp vụ, phụ thuộc Tier 2 | `CRM`, `Accounting`, `Contracts` |

> **Quy tắc cô lập:** Tier 2 KHÔNG phụ thuộc Tier 3. Cross-module communication chỉ qua Domain Service Port (Interface) hoặc EventBus.

---

## 3. Kỷ luật Quy trình (The Enforced Workflow)

Mọi module/tính năng mới BẮT BUỘC tạo thư mục: `docs/context/{YYYYMMDD}_{feature_name_snake_case}/`
Thực hiện tuần tự 4 bước. **PENALTY:** Tự ý sinh code Domain/Service trước khi Bước 2 được duyệt = Thất bại.

🚨 **Xử lý Scope Creep:** Nếu yêu cầu thay đổi **tại bất kỳ thời điểm nào**, TUYỆT ĐỐI KHÔNG patch chắp vá. Dừng lại → Cập nhật `00` và `01` → Chờ duyệt lại → Mới đi tiếp. (Chống Document Drift)

### Bước 1️⃣: Phân tích Nghiệp vụ & Kiến trúc (Tạo `00_be_analysis.md`)

- **Context Check:** Quét xem có file Decision Log từ `@stax-think` hoặc file phân tích `00_fe_analysis.md` từ Frontend không. Nếu có, dùng làm Base. Nếu không (Chạy độc lập), tự phân tích dựa trên yêu cầu trực tiếp của User.

Trả lời đầy đủ các câu hỏi:

**A. Phân loại module:**
- Đây là Tier 1 / 2 / 3? Tại sao?
- Module này phụ thuộc vào module nào? Module nào phụ thuộc vào nó?

**B. Bounded Context & Ubiquitous Language:**
- Domain này là gì (Entity, Process, Transaction)?
- Bảng đối trọng: Tên nghiệp vụ ↔ Tên kỹ thuật trong code (giống ADR Ubiquitous Language của STAX)

**C. Data Flow & API Design:**
- Client → Controller → Use Case → Domain → Repository → DB
- API endpoint nào cần thiết? (Method, Path, Permission)

**D. Cross-module dependencies:**
- Module này cần gọi module nào qua Port/Interface?
- Module này có phát Domain Event không? Event nào?

**E. Multi-tenancy:**
- Dữ liệu có cần lọc theo `organizationId` không?
- Có trường hợp nào cần bypass tenant isolation không (ví dụ: STAX Internal Admin)?

**F. Security (`_actions` / Server-Driven UI):**
- Những Entity nào cần trả về `_actions` cho Frontend?
- Logic phán xử `_actions` dựa trên trạng thái + Role như thế nào?

**[🛑 HARD STOP]:** DỪNG TRẢ LỜI. Thêm dòng: _"Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết."_

---

### Bước 2️⃣: Kế hoạch Kiến trúc Chi tiết (Tạo `01_be_implementation_plan.md`)

**A. Database Schema** — Drizzle ORM
- Tên bảng (snake_case, số nhiều)
- Các cột: kiểu dữ liệu, nullable, default, FK
- pgEnum cần tạo mới
- Indexes (composite index cho multi-tenancy + status)
- Migrate strategy: `drizzle-kit generate` hay `quick-fix.ts`?

**B. Domain Layer** — Không phụ thuộc Framework
- Entity/Aggregate: Props interface, Rich Domain Methods
- Value Objects (nếu có)
- Domain Events (nếu có): implement `IAuditableEvent`
- Repository Interface (Port): `Symbol` token + Interface

**C. Infrastructure Layer** — Framework-aware
- Drizzle Schema file path
- Mapper: `toDomain()` ↔ `toPersistence()`
- Repository Implementation: kế thừa `DrizzleBaseRepository`
- Sử dụng `mapToUpdate()` để bảo vệ immutable fields

**D. Application Layer** — Orchestration only
- Service methods: tên, input, output
- Transaction boundary: bọc gì trong `txManager.runInTransaction()`?
- Cross-module calls: gọi Port/Interface nào?
- Domain Events publish: ở đâu trong flow?

**E. Presentation Layer & Contracts** — HTTP/Swagger/Zod
- Shared Contracts: Cập nhật Zod schema tại `shared/contracts/`
- Controller: route, method, permission decorator
- Request DTO: validation rules (`class-validator` hoặc `zod`)
- Response DTO: fields trả về, `_actions` structure nếu cần
- Swagger annotations

**F. Module Wiring** — NestJS Module
- `providers`: DI binding (Symbol → Implementation)
- `imports`: Module dependencies
- `exports`: Những gì expose ra ngoài qua `index.ts`

**[🛑 HARD STOP]:** DỪNG TRẢ LỜI. Thêm dòng: _"Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist."_

---

### Bước 3️⃣: Checklist Thực thi (Tạo `02_be_tasks.md`)

Trình tự BẮT BUỘC:

```
[ ] 1. Shared Contracts (Zod tại shared/contracts/)
[ ] 2. Database Schema (schema file + index export)
[ ] 3. pgEnum definitions
[ ] 4. Run migration (drizzle-kit generate / quick-fix)
[ ] 5. Domain Entity + Props interface
[ ] 6. Value Objects (nếu có)
[ ] 7. Repository Interface (Port + DI Token)
[ ] 8. Domain Events (nếu có)
[ ] 9. Mapper (toDomain + toPersistence)
[ ] 10. Repository Implementation (DrizzleXxxRepository)
[ ] 11. Application Service
[ ] 12. Request/Response DTOs
[ ] 13. Controller
[ ] 14. Module Wiring + index.ts export
[ ] 15. Unit Test (Service — mock repositories)
[ ] 16. Integration Test (Repository — PGLite)
[ ] 17. npm run build — 0 TypeScript error
[ ] 18. Manual API test via Swagger
```

**[🛑 HARD STOP]:** DỪNG TRẢ LỜI. Hỏi: _"Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?"_

---

### Bước 4️⃣: Báo cáo & Lưu trữ (Tạo `03_be_walkthrough.md`)

Chỉ làm SAU KHI code xong và `npm run build` pass.

BẮT BUỘC xuất theo template:

```markdown
## 1. Tóm tắt tính năng (Feature Summary)
- Tier: [1/2/3] — [Tên module]
- Endpoints đã tạo: [danh sách]
- Tables/Enums mới: [danh sách]

## 2. Quyết định kiến trúc (Architecture Decisions)
- Tại sao chọn pattern này?
- Transaction boundary được đặt ở đâu và tại sao?
- Domain Events nào được phát? Handler nào lắng nghe?

## 3. Khó khăn & Xử lý (Troubleshooting)
- Lỗi TypeScript hoặc Drizzle gặp phải và cách fix.
- Vấn đề PGLite / Migration nếu có.

## 4. Bàn giao cho Frontend (Frontend Handoff)
- File Contract Zod cần lấy: `shared/contracts/xxx.ts`
- Cấu trúc `_actions` API trả về cho Server-Driven UI.
```

**Lưu trữ:** Move thư mục sang `docs/history/` (nếu đây là module chạy độc lập).

---

## 4. Cẩm nang Mẫu (Cheat Sheet & Mandatory Patterns)

Khi viết code, BẮT BUỘC tuân theo các mẫu sau. Không được tự bịa format khác.

### A. Database Schema (Drizzle)

```typescript
// src/database/schema/{domain}/{entity}.schema.ts
import { pgTable, bigserial, varchar, text, boolean, timestamp, integer, bigint } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { myStatusEnum } from './enums';

export const myEntities = pgTable('my_entities', {
  id:             bigserial('id', { mode: 'number' }).primaryKey(),
  organizationId: bigint('organization_id', { mode: 'number' }).notNull(),
  name:           varchar('name', { length: 255 }).notNull(),
  status:         myStatusEnum('status').notNull().default('ACTIVE'),
  metadata:       text('metadata'),                      // JSONB nếu cần hybrid storage
  createdAt:      timestamp('created_at').defaultNow().notNull(),
  updatedAt:      timestamp('updated_at').defaultNow().notNull(),
}, (t) => ({
  orgIdx:    uniqueIndex('idx_my_entities_org_name').on(t.organizationId, t.name),
  statusIdx: index('idx_my_entities_status').on(t.organizationId, t.status),
}));
```

### B. pgEnum

```typescript
// Luôn khai báo pgEnum trong file schema, export ra dùng chung
import { pgEnum } from 'drizzle-orm/pg-core';

export const myStatusEnum = pgEnum('my_status_enum', ['ACTIVE', 'INACTIVE', 'ARCHIVED']);
export type MyStatus = typeof myStatusEnum.enumValues[number];
```

### C. Domain Entity (Rich Domain Model)

```typescript
// src/modules/{domain}/domain/entities/{entity}.entity.ts
// TUYỆT ĐỐI không import NestJS hay Drizzle ở đây

export interface MyEntityProps {
  id?: number;
  organizationId: number;
  name: string;
  status: MyStatus;
  createdAt?: Date;
  updatedAt?: Date;
}

export class MyEntity {
  private _id?: number;
  private _organizationId: number;
  private _name: string;
  private _status: MyStatus;
  private _createdAt?: Date;
  private _updatedAt?: Date;

  constructor(props: MyEntityProps) {
    this._id = props.id;
    this._organizationId = props.organizationId;
    this._name = props.name;
    this._status = props.status ?? 'ACTIVE';
    this._createdAt = props.createdAt;
    this._updatedAt = props.updatedAt;
  }

  // --- Getters ---
  get id() { return this._id; }
  get organizationId() { return this._organizationId; }
  get name() { return this._name; }
  get status() { return this._status; }

  // --- Business Methods (Invariants) ---
  archive(): void {
    if (this._status === 'ARCHIVED') {
      throw new BusinessRuleValidationException('Entity đã bị lưu trữ.');
    }
    this._status = 'ARCHIVED';
    this._updatedAt = new Date();
  }

  rename(newName: string): void {
    if (!newName?.trim()) {
      throw new BusinessRuleValidationException('Tên không được để trống.');
    }
    this._name = newName.trim();
    this._updatedAt = new Date();
  }
}
```

### D. Repository Interface (Port + DI Token)

```typescript
// src/modules/{domain}/domain/repositories/{entity}.repository.ts
import { PaginatedResult } from '@core/shared/application/pagination/pagination.types';

// Token và Interface PHẢI cùng tên — pattern Declaration Merging
export const IMyEntityRepository = Symbol('IMyEntityRepository');

export interface IMyEntityRepository {
  findById(id: number, orgId: number): Promise<MyEntity | null>;
  findAll(filters: MyEntityFilters, orgId: number): Promise<PaginatedResult<MyEntity>>;
  save(entity: MyEntity, tx?: Transaction): Promise<MyEntity>;
  delete(id: number, tx?: Transaction): Promise<void>;
}
```

### E. Mapper

```typescript
// src/modules/{domain}/infrastructure/mappers/{entity}.mapper.ts
import { InferSelectModel } from 'drizzle-orm';
import { myEntities } from '@database/schema';

type MyEntityRecord = InferSelectModel<typeof myEntities>;

export class MyEntityMapper {
  static toDomain(record: MyEntityRecord): MyEntity {
    return new MyEntity({
      id:             record.id,
      organizationId: record.organizationId,
      name:           record.name,
      status:         record.status,
      createdAt:      record.createdAt,
      updatedAt:      record.updatedAt,
    });
  }

  static toPersistence(entity: MyEntity): Omit<MyEntityRecord, 'id' | 'createdAt'> {
    return {
      organizationId: entity.organizationId,
      name:           entity.name,
      status:         entity.status,
      updatedAt:      new Date(),
    };
  }
}
```

### F. Repository Implementation

```typescript
// src/modules/{domain}/infrastructure/persistence/drizzle-{entity}.repository.ts
import { Injectable } from '@nestjs/common';
import { DrizzleBaseRepository } from '@core/shared/infrastructure/persistence/drizzle-base.repository';

@Injectable()
export class DrizzleMyEntityRepository
  extends DrizzleBaseRepository
  implements IMyEntityRepository
{
  async findById(id: number, orgId: number): Promise<MyEntity | null> {
    const db = this.getDb();
    const result = await db
      .select()
      .from(myEntities)
      .where(and(eq(myEntities.id, id), eq(myEntities.organizationId, orgId)))
      .limit(1);

    return result[0] ? MyEntityMapper.toDomain(result[0]) : null;
  }

  async save(entity: MyEntity, tx?: Transaction): Promise<MyEntity> {
    const db = this.getDb(tx);
    const data = MyEntityMapper.toPersistence(entity);

    if (entity.id) {
      // UPDATE: dùng mapToUpdate để bảo vệ immutable fields
      await db
        .update(myEntities)
        .set(this.mapToUpdate(data))
        .where(eq(myEntities.id, entity.id));
      return entity;
    }

    // INSERT
    const [inserted] = await db
      .insert(myEntities)
      .values(data)
      .returning();
    return MyEntityMapper.toDomain(inserted);
  }
}
```

### G. Application Service (Orchestration Only)

```typescript
// src/modules/{domain}/application/services/{entity}.service.ts
import { Injectable, Inject } from '@nestjs/common';
import { ITransactionManager } from '@core/shared/application/ports/transaction-manager.port';
import { IEventBus } from '@core/shared/application/ports/event-bus.port';

@Injectable()
export class MyEntityService {
  constructor(
    @Inject(IMyEntityRepository) private readonly repo: IMyEntityRepository,
    @Inject('ITransactionManager') private readonly txManager: ITransactionManager,
    @Inject('IEventBus') private readonly eventBus: IEventBus,
  ) {}

  async create(dto: CreateMyEntityDto, orgId: number): Promise<MyEntity> {
    // Validation logic (nếu cần check duplicate)
    const existing = await this.repo.findByName(dto.name, orgId);
    if (existing) {
      throw new BusinessRuleValidationException(`Tên "${dto.name}" đã tồn tại.`);
    }

    return this.txManager.runInTransaction(async (tx) => {
      const entity = new MyEntity({
        organizationId: orgId,
        name: dto.name,
        status: 'ACTIVE',
      });

      const saved = await this.repo.save(entity, tx);

      // Fire-and-forget audit log — KHÔNG await trực tiếp
      this.auditLog.log({ ... }).catch(() => {});

      // Publish domain event SAU transaction
      await this.eventBus.publish(new MyEntityCreatedEvent(saved));

      return saved;
    });
  }
}
```

### H. Module Wiring

```typescript
// src/modules/{domain}/{domain}.module.ts
import { Module } from '@nestjs/common';
import { IMyEntityRepository } from './domain/repositories/my-entity.repository';
import { DrizzleMyEntityRepository } from './infrastructure/persistence/drizzle-my-entity.repository';
import { MyEntityService } from './application/services/my-entity.service';
import { MyEntityController } from './infrastructure/controllers/my-entity.controller';

@Module({
  controllers: [MyEntityController],
  providers: [
    MyEntityService,
    { provide: IMyEntityRepository, useClass: DrizzleMyEntityRepository },
  ],
  exports: [
    MyEntityService,
    IMyEntityRepository,    // Export Symbol, không export Class
  ],
})
export class MyEntityModule {}
```

### I. Public API (index.ts)

```typescript
// src/modules/{domain}/index.ts
// CHỈ export những gì module khác được phép dùng
export * from './application/dtos/my-entity.dto';
export * from './application/ports/my-entity-service.port';  // nếu cần Port
export { MyEntityModule } from './my-entity.module';
```

---

## 5. Hiến pháp Hệ thống (Do This, NOT That)

| Lĩnh vực | ❌ CẤM LÀM (NOT THAT) | ✅ BẮT BUỘC LÀM (DO THIS) |
| :--- | :--- | :--- |
| **Data Scope** | Cấm hardcode ẩn/hiện dữ liệu danh sách khách hàng tại Client dựa trên `organizationId`. | BẮT BUỘC nhận diện ngữ cảnh: User của "Công ty chủ quản STAX" sẽ được xem nhiều tổ chức (dựa trên Role/Gán chăm sóc). Frontend chỉ render những gì API trả về, lọc dữ liệu là việc của Backend. |
| **Domain Purity** | Import `@nestjs/common`, Drizzle vào Domain Entity. | Domain Entity chỉ dùng TypeScript thuần. |
| **DI Token** | `@Inject(DrizzleMyEntityRepository)` (inject class). | `@Inject(IMyEntityRepository)` (inject Symbol). |
| **Shared Contracts** | Để DTO rải rác trong `src/modules/...` không chia sẻ được với FE. | BẮT BUỘC định nghĩa Zod Schema tại `shared/contracts/` để Frontend dùng. Đây là Source of Truth. |
| **Exception** | Throw `NotFoundException`, `BadRequestException` trong Service/Domain. | Throw `EntityNotFoundException`, `BusinessRuleValidationException` từ `@core/shared`. |
| **Transaction** | Truyền `tx` qua từng tầng thủ công, tự gọi `db.transaction()`. | Bọc logic trong `txManager.runInTransaction()`. |
| **Audit Log** | `await this.auditLog.log(...)` ngay trong transaction chính. | `this.auditLog.log(...).catch(() => {})` — fire-and-forget. |
| **Domain Event** | Publish event TRONG `runInTransaction()`. | Publish event SAU khi transaction hoàn tất. |
| **Update Safety** | `.set(fullEntityData)` — ghi đè cả `id`, `createdAt`. | `.set(this.mapToUpdate(data))` — bảo vệ immutable fields. |
| **Cross-module** | Import `DrizzleLeadRepository` vào `FinoteService`. | Inject `ILeadRepository` (Port/Interface) thông qua DI. |
| **Tenant Isolation** | `?orgId=xxx` từ Query String để filter data nhạy cảm. | Lấy `organizationId` từ `currentUser` trong JWT/Session. |
| **Status Logic** | `if (status === 'PENDING') allowApprove = true` trong Controller. | Tính `_actions` trong DTO Mapper dựa trên Entity state + User role. |
| **Enum** | `status: string` — lưu text tự do. | `status: pgEnum(...)` — ràng buộc cứng ở DB level. |
| **Entity Leak** | Return raw Drizzle record trực tiếp từ Controller. | Luôn qua Mapper → Domain Entity → Response DTO. |

---

## 6. Tiêu chí Nghiệm thu (Strict Exit Criteria)

Trước khi báo cáo "Xong", bạn PHẢI tự audit toàn bộ list sau:

1. [ ] **TypeScript:** `npm run build` pass — 0 error, 0 `any`.
2. [ ] **Domain Purity:** `grep -r "@nestjs\|drizzle-orm" src/modules/{domain}/domain/` → kết quả trống.
3. [ ] **Tenant Isolation:** Mọi query đều có `.where(eq(table.organizationId, orgId))`.
4. [ ] **Immutable Fields:** Mọi UPDATE đều dùng `this.mapToUpdate()`, không ghi đè `id`/`createdAt`.
5. [ ] **Exception Compliance:** `grep -r "NotFoundException\|BadRequestException\|ForbiddenException" src/modules/{domain}/` → chỉ được xuất hiện ở `infrastructure/filters/`, không có trong `domain/` hay `application/`.
6. [ ] **Audit Log Fire-and-forget:** Mọi `auditLog.log()` đều có `.catch(() => {})`, không có `await` đứng một mình.
7. [ ] **Shared Contracts:** Mọi Request/Response quan trọng đều có schema map tương ứng trong `shared/contracts/`.
8. [ ] **Unit Test:** Service spec pass với mocked repositories.
9. [ ] **Integration Test:** Repository spec pass trên PGLite.
10. [ ] **Console sạch:** Không có `console.error` / `console.warn` khi chạy test.
11. [ ] **Quy trình:** Đã xuất `03_be_walkthrough.md` đúng template.
