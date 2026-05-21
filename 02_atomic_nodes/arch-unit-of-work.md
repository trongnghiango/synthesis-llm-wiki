---
id: arch-unit-of-work
title: "Thiết kế Unit of Work qua Transaction Manager"
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Đảm bảo tính toàn vẹn dữ liệu (ACID) khi điều phối nhiều Repositories/Modules trong cùng một Use Case bằng Unit of Work."
tags: [architecture, ddd, unit-of-work, transaction, nestjs]
---

### 1. Kiến trúc Unit of Work (UoW)
Giải quyết bài toán bất đồng bộ và nhất quán dữ liệu (Data Inconsistency) khi gọi ghi dữ liệu liên module. UoW hoạt động như một wrapper quanh **Database Transaction**.

```typescript
// Core Port: src/core/shared/application/ports/transaction-manager.port.ts
export interface ITransactionManager {
  runInTransaction<T>(work: (tx: any) => Promise<T>): Promise<T>;
}
```

### 2. Mẫu triển khai Use Case Orchestrator
Use Case đóng vai trò nhạc trưởng điều phối, các Repository nhận tham số `tx` để chạy chung một transaction context.

```typescript
@Injectable()
export class OnboardEmployeeUseCase {
  constructor(
    @Inject(ITransactionManager) private readonly txManager: ITransactionManager,
    @Inject(IUserRepository) private readonly userRepo: IUserRepository,
    @Inject(IEmployeeRepository) private readonly employeeRepo: IEmployeeRepository,
  ) {}

  async execute(dto: any): Promise<any> {
    // 1. Validation ngoài Transaction (Tránh lock DB sớm)
    const exists = await this.userRepo.exists(dto.email);
    if (exists) throw new BadRequestException('Email already exists');

    // 2. Thực thi Unit of Work
    return this.txManager.runInTransaction(async (tx) => {
      const user = await this.userRepo.save(new User(dto), tx); // Truyền 'tx'
      const employee = await this.employeeRepo.save({ userId: user.id, ...dto }, tx);
      return { user, employee };
    }); // Tự động Rollback nếu xảy ra Exception bên trong block
  }
}
```

### 3. Quy tắc vận hành (Golden Rules)
1. **Orchestration Only:** Use Case chỉ điều phối dữ liệu, không chứa core business logic (chuyển dịch logic vào Domain Entity hoặc Domain Service).
2. **Strict Transaction Propagation:** Bắt buộc truyền tham số `tx` vào tất cả hàm ghi (`save`, `update`, `delete`) của Repository nằm trong block UoW.
3. **Read Optimization:** Các câu truy vấn kiểm tra (Read/Validation) nên đặt bên ngoài `runInTransaction` để tối ưu hóa hiệu năng và hạn chế khóa bảng (table lock).