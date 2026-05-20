---
id: std-api-contracts
title: Hợp đồng API dùng chung (Zod & Shared Contracts)
layer: 3-atomic
parent: "[[02_standards_governance]]"
depends_on: []
summary: "Quy chuẩn thiết kế API dựa trên hợp đồng dùng chung định nghĩa qua Zod Schema giữa Backend và Frontend."
tags: [standards, api-contracts, zod, validation, communication]
---

# Hợp đồng API dùng chung (Zod & Shared Contracts)

Hệ thống STAX áp dụng triết lý **Contract-Driven Development** (Phát triển hướng hợp đồng) để đồng bộ hóa hoàn toàn luồng giao tiếp giữa Backend (BE) và Frontend (FE).

## 1. Định nghĩa Zod Schema dùng chung
*   Mọi cấu trúc dữ liệu giao tiếp (Request DTO và Response DTO) bắt buộc được định nghĩa dưới dạng **Zod Schema** tại thư mục `shared/contracts/`.
*   Cả BE và FE đều import chung schema này để thực hiện xác thực (validation) dữ liệu:
    *   Backend dùng để parse request payload và gán kiểu tĩnh.
    *   Frontend dùng để validate form đầu vào và cấu hình API client.

## 2. Định dạng phản hồi chuẩn (Standard Envelope)
Tất cả các API của hệ thống bắt buộc phải trả về dữ liệu được đóng gói trong một phong bì (Envelope) tiêu chuẩn:

```typescript
{
  success: boolean;       // Trạng thái thành công hay thất bại
  data: T;                // Dữ liệu payload thực tế (nếu thành công)
  error?: {               // Thông tin lỗi chi tiết (nếu thất bại)
    code: string;         // Mã lỗi định danh (e.g. USER_NOT_FOUND)
    message: string;      // Thông điệp hiển thị cho lập trình viên/user
    details?: Record<string, any>; // Các lỗi chi tiết của từng trường
  }
}
```
*Việc này đảm bảo tính nhất quán tuyệt đối và giúp Frontend viết code xử lý lỗi chung (Global Error Handler) dễ dàng.*
