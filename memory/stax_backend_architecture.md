---
name: stax-backend-architecture
description: Reference design patterns for NestJS + Drizzle + DDD/Clean Architecture extracted from STAX_ASP
metadata: 
  node_type: memory
  type: reference
  originSessionId: f7c0515d-478f-4eda-94ac-3f8a719a2589
---

# STAX Backend Architecture Patterns (DDD & Clean Architecture Reference)

This memory serves as the canonical reference for designing and implementing NestJS Backend services according to the DDD and Clean Architecture standards established in the `STAX_ASP` codebase.

## 1. Domain Layer Patterns (Pure TypeScript)

*   **Location:** `src/modules/{domain}/domain/`
*   **Purity Rule:** Absolutely NO framework-specific imports (e.g., NestJS, Drizzle-ORM, or TypeORM decorators). Only raw TS.

### Rich Domain Entity Pattern
Entities must contain both state and business logic invariants. Use Props interfaces for initialization.

```typescript
// domain/entities/session.entity.ts
export interface SessionProps {
  id?: string;
  userId: number;
  token: string;
  refreshToken: string;
  expiresAt: Date;
  ipAddress?: string;
  userAgent?: string;
  createdAt?: Date;
}

export class Session {
  public id?: string;
  public userId: number;
  public token: string;
  public refreshToken: string;
  public expiresAt: Date;
  public ipAddress?: string;
  public userAgent?: string;
  public createdAt?: Date;

  constructor(props: SessionProps) {
    this.id = props.id;
    this.userId = props.userId;
    this.token = props.token;
    this.refreshToken = props.refreshToken;
    this.expiresAt = props.expiresAt;
    this.ipAddress = props.ipAddress;
    this.userAgent = props.userAgent;
    this.createdAt = props.createdAt;
  }

  isExpired(): boolean {
    return new Date() > this.expiresAt;
  }
}
```

### Repository Interface (Port)
Define interfaces using Symbol tokens to leverage NestJS Dependency Inversion.

```typescript
// domain/repositories/session.repository.ts
import { Session } from '../entities/session.entity';

export const ISessionRepository = Symbol('ISessionRepository');

export interface ISessionRepository {
  create(session: Session): Promise<void>;
  findByUserId(userId: number): Promise<Session[]>;
  deleteByUserId(userId: number): Promise<void>;
  findByRefreshToken(refreshToken: string): Promise<Session | null>;
  update(id: string, data: Partial<Session>): Promise<void>;
  findByToken(token: string): Promise<Session | null>;
  deleteByToken(token: string): Promise<void>;
}
```

---

## 2. Infrastructure Layer Patterns (Framework Aware)

*   **Location:** `src/modules/{domain}/infrastructure/`
*   **Libraries:** NestJS, Drizzle ORM.

### Mapper Pattern (Entity ↔ Record)
Mappers isolate the database details (e.g., snake_case database schema fields, json formats) from the domain objects.

```typescript
// infrastructure/persistence/mappers/session.mapper.ts
import { InferSelectModel } from 'drizzle-orm';
import { Session } from '../../../domain/entities/session.entity';
import { sessions } from '@database/schema';

type SessionRecord = InferSelectModel<typeof sessions>;

export class SessionMapper {
  static toDomain(raw: SessionRecord | null): Session | null {
    if (!raw) return null;

    return new Session({
      id: raw.id,
      userId: Number(raw.userId),
      token: raw.token,
      refreshToken: raw.refreshToken,
      expiresAt: raw.expiresAt,
      ipAddress: raw.ipAddress || undefined,
      userAgent: raw.userAgent || undefined,
      createdAt: raw.createdAt || undefined,
    });
  }

  static toPersistence(domain: Session) {
    return {
      id: domain.id,
      userId: domain.userId,
      token: domain.token,
      refreshToken: domain.refreshToken,
      expiresAt: domain.expiresAt,
      ipAddress: domain.ipAddress || null,
      userAgent: domain.userAgent || null,
      createdAt: domain.createdAt || new Date(),
    };
  }
}
```

