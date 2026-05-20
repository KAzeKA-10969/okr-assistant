# MCP 工具详细约束

本技能依赖两个 MCP 服务，以下是各服务的完整工具清单及参数约束。在调用前请务必查阅此文档以确保参数准确。

## 钉钉通讯录服务（mcpId: 2400）

**可用工具清单**：

| 工具名 | 用途 | 关键参数约束 |
|--------|------|-------------|
| `get_current_user_profile` | 获取当前用户基本信息、组织信息、主管、部门、角色 | 无参数 |
| `search_user_by_key_word` | 按关键词搜索用户，返回 userId | `keyWord`（必填，string）- 搜索关键词 |
| `get_user_info_by_user_ids` | 批量获取用户详细信息 | `user_id_list`（必填，string[]）- userId 数组 |
| `search_user_by_mobile` | 通过手机号搜索用户 | `mobile`（必填，string）- 手机号 |
| `get_dept_members_by_deptId` | 获取指定部门下的所有成员 | `deptIds`（必填，number[]）- 部门 ID 数组 |
| `search_dept_by_keyword` | 按关键词模糊搜索部门 | `query`（必填，string）- 搜索关键词 |
| `get_dept_info_by_dept_id` | 根据部门 ID 获取部门详情 | `deptId`（必填，number）- 部门 ID |
| `get_sub_depts_by_dept_id` | 获取指定部门的直接子部门列表 | `deptId`（必填，number）- 父部门 ID |
| `search_contact_by_key_word` | 搜索好友和同事 | `keyword`（必填，string）- 搜索关键词 |
| `list_my_followings` | 获取我的特别关注列表 | 无参数 |

**使用约束**：
- 所有涉及部门 ID 的参数类型为 `number`，禁止传入字符串
- 用户 ID 参数类型为 `string`
- 搜索结果受组织可见性控制，可能返回空或部分数据
- 调用 `get_current_user_profile` 是获取当前用户身份的首选方式

## OKR 目标管理服务（mcpId: 10030）

**可用工具清单**：

| 工具名 | 用途 | 关键参数约束 |
|--------|------|-------------|
| `get_okr_app_context` | 获取应用开通情况、空间列表、用户权限 | 无参数 |
| `get_user_okr_periods` | 获取用户的 OKR 周期列表 | `spaceId`（必填，string）；`type`（可选，number：1-月度、2-季度、3-半年度、4-年度、5-自定义、6-双月、7-周）；`status`（可选，number：0-不过滤、1-未开始、2-进行中、3-已结束）；`archiveStatus`（可选，number：0-不过滤、1-未归档、2-已归档）；`name`（可选，string）；`menu`（可选，number：1-全部、2-可以制定的、3-父周期数据） |
| `get_objective_list_by_period` | 获取指定周期下的 OKR 列表 | `type`（必填，number：0-全部、1-公司级、2-部门级、3-个人级、4-我部门的、5-我的OKR、6-直属上级、7-直属下级）；`pageNo`（必填，number，最小值1）；`pageSize`（必填，number，最小值1，默认20）；`spaceId`（必填，string）；`periodId`（必填，string）；`userIds`（可选，string[]）；`needDraft`（可选，boolean，默认false）；`needApproval`（可选，boolean，默认false） |
| `batch_submit_okrs` | 批量提交 OKR（目标+KR+对齐关系） | `spaceId`（必填，string）；`periodId`（必填，string）；`objectives`（必填，Objective[]）；`draftId`（可选，string） |
| `get_okr_module_settings` | 获取空间的 OKR 字段约束 | `spaceId`（必填，string） |
| `gen_okr_alignment` | 生成 OKR 对齐视图 | `objectives`（必填，ObjectiveView[]，至少一个元素） |

### batch_submit_okrs 参数详细约束

`objectives` 数组中每个目标对象的字段约束：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tempId` | string | 新增时必填 | 调用方生成的唯一标识，用于响应映射和 aligns 引用 |
| `objectiveId` | string | 更新时必填 | 已有目标的 ID，新增时不传 |
| `name` | string | 是 | 目标标题 |
| `type` | number | 是 | 1-公司级、2-部门级、3-个人级 |
| `owner` | string | 是 | 目标负责人的 userId |
| `displayType` | number | 否 | 1-挑战型、2-承诺型 |
| `weight` | number | 否 | 目标权重（取决于空间配置） |
| `deptId` | string | type=2 时建议填写 | 部门级目标的部门 ID |
| `krs` | KR[] | 否 | 关键结果数组，可为空 |
| `aligns` | Align[] | 否 | 对齐关系数组 |

`krs` 数组中每个 KR 对象的字段约束：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tempId` | string | 新增时必填 | 调用方生成的唯一标识 |
| `krId` | string | 更新时必填 | 已有 KR 的 ID |
| `content` | string | 是 | KR 内容 |
| `unit` | string | 否 | 单位（如个、%、次） |
| `startValue` | number | 否 | 起始值（量化型 KR） |
| `targetValue` | number | 否 | 目标值（量化型 KR） |
| `currentValue` | number | 否 | 当前值（量化型 KR） |
| `progress` | number | 否 | 进度值 |
| `confidence` | number | 否 | 信心值（0-10，默认5） |
| `deadline` | number | 否 | 截止时间（毫秒时间戳） |
| `weight` | number | 否 | KR 权重（取决于空间配置） |

`aligns` 数组中每个对齐对象的字段约束（二选一）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `objectiveId` | string | 对齐系统中已有的目标 |
| `objectiveTempId` | string | 对齐本批次新增的目标（引用 objectives 中的 tempId） |
| `krId` | string | 对齐系统中已有的 KR |
| `krTempId` | string | 对齐本批次新增的 KR（引用 krs 中的 tempId） |

**注意**：`objectiveId` 与 `objectiveTempId` 二选一，`krId` 与 `krTempId` 二选一。

### gen_okr_alignment 参数详细约束

`objectives` 数组中每个元素的字段约束：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 目标 ID |
| `name` | string | 是 | 目标名称 |
| `krs` | KRView[] | 否 | KR 列表 |
| `user` | string | 否 | 负责人展示名 |
| `period` | string | 否 | 周期展示文案 |
| `alignId` | string | 否 | 对齐上级目标 ID |
| `displayType` | string | 否 | 展示类型："挑战型" 或 "承诺型" |

`krs` 数组中每个元素的字段约束：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | KR ID |
| `name` | string | 是 | KR 名称 |

**使用约束**：
- `batch_submit_okrs` 必须由用户明确许可后才能调用，禁止自动提交
- 提交前必须先调用 `get_okr_app_context` 确认用户有权限，再调用 `get_user_okr_periods` 确认周期存在
- `get_objective_list_by_period` 的 `type` 参数枚举值必须严格匹配，不可传入其他数值
- `gen_okr_alignment` 只用于生成对齐视图，不要生成其他类型的关系图
- 所有涉及 ID 的参数类型为 `string`，涉及数量的参数类型为 `number`
