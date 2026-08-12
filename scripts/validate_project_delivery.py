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
    "workflow.md",
    "interview-questions.md",
    "output-modes.md",
    "prd-template.md",
    "diagrams-template.md",
    "tech-plan-template.md",
    "database-template.md",
    "doc-gen-rules.md",
    "compliance-rules.md",
    "review-template.md",
]


def emit(level, message):
    print(f"{level}: {message}")


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def validate_skill(root):
    root = Path(root)
    failures = 0
    skill_md = root / "SKILL.md"
    refs = root / "references"
    script = root / "scripts" / "validate_project_delivery.py"
    agent = root / "agents" / "openai.yaml"

    for path in [skill_md, refs, script, agent]:
        if not path.exists():
            emit("FAIL", f"missing required path: {path}")
            failures += 1

    if skill_md.exists():
        text = read_text(skill_md)
        match = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not match:
            emit("FAIL", "SKILL.md frontmatter missing")
            failures += 1
        else:
            fm = {}
            for line in match.group(1).splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    fm[key.strip()] = value.strip()
            name = fm.get("name", "")
            desc = fm.get("description", "")
            if name != "project-delivery-analyst":
                emit("FAIL", f"unexpected skill name: {name}")
                failures += 1
            if not desc or len(desc) > 1024 or "<" in desc or ">" in desc:
                emit("FAIL", "description is empty, too long, or contains angle brackets")
                failures += 1
            if "[TODO" in text:
                emit("FAIL", "SKILL.md still contains TODO placeholders")
                failures += 1

    if refs.exists():
        for filename in REQUIRED_REFERENCES:
            if not (refs / filename).exists():
                emit("FAIL", f"missing reference: {filename}")
                failures += 1
        count = len(list(refs.glob("*.md")))
        emit("INFO", f"reference markdown count: {count}")

    if failures:
        return 1
    emit("PASS", "skill structure passed")
    return 0


def heading_count(text):
    return len(re.findall(r"^#{1,6}\s+", text, re.M))


def analyze_doc(doc, mode):
    text = read_text(doc)
    failures = 0
    warnings = 0

    emit("INFO", f"headings={heading_count(text)}")

    if mode == "pure-business":
        hits = []
        for keyword in PURE_FORBIDDEN:
            count = len(re.findall(re.escape(keyword), text, re.I))
            if count:
                hits.append(f"{keyword}:{count}")
        if hits:
            emit("FAIL", "pure business document contains technical terms: " + ", ".join(hits[:30]))
            failures += 1
        for required in ["业务", "角色", "功能", "流程", "约束"]:
            if required not in text:
                emit("WARN", f"missing expected business keyword: {required}")
                warnings += 1

    elif mode == "hybrid":
        for required in ["业务", "功能", "验收"]:
            if required not in text:
                emit("FAIL", f"missing hybrid core keyword: {required}")
                failures += 1
        if not any(key in text for key in ["非功能", "工单", "服务边界", "技术验收"]):
            emit("FAIL", "hybrid document lacks controlled technical acceptance sections")
            failures += 1

    elif mode == "technical":
        for required in ["技术", "架构", "模块", "风险"]:
            if required not in text:
                emit("WARN", f"missing technical review keyword: {required}")
                warnings += 1
        if not any(key in text for key in ["需求溯源", "来源", "PRD", "工单", "用户确认"]):
            emit("WARN", "technical document may lack traceability markers")
            warnings += 1

    else:
        emit("FAIL", f"unknown mode: {mode}")
        failures += 1

    if failures:
        return 1
    emit("PASS", f"{mode} initial validation passed with {warnings} warning(s)")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", type=Path)
    parser.add_argument("--doc", type=Path)
    parser.add_argument("--mode", choices=["pure-business", "hybrid", "technical"])
    args = parser.parse_args()

    rc = 0
    if args.skill_root:
        rc |= validate_skill(args.skill_root)
    if args.doc:
        if not args.mode:
            emit("FAIL", "--mode is required with --doc")
            rc |= 1
        else:
            rc |= analyze_doc(args.doc, args.mode)
    if not args.skill_root and not args.doc:
        parser.print_help()
        rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
