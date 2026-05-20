---
title: "Quy chuẩn Frontend UI Components"
description: "Hướng dẫn sử dụng và chuẩn hóa UI Components, Grid, Stats và layout trong STAX"
tags: [standards, frontend, ui, react, components]
last_updated: "2026-05-21"
---

# Standard UI Components Guide

Tài liệu này hướng dẫn cách sử dụng các UI Components chuẩn đã được xây dựng để đảm bảo tính nhất quán trên toàn hệ thống STAX.

## 1. PageHeader
Sử dụng cho phần đầu trang để hiển thị tiêu đề, mô tả và các nút hành động.

```tsx
import { PageHeader } from "@/components/common/PageHeader";

<PageHeader 
  title="Tiêu đề trang" 
  description="Mô tả ngắn về nội dung trang"
  backUrl="/admin/crm/leads" // Tùy chọn: dùng cho Detail Page
  titleBadge={<Badge>Trạng thái</Badge>} // Tùy chọn
>
  <Button>Hành động chính</Button>
</PageHeader>
```

## 2. DataGrid
Component bọc quanh Table để tự động hóa việc hiển thị dữ liệu, phân trang và trạng thái Loading.

```tsx
import { DataGrid } from "@/components/common/DataGrid";

<DataGrid
  columns={[
    { header: "Tên", accessorKey: "name" },
    { header: "Giá trị", cell: (row) => formatCurrency(row.value) }
  ]}
  data={items}
  isLoading={isLoading}
  pagination={{
    currentPage: page,
    totalPages: totalPages,
    onPageChange: setPage,
    totalCount: total
  }}
  emptyTitle="Không có dữ liệu"
/>
```

## 3. StatsCard
Sử dụng cho các Dashboard hoặc tóm tắt dữ liệu.

```tsx
import { StatsCard } from "@/components/common/StatsCard";

<StatsCard
  title="Tổng doanh thu"
  value={formatCurrency(1000000)}
  icon={<DollarSign className="h-4 w-4" />}
  description="+12% so với tháng trước"
  trend="up"
/>
```

## Nguyên tắc chung
- Luôn ưu tiên sử dụng các component này thay vì viết HTML Table hoặc Header thủ công.
- Đảm bảo tính Responsive: Các component này đã được tối ưu cho Mobile.
- Nếu cần tùy chỉnh sâu hơn, hãy cân nhắc nâng cấp component dùng chung thay vì viết ad-hoc styles tại trang.
