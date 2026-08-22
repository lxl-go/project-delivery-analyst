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
    "technical": {
        "min_chars": 500,
        "min_headings": 6,
        "heading_groups": [
            ("需求溯源", "评审范围", "来源"),
            ("架构", "技术选型"),
            ("模块", "边界"),
            ("流程", "接口", "集成"),
            ("风险", "回滚"),
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


def analyze_doc(doc, mode):
    text = read_text(doc)
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
        if not re.search(r"缓解|应对|回滚|降低|规避", text):
            emit("WARN", "technical risks may lack mitigation")
            warnings += 1

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
