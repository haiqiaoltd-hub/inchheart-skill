#!/usr/bin/env python3
"""
自动检查生成的SKILL.md是否通过Phase 4质量标准。
对照通过标准表格逐项检查，输出通过/不通过和具体原因。

用法:
    python3 quality_check.py <SKILL.md路径>

示例:
    python3 quality_check.py references/perspectives/elon-musk-perspective/PERSPECTIVE.md
"""

import sys
import re
from pathlib import Path
from urllib.parse import urlparse


GENERIC_URL_PATHS = {
    "",
    "/",
    "/search",
    "/search/",
    "/topic",
    "/topic/",
    "/tag",
    "/tag/",
    "/video",
    "/video/",
    "/article",
    "/article/",
    "/read",
    "/read/",
}


def is_concrete_url(url: str) -> bool:
    """Return whether a URL looks like a specific source rather than a homepage/search page."""
    parsed = urlparse(url.rstrip(".,"))
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False

    path = (parsed.path or "").rstrip("/")
    normalized = path or "/"
    if normalized in GENERIC_URL_PATHS:
        return False

    segments = [segment for segment in path.split("/") if segment]
    if len(segments) >= 2:
        return True
    if segments and len(segments[0]) >= 8:
        return True

    query = parsed.query.lower()
    return any(marker in query for marker in ("id=", "vid=", "aid=", "bvid=", "p=", "article"))


def check_mental_models(content: str) -> tuple[bool, str]:
    """检查心智模型数量（3-7个）"""
    # 匹配 ### 模型N: 或 ### N. 等模式
    models = re.findall(r'^###\s+(?:模型|Model|心智模型)\s*\d', content, re.MULTILINE)
    if not models:
        # fallback: 数「### 」开头的行在心智模型section中
        in_section = False
        count = 0
        for line in content.split('\n'):
            if re.match(r'^##\s+.*心智模型|Mental Model', line, re.IGNORECASE):
                in_section = True
                continue
            if in_section and re.match(r'^##\s+', line) and '心智模型' not in line:
                break
            if in_section and re.match(r'^###\s+', line):
                count += 1
        if count > 0:
            passed = 3 <= count <= 7
            return passed, f"{count}个心智模型 {'✅' if passed else '❌ (应为3-7个)'}"

    count = len(models)
    if count == 0:
        return False, "未检测到心智模型section"
    passed = 3 <= count <= 7
    return passed, f"{count}个心智模型 {'✅' if passed else '❌ (应为3-7个)'}"


def check_limitations(content: str) -> tuple[bool, str]:
    """检查每个模型是否有局限性"""
    has_limitation = bool(re.search(r'局限|失效|不适用|盲区|limitation|blind spot', content, re.IGNORECASE))
    return has_limitation, "有局限性标注 ✅" if has_limitation else "❌ 未找到局限性描述"


def check_expression_dna(content: str) -> tuple[bool, str]:
    """检查表达DNA辨识度"""
    dna_section = bool(re.search(r'表达DNA|Expression DNA|表达风格', content, re.IGNORECASE))
    if not dna_section:
        return False, "❌ 未找到表达DNA section"

    # 检查是否有具体的风格描述（句式、词汇等）
    style_markers = len(re.findall(r'句式|词汇|语气|幽默|节奏|确定性|引用|口头禅', content))
    passed = style_markers >= 3
    return passed, f"表达DNA特征: {style_markers}项 {'✅' if passed else '❌ (应≥3项)'}"


