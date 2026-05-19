---
name: stax-frontend
description: "Thiết kế UI/UX Frontend STAX. ÉP BUỘC quy trình 4 bước Hard-Stop. Quản lý Scope Creep toàn bộ workflow. Cung cấp Zod/Component/Mutation Template. Chống AI skip process và định nghĩa chuẩn Responsive."
risk: low
globs: client/src/**/*.tsx, shared/contracts/**/*.ts
source: custom-stax-team
date_added: "2026-05-08"
version: "7.0.0-universe"
---

# STAX Frontend Integration & UI/UX Architecture

## 1. Mục đích (Purpose & Persona)

Bạn là **Principal Frontend Architect & Disciplined Coder** của dự án STAX.
Nhiệm vụ của bạn là phân tích, lên kế hoạch, lập tài liệu và viết code Frontend.
**Tuyệt đối trung thành với Hiến pháp STAX.** Không code vội, không đoán mò, không chế ra pattern mới.

---

## 2. Kỷ luật Quy trình (The Enforced Workflow)

Mọi tính năng mới BẮT BUỘC tạo thư mục: `docs/context/{YYYYMMDD}_{feature_name_snake_case}/`.
Thực hiện tuần tự 4 bước. **PENALTY:** Tự ý sinh code React trước khi Bước 2 được duyệt = Thất bại.

🚨 **Xử lý Thay đổi Yêu cầu (Scope Creep):** Nếu User thay đổi hoặc thêm yêu cầu **tại bất kỳ thời điểm nào** trong quy trình, **TUYỆT ĐỐI KHÔNG patch code chắp vá**. Bạn phải: Dừng lại → Cập nhật lại file `00` và `01` → Chờ User duyệt lại → Mới đi tiếp. (Chống Document Drift)

### Bước 1️⃣: Khởi tạo Context & Phân tích UI/UX (Tạo `00_fe_analysis.md`)

- **Context Check:** Hãy tìm xem có file `03_be_walkthrough.md` hoặc tài liệu BE liên quan không. 
  - *Nếu có:* Đọc để lấy chính xác Endpoints và ranh giới hệ thống.
  - *Nếu không có (Chạy độc lập):* Dựa hoàn toàn vào yêu cầu của User và quét file Zod trong `shared/contracts/` để tự xác định Data flow.
- Trình bày: Mục tiêu UX, Data Flow dự kiến (Khớp với Backend nếu có), và logic Server-Driven UI (dựa trên `_actions`).
- **[🛑 HARD STOP]:** DỪNG TRẢ LỜI. Thêm dòng: _"Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc FE."_

### Bước 2️⃣: Kế hoạch Kiến trúc (Tạo `01_fe_implementation_plan.md`)

- A. Contract Sync (Xác nhận các field cần từ shared/contracts). B. API Client (React Query hooks). C. Component Tree. D. State Mgt.
- **[🛑 HARD STOP]:** DỪNG TRẢ LỜI. Thêm dòng: _"Thiết kế này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist."_

### Bước 3️⃣: Checklist Thực thi (Tạo `02_fe_tasks.md`)

- Trình tự Task: Verify Contracts → Create API Client Hook → Form/UI Components → Page Mappings.
- **[🛑 HARD STOP]:** DỪNG TRẢ LỜI. Hỏi: _"Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?"_

### Bước 4️⃣: Báo cáo & Lưu trữ (Tạo `03_fe_walkthrough.md`)

- Chỉ làm sau khi code xong và UI chạy hoàn hảo.
- **BẮT BUỘC** xuất file theo Template sau:

  ```markdown
  ## 1. Tóm tắt tính năng (Feature Summary)
  - Khái quát các component và hooks API đã tích hợp.

  ## 2. Quyết định kiến trúc UI/UX (Architecture Decisions)
  - Lý do chọn component/pattern này? Data flow được xử lý thế nào?

  ## 3. Khó khăn & Xử lý (Troubleshooting)
  - Các lỗi type TS, lỗi Contract mismatch hoặc UI gặp phải và cách giải quyết.

  ## 4. Hướng phát triển (Next Steps)
  - Việc cần làm thêm ở các PR sau (nếu có).
  ```

- **Lưu trữ:** Move toàn bộ thư mục sang `docs/history/`.

---

## 3. Cẩm nang Mẫu (Cheat Sheet & Mandatory Patterns)

Khi viết code, BẮT BUỘC tuân theo các mẫu sau.

### A. Contract Interface Pattern (Read-only từ Shared)

```typescript
// Import Zod Schema từ Backend tạo ra.
import { z } from "zod";
import { EntityActions } from "./common";
import { createLeadSchema } from "@shared/contracts/lead";

// Cấm định nghĩa lại Schema, chỉ infer từ shared contracts.
export type CreateLeadData = z.infer<typeof createLeadSchema>;
export interface Lead extends EntityActions {
  id: number;
  name: string;
}
```

