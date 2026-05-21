---
id: arch-unit-of-work
title: Unit of Work Pattern trong Clean Architecture
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Hướng dẫn áp dụng Unit of Work qua ITransactionManager đảm bảo tính ACID khi điều phối nhiều Repository/Module trong một Use Case."
tags: [architecture, ddd, unit-of-work, transaction, nestjs]
---

## 1. Bản chất & Core Interface
* **Unit of Work (UoW)**: Gom tất cả tác vụ ghi DB trong một Use Case vào một Database Transaction duy nhất. Thất bại một bước -> Rollback toàn bộ để đảm bảo tính toàn vẹn dữ liệu.
* **Interface trừu tượng (`ITransactionManager`):**
```typescript
export interface ITransactionManager {
  runInTransaction<T>(work: (tx: any) => Promise<T>): Promise<T>;
}
```

## 2. Triển khai Use Case Điều phối (Orchestrator)
Use Case nhận `ITransactionManager` và truyền kết nối transaction (`tx`) xuyên suốt qua các Repository của các Module khác nhau:

```typescript
@Injectable()
export class OnboardEmployeeUseCase {
  constructor(
    @Inject(ITransactionManager) private readonly txManager: ITransactionManager,
    @Inject(IUserRepository) private readonly userRepo: IUserRepository,
    @Inject(IEmployeeRepository) private readonly employeeRepo: IEmployeeRepository,
  ) {}

  async execute(dto: any): Promise<any> {
    // 1. Validation (Ngoại vi transaction để giảm Lock DB)
    if (!dto.email) throw new BadRequestException('Email invalid');

    // 2. Chạy Unit of Work
    return this.txManager.runInTransaction(async (tx) => {
      const user = await this.userRepo.save(new User(dto), tx); // Truyền tx
      const employee = await this.employeeRepo.save({ userId: user.id, ...dto }, tx); 
      return { user, employee }; // Tự động COMMIT nếu thành công, ROLLBACK nếu quăng Error
    });
  }
}
```

## 3. Quy tắc Thiết kế Bắt buộc
1. **Truyền `tx` bắt buộc**: Quên truyền `tx` vào bất kỳ Repository nào trong block transaction sẽ phá vỡ UoW, gây rác dữ liệu.
2. **Tách biệt Đọc/Ghi**: Tác vụ đọc (Read/Validate) nên đặt bên ngoài `runInTransaction` để tối ưu hiệu năng và tránh deadlock DB.
3. **Use Case siêu mỏng**: Use Case chỉ đóng vai trò nhạc trưởng điều phối. Logic nghiệp vụ lõi (Core Domain Logic) phải nằm ở Domain Entity hoặc Domain Service.