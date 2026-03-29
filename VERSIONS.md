# SEO & GEO Skills Library — Versions

Current versions of all skills. Agents can fetch this file from `https://raw.githubusercontent.com/aaron-he-zhu/seo-geo-claude-skills/main/VERSIONS.md` once per session to check for updates.

**Versioning**: Skill versions (`metadata.version` in SKILL.md) track skill content changes independently. Plugin version (in `plugin.json`) tracks manifest and infrastructure changes.

## Skills

| Skill | Category | Version | Last Updated |
|-------|----------|---------|--------------|
| keyword-research | research | 5.1.0 | 2026-03-29 |
| competitor-analysis | research | 5.1.0 | 2026-03-29 |
| serp-analysis | research | 5.1.0 | 2026-03-29 |
| content-gap-analysis | research | 5.1.0 | 2026-03-29 |
| seo-content-writer | build | 5.1.0 | 2026-03-29 |
| geo-content-optimizer | build | 5.1.0 | 2026-03-29 |
| meta-tags-optimizer | build | 5.1.0 | 2026-03-29 |
| schema-markup-generator | build | 5.1.0 | 2026-03-29 |
| on-page-seo-auditor | optimize | 5.1.0 | 2026-03-29 |
| technical-seo-checker | optimize | 5.1.0 | 2026-03-29 |
| internal-linking-optimizer | optimize | 5.1.0 | 2026-03-29 |
| content-refresher | optimize | 5.1.0 | 2026-03-29 |
| rank-tracker | monitor | 5.1.0 | 2026-03-29 |
| backlink-analyzer | monitor | 5.1.0 | 2026-03-29 |
| performance-reporter | monitor | 5.1.0 | 2026-03-29 |
| alert-manager | monitor | 5.1.0 | 2026-03-29 |
| content-quality-auditor | cross-cutting | 5.1.0 | 2026-03-29 |
| domain-authority-auditor | cross-cutting | 5.1.0 | 2026-03-29 |
| entity-optimizer | cross-cutting | 5.1.0 | 2026-03-29 |
| memory-management | cross-cutting | 5.1.0 | 2026-03-29 |

## Changelog

### v5.1.0 (2026-03-29)

Multilingual trigger optimization and refinement for ClawHub/skills.sh marketplace discoverability. Reviewed by 8-agent team (code reviewer, trigger quality, description SEO, ZH/JA/KO/ES/EN language specialists).

**Description rewrite (all 20 skills)**:
- Rewrote all descriptions to fit within 250-char truncation limit (were 376-655 chars, all truncated)
- Added 5-language coverage: EN + ZH + JA + KO + ES in every description
- Pain-point phrasing over feature names for better LLM semantic matching
- Reordered YAML fields: name → description → version (maximizes ClawHub file[0:250] info density)
- Refined description openings: content-quality-auditor leads with "Publish-readiness gate", memory-management leads with "Persist SEO/GEO campaign context"
- geo-content-optimizer now names 6 AI products: ChatGPT, Perplexity, AI Overviews, Gemini, Claude, Copilot

**Triggers expansion (all 20 skills, ~247 → ~750+)**:
- 11 categories: EN-formal, EN-casual, EN-question, EN-competitor, ZH-pro, ZH-casual, JA, KO, ES, PT, misspellings
- ZH: Added 挖词, 收录, 友链, 月报, 品牌词, TDK, 锚文本, 词库, 数据看板 and 20+ more
- KO: Added casual question forms to 8 skills (키워드 어떻게 찾아요, 왜 순위가 안 올라가, etc.)
- JA: Added ロングテールキーワード, インデックス登録, 検索順位チェック, モバイル最適化, 検索意図分析
- ES: Added posicionamiento web, mi sitio no aparece en Google, posicionamiento SEO
- PT: Added meu site não aparece no Google, monitoramento de posições
- EN: Added canonical tag issues, my rankings tanked, Google penalty recovery, Perplexity/ChatGPT competitor triggers

**Trigger mislocation fixes**:
- Moved "排名上不去" from seo-content-writer to on-page-seo-auditor
- Replaced "帮我写软文" (advertorial) → "帮我写SEO文章"
- Replaced "网站打不开" (hosting) → "网站加载太慢"
- Replaced "流量太低" (ambiguous) → "帮我挖词"
- Replaced "网站权重怎么样" (Baidu Weight) → "网站可信度怎么样"
- Fixed EN cross-skill ambiguity: "off-page SEO" → "link profile analysis"

**Tags expansion (all 20 skills)**:
- Added multilingual tags (ZH, JA, KO, ES) to all skills
- Added competitor tool cross-discovery tags

**Infrastructure**:
- Added scripts/validate-descriptions.py (dual-budget validation: desc≤250 + file[0:250] coverage)
- Fixed 5 pre-existing YAML formatting bugs in trigger lists
- Fixed JA trigger quality: サープ→検索結果, パフォーマンス報告→パフォーマンスレポート

### v5.0.0 (2026-03-29)

Unified operating model: shared skill contract, prompt-based hook automation, three-tier temperature memory, protocol-layer gates, state write-through, trigger widening, and published-link hardening.

**Unified skill contract (Plan C)**:
- Added shared [skill contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md) and [state model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) reference documents
- Updated all 20 SKILL.md files with `When This Must Trigger`, `Quick Start`, `Skill Contract`, and `Next Best Skill` sections
- Replaced bulky per-file 20-skill navigation blocks with a compact system-mode header

**Hook lifecycle (Plan C+)**:
- Added 4-event prompt-based hooks in hooks/hooks.json (SessionStart, UserPromptSubmit, PostToolUse, Stop)
- SessionStart auto-loads memory/hot-cache.md and reminds stale open loops (>7 days)
- PostToolUse auto-recommends content-quality-auditor after content writing
- Stop prompts to save findings and auto-saves veto-level issues to hot-cache

**Temperature memory (Plan C+)**:
- Three-tier model: HOT (80 lines, auto-loaded) / WARM (200 lines/file, on-demand) / COLD (archive, unlimited)
- Automatic promotion (2+ skill refs or 3+ refs within 7 days) and demotion (30 days HOT→WARM, 90 days WARM→COLD)
- memory-management upgraded to Campaign Memory Loop with sole WARM→COLD archival authority

**Protocol-layer gates (Plan C + C+)**:
- content-quality-auditor → Publish Readiness Gate with SHIP/FIX/BLOCK verdicts
- domain-authority-auditor → Citation Trust Gate with TRUSTED/CAUTIOUS/UNTRUSTED verdicts
- entity-optimizer → Canonical Entity Profile with sole write authority for memory/entities/
- memory-management → Campaign Memory Loop with cross-skill aggregation and lifecycle management
- Gate checks automatically recommended in build and monitor skill handoffs

**State write-through (Plan C+)**:
- All 20 skills include Save Results flow with user confirmation
- Veto-level issues (CORE-EEAT T04/C01/R10, CITE T03/T05/T09) auto-save to memory/hot-cache.md
- Dated file naming: YYYY-MM-DD-topic.md across all memory/ paths

**Trigger widening (Plan C+)**:
- All 20 skills add 3-4 everyday language triggers alongside professional terms
- When This Must Trigger sections add scenario lead-in for intent matching without SEO terminology

**Published link reliability**:
- Replaced repo-internal relative Markdown links with absolute GitHub links across all docs, commands, skills, and references
- Updated README badges and navigation links to point at canonical GitHub pages
- Corrected mis-nested cross-reference targets during link conversion

**Documentation and positioning**:
- README, AGENTS, CLAUDE, CONTRIBUTING updated for operating-model positioning
- AGENTS.md: new Hooks & Automation section with hook table and temperature memory model
- CLAUDE.md: added hook automation and temperature memory references
- README: added Automation and Memory subsections to Operating Model

**Infrastructure**:
- plugin.json: hooks array expanded to 4 events; description updated; version 5.0.0
- marketplace.json: version synced to 5.0.0
- All 20 skill metadata.version bumped to 5.0.0

### v4.0.0 (2026-03-24)

ClawHub-first marketplace optimization: security fixes, vector search descriptions, multi-ecosystem install documentation.

**Security & metadata fixes**:
- Removed self-contradictory `metadata.openclaw` blocks from 9 skills (soft dependencies incorrectly declared as hard requirements)
- Fixed copy-paste error: alert-manager and performance-reporter had `primaryEnv: AMPLITUDE_API_KEY` (unrelated to their function)
- Added credential-optional statements to 11 skills with external tool integrations
- Added `homepage` field to all 20 SKILL.md frontmatters

**ClawHub search optimization**:
- Rewrote all 20 skill descriptions with natural language summaries prepended for vector search discovery
- Streamlined trigger phrases to 6-8 highest-frequency per skill
- Updated footer links to include GitHub, ClawHub, and skills.sh

**Documentation migration**:
- README: Replaced single-recommendation install with tool-based routing table (OpenClaw / Claude Code / Cursor+Codex+Windsurf)
- AGENTS.md: ClawHub moved to first position in ecosystem table; install section uses routing table
- CONTRIBUTING.md: Fixed template missing ClawHub and Vercel Labs in compatibility field; added `clawhub publish` / `clawhub sync` commands
- CLAUDE.md: Added ClawHub and skills.sh marketplace links
- config.yml: Added ClawHub Marketplace as issue template contact link

**Infrastructure**:
- plugin.json: homepage changed from skills.sh to GitHub repo URL (neutral)
- marketplace.json: version synced to 4.0.0
- validate-skill.sh: Updated openclaw check from WARN-if-missing to PASS-if-missing (pure instruction skills don't need runtime declarations)

### v3.0.0 (2026-03-04)

Consolidates all post-2.0.0 changes into a single major release aligned with plugin-dev, skill-creator, and financial-services-plugins standards.

**Plugin manifest (plugin-dev spec)**:
- Added `schemaVersion: "1.0.0"` and `id` fields
- Added `description` to all 9 commands and 20 skills in plugin.json and marketplace.json
- Restructured `hooks` from object to array format `[{event, path}]`
- Restructured `mcpServers` from object to array format `[{id, path}]`
- Added `displayName`, `capabilities`, `metadata` blocks
- Added typed `parameters` to all 9 command files

**Skill format (skill-creator spec)**:
- Added top-level `version` field to all 20 SKILL.md frontmatters
- Added `compatibility` field to all 20 skills
- Added `allowed-tools: WebFetch` to 5 skills with live URL fetching
- Added `allowed-tools: ["WebFetch"]` to 3 commands (audit-page, check-technical, generate-schema)
- Trimmed 7 SKILL.md files to ≤350 lines (deduplicated tags, condensed verbose sections)

**Infrastructure (financial-services-plugins patterns)**:
- Added `CLAUDE.md` for Claude Code auto-loading context
- Added `hooks/hooks.json` scaffold
- Added `scripts/validate-skill.sh` CLI validation tool
- Added disclaimer section to README.md
- Moved `marketplace.json` from `.claude-plugin/` to repo root
- Extracted reference data from 5 oversized skills into `references/` subdirectories

**Fixes**:
- Fixed `marketplace.json` name mismatch
- Fixed step numbering bug in `geo-content-optimizer`
- Updated CONTRIBUTING.md with 5-file sync requirement

### v2.0.0 (2026-02-08)
- CORE-EEAT content quality benchmark (80 items, 8 dimensions, veto system)
- CITE domain authority rating (40 items, 4 dimensions, veto system)
- Content-type weighted scoring and domain-type weighted scoring
- Entity optimizer with Knowledge Graph + Wikidata + AI resolution
- Memory management with two-layer hot/cold storage
- Tool-agnostic ~~placeholder connector system with progressive enhancement tiers
- 9 one-shot commands (`/seo:audit-page`, `/seo:audit-domain`, etc.)
- Inter-skill handoff protocol with score passthrough
- skills.sh marketplace and Claude Code plugin distribution

### v1.0.0 (2026-01-28)
- 20 skills across 5 categories (research, build, optimize, monitor, cross-cutting)
- Basic SEO and GEO content optimization workflows
