# 01. Kế hoạch Kiến trúc Chi tiết: Google Drive Multi-Tenant Cleanup

**Ngày:** 2026-05-22 | **Tier:** 1 — Foundation | **Scope:** Core Infrastructure / Storage

---

## A. Database Schema

Chúng ta sẽ khai báo bảng mới `google_drive_folders` trong file schema hệ thống `backend/src/database/schema/system/attachments.schema.ts` (hoặc tạo file mới `google-drive-folders.schema.ts`).
Để gọn gàng, chúng ta sẽ viết trực tiếp vào file schema mới: `backend/src/database/schema/system/google-drive-folders.schema.ts`.

### 1. Chi tiết Schema bảng `google_drive_folders`
```typescript
import { pgTable, serial, text, timestamp, index, integer, uniqueIndex } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { organizations } from '../crm/organizations.schema';

export const googleDriveFolders = pgTable('google_drive_folders', {
    id: serial('id').primaryKey(),
    
    organizationId: integer('organization_id')
        .notNull()
        .references(() => organizations.id, { onDelete: 'cascade' }),
        
    // Đường dẫn logic ảo dạng: "crm-leads/2026-05" hoặc "root" (thư mục gốc của tenant)
    path: text('path').notNull(),
    
    // ID thật của thư mục này trên Google Drive
    driveFolderId: text('drive_folder_id').notNull().unique(),
    
    createdAt: timestamp('created_at').defaultNow().notNull(),
    updatedAt: timestamp('updated_at').defaultNow().notNull(),
}, (table) => ({
    org_idx: index('idx_gd_folders_org').on(table.organizationId),
    tenant_path_uniq: uniqueIndex('uniq_idx_gd_folders_tenant_path').on(table.organizationId, table.path),
}));

export const googleDriveFoldersRelations = relations(googleDriveFolders, ({ one }) => ({
    organization: one(organizations, {
        fields: [googleDriveFolders.organizationId],
        references: [organizations.id],
    }),
}));
```

### 2. Chiến lược Migrate
Chạy lệnh phát sinh migration của Drizzle:
```bash
pnpm --dir backend db:generate
```
Sau đó áp dụng migrate hoặc push trực tiếp trên môi trường dev:
```bash
pnpm --dir backend db:push
```

---

## B. Domain Layer

### 1. Cập nhật `IFileStoragePort` (`backend/src/modules/system/application/ports/file-storage.port.ts`)
Mở rộng phương thức `uploadFile` để nhận thêm `options` chứa thông tin Tenant và Phân hệ nghiệp vụ:
```typescript
export interface IFileStoragePort {
  uploadFile(
    fileName: string, 
    buffer: Buffer, 
    mimeType?: string,
    options?: {
      organizationId?: number;
      entityType?: string;
      entityId?: number;
    }
  ): Promise<{ fileId: string; webViewLink: string; downloadLink: string }>;
  
  deleteFile(fileId: string): Promise<void>;
}
```

---

## C. Infrastructure Layer

### 1. Hàm dọn dẹp tiếng Việt và chuẩn hóa tên file (`sanitizeFilename`)
Hàm này sẽ được đặt làm helper nội bộ trong `GoogleDriveService`.

### 2. Triển khai `GoogleDriveService` (`backend/src/modules/system/infrastructure/services/google-drive.service.ts`)
- Inject DB connection `NodePgDatabase<typeof schema>` với token `DRIZZLE`.
- Cập nhật phương thức `uploadFile` để:
  1. Nếu `provider === 'local'`, gọi `uploadLocal` bình thường.
  2. Nếu `provider === 'google'`:
     - Phân tích và trích xuất `organizationId`, `entityType`, `entityId`.
     - Lấy thông tin `organizationName` từ bảng `organizations` nếu có `organizationId`.
     - Chạy hàm `sanitizeFilename` để tạo slug sạch sẽ cho tên công ty.
     - Gọi `resolveFolder` để tìm hoặc khởi tạo cây thư mục 3 cấp:
       - Cấp 1: Thư mục gốc của doanh nghiệp (`root` path).
       - Cấp 2: Thư mục phân hệ (ví dụ: `crm-leads`).
       - Cấp 3: Thư mục theo kỳ thời gian dạng `YYYY-MM`.
     - Tạo tên file chuẩn hóa: `[ENTITY_TYPE]_[ENTITY_ID]_[TIMESTAMP]_[SANITIZED_ORIGINAL_NAME].[EXT]`.
     - Upload file lên Google Drive theo đúng ID thư mục đã tìm thấy.

---

## D. Application Layer

### 1. Cập nhật `AttachmentService` (`backend/src/modules/system/application/services/attachment.service.ts`)
- Khi gọi `fileStorage.uploadFile`, truyền đầy đủ `options`:
```typescript
const driveResult = await this.fileStorage.uploadFile(
  file.originalname, 
  file.buffer, 
  file.mimetype,
  {
    organizationId: orgId,
    entityType: entityType,
    entityId: entityId
  }
);
```
- Đảm bảo tên file được lưu trữ trong CSDL khớp với tên file thật được lưu trên Drive (`driveResult.fileName` hoặc tên đã được chuẩn hóa).

---

## E. Presentation Layer & Contracts

Hợp đồng API và DTO hiện tại đã hoàn thiện nên không cần thay đổi lớn. Chúng ta chỉ cần đảm bảo TypeScript biên dịch sạch sẽ không có bất kỳ lỗi nào.

---

## F. Module Wiring

Chúng ta sẽ đăng ký file schema mới `google-drive-folders.schema.ts` vào file chỉ mục `backend/src/database/schema/index.ts` để Drizzle tự động nhận diện và sinh migration.

---

Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
