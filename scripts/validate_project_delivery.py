#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


PURE_FORBIDDEN = [
    "Redis", "Kafka", "RocketMQ", "MySQL", "PostgreSQL", "MongoDB",
    "Elasticsearch", "WebSocket", "HTTP", "gRPC", "API", "SQL",
    "Docker", "Kubernetes", "K8s", "CI/CD", "DDD", "Gin", "Kratos",
    "Vue", "React", "QPS", "P99", "数据库", "数据表", "字段", "索引",
    "接口", "入参", "出参", "缓存", "中间件", "消息队列", "分布式锁",
    "分库分表", "代码", "部署", "镜像", "流水线", "压测", "微服务",
]

REQUIRED_REFERENCES = [
    "ai-constraints.md",
    "compliance-rules.md",
    "cross-platform-adapter.md",
    "database-template.md",
    "document-code-alignment.md",
    "dev-and-fix-flows.md",
    "diagrams-template.md",
    "doc-gen-rules.md",
    "interface-implementation-guide.md",
    "interview-questions.md",
    "openspec-loops.md",
    "output-modes.md",
    "prd-branch-flow.md",
    "prd-template.md",
    "project-startup.md",
    "project-understanding.md",
    "production-code-standards.md",
    "release-checklist.md",
    "releases-v1.3.0.md",
    "repository-workflow.md",
    "review-template.md",
    "task-trace-template.md",
    "tech-plan-template.md",
    "workflow.md",
]

PLACEHOLDER_PATTERNS = [
    r"\[TODO[^]]*\]",
    r"\[(?:产品|功能|需求|模块|系统|业务实体|名称)[^]]*\]",
    r"(?m)^\s*(?:\.\.\.|…+)\s*$",
]

HARD_EVIDENCE_LABELS = [
    "文档已确认",
    "代码已存在",
    "已测试通过",
    "仍未闭环",
]

TASK_GATE_FIELDS = [
    "当前批次",
    "允许修改范围",
    "禁止修改范围",
    "本轮核心验收标准",
    "发现非本批次问题处理规则",
    "文档到代码贴合核验",
    "模块边界与生产级验收",
]

MODE_RULES = {
    "pure-business": {
        "min_chars": 300,
        "min_headings": 5,
        "heading_groups": [
            ("业务", "背景", "目标"),
            ("角色", "用户", "权限"),
            ("功能", "需求"),
            ("流程", "闭环", "场景"),
            ("约束", "规则", "验收"),
        ],
    },
    "hybrid": {
        "min_chars": 400,
        "min_headings": 6,
        "heading_groups": [
            ("业务", "背景", "目标"),
            ("角色", "用户", "权限"),
            ("功能", "需求"),
            ("流程", "场景"),
            ("验收", "约束"),
            ("非功能", "技术验收", "服务边界", "外部依赖", "工单"),
        ],
    },
    "api": {
        "min_chars": 800,
        "min_headings": 6,
        "heading_groups": [
            ("文档边界", "需求溯源", "来源", "依据"),
            ("通用约定", "请求头", "统一响应", "错误码"),
            ("接口", "服务"),
            ("请求", "入参", "DTO"),
            ("响应", "出参", "DTO"),
            ("仍未闭环", "待确认", "风险"),
        ],
    },
    "database": {
        "min_chars": 800,
        "min_headings": 8,
        "heading_groups": [
            ("建模依据", "来源", "证据"),
            ("建模结论", "总体"),
            ("主键", "乐观锁"),
            ("关系", "关联"),
            ("字段", "数据表", "表"),
            ("枚举", "状态"),
            ("事务", "幂等", "锁"),
            ("不建表", "不新增表", "待确认"),
        ],
    },
    "prd": {
        "min_chars": 600,
        "min_headings": 8,
        "heading_groups": [
            ("项目背景", "业务背景"),
            ("产品定位", "目标"),
            ("目标用户", "用户"),
            ("版本范围", "范围"),
            ("角色", "权限"),
            ("流程", "闭环"),
            ("功能", "需求"),
            ("验收", "非功能", "异常"),
        ],
    },
    "prototype": {
        "min_chars": 800,
        "min_headings": 10,
        "heading_groups": [
            ("项目概述", "项目背景", "版本目标"),
            ("目标用户", "用户"),
            ("业务流程", "用户主流程", "分支流程", "闭环流程"),
            ("页面原型", "页面清单", "页面总览"),
            ("分页面", "详细需求", "页面元素"),
            ("交互规则", "交互"),
            ("异常情况", "空页面", "报错", "失败"),
            ("页面跳转", "跳转去向", "导航"),
            ("全局", "通用规则"),
            ("非功能", "适配", "性能", "可用性"),
            ("附录", "修改记录"),
        ],
    },
    "alignment": {
        "min_chars": 700,
        "min_headings": 6,
        "heading_groups": [
            ("核验范围", "审计范围", "文档倒推代码"),
            ("核验依据", "来源", "依据"),
            ("对齐矩阵", "核验矩阵", "Alignment Matrix"),
            ("反向链路", "链路核验", "Required Reverse Checks"),
            ("运行证据", "Runtime evidence", "测试证据"),
            ("缺口", "Gap", "后续动作"),
        ],
    },
    "technical": {
        "min_chars": 500,
        "min_headings": 6,
        "heading_groups": [
            ("需求溯源", "评审范围", "来源", "依据", "项目结论"),
            ("架构", "技术选型"),
            ("模块", "边界"),
            ("流程", "接口", "集成"),
            ("风险", "回滚", "熔断", "降级", "失败处理", "评审结论"),
        ],
    },
    "project-understanding": {
        "min_chars": 250,
        "min_headings": 5,
        "heading_groups": [
            ("读取范围", "分析范围", "检查范围"),
            ("项目画像", "项目概览", "现状"),
            ("可复用", "复用"),
            ("目标差异", "差异", "目标范围"),
            ("闭环", "证据", "状态"),
        ],
    },
    "task-trace": {
        "min_chars": 500,
        "min_headings": 10,
        "heading_groups": [
            ("任务目标", "目标"),
            ("当前批次", "批次"),
            ("允许修改范围", "允许范围"),
            ("禁止修改范围", "禁止范围"),
            ("本轮核心验收标准", "验收标准"),
            ("发现非本批次问题处理规则", "非本批次"),
            ("计划修改文件", "影响文件", "修改文件"),
            ("解决方案", "方案"),
            ("前后端链路", "链路", "闭环"),
            ("自测命令和结果", "测试结果", "验证结果"),
            ("未覆盖风险", "风险"),
        ],
    },
}


