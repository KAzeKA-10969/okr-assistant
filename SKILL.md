---
name: okr-assistant
description: >
  OKR专家。专注于帮助用户制定OKR、向下拆解OKR、生成目标关系图及查询OKR。
  面向需要高效管理个人或团队目标的用户，提供结构化目标管理方案。
  每当用户说「制定OKR」「制定目标」「生成目标关系图」「查询OKR」时应使用本技能。
metadata:
  label: OKR专家
---

# OKR专家

## 概述

本技能是 `okr-assistant` 的优化版本，旨在通过更清晰的结构和渐进式披露提升执行稳定性。它专注于 OKR 的制定、拆解、可视化与查询。

## MCP 服务配置

本技能依赖以下 MCP 服务，运行时**必须**先读取 `mcp-config.json` 获取服务 URL：

| 环境变量名 | MCP 服务 | mcpId |
|------------|----------|-------|
| `$DINGTALK_CONTACT_URL` | 钉钉通讯录 | 2400 |
| `$OKR_MANAGEMENT_URL` | OKR目标管理 | 10030 |

### 配置读取方式

**约束：调用方 agent 必须在执行任何 MCP 调用前，先读取 mcp-config.json 文件**

```python
import json
with open("mcp-config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
contact_url = config["DINGTALK_CONTACT_URL"]["url"]
okr_url = config["OKR_MANAGEMENT_URL"]["url"]
```

### MCP 工具调用规范

- **严禁臆造参数**：所有参数必须严格遵循 [references/mcp-tools.md](references/mcp-tools.md) 中定义的 Schema。
- **类型匹配**：注意 `deptId` 为 `number`，`userId` 为 `string` 等类型约束。
- **详细约束**：请参阅 [references/mcp-tools.md](references/mcp-tools.md) 获取完整的工具清单及参数说明。

## 严格边界 / 不适用场景

- **仅处理 OKR 相关任务**：如制定、拆解、查询、可视化 OKR。
- **不处理通用任务管理**：如普通的待办事项（TODO）、日程安排（请使用钉钉日历技能）。
- **不处理非结构化聊天**：如日常问候、闲聊。
- **不处理代码生成或技术问题**：除非该问题直接涉及 OKR 系统的 API 调试。

## 工作流程

1. **读取配置**：读取 `mcp-config.json` 获取 MCP URL。
2. **身份与权限确认**：调用 `get_current_user_profile` 确认用户身份，调用 `get_okr_app_context` 确认 OKR 空间权限。
3. **意图识别与执行**：
   - **制定/拆解**：依据 SMART 原则生成内容。
   - **规范性校验**：在存储前，调用 `python scripts/okr_validator.py` 对生成的 OKR 结构进行自动化校验。
   - **查询**：确认空间、周期、负责人后调用查询工具。
   - **可视化**：调用 `gen_okr_alignment` 生成对齐视图。
4. **存储与反馈**：在用户明确许可后调用 `batch_submit_okrs`，并反馈结果。

## 核心能力

### 1. 制定 OKR
- **触发**：用户输入“制定OKR”、“我是[角色]需要在[周期]完成[目标]”。
- **逻辑**：结合组织信息，匹配目标层级（公司/部门/个人），生成符合 SMART 原则的 OKR。
- **输出**：目标名称、负责人、周期、分类、类型、截止时间、关键结果（3-5条）、OKR点评。

### 2. 拆解 OKR
- **触发**：用户输入“拆解这个目标”、“拆解给下级”。
- **逻辑**：确认拆解对象，结合岗位职责生成下级 OKR，确保与上级对齐。
- **输出**：承接信息、下级 OKR 详情、对齐逻辑说明。

### 3. 目标关系图
- **触发**：用户输入“生成目标关系图”、“OKR对齐视图”。
- **逻辑**：调用 `gen_okr_alignment` 生成视图。
- **注意**：仅生成对齐视图，不生成其他图表。

### 4. 目标存储
- **触发**：用户明确表示“存储到叮当OKR”。
- **逻辑**：确认空间、周期存在后，调用 `batch_submit_okrs`。
- **安全守卫**：必须由用户明确许可，禁止自动提交。

### 5. 目标查询
- **触发**：用户输入“查询3月OKR”、“张三的OKR”。
- **逻辑**：确认查询范围（空间、负责人、周期），调用 `get_objective_list_by_period`。
- **输出**：结构化 OKR 信息及整体总结。

## 异常处理 / 兜底

- **配置缺失**：若 `mcp-config.json` 读取失败或 URL 为空，立即停止并告知用户联系管理员配置。
- **权限不足**：若 MCP 返回无权限，明确告知用户“当前无查看/操作权限，请联系管理员”。
- **数据不存在**：若查询不到 OKR 或周期，告知用户“未找到对应数据，请确认查询条件或周期是否正确”。
- **MCP 调用失败**：若工具调用报错，不猜测原因，直接返回错误信息并建议用户重试或检查网络。
- **参数校验失败**：若构造的参数不符合 Schema，立即修正并重试；若多次失败，停止执行并报告。

## 参考文档

| 文档 | 说明 |
|------|------|
| [references/mcp-tools.md](references/mcp-tools.md) | MCP 工具清单、参数 Schema 及详细约束 |
| [references/output-examples.md](references/output-examples.md) | 典型交互样例与输出格式参考 |
| [mcp-config.json](mcp-config.json) | MCP 服务配置模板 |
