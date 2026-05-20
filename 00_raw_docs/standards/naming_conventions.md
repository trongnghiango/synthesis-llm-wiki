---
title: "Quy chuẩn Đặt tên"
description: "Quy định đặt tên đồng bộ cho tệp tin, lớp, biến, API và CSDL trong dự án STAX"
tags: [standards, naming, conventions, styles]
last_updated: "2026-05-21"
---

# Quy tắc đặt tên (Naming Conventions)

Tài liệu này quy định cách đặt tên cho các thành phần trong dự án nhằm đảm bảo tính nhất quán và dễ đọc cho cả người và AI.

## 1. Thư mục và Tệp tin
- **Thư mục**: Sử dụng `kebab-case` (ví dụ: `shared-ui`, `lead-detail`).
- **Tệp tin Component**: Sử dụng `kebab-case` hoặc `PascalCase` (ưu tiên `kebab-case` cho đồng bộ với folder, nhưng React Component thường dùng `PascalCase` trong code).
- **Tệp tin Logic (JS/TS)**: Sử dụng `kebab-case` (ví dụ: `http-client.ts`, `crm.api.ts`).

## 2. Biến và Hàm
- **Biến/Hàm**: Sử dụng `camelCase` (ví dụ: `isLoading`, `fetchLeads`).
- **Hằng số**: Sử dụng `SCREAMING_SNAKE_CASE` (ví dụ: `MAX_RETRY_COUNT`).
- **Boolean**: Nên bắt đầu bằng `is`, `has`, `should` (ví dụ: `isActive`, `hasPermission`).

## 3. React Specific
- **Components**: Sử dụng `PascalCase` (ví dụ: `Button`, `LeadCard`).
- **Hooks**: Sử dụng `camelCase` bắt đầu bằng `use` (ví dụ: `useAuth`, `useLeads`).
- **Props**: Sử dụng `camelCase`.

## 4. Database & API (Shared Contracts)
- **Schema/Interfaces**: Sử dụng `PascalCase` (ví dụ: `LeadDto`, `UserStatus`).
- **API Endpoints**: Sử dụng `kebab-case` cho path (ví dụ: `/api/crm/lead-activities`).

---
*Mọi tệp tin mới được tạo ra phải tuân thủ đúng định dạng này.*
