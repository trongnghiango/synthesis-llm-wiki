---
id: arch-als-transactions
title: Quản lý Giao dịch ngầm qua ALS (Implicit Transactions)
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Cơ chế quản lý transactional boundaries ngầm định xuyên suốt các Repository gọi trong cùng luồng ALS sử dụng ITransactionManager."
tags: [architecture, database, transactions, als, transaction-manager]
---

# Quản lý Giao dịch ngầm qua ALS (Implicit Transactions)

Trong các hệ thống nghiệp vụ phức tạp, một Use Case có thể gọi nhiều hàm ghi dữ liệu tại các Repository khác nhau. Đảm bảo tính nguyên tử (Atomicity - ACID) yêu cầu tất cả các lệnh này phải chạy chung một giao dịch cơ sở dữ liệu.

## 1. Giao dịch ngầm định (Implicit Transaction Propagation)
*   STAX không yêu cầu truyền tham số `transaction` hoặc `client` thủ công qua các tham số hàm.
*   Tầng Application kiểm soát ranh giới giao dịch thông qua:
    ```typescript
    await this.transactionManager.runInTransaction(async () => {
      await this.employeeRepository.create(employee);
      await this.rbacService.assignRole(employee.id, 'staff');
    });
    ```

## 2. Cách hoạt động bên dưới hạ tầng
*   `ITransactionManager` sử dụng Async Local Storage để lưu trữ thực thể kết nối giao dịch Drizzle DB hiện tại (`DrizzleTransaction`).
*   Khi Repository thực hiện các hành động ghi hoặc đọc, nó sẽ kiểm tra xem trong ALS hiện tại có chứa kết nối giao dịch (`DrizzleTransaction`) đang mở hay không.
*   Nếu có, Repository sẽ tự động dùng kết nối đó để truy vấn. Nếu không có, Repository sẽ dùng kết nối DB thông thường.
*   Điều này giúp việc viết code cực kỳ sạch sẽ, giữ tính độc lập của Use Case mà vẫn bảo đảm tính an toàn dữ liệu tuyệt đối.