### Repository Implementation (Adapter)
Inherit `DrizzleBaseRepository` and execute raw SQL-like Drizzle commands.

```typescript
// infrastructure/persistence/drizzle-session.repository.ts
import { Injectable } from '@nestjs/common';
import { eq } from 'drizzle-orm';
import { ISessionRepository } from '../../domain/repositories/session.repository';
import { Session } from '../../domain/entities/session.entity';
import { DrizzleBaseRepository } from '@core/shared/infrastructure/persistence/drizzle-base.repository';
import { sessions } from '@database/schema';
import { SessionMapper } from './mappers/session.mapper';

@Injectable()
export class DrizzleSessionRepository
  extends DrizzleBaseRepository
  implements ISessionRepository 
{
  async create(session: Session): Promise<void> {
    const db = this.getDb();
    const data = SessionMapper.toPersistence(session);

    if (data.id) {
      await db.insert(sessions).values(data as any);
    } else {
      const { id, ...insertData } = data;
      await db.insert(sessions).values(insertData as typeof sessions.$inferInsert);
    }
  }

  async findByUserId(userId: number): Promise<Session[]> {
    const results = await this.db
      .select()
      .from(sessions)
      .where(eq(sessions.userId, userId));
    return results.map((r) => SessionMapper.toDomain(r)!);
  }
  
  // Implementation of findByRefreshToken, deleteByUserId, etc.
}
```

---

## 3. NestJS Module Wiring

Glue components together by providing the interface symbol mapped to the concrete implementation class. Export the **Symbol**, not the raw Repository class!

```typescript
// auth.module.ts
import { Module } from '@nestjs/common';
import { AuthenticationService } from './application/services/authentication.service';
import { AuthController } from './infrastructure/controllers/auth.controller';
import { DrizzleSessionRepository } from './infrastructure/persistence/drizzle-session.repository';
import { ISessionRepository } from './domain/repositories/session.repository';

@Module({
  imports: [UserModule],
  controllers: [AuthController],
  providers: [
    AuthenticationService,
    { provide: ISessionRepository, useClass: DrizzleSessionRepository },
  ],
  exports: [AuthenticationService, ISessionRepository],
})
export class AuthModule {}
```

## 4. Key Lessons & Failure Prevention
- **Unit of Work Transactions:** Always coordinate writes using `ITransactionManager` in the application layer. Keep events and audit logs non-blocking and dispatch them after transaction commits.
- **Drizzle Safety:** Use Drizzle schema constants like `sessions` through global mappings (`@database/schema`) rather than direct file imports to prevent circular dependencies.
- **Dynamic Multi-Tenancy Isolation:** Bảng `sessions` và thực thể `Session` vật lý cố tình **không** lưu `organizationId`. Việc cô lập Tenant động được giải quyết tối giản và tinh tế bằng:
  1. Khi Đăng nhập: `IVisibilityResolverService` tính toán ngữ cảnh dữ liệu (`VisibilityContext`) dựa trên vai trò của User, nhúng nó làm `visibilityContext` vào **JWT Payload**.
  2. Mỗi Request: `JwtStrategy` giải mã JWT Payload, đẩy trực tiếp `VisibilityContext` vào **AsyncLocalStorage (ALS)** thông qua `RequestContextService`.
  3. Tầng Persistence: `DrizzleBaseRepository.applyTenantIsolation()` tự động lấy `VisibilityContext` từ ALS để áp dụng mệnh đề điều kiện `where` cho các truy vấn có trường `organizationId`, `tenantId`, hoặc bảng `organizations` tự thân (`table.id`) mà không cần truyền thủ công.
- **Tenant Scope Enforcement:** In multi-tenant scopes, repository functions MUST check for `organizationId` or `tenantId` from the context or parameters via `applyTenantIsolation(conditions, table)`. Bảng `organizations` được lọc an toàn dựa trên chính khóa `id` của nó khi phát hiện `'organizationName' in table`. Bảng `finotes` được cô lập bằng cột `tenantId` khi phát hiện `'tenantId' in table`.