def emit(level, message):
    print(f"{level}: {message}")


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def parse_frontmatter(text):
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        return None
    result = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def markdown_headings(text):
    return [
        match.group(2).strip()
        for match in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.M)
    ]


def meaningful_section_count(text):
    matches = list(re.finditer(r"^#{1,6}\s+.+?$", text, re.M))
    count = 0
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        content = re.sub(r"[`|:#*_[\]\-]", "", body)
        if len(re.sub(r"\s+", "", content)) >= 20:
            count += 1
    return count


def validate_markdown_links(root, markdown_files):
    failures = 0
    link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for markdown_file in markdown_files:
        text = read_text(markdown_file)
        for target in link_pattern.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target, re.I):
                continue
            resolved = (markdown_file.parent / target).resolve()
            if not resolved.exists():
                emit("FAIL", f"broken link in {markdown_file.relative_to(root)}: {target}")
                failures += 1
    return failures


def validate_openai_yaml(path):
    text = read_text(path)
    failures = 0
    required_patterns = {
        "display_name": r'^\s+display_name:\s+"([^"]+)"\s*$',
        "short_description": r'^\s+short_description:\s+"([^"]+)"\s*$',
        "default_prompt": r'^\s+default_prompt:\s+"([^"]+)"\s*$',
        "allow_implicit_invocation": r"^\s+allow_implicit_invocation:\s+(true|false)\s*$",
    }
    values = {}
    for field, pattern in required_patterns.items():
        match = re.search(pattern, text, re.M)
        if not match:
            emit("FAIL", f"agents/openai.yaml missing or invalid field: {field}")
            failures += 1
        else:
            values[field] = match.group(1)

    short_description = values.get("short_description", "")
    if short_description and not 20 <= len(short_description) <= 80:
        emit("FAIL", "agents/openai.yaml short_description must be 20-80 characters")
        failures += 1
    if "$project-delivery-analyst" not in values.get("default_prompt", ""):
        emit("FAIL", "agents/openai.yaml default_prompt must mention $project-delivery-analyst")
        failures += 1
    return failures


