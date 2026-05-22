# STAX / KA — Master Workflow

## Bản đồ Skills

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENTRY POINTS                             │
├──────────────────────┬──────────────────────────────────────────┤
│  Còn mơ hồ,          │  Đã rõ hướng,                           │
│  cần suy nghĩ        │  cần thiết kế                            │
│                      │                                          │
│  @stax-mindstorm     │  @stax-think (STAX-specific)            │
│  @ka-think (generic) │  @ka-think (generic)                    │
└──────────┬───────────┴───────────────┬──────────────────────────┘
           │                           │
           │  Khi đủ rõ               │  Sau Understanding Lock
           └───────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  context_handoff │  ← File bắt cầu giữa các skill
              │      .md         │
              └────────┬─────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
  @stax-backend           @stax-frontend
  (NestJS + DDD)          (React + TanStack)
           │                       │
           │  03_be_walkthrough    │  03_fe_walkthrough
           └───────────┬───────────┘
                       │
                       ▼
              ┌────────────────┐
              │  docs/history/ │  ← Archive sau khi hoàn thành
              └────────────────┘

SONG SONG / BẤT KỲ LÚC NÀO:
  @stax-naming-auditor  →  02_fix_manifest.md  →  @stax-quick-task
  @stax-docs-architect  (dọn dẹp tài liệu)
  @stax-quick-task      (bug fix / micro-feature độc lập)
```

---

## Luồng Chuẩn (Happy Path)

### Giai đoạn 1 — Tư duy & Thiết kế
```
User có ý tưởng
    │
    ├─ Còn mơ hồ → @stax-mindstorm (brainstorm)
    │                    │
    │                    └─ Khi đủ rõ → @stax-think
    │
    └─ Đã rõ → @stax-think
                    │
                    ├─ Mode Q: Trả lời nhanh, kết thúc
                    ├─ Mode D: D1→D2(Lock)→D3→D4→D5→D6(Handoff)
                    └─ Mode A: A1→A2(NFR)→A3(Risk)→D2→D5→D6(Handoff)
```

### Giai đoạn 2 — Implementation
```
context_handoff.md sẵn sàng
    │
    ├─ Cần BE → @stax-backend
    │              Step1(00_be_analysis) → [OK]
    │              Step2(01_be_plan)     → [OK]
    │              Step3(02_be_tasks)    → [OK]
    │              Step4(Exit Verify + 03_be_walkthrough)
    │
    └─ Cần FE → @stax-frontend
                   Step1(00_fe_analysis) → [OK]
                   Step2(01_fe_plan)     → [OK]
                   Step3(02_fe_tasks)    → [OK]
                   Step4(Exit Verify + 03_fe_walkthrough)
```

### Giai đoạn 3 — Archive
```
Sau khi cả BE + FE hoàn thành:
    Move docs/context/{session}/ → docs/history/{session}/
    Cập nhật docs/history/INDEX.md
```

---

## 3 Trụ cột Kiểm soát (Áp dụng cho MỌI skill)

### 1. Hard Stop Gates
Mọi bước quan trọng phải có xác nhận tường minh từ User trước khi đi tiếp.
Không có xác nhận = không được tự tiến.

### 2. Proof of Knowledge Chain
Mọi đề xuất phi tầm thường: Statement → Reasoning → Evidence.
Priority: (a) Internal doc → (b) Industry pattern → (c) Concrete example → (d) New proposal.
Khi label (d): thừa nhận tường minh và User có quyền phản biện.

### 3. Scope Gate + Anti-Creep
Scope được xác lập sau Understanding Lock.
Yêu cầu mới xuất hiện giữa chừng → ghi nhận, KHÔNG patch, hoàn thành scope hiện tại trước.

---

## Context Handoff — Giao thức Bắt cầu

File `context_handoff.md` là cơ chế duy nhất truyền context giữa các skill.

**Skill tạo:** `@stax-think`, `@ka-think`
**Skill đọc:** `@stax-backend`, `@stax-frontend`

```markdown
## Handoff Summary
Skill vừa hoàn thành: [tên]
Skill tiếp theo: [tên]

## Decisions đã lock (KHÔNG được reopen)
- [D1]: ...

## Assumptions đã document
- [A1]: ...

## Open questions (skill tiếp theo phải giải quyết)
- [Q1]: ...

## Files đã tạo
- [đường dẫn]: [mô tả]
```

**Quy tắc:**
- Skill nhận handoff PHẢI đọc file này trước Bước 1.
- "Locked Decisions" không được reopen dù bất kỳ lý do gì.
- Nếu không có handoff file → skill chạy ở chế độ độc lập, phải tự phân tích.

---

## Exit Verification — Nguyên tắc Chung

**Không được tự khai báo hoàn thành.** Phải paste kết quả thực tế từ lệnh terminal.

| Skill | Lệnh verify bắt buộc |
|---|---|
| stax-backend | `npm run build` + 4 lệnh `grep` |
| stax-frontend | `npm run check` + `grep` any/hard-coded + console check |
| stax-quick-task | `npm run build` + `grep` any + relevant tests |
| stax-naming-auditor | N/A (read-only, không cần verify) |

---

## Khi nào dùng skill nào

| Tình huống | Skill |
|---|---|
| Câu hỏi còn mơ hồ, chưa biết hướng | `@stax-mindstorm` |
| Câu hỏi kỹ thuật nhanh (≤2 min) | `@stax-think` Mode Q |
| Thiết kế tính năng mới | `@stax-think` Mode D |
| Quyết định kiến trúc hệ thống | `@stax-think` Mode A |
| Implement Backend module/feature | `@stax-backend` |
| Implement Frontend UI/feature | `@stax-frontend` |
| Bug fix / thêm field nhỏ | `@stax-quick-task` |
| Fix lỗi từ naming audit | `@stax-quick-task` Mode Fix |
| Audit naming convention | `@stax-naming-auditor` |
| Dọn dẹp / tổ chức tài liệu | `@stax-docs-architect` |
| Thinking không liên quan STAX | `@ka-think` |
