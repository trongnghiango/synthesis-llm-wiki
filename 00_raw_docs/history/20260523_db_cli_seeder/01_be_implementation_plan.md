# Detailed Architectural Implementation Plan: Database CLI Seeder & Utility Tool

## A. Database Schema & Migration Strategy
- Không có bảng mới được tạo cho tính năng này.
- Các command script chỉ thao tác CRUD trực tiếp lên các bảng hiện hữu (như `users`, `employees`, v.v.) thông qua Drizzle ORM.
- **Migration:** Không yêu cầu migration.

## B. Domain Layer & Pure Core Setup
Do CLI là một công cụ hạ tầng Tier 1, không tạo thêm Domain Entity cụ thể hay Aggregate nào. Tất cả logic nghiệp vụ của các script được định nghĩa ở dạng Command script độc lập, giữ nguyên cấu trúc schema của hệ thống.

## C. Infrastructure Layer & Direct Drizzle DB Client
Chúng ta sẽ tạo thư mục `backend/scripts/` và `backend/scripts/commands/` để chứa mã nguồn.

### 1. `backend/scripts/db-client.ts`
Khởi tạo Pool kết nối PostgreSQL và Drizzle Client độc lập.

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as dotenv from 'dotenv';
import * as path from 'path';
import * as schema from '../src/database/schema';

// Tự động load biến môi trường dựa trên NODE_ENV
const envFile = process.env.NODE_ENV ? `.env.${process.env.NODE_ENV}` : '.env';
dotenv.config({ path: path.resolve(process.cwd(), envFile) });

if (!process.env.DATABASE_URL && !process.env.DB_HOST) {
  throw new Error('❌ LỖI: Không tìm thấy cấu hình môi trường Database!');
}

const connectionString = process.env.DATABASE_URL;
const poolConfig = connectionString
  ? { connectionString }
  : {
      host: process.env.DB_HOST,
      port: Number(process.env.DB_PORT || 5432),
      user: process.env.DB_USERNAME,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
    };

export const pool = new Pool(poolConfig);
export const db = drizzle(pool, { schema });
```

---

## D. Base Interface for Commands

### 2. `backend/scripts/commands/base.command.ts`
```typescript
import { Command } from 'commander';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import * as schema from '../../src/database/schema';

export interface CliCommand {
  name: string;
  description: string;
  setup?: (program: Command) => void;
  action: (options: any, db: NodePgDatabase<typeof schema>) => Promise<void>;
}
```

---

## E. Presentation Layer (CLI Entrypoint & Command Implementation)

### 3. `backend/scripts/commands/seed-users.command.ts`
Implement lệnh seed users mẫu:
```typescript
import { Command } from 'commander';
import { CliCommand } from './base.command';
import * as schema from '../../src/database/schema';
import { count } from 'drizzle-orm';

export const seedUsersCommand: CliCommand = {
  name: 'seed:users',
  description: 'Gieo dữ liệu (seed) người dùng mẫu cho môi trường Phát triển',
  
  setup(cmd: Command) {
    cmd
      .option('-c, --clean', 'Xóa tất cả người dùng hiện tại trước khi gieo dữ liệu', false)
      .option('-n, --count <number>', 'Số lượng người dùng mẫu muốn tạo', '5');
  },

  async action(options: { clean: boolean; count: string }, db) {
    const userCount = parseInt(options.count, 10);
    console.log(`⏳ Đang thực thi seed:users... (Số lượng: ${userCount})`);

    if (options.clean) {
      console.log('🧹 Đang xóa sạch dữ liệu bảng users cũ...');
      await db.delete(schema.users);
      console.log('✅ Đã dọn sạch bảng users.');
    }

    const seedData = Array.from({ length: userCount }).map((_, index) => {
      const id = `usr_seed_${Date.now()}_${index}`;
      return {
        id,
        email: `dev.user.${index + 1}@stax.dev`,
        password: '$2b$10$EPf9XJdb897T6u4n.o822uQ9p1JEq.8x8V5mK0U3h7W9Y5qCq/5pG', // bcrypt mock của 'password123'
        fullName: `STAX Developer ${index + 1}`,
        status: 'ACTIVE' as const,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
    });

    console.log(`📝 Đang insert ${seedData.length} người dùng mẫu vào database...`);
    await db.insert(schema.users).values(seedData);

    const [{ value: totalUsers }] = await db.select({ value: count() }).from(schema.users);
    console.log(`🎉 Gieo dữ liệu thành công! Tổng số người dùng hiện tại: ${totalUsers}`);
  }
};
```

### 4. `backend/scripts/cli.ts`
CLI Dispatcher chính, load tất cả các commands và thực thi.
```typescript
import { Command } from 'commander';
import { db, pool } from './db-client';
import { seedUsersCommand } from './commands/seed-users.command';
import { CliCommand } from './commands/base.command';

const program = new Command();

program
  .name('stax-cli')
  .description('Bộ công cụ CLI quản trị database và tác vụ tiện ích của STAX Backend')
  .version('1.0.0');

const commands: CliCommand[] = [
  seedUsersCommand,
];

for (const cmd of commands) {
  const cliCmd = program
    .command(cmd.name)
    .description(cmd.description);

  if (cmd.setup) {
    cmd.setup(cliCmd);
  }

  cliCmd.action(async (options) => {
    try {
      await cmd.action(options, db);
    } catch (error) {
      console.error(`❌ Lỗi khi thực thi lệnh [${cmd.name}]:`, error);
      process.exit(1);
    } finally {
      await pool.end();
    }
  });
}

program.parse(process.argv);
```

---

## F. NPM Package Scripts Update
Cập nhật `backend/package.json` để thêm các alias script giúp lập trình viên chạy tiện lợi.

```json
"cli": "tsx scripts/cli.ts",
"db:seed": "tsx scripts/cli.ts seed:users"
```

---

Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist (Bước 3).
