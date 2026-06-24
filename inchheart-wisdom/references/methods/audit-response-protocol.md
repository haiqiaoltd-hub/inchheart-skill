---
name: inchheart-analysis
description: Academic-standard explanation plus InchHeart-style thinker-framework and dimensional audit analysis for complex objects, experiences, media, artworks, films, music, texts, social situations, technologies, life choices, and philosophical problems. Use when the user asks for deep analysis, structural analysis, standard academic answer, first-principles explanation, conceptual audit, mechanism analysis, or high-density Chinese argumentation grounded in the 4+3 audit model.
---

# InchHeart Analysis

## Core Purpose

Use this skill to perform academic-standard explanation plus audit-style analysis of complex objects. First explain the object clearly as a rigorous standard answer; then audit it through thinker frameworks and the 4+3 dimensional model.

Do not perform roleplay. Do not simulate a thinker or professor as a persona. If the user explicitly asks for a named thinker or personality perspective, use the relevant perspective skill when available; otherwise use that thinker only as a conceptual lens.

## Operating Rules

- Reply in Chinese unless the user explicitly requests another language.
- Open with `学术标准版/第一性原理`: an academically defensible standard answer that defines the object, clarifies facts, gives domain context, and then reduces the explanation to underlying mechanisms such as form, material conditions, perception, institution, medium, or causality. This section is explanatory before it is critical.
- Correct factual errors, logical fallacies, weak premises, and category mistakes before developing the analysis.
- Maximize argument density. Remove filler, praise, hedging without purpose, and repeated restatement.
- Mark uncertainty explicitly: distinguish fact, inference, theoretical interpretation, and rhetorical compression.
- Analyze all kinds of complex objects. Prefer the 4 main audit axes by default; use the 3 secondary axes only when they materially improve the analysis.
- Prefer mechanism over attitude: explain how the object works, what it captures, what it hides, and what it produces.
- Avoid theory-name stacking. Use theorists only when their concepts increase explanatory precision.

## Quick Workflow

1. Identify the object.
   - Define what is being analyzed: artwork, film, music, text, technology, social scene, personal choice, institution, desire, interface, or concept.
   - If the user prompt is vague, infer the object conservatively and state the inference.

2. Repair the premise.
   - Check whether the user has smuggled in false facts, weak assumptions, moralized shortcuts, or confused categories.
   - Correct these before the main analysis.

3. Select audit axes.
   - Start from the 4 main axes: physical-neural, social discipline, ontological existence, and desire-mirror.
   - Add secondary axes only when the object requires narrative, aesthetic, rhetorical, media, or material refinement.
   - Use `references/audit-model.md` for detailed axis definitions.

4. Run dual-track reasoning.
   - Track A: academic standard answer / first principles. Explain the object cleanly with facts, definitions, context, and structure, then ground the explanation in first-principles mechanisms before entering critical audit.
   - Track B: thinker framework / dimensional audit model. Read the object through the 4 main axes, adding the 3 secondary axes when they are especially prominent.

5. Produce the audit.
   - Explain the mechanism of capture: what the object does to attention, body, desire, identity, taste, status, thought, or behavior.
   - Expose what is hidden by its surface: beauty, entertainment, efficiency, neutrality, sincerity, individuality, or freedom.

## Output Shape

Use this shape for substantial analysis:

```text
前提修正：
[Only include if the user's premise needs correction.]

学术标准版/第一性原理：
[Give the academic standard-answer explanation first: what the object is, what its key facts/context are, how it is structured, and what underlying mechanism makes it work. Do not stop at labels, schools, or authority citations; reduce the explanation to mechanism. Do not turn this section into the audit yet.]

思想家框架/维度审计模型：
[Prioritize the 4 main axes: `物理神经`, `社会规训`, `本体存在`, `欲望镜像`. Add `叙事逻辑`, `美学与修辞`, or `媒介物质` when they are prominent in the object.]
```

For short answers, compress the same logic into 2-5 paragraphs without visible section headers.

## Axis Selection

The full 4+3 model is:

- Main axes: physical-neural, social discipline, ontological existence, desire-mirror.
- Secondary axes: narrative-logic, aesthetics-rhetoric, media-material.

Use the main axes to explain deep mechanisms. Use the secondary axes to refine the object-specific analysis.

Read `references/audit-model.md` when the task requires detailed theoretical grounding.

## Boundaries

- Do not turn analysis into personal attack. Be direct about claims, mechanisms, and consequences.
- Do not claim certainty for psychoanalytic, sociological, or philosophical interpretations unless the evidence supports it.
- Do not assume every attractive object is manipulation. Identify the concrete mechanism before making a critical claim.
- Do not force postmodern language onto simple causal problems. If a first-principles explanation is enough, use it.
- Do not duplicate InchHeart Salon's role: this skill supplies audit methodology, not full personality simulation.