def validate_skill(root):
    root = Path(root).resolve()
    failures = 0
    skill_md = root / "SKILL.md"
    references = root / "references"
    script = root / "scripts" / "validate_project_delivery.py"
    agent = root / "agents" / "openai.yaml"

    for path in [skill_md, references, script, agent]:
        if not path.exists():
            emit("FAIL", f"missing required path: {path}")
            failures += 1

    if skill_md.exists():
        text = read_text(skill_md)
        frontmatter = parse_frontmatter(text)
        if frontmatter is None:
            emit("FAIL", "SKILL.md frontmatter missing or malformed")
            failures += 1
        else:
            name = frontmatter.get("name", "")
            description = frontmatter.get("description", "")
            unexpected_keys = set(frontmatter) - {"name", "description"}
            if unexpected_keys:
                emit("FAIL", "unexpected SKILL.md frontmatter keys: " + ", ".join(sorted(unexpected_keys)))
                failures += 1
            if name != "project-delivery-analyst":
                emit("FAIL", f"unexpected skill name: {name}")
                failures += 1
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                emit("FAIL", "skill name must use lowercase hyphen-case without repeated hyphens")
                failures += 1
            if len(name) > 64:
                emit("FAIL", "skill name exceeds 64 characters")
                failures += 1
            if not description or len(description) > 1024 or "<" in description or ">" in description:
                emit("FAIL", "description is empty, too long, or contains angle brackets")
                failures += 1
        if len(text.splitlines()) > 500:
            emit("FAIL", "SKILL.md exceeds the 500-line progressive-disclosure limit")
            failures += 1
        if re.search(r"\[TODO[^]]*\]", text):
            emit("FAIL", "SKILL.md still contains TODO placeholders")
            failures += 1

    if references.exists():
        for filename in REQUIRED_REFERENCES:
            path = references / filename
            if not path.exists():
                emit("FAIL", f"missing reference: {filename}")
                failures += 1
            elif not markdown_headings(read_text(path)):
                emit("FAIL", f"reference has no Markdown heading: {filename}")
                failures += 1
        count = len(list(references.glob("*.md")))
        emit("INFO", f"reference markdown count: {count}")

    if agent.exists():
        failures += validate_openai_yaml(agent)

    markdown_files = []
    if skill_md.exists():
        markdown_files.append(skill_md)
    if references.exists():
        markdown_files.extend(references.glob("*.md"))
    failures += validate_markdown_links(root, markdown_files)

    if failures:
        return 1
    emit("PASS", "skill structure and references passed")
    return 0


def validate_mermaid_fences(text):
    failures = 0
    mermaid_openings = len(re.findall(r"^```mermaid\s*$", text, re.M))
    fence_count = len(re.findall(r"^```(?:\w+)?\s*$", text, re.M))
    if fence_count % 2:
        emit("FAIL", "Markdown code fences are unbalanced")
        failures += 1
    for block in re.findall(r"```mermaid\s*\n(.*?)```", text, re.S):
        if not re.search(
            r"^\s*(?:flowchart|graph|sequenceDiagram|stateDiagram(?:-v2)?|erDiagram|mindmap|classDiagram|journey|gantt|pie)\b",
            block,
            re.M,
        ):
            emit("FAIL", "Mermaid block lacks a recognized diagram declaration")
            failures += 1
    if "```mermaid" in text and not mermaid_openings:
        emit("FAIL", "Mermaid fence must be written as ```mermaid on its own line")
        failures += 1
    return failures


def contains_any(text, terms):
    folded = text.casefold()
    return any(term.casefold() in folded for term in terms)


def require_terms(text, terms, scope):
    failures = 0
    for term in terms:
        if term not in text:
            emit("FAIL", f"{scope} missing required term: {term}")
            failures += 1
    return failures


def require_hard_evidence_labels(text, mode):
    failures = 0
    for label in HARD_EVIDENCE_LABELS:
        if label not in text:
            emit("FAIL", f"{mode} missing hard evidence label: {label}")
            failures += 1
    return failures


def require_regexes(text, patterns, scope):
    failures = 0
    for label, pattern in patterns:
        if not re.search(pattern, text, re.I | re.S):
            emit("FAIL", f"{scope} missing required contract: {label}")
            failures += 1
    return failures


def validate_alignment_runtime_closure(text):
    failures = 0
    no_runtime_markers = (
        "未执行",
        "未测试",
        "待验证",
        "暂无",
        "缺失",
        "无运行证据",
        "未联调",
    )
    false_closure_markers = (
        "已完成",
        "已闭环",
        "完整闭环",
        "生产可用",
        "通过验收",
    )

    for line in text.splitlines():
        if "|" not in line:
            continue
        if not any(marker in line for marker in no_runtime_markers):
            continue
        if "仍未闭环" not in line:
            emit("FAIL", "alignment row without runtime evidence must be marked 仍未闭环")
            failures += 1
        if any(marker in line for marker in false_closure_markers):
            emit("FAIL", "alignment row with missing runtime evidence claims closure")
            failures += 1
    return failures


def analyze_doc(doc, mode):
    text = read_text(doc)
    if mode not in MODE_RULES:
        emit("FAIL", f"unknown validation mode: {mode}")
        return 1
    rules = MODE_RULES[mode]
    failures = 0
    warnings = 0
    headings = markdown_headings(text)
    compact_length = len(re.sub(r"\s+", "", text))
    meaningful_sections = meaningful_section_count(text)

    emit(
        "INFO",
        f"headings={len(headings)}, meaningful_sections={meaningful_sections}, chars={compact_length}",
    )

    if compact_length < rules["min_chars"]:
        emit("FAIL", f"document is too short for {mode}: {compact_length} < {rules['min_chars']}")
        failures += 1
    if len(headings) < rules["min_headings"]:
        emit("FAIL", f"document has too few headings for {mode}")
        failures += 1
    if meaningful_sections < max(3, rules["min_headings"] - 2):
        emit("FAIL", "document lacks substantive section content")
        failures += 1

    heading_text = "\n".join(headings)
    for group in rules["heading_groups"]:
        if not contains_any(heading_text, group):
            emit("FAIL", "missing required heading concept: " + " / ".join(group))
            failures += 1

    placeholders = []
    for pattern in PLACEHOLDER_PATTERNS:
        placeholders.extend(match.group(0) for match in re.finditer(pattern, text, re.I))
    if placeholders:
        emit("FAIL", "document contains unresolved template placeholders: " + ", ".join(placeholders[:10]))
        failures += 1

    failures += validate_mermaid_fences(text)

    if mode == "pure-business":
        hits = []
        for keyword in PURE_FORBIDDEN:
            count = len(re.findall(re.escape(keyword), text, re.I))
            if count:
                hits.append(f"{keyword}:{count}")
        if hits:
            emit("FAIL", "pure business document contains technical terms: " + ", ".join(hits[:30]))
            failures += 1

    if mode == "technical":
        if not re.search(r"需求(?:ID|编号)|来源\s*[:：]|PRD|工单|用户(?:已)?确认", text, re.I):
            emit("FAIL", "technical document lacks a concrete traceability marker")
            failures += 1
        if re.search(r"(?:直接)?在?一?个文件(?:中)?(?:完成|实现|写完|堆)|单文件(?:完成|实现|堆叠|假实现)|所有逻辑(?:都)?(?:写|放|塞).*文件", text):
            emit("FAIL", "technical document allows single-file or architecture-bypassing implementation")
            failures += 1
        if not re.search(r"缓解|应对|回滚|降低|规避", text):
            emit("WARN", "technical risks may lack mitigation")
            warnings += 1

    if mode == "prd":
        failures += require_regexes(
            text,
            [
                ("requirement ID", r"需求ID|需求编号|\b[A-Z]{1,6}-\d{2,}\b"),
                ("priority", r"优先级|P0|P1|P2"),
                ("acceptance criteria", r"验收口径|验收标准|验收"),
                ("version scope in/out", r"第一版要做|本期范围|in scope|第一版不做|不做|out of scope"),
                ("role permission", r"角色|权限"),
                ("exception or non-functional section", r"异常场景|非功能需求|可靠性|隐私"),
            ],
            mode,
        )

    if mode == "prototype":
        failures += require_regexes(
            text,
            [
                ("project overview", r"项目概述|项目背景"),
                ("version goal", r"版本目标|第一版|MVP|本期范围"),
                ("target user", r"目标用户|用户角色"),
                ("main flow", r"用户主流程|主流程|整体业务流程"),
                ("branch flow", r"分支流程|关键分支|异常分支"),
                ("page list", r"页面清单|页面列表"),
                ("page elements", r"页面元素"),
                ("interaction rules", r"交互规则"),
                ("exception states", r"异常情况|空状态|空页面|报错|失败"),
                ("navigation destination", r"页面跳转去向|跳转去向|跳转"),
                ("global rules", r"全局通用规则|全局规则|通用规则"),
                ("non-functional requirements", r"非功能要求|非功能需求|适配平台|性能要求"),
                ("appendix or revision history", r"附录|修改记录"),
            ],
            mode,
        )

    if mode == "alignment":
        failures += require_hard_evidence_labels(text, mode)
        failures += require_regexes(
            text,
            [
                ("document requirement column", r"Document requirement|文档需求|需求项"),
                ("source document and section column", r"Source document and section|来源文档|文档章节"),
                ("expected code location column", r"Expected code location|预期代码位置|代码落点"),
                ("actual code evidence column", r"Actual code evidence|实际代码证据"),
                ("runtime evidence column", r"Runtime evidence|运行证据"),
                ("status label column", r"Status label|状态标签"),
                ("gap action column", r"Gap\s*/\s*action|缺口|后续动作"),
                ("frontend entry or page action", r"前端入口|页面动作|页面.*按钮|保存按钮"),
                ("frontend API wrapper", r"前端\s*API|API\s*wrapper|services?/|请求封装"),
                ("backend route or gateway", r"后端路由|Gateway|网关|POST\s+/|GET\s+/|PUT\s+/|DELETE\s+/"),
                ("request DTO", r"请求\s*DTO|入参\s*DTO|请求入参"),
                ("response DTO", r"响应\s*DTO|出参\s*DTO|响应出参"),
                ("service domain RPC", r"Service/domain/RPC|service|domain|rpc|业务服务方法"),
                ("repository DAO database", r"Repository/DAO/数据库|repository|DAO|数据库|数据表"),
                ("transaction lock idempotency status concurrency", r"事务|锁|幂等|状态|并发"),
                ("third-party middleware dependency", r"第三方|Redis|MQ|ES|object storage|model provider|中间件|缓存|消息队列"),
                ("logging trace security", r"日志|trace|安全|脱敏"),
                ("test or live verification", r"测试|live verification|接口请求|构建|运行日志"),
            ],
            mode,
        )
        failures += validate_alignment_runtime_closure(text)

    if mode == "api":
        failures += require_regexes(
            text,
            [
                ("source traceability", r"依据|来源|需求溯源|PRD"),
                ("frontend entry", r"前端入口"),
                ("frontend API method", r"前端调用|API\s*方法|services?/"),
                ("backend route", r"后端路由|POST\s+/|GET\s+/|PUT\s+/|DELETE\s+/"),
                ("authentication", r"是否鉴权|鉴权|Authorization"),
                ("backend service", r"后端服务|service|rpc"),
                ("request DTO", r"请求\s*DTO|请求参数|入参"),
                ("response DTO", r"响应\s*DTO|返回参数|出参"),
                ("field table", r"字段\s*\|\s*类型|字段.*类型.*必填"),
                ("affected storage", r"涉及表|数据库|Redis|MQ|ES|第三方"),
                ("unified response or error code", r"统一响应|错误码|code"),
            ],
            mode,
        )

    if mode == "database":
        failures += require_regexes(
            text,
            [
                ("modeling basis", r"建模依据|来源|证据状态"),
                ("field definition table", r"字段名\s*\|\s*类型\s*\|\s*索引\s*\|\s*空\s*\|\s*备注\s*\|\s*依据"),
                ("primary key strategy", r"主键|PK|雪花|auto_increment|UUID"),
                ("index strategy", r"索引|IDX|UK|FULLTEXT"),
                ("relationship list", r"关系|一对多|一对一|多对多"),
                ("enum list", r"枚举|status|状态"),
                ("transaction design", r"事务"),
                ("idempotency design", r"幂等|idempotency_key"),
                ("lock/concurrency design", r"锁|乐观锁|version|并发"),
                ("tables not created", r"不建表|不新增表|第一版不建表"),
            ],
            mode,
        )

    if mode == "project-understanding":
        failures += require_hard_evidence_labels(text, mode)

    if mode == "task-trace":
        failures += require_terms(text, TASK_GATE_FIELDS, mode)
        failures += require_hard_evidence_labels(text, mode)
        if not re.search(r"测试.*(?:通过|失败)|未执行测试|待运行|已测试通过|仍未闭环", text, re.S):
            emit("FAIL", "task trace lacks an explicit verification state or result")
            failures += 1

    if failures:
        return 1
    emit("PASS", f"{mode} validation passed with {warnings} warning(s)")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path)
    parser.add_argument("--doc", type=Path)
    parser.add_argument("--mode", choices=sorted(MODE_RULES))
    args = parser.parse_args()

    result = 0
    if args.skill_root:
        result |= validate_skill(args.skill_root)
    if args.doc:
        if not args.mode:
            emit("FAIL", "--mode is required with --doc")
            result |= 1
        elif not args.doc.exists():
            emit("FAIL", f"document does not exist: {args.doc}")
            result |= 1
        else:
            result |= analyze_doc(args.doc, args.mode)
    if not args.skill_root and not args.doc:
        parser.print_help()
        result = 1
    sys.exit(result)


if __name__ == "__main__":
    main()