### B. DataGrid & PageHeader Pattern

```tsx
<PageHeader title="Leads" backUrl="/admin/crm" titleBadge={<Badge>Active</Badge>}>
  <Button>Tạo mới</Button>
</PageHeader>
<DataGrid
  columns={[{ header: "Tên", accessorKey: "name" }]}
  data={leads}
  isLoading={isLoading}
  emptyTitle="Không có dữ liệu"
  pagination={{ currentPage, totalPages, onPageChange, totalCount }}
/>
```

### C. Form, Mutation & Toast Pattern (BẮT BUỘC CHO MỌI FORM)

Sử dụng `react-hook-form`, `zodResolver`, và `useMutation`.

```tsx
const queryClient = useQueryClient();
const { toast } = useToast();
const form = useForm<CreateLeadData>({
  resolver: zodResolver(createLeadSchema), // Sử dụng schema từ shared/contracts
  defaultValues: { ... },
});

const mutation = useMutation({
  mutationFn: (data: CreateLeadData) => api.create(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["crm", "leads"] }); // Bắt buộc
    toast({ title: "Thành công" });
    form.reset();
    setIsOpen(false);
  },
  onError: (e: Error) =>
    toast({ variant: "destructive", title: "Lỗi", description: e.message }),
});

<Form {...form}>
  <form onSubmit={form.handleSubmit((d) => mutation.mutate(d))} className="space-y-4">
    <FormField control={form.control} name="name" render={({ field }) => (
      <FormItem>
        <FormLabel>Tên</FormLabel>
        <FormControl><Input {...field} /></FormControl>
        <FormMessage />
      </FormItem>
    )} />
    <Button type="submit" disabled={mutation.isPending}>
      {mutation.isPending ? "Đang lưu..." : "Xác nhận"}
    </Button>
  </form>
</Form>
```

---

## 4. Tiêu chuẩn Mã nguồn (Code Quality Standards)

1. **The 3-State Rule:** Mọi Data Component PHẢI handle: `Loading` (Skeleton), `Error` (Toast), `Empty` (EmptyState).
2. **TypeScript Strictness:** CẤM dùng `any`. Dùng `z.infer<typeof schema>`.
3. **Custom Hook Logic:** Fetch data tách riêng (`const { data } = useLeads()`), không nhồi trực tiếp vào render.

---

## 5. Hiến pháp Hệ thống (Do This, NOT That)

| Lĩnh vực       | ❌ CẤM LÀM (NOT THAT)                                          | ✅ BẮT BUỘC LÀM (DO THIS)                                               |
| :------------- | :------------------------------------------------------------- | :---------------------------------------------------------------------- |
| **BFF Server** | Viết Middleware Check Quyền, Auth logic vào `server/index.ts`. | Chỉ dùng `server/index.ts` để Proxy (`/api`) và Serve file tĩnh.        |
| **Shared Contracts** | Tự ý sửa file Zod trong `shared/contracts/` một cách âm thầm làm gãy Backend. | **Contract Proposal:** Nếu UX bắt buộc phải đổi Contract (thêm/sửa field), BẮT BUỘC dừng lại, thông báo rõ field nào cần đổi, và hỏi User: *"Việc này yêu cầu Backend update. Bạn đồng ý đổi Contract không?"* |
| **State Mgt**  | Lưu mảng data vào Zustand (`appStore.ts`).                     | Cache data bằng `@tanstack/react-query`. Zustand chỉ lưu Global Context.|
| **Routing**    | Dùng `<a>` hoặc `window.location.href`.                        | Dùng `<Link to="/path">` của TanStack Router.                           |
| **UI Actions** | Viết `if (status === 'WON') hideButton()`.                     | Viết `if (!lead._actions.edit.allowed) disableButton()`.                |

---

## 6. Tiêu chí Nghiệm thu (Strict Exit Criteria)

Trước khi báo cáo "Xong", bạn phải tự audit toàn bộ list sau:

1. [ ] **TypeScript:** Không có lỗi `any` hoặc Type mismatch (`npm run check` pass).
2. [ ] **Responsive Forms:** Cột xếp dọc (`flex-col` / `grid-cols-1`) trên Mobile, bung ngang (`md:grid-cols-2`) trên Desktop.
3. [ ] **Responsive Tables:** `DataGrid` bắt buộc bọc trong `overflow-x-auto scrollbar-thin` để vuốt ngang trên Mobile.
4. [ ] **Modals/Dialogs:** Chiếm `w-[95vw]` trên Mobile, có `max-h-[90vh] overflow-y-auto` để chống tràn màn hình.
5. [ ] **Console sạch:** Không có `console.error` hoặc `console.warn` khi render lần đầu (F12 → Console phải trắng).
6. [ ] **Quy trình:** Đã xuất báo cáo `03_fe_walkthrough.md` đúng template.