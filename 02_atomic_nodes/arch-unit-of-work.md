---
id: arch-unit-of-work
title: Pattern Unit of Work & Quản lý Giao dịch
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Quy chuẩn áp dụng Unit of Work (UoW) qua ITransactionManager để đảm bảo tính toàn vẹn dữ liệu (ACID) khi điều phối nghiệp vụ liên module."
tags: [architecture, uow, transaction, clean-architecture, ddd]
---

### 1. Kiến trúc Core
Mẫu thiết kế UoW trừu hóa Database Transaction qua `ITransactionManager` nhằm cô lập và đảm bảo tính nguyên tử (Atomicity) cho Use Case liên module.

```typescript
export interface ITransactionManager {
  runInTransaction<T>(work: (tx: any) => Promise<T>): Promise<T>;
}
```

### 2. Mẫu Triển Khai Use Case (Orchestrator)
```typescript
@Injectable()
export class OnboardEmployeeUseCase {
  constructor(
    @Inject(ITransactionManager) private readonly txManager: ITransactionManager,
    @Inject(IUserRepository) private readonly userRepo: IUserRepository,
    @Inject(IEmployeeRepository) private readonly employeeRepo: IEmployeeRepository,
  ) {}

  async execute(dto: any): Promise<any> {
    // 1. Validation ngoài Transaction để tối ưu hiệu năng
    if (await this.userRepo.exists(dto.email)) throw new BadRequestException();

    // 2. Thực thi Unit of Work
    return this.txManager.runInTransaction(async (tx) => {
      const user = await this.userRepo.save(new User(dto), tx); // Bắt buộc truyền tx
      const employee = await this.employeeRepo.save({ userId: user.id, ...dto }, tx);
      return { user, employee };
    });
  }
}
```

### 3. Nguyên Tắc Vàng
1. **Vai trò Use Case:** Chỉ làm nhiệm vụ điều phối (Orchestrator). Logic nghiệp vụ cốt lõi phải nằm ở Domain Entity hoặc Domain Service.
2. **Lan truyền Giao dịch (`tx`):** Mọi thao tác ghi dữ liệu thuộc UoW bắt buộc phải truyền tham số `tx` xuống Repository tương ứng.
3. **Tối ưu hóa khóa (Lock):** Tác vụ đọc/kiểm tra dữ liệu (Read-only validation) nên thực hiện trước/ngoài block `runInTransaction`.
4. **Xử lý ngoại lệ:** Mọi lỗi phát sinh trong block `runInTransaction` phải được throw ra ngoài để trigger tự động Rollback.