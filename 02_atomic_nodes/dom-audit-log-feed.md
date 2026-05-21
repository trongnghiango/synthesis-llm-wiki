---
id: dom-audit-log-feed
title: Chuẩn hóa Audit Log & Activity Feed
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
summary: "Chuẩn hóa hạ tầng Audit Log (Drizzle, camelCase) và triển khai Omnichannel Activity Feed hợp nhất timeline tổ chức."
tags: [audit-log, activity-feed, drizzle, camelcase, onboarding]
---

### 1. Kiến trúc Audit Log & Chuẩn hóa Naming
- **Cơ chế:** Ghi log bất đồng bộ (*fire-and-forget*) qua `DrizzleAuditLogService` kế thừa `AUDIT_LOG_PORT`.
- **Tích hợp:** Áp dụng cho Lead Won, Payment Allocated, Role Assigned, và User Provisioned.
- **Mapping:** Chuyển đổi toàn diện từ `snake_case` (DB) sang `camelCase` (Application/TS) bằng cấu hình map của Drizzle ORM (`[[hb-drizzle-base-repo]]`).
- **Bảng DB:** `audit_logs` (lưu trữ delta-change, hỗ trợ đánh chỉ mục `target_id`, `actor_id` phục vụ truy vấn lịch sử `[[hb-delta-logging]]`).

### 2. Omnichannel Activity Feed
Hệ thống timeline hội tụ dữ liệu từ nhật ký hệ thống tự động (`audit_logs`) và ghi chú tương tác thủ công (`interaction_notes`).

#### Schema & API Contract:
- **Bảng `interaction_notes`:**
  ```typescript
  export const interactionNotes = pgTable('interaction_notes', {
    id: uuid('id').primaryKey().defaultRandom(),
    orgId: uuid('org_id').references(() => organizations.id).notNull(),
    authorId: uuid('author_id').notNull(),
    noteType: text('note_type').$type<'call' | 'meeting' | 'email'>().notNull(),
    content: text('content').notNull(),
    createdAt: timestamp('created_at').defaultNow().notNull()
  });
  ```
- **Service (`ActivityFeedService`):** Hợp nhất và phân trang dữ liệu từ cả `audit_logs` và `interaction_notes`, sắp xếp theo `createdAt` giảm dần.
- **API Endpoint:** `GET /organizations/:orgId/timeline`
  - **Query Params:** `limit: number`, `cursor: string`, `type?: 'system' | 'manual'`
  - **Response:** Mảng các sự kiện đã được định dạng chuẩn giao diện timeline.

### 3. Unified Onboarding Automation
- **Trigger:** Event khách hàng mới kích hoạt thành công (Onboarded).
- **Luồng:** Tự động gửi thông báo chào mừng, thiết lập dữ liệu mặc định, và ghi nhận nhật ký hệ thống thông qua `DrizzleAuditLogService`.