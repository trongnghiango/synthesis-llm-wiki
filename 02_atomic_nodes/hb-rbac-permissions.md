---
id: hb-rbac-permissions
title: Phân quyền vai trò tĩnh (RBAC Permissions)
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on: []
summary: "Đặc tả kỹ thuật thiết lập quyền hạn tĩnh định dạng domain:resource:action và bảo vệ tài nguyên qua Guard."
tags: [handbooks, rbac, permissions, security, guards]
---

# Phân quyền vai trò tĩnh (RBAC Permissions)

STAX sử dụng cơ chế RBAC tĩnh làm lớp phòng thủ đầu tiên chặn đứng các request không hợp lệ ngay tại cổng vào của API (NestJS Controllers).

## 1. Định cấu trúc Quyền (Permission Syntax)
Mỗi quyền hạn trong hệ thống bắt buộc được định nghĩa dưới dạng một chuỗi văn bản thuần có cấu trúc 3 phần phân tách bằng dấu hai chấm:
`[domain]:[resource]:[action]`

*   `domain`: Bounded context lớn (e.g. `crm`, `hrm`, `accounting`).
*   `resource`: Tài nguyên cụ thể bên trong module (e.g. `leads`, `employees`, `finotes`).
*   `action`: Hành động thực thi (`read`, `create`, `update`, `delete`, `import`, `export`).
*   *Ví dụ:* `crm:leads:create`, `accounting:finotes:delete`.

## 2. Sử dụng Guard kiểm soát quyền
Lập trình viên sử dụng Decorator `@RequirePermissions` đặt trên đầu của các hàm Controller để kích hoạt việc kiểm soát phân quyền:

```typescript
@Controller('leads')
export class LeadController {
  @Post()
  @RequirePermissions('crm:leads:create') // Chặn thô qua Guard
  async create(@Body() dto: CreateLeadDto) {
    return this.createLeadUseCase.execute(dto);
  }
}
```
*Hệ thống Guard sẽ trích xuất token người dùng, đối chiếu mảng permissions của vai trò (Role) người đó sở hữu với yêu cầu trước khi cho phép đi tiếp.*
