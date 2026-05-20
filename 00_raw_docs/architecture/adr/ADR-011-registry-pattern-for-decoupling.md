# ADR-011: Giải quyết Circular Dependency bằng Registry Pattern

## Bối cảnh
Trong kiến trúc Clean Architecture của STAX, các module được phân tầng (Tier):
- **Tier 1**: Core/System (SystemModule, AuthModule, RbacModule).
- **Tier 3**: Business Domains (CrmModule, AccountingModule).

Quy tắc phân tầng tuyệt đối cấm Tier thấp (Tier 1) phụ thuộc vào Tier cao (Tier 3). Tuy nhiên, thực tế phát sinh nhu cầu:
1. `SystemModule` (`LookupService`) cần tổng hợp Enum/Master Data từ các module nghiệp vụ.
2. `SystemModule` (`BootstrapService`) cần tổng hợp số liệu Summary từ các module nghiệp vụ để trả về cho Frontend.

Nếu `SystemModule` import `CrmModule` và `AccountingModule`, và ngược lại các module này import `SystemModule` để dùng các dịch vụ hạ tầng (như Google Drive, File Storage), sẽ tạo ra vòng lặp phụ thuộc (**Circular Dependency**), làm sập chuỗi khởi tạo của NestJS.

Việc dùng `forwardRef()` là một giải pháp vá (patch) tạm thời, vi phạm nguyên tắc Clean Architecture và tạo ra Code Smell lớn.

## Quyết định
Chúng tôi quyết định áp dụng **Registry Pattern** (hoặc Plugin Pattern) để đảo ngược phụ thuộc (Inversion of Control) và bẻ gãy Circular Dependency.

### Cơ chế hoạt động:
1. **Module Hạ tầng (Tier 1)**:
   - Định nghĩa một Interface (Port) cho dữ liệu cần thu thập (ví dụ: `ILookupProvider`, `IBootstrapProvider`).
   - Cung cấp một `Registry` service quản lý danh sách các provider.
   - KHÔNG import bất kỳ module Tier 3 nào.
2. **Module Nghiệp vụ (Tier 3)**:
   - Implement Interface (Port) được định nghĩa ở Tier 1.
   - Import module Tier 1 (Hợp lệ).
   - Tự đăng ký (Register) mình với `Registry` của Tier 1 trong hook `onModuleInit`.

### Ví dụ minh họa (Bootstrap Registry):

**Tại SystemModule (Tier 1):**
```typescript
// bootstrap-provider.interface.ts
export interface IBootstrapProvider {
    getSummaryData(tenantId: number): Promise<any>;
}

// bootstrap-registry.service.ts
@Injectable()
export class BootstrapRegistry {
    private providers = new Map<string, IBootstrapProvider>();
    registerProvider(key: string, provider: IBootstrapProvider) {
        this.providers.set(key, provider);
    }
    // ... gọi tất cả provider để tổng hợp dữ liệu
}
```

**Tại CrmModule (Tier 3):**
```typescript
@Injectable()
export class CrmBootstrapProvider implements IBootstrapProvider {
    async getSummaryData(tenantId: number) { ... }
}

@Module({ imports: [SystemModule], ... })
export class CrmModule implements OnModuleInit {
    constructor(
        private readonly registry: BootstrapRegistry,
        private readonly provider: CrmBootstrapProvider
    ) {}
    onModuleInit() {
        this.registry.registerProvider('crm', this.provider);
    }
}
```

## Hệ quả
- **Ưu điểm**:
  - Loại bỏ hoàn toàn lỗi Circular Dependency mà không dùng `forwardRef()`.
  - Giữ vững ranh giới phân tầng (Tier). `SystemModule` không còn biết đến sự tồn tại của `CrmModule` hay `AccountingModule`.
  - Khả năng mở rộng (Extensibility) cao: Khi thêm module mới (ví dụ: `HrmModule`), chỉ cần tạo Provider mới và tự đăng ký, không cần sửa code của `SystemModule`.
- **Nhược điểm**:
  - Tăng độ phức tạp của code do phải tạo thêm Interface và Registry.
  - Cần đảm bảo thứ tự khởi tạo module (NestJS xử lý tốt nếu không có circular).

## Trạng thái
- **Đã phê duyệt** (Approved) - Ngày 13/05/2026.