def check_honest_boundary(content: str) -> tuple[bool, str]:
    """检查诚实边界（至少3条）"""
    # 找诚实边界section
    boundary_match = re.search(r'^(?:##\s+[^\n]*诚实边界|## Honest Boundary)(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    if not boundary_match:
        return False, "❌ 未找到诚实边界section"

    boundary_text = boundary_match.group(1)
    # 计算列表项，兼容 bullet 和编号列表
    items = re.findall(r'^\s*(?:[-*]|\d+[.)])\s+', boundary_text, re.MULTILINE)
    count = len(items)
    passed = count >= 3
    return passed, f"诚实边界: {count}条 {'✅' if passed else '❌ (应≥3条)'}"


def check_tensions(content: str) -> tuple[bool, str]:
    """检查内在张力（至少2对）"""
    tension_markers = len(re.findall(r'张力|矛盾|tension|paradox|一方面.*另一方面|既.*又', content, re.IGNORECASE))
    passed = tension_markers >= 2
    return passed, f"内在张力: {tension_markers}处 {'✅' if passed else '❌ (应≥2处)'}"


def check_primary_sources(content: str) -> tuple[bool, str]:
    """检查一手来源占比"""
    # 找调研来源section
    source_section = re.search(r'(?:##\s+.*来源|## Source|## Reference)(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE)
    if not source_section:
        return True, "未找到来源section（跳过检查）"

    source_text = source_section.group(1)
    primary = len(re.findall(r'一手|primary|本人著作|原始', source_text, re.IGNORECASE))
    secondary = len(re.findall(r'二手|secondary|转述|评论', source_text, re.IGNORECASE))
    total = primary + secondary
    if total == 0:
        return True, "未标记来源类型（跳过检查）"

    ratio = primary / total
    passed = ratio > 0.5
    return passed, f"一手来源占比: {primary}/{total} ({ratio:.0%}) {'✅' if passed else '❌ (应>50%)'}"


def check_source_grounding(content: str) -> tuple[bool, str]:
    """检查来源是否具体可追溯。"""
    source_section = re.search(r'(?:##\s+.*来源|## Source|## Reference)(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE)
    if not source_section:
        return False, "❌ 未找到来源section"

    source_text = source_section.group(1)
    urls = re.findall(r'https?://[^\s)>\]]+', source_text)
    concrete = {url.rstrip(".,") for url in urls if is_concrete_url(url)}
    local_sources = re.findall(r'(?:本地文件|local file|file:|/Users/)[^\n]*', source_text, re.IGNORECASE)
    count = len(concrete) + len(local_sources)
    passed = count >= 2
    return passed, f"具体来源: {count}个 {'✅' if passed else '❌ (应≥2个具体URL或本地文件)'}"


def check_agentic_protocol(content: str) -> tuple[bool, str]:
    """检查回答工作流是否包含非通用的研究协议。"""
    match = re.search(r'^(?:##\s+.*(?:Agentic Protocol|回答工作流))(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    if not match:
        return False, "❌ 未找到回答工作流/Agentic Protocol section"

    text = match.group(1)
    has_steps = len(re.findall(r'Step\s*\d|步骤\s*\d|###\s+', text, re.IGNORECASE)) >= 3
    has_research = bool(re.search(r'研究|查证|搜索|WebSearch|事实|证据|source|evidence', text, re.IGNORECASE))
    has_model_link = bool(re.search(r'心智模型|模型|镜片|heuristic|framework|维度', text, re.IGNORECASE))
    passed = has_steps and has_research and has_model_link
    detail = f"steps={has_steps}, research={has_research}, model_link={has_model_link}"
    return passed, f"Agentic Protocol {detail} {'✅' if passed else '❌'}"


def check_intellectual_genealogy(content: str) -> tuple[bool, str]:
    """检查智识谱系是否存在。"""
    has_section = bool(re.search(r'智识谱系|Intellectual Genealogy|Influenced By|influenced by|影响过我的人', content, re.IGNORECASE))
    return has_section, "有智识谱系 ✅" if has_section else "❌ 未找到智识谱系"


def check_soul_kernel(content: str) -> tuple[bool, str]:
    """检查灵魂内核四项是否存在。"""
    match = re.search(
        r'^(?:##\s+.*(?:灵魂内核|Soul Kernel))(.*?)(?=\n##\s|\Z)',
        content,
        re.DOTALL | re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        return False, "❌ 未找到灵魂内核/Soul Kernel section"

    text = match.group(1)
    checks = {
        "default_loop": bool(re.search(r'不得不|Default Loop|Compulsion|默认循环|思想钢印', text, re.IGNORECASE)),
        "sacrifice": bool(re.search(r'愿意.*输|牺牲|Asymmetric Sacrifice|Hard Constraint|代价排序', text, re.IGNORECASE)),
        "paradox": bool(re.search(r'核心矛盾|Core Paradox|张力|矛盾|paradox|tension', text, re.IGNORECASE)),
        "filter": bool(re.search(r'选择性失明|Information Filter|高亮信号|背景噪音|注意力权重|blind spot', text, re.IGNORECASE)),
    }
    evidence = bool(re.search(r'证据|Evidence|来源|Source|推断|置信度|confidence', text, re.IGNORECASE))
    passed = all(checks.values()) and evidence
    detail = ", ".join(f"{key}={value}" for key, value in checks.items()) + f", evidence={evidence}"
    return passed, f"灵魂内核 {detail} {'✅' if passed else '❌'}"


def check_correction_log(content: str) -> tuple[bool, str]:
    """检查是否保留纠错入口。"""
    has_log = bool(re.search(r'Correction Log|纠错记录|修正记录|校正记录', content, re.IGNORECASE))
    return has_log, "有Correction Log ✅" if has_log else "❌ 未找到Correction Log"


def check_evidence_inference_boundary(content: str) -> tuple[bool, str]:
    """检查是否区分证据和推断。"""
    evidence = bool(re.search(r'证据|Evidence|来源|Source', content, re.IGNORECASE))
    inference = bool(re.search(r'推断|Inference|基于.*推测|置信度|confidence', content, re.IGNORECASE))
    passed = evidence and inference
    return passed, f"证据/推断边界 evidence={evidence}, inference={inference} {'✅' if passed else '❌'}"


def is_topic_framework(content: str) -> bool:
    """Detect topic/framework cards that should not be judged as person perspectives."""
    return bool(
        re.search(r'topic-framework|主题Skill|主题框架|##\s+问题路由|##\s+执行规则', content, re.IGNORECASE)
        and re.search(r'##\s+诚实边界', content)
    )


def check_topic_routing(content: str) -> tuple[bool, str]:
    has_routing = bool(re.search(r'##\s+问题路由|routing', content, re.IGNORECASE))
    has_scenarios = len(re.findall(r'场景[A-ZＡ-Ｚ]?:|Scenario|Step\s*\d', content, re.IGNORECASE)) >= 3
    passed = has_routing and has_scenarios
    return passed, f"主题路由 routing={has_routing}, scenarios={has_scenarios} {'✅' if passed else '❌'}"


def check_topic_operability(content: str) -> tuple[bool, str]:
    has_rules = bool(re.search(r'##\s+执行规则|##\s+工作流|workflow', content, re.IGNORECASE))
    has_checkpoint = bool(re.search(r'CHECKPOINT|检查点|Fallback|失败模式', content, re.IGNORECASE))
    passed = has_rules and has_checkpoint
    return passed, f"主题执行 rules={has_rules}, checkpoint={has_checkpoint} {'✅' if passed else '❌'}"


def check_reference_index(content: str) -> tuple[bool, str]:
    has_index = bool(re.search(r'Reference索引|references/|调研来源|来源', content, re.IGNORECASE))
    return has_index, "有Reference/来源索引 ✅" if has_index else "❌ 未找到Reference/来源索引"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 quality_check.py <SKILL.md路径> [--strict]")
        sys.exit(1)

    strict = "--strict" in sys.argv[2:]
    skill_path = Path(sys.argv[1])
    if not skill_path.exists():
        print(f"❌ 文件不存在: {skill_path}")
        sys.exit(1)

    content = skill_path.read_text(encoding='utf-8')

    topic_mode = is_topic_framework(content)
    if topic_mode:
        core_checks = [
            ("主题路由", check_topic_routing),
            ("主题执行", check_topic_operability),
            ("诚实边界", check_honest_boundary),
            ("来源索引", check_reference_index),
        ]
        advanced_checks = [
            ("纠错入口", check_correction_log),
            ("证据推断边界", check_evidence_inference_boundary),
        ]
    else:
        core_checks = [
            ("心智模型数量", check_mental_models),
            ("模型局限性", check_limitations),
            ("表达DNA辨识度", check_expression_dna),
            ("诚实边界", check_honest_boundary),
            ("内在张力", check_tensions),
            ("一手来源占比", check_primary_sources),
        ]
        advanced_checks = [
            ("来源具体性", check_source_grounding),
            ("Agentic协议", check_agentic_protocol),
            ("灵魂内核", check_soul_kernel),
            ("智识谱系", check_intellectual_genealogy),
            ("纠错入口", check_correction_log),
            ("证据推断边界", check_evidence_inference_boundary),
        ]
    checks = core_checks + advanced_checks

    print(f"质量检查: {skill_path.name}")
    mode_name = "topic-framework" if topic_mode else "person-perspective"
    print(f"类型: {mode_name}")
    print(f"模式: {'strict / 新建交付' if strict else 'legacy-compatible / 旧卡兼容'}")
    print("=" * 50)

    passed_count = 0
    total = len(checks)
    blocking_failed = []

    for name, check_fn in checks:
        passed, detail = check_fn(content)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:<12} {status}  {detail}")
        if passed:
            passed_count += 1
        elif strict or name in {item[0] for item in core_checks}:
            blocking_failed.append(name)

    print("=" * 50)
    print(f"结果: {passed_count}/{total} 通过")

    if not blocking_failed and passed_count == total:
        print("🎉 全部通过，可以交付")
    elif not blocking_failed:
        print("⚠️ 核心项通过；高级项为旧卡兼容警告。新建/更新卡请使用 --strict")
    elif passed_count >= total - 1:
        print("⚠️ 基本通过，建议修复不通过项后交付")
    else:
        print(f"❌ 阻塞项不通过: {', '.join(blocking_failed)}，建议回到对应Phase迭代")

    sys.exit(0 if not blocking_failed else 1)


if __name__ == '__main__':
    main()
