import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_project_delivery.py"
SPEC = importlib.util.spec_from_file_location("validate_project_delivery", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class SkillValidationTests(unittest.TestCase):
    def validate_text(self, text, mode):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.md"
            path.write_text(text, encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                return VALIDATOR.analyze_doc(path, mode)

    def test_current_skill_structure_passes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(VALIDATOR.validate_skill(ROOT), 0)

    def test_keyword_only_documents_fail_all_modes(self):
        cases = {
            "pure-business": "# 空文档\n\n业务 角色 功能 流程 约束",
            "hybrid": "# 空文档\n\n业务 角色 功能 流程 验收 非功能",
            "technical": "# 空文档\n\n业务 技术 架构 模块 风险 PRD",
            "project-understanding": "# 空文档\n\n读取范围 项目画像 可复用 目标差异 文档已确认 仍未闭环",
            "task-trace": "# 空文档\n\n当前批次 允许修改范围 禁止修改范围 文档已确认 代码已存在 已测试通过 仍未闭环",
        }
        for mode, text in cases.items():
            with self.subTest(mode=mode):
                self.assertEqual(self.validate_text(text, mode), 1)

    def test_substantive_pure_business_document_passes(self):
        text = """# 售后申请业务需求

## 业务背景与目标
购买者需要在订单完成后提交售后申请，并能持续看到处理进度。目标是减少人工沟通和重复登记。

## 用户角色与权限
购买者可以创建和查看本人申请；客服可以受理、补充说明和给出处理结果；主管可以处理升级事项。

## 功能需求
购买者选择订单、填写原因并提交。系统展示申请编号、当前状态、处理人和更新时间，并避免重复提交。

## 业务流程与异常场景
提交后进入待受理状态。资料不足时退回补充，符合条件时进入处理中，完成后展示结果。订单无效时明确提示原因。

## 业务约束与验收
同一订单的同一商品不能同时存在两条处理中申请。各角色只能执行被授权的操作。正常、退回和拒绝场景都应有可观察结果。

## 待确认问题
退款到账时限由财务规则决定，目前需要业务负责人确认。
"""
        self.assertEqual(self.validate_text(text, "pure-business"), 0)

    def test_unresolved_template_placeholder_fails(self):
        text = """# 技术评审

## 评审范围与需求溯源
来源：PRD-001，覆盖售后提交与状态查询。

## 架构设计
沿用现有分层，复用统一鉴权和错误处理。

## 模块职责与边界
[模块名] 负责接收请求，业务层负责校验状态，存储层负责持久化。

## 核心流程与接口
请求经过权限校验和业务校验后写入记录，并返回可追踪编号。

## 发布与回滚
采用兼容发布；异常时回滚应用版本并停用新入口。

## 风险与应对
重复提交可能产生重复记录，通过业务唯一约束和重复操作检查降低风险。
"""
        self.assertEqual(self.validate_text(text, "technical"), 1)

    def test_project_understanding_requires_hard_labels(self):
        text = """# 项目理解报告

## 读取范围
只读检查 README、路由、接口定义、模型文件和代表性服务实现，不修改任何项目文件。读取范围只覆盖当前目标所需证据，不扫描缓存、构建产物、历史归档和无关模块。

## 项目画像
文档已确认：项目目标来自 README。代码已存在：服务入口和页面入口已经在当前仓库中存在。当前项目采用页面入口调用统一请求封装，再进入服务层校验状态并返回结果的基本结构。

## 可复用内容
代码已存在：可以复用现有请求封装、状态枚举、错误处理和页面组件。复用这些内容可以降低改动范围，避免新增重复 API、重复状态常量和重复展示逻辑。

## 目标差异
文档已确认：本次只处理指定目标，不增加登录、通知、支付或数据库迁移。目标差异集中在状态展示和保存闭环，不改变既有角色权限、页面导航和服务部署方式。

## 闭环状态
仍未闭环：没有运行服务端联调。已测试通过：只读结构检查已经完成。后续如果进入开发批次，需要重新输出允许修改范围、禁止修改范围、影响文件清单和自测命令。
"""
        self.assertEqual(self.validate_text(text, "project-understanding"), 0)

    def test_task_trace_requires_batch_gate_and_hard_labels(self):
        text = """# 增加等待反馈状态

## 任务目标
补齐等待反馈状态，使页面、接口、数据和测试保持一致。目标不是重做工单模块，而是在既有状态模型上增加一个可追踪、可保存、可展示的新状态。

## 当前批次
本批次只处理状态闭环，不扩展其他工单能力。所有发现的通知提醒、权限细化、批量操作和报表统计需求，都不能插入本批次实现。

## 允许修改范围
允许修改服务、页面脚本、样式、测试和本任务追踪文档。允许范围必须能直接解释为等待反馈状态闭环的一部分，不能借机调整目录结构或公共依赖。

## 禁止修改范围
不修改登录、通知、数据库迁移、拖拽排序和其他无关功能。已经验证通过的查询、创建、删除和导出逻辑只作为依赖读取，不做二次改造。

## 本轮核心验收标准
页面可以展示等待反馈状态，接口可以保存并返回该状态，测试覆盖正常和异常场景。

## 发现非本批次问题处理规则
仅登记留存，不插入当前批次修复。

## 计划修改文件
服务文件增加状态校验，页面文件增加筛选和泳道，测试文件固化契约。每个文件改动都必须对应链路中的状态枚举、请求参数、响应展示或验证断言。

## 解决方案
复用既有状态模型，只把等待反馈加入统一枚举、筛选和看板渲染。不新建临时状态字段，不绕过服务端校验，也不使用前端假数据制造完成效果。

## 前后端链路
页面提交状态，服务校验后写入本地数据，再返回工单并刷新泳道。链路验收需要同时观察请求入参、响应状态、页面展示和持久化结果。

## 数据库、第三方、配置影响
不涉及数据库、第三方服务和生产配置，继续使用本地文件存储。

## 自测命令和结果
已测试通过：执行单元测试和接口验证，测试通过。代码已存在：状态校验位于服务层。

## 未覆盖风险
仍未闭环：本地文件并发写入尚未验证，不属于当前单用户实验声明。

## 非本批次发现问题登记
文档已确认：通知提醒仅登记为范围外事项，不插入当前批次。
"""
        self.assertEqual(self.validate_text(text, "task-trace"), 0)

    def test_task_trace_without_hard_labels_fails(self):
        text = """# 任务追溯

## 当前批次
本批次只处理状态闭环，不扩展其他能力。

## 允许修改范围
允许修改服务和测试。

## 禁止修改范围
不修改通知和登录。

## 本轮核心验收标准
状态链路可以正常保存和展示。

## 发现非本批次问题处理规则
仅登记留存。

## 计划修改文件
服务文件和测试文件。

## 解决方案
增加状态枚举并补充测试。

## 前后端链路
页面请求服务，服务返回状态。

## 自测命令和结果
测试通过。

## 未覆盖风险
并发未验证。
"""
        self.assertEqual(self.validate_text(text, "task-trace"), 1)


if __name__ == "__main__":
    unittest.main()
