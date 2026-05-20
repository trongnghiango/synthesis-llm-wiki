---
id: hb-drizzle-base-repo
title: Triển khai Repository với Drizzle ORM
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[arch-clean-boundaries]]"
  - "[[arch-als-tenant-isolation]]"
summary: "Hướng dẫn xây dựng Drizzle Repository Adapter kế thừa từ DrizzleBaseRepository kết hợp ánh xạ thực thể qua Mapper."
tags: [handbooks, drizzle, orm, database, mapping, repository]
---

# Triển khai Repository với Drizzle ORM

Lớp Infrastructure thực thi các cổng lưu trữ (Repository Interfaces) của lớp Domain bằng cách sử dụng Drizzle ORM và kế thừa lớp cơ sở `DrizzleBaseRepository`.

## 1. Thừa kế `DrizzleBaseRepository`
`DrizzleBaseRepository` cung cấp sẵn các phương thức CRUD cơ bản được cấu hình an toàn với đa doanh nghiệp (ALS logic).

```typescript
// infrastructure/persistence/repositories/session.repository.ts
import { DrizzleBaseRepository } from '@core/database';
import { ISessionRepository } from '../../../domain/repositories/session.repository';
import { Session } from '../../../domain/entities/session.entity';
import { sessions } from '@database/schema';
import { Injectable } from '@nestjs/common';
import { SessionMapper } from '../mappers/session.mapper';

@Injectable()
export class SessionRepository 
  extends DrizzleBaseRepository<typeof sessions, Session>
  implements ISessionRepository 
{
  constructor() {
    super(sessions, SessionMapper); // Inject table schema và Mapper
  }

  // Hiện thực hóa các query nghiệp vụ đặc thù
  async findByToken(token: string): Promise<Session | null> {
    const record = await this.db
      .select()
      .from(sessions)
      .where(eq(sessions.token, token))
      .limit(1)
      .execute();
      
    return record[0] ? SessionMapper.toDomain(record[0]) : null;
  }
}
```

## 2. Quy tắc Mapper Bắt buộc
Mọi Repository bắt buộc sử dụng một Mapper để chuyển đổi dữ liệu qua lại giữa Domain Entity và Database Record, giữ cho lớp Domain hoàn toàn cô lập khỏi định dạng lưu trữ thực tế.
