# 项目仓库、源码收藏与本地服务

这类目录不要按“编程语言”或“技术主题”作为第一主轴。更稳定的主轴是对象角色：

| 目录 | 角色 | 核心问题 |
|---|---|---|
| `/Users/mac/Repository/Projects` | 自己要维护、修改、交付的项目 | 这个项目属于哪种交付物？ |
| `/Users/mac/Repository/Sources` | 外部源码收藏、阅读、研究、参考 | 这个源码来自哪里，用来研究什么？ |
| `/Users/mac/Repository/Services` | 本机部署、运行、调试的服务实例 | 这个服务如何启动、配置、持久化？ |

判断句：

> 仓库是代码边界；源码收藏是阅读边界；本地服务是运行边界。

不要把它们混在同一棵树里。

## Projects

`Projects` 放用户自己拥有、正在开发、会提交修改、会长期维护的项目。

推荐主轴：交付物类型 + 所属系统。

```text
Projects/
├── InchHeart Skill/
├── MCP/
├── Apps/
├── Websites/
├── Tools/
├── Experiments/
└── Archive/
```

规则：

- 用户自己创建、维护、改代码的项目放这里。
- Skill、MCP、插件、网站、工具按交付类型分。
- 临时实验放 `Experiments/`，成熟后再移动到正式类别。
- 不按语言建顶层：`Python/`、`Go/`、`Rust/` 不是稳定主轴。
- 不把已部署服务的数据、日志、运行配置放进这里；那些属于 `Services`。
- 不把只为阅读而克隆的外部项目放进这里；那些属于 `Sources`。
- 不使用数字前缀。

适合进入 `Projects` 的例子：

| 类型 | 示例 |
|---|---|
| 技能 | `InchHeart Skill/inchheart-assets` |
| MCP | `MCP/inchheart-search` |
| 应用 | `Apps/some-app` |
| 个人工具 | `Tools/bookmark-cleaner` |
| 网站 | `Websites/eastart-site` |

## Sources

`Sources` 放外部项目源码：阅读、研究、临时试跑、学习架构、参考实现。

推荐主轴：来源生态 + 研究用途。

```text
Sources/
├── GitHub/
│   ├── openai/
│   ├── anthropics/
│   ├── google-gemini/
│   └── community/
├── AI-Code/
├── Browser-Automation/
├── Obsidian/
├── Terminal/
└── Archive/
```

规则：

- 外部项目如果只是阅读或研究，放 `Sources`。
- 可以按来源 owner/repo 保存，便于追踪上游。
- 可以按研究主题建集合，但不要和 `Projects` 混放。
- 不在外部源码里直接做长期个人改造；如果要维护 fork 或二次开发，复制/迁移到 `Projects`。
- 克隆后应保留上游信息：remote、README、notes。
- 长期不用的源码进 `Archive/`，不要散落在顶层。

判断：

| 情况 | 放哪 |
|---|---|
| 只是读源码 | `Sources` |
| 临时跑 demo | `Sources` |
| 准备长期修改 | `Projects` |
| 已经成为本机服务 | 源码可在 `Projects`，运行实例在 `Services` |

## Services

`Services` 放本机部署和运行的服务。这里的主轴不是代码，而是服务实例。

推荐主轴：服务边界。

```text
Services/
├── search/
├── bookmarks/
├── obsidian/
├── browser/
├── proxy/
├── ai-gateway/
└── archive/
```

单个服务建议结构：

```text
service-name/
├── README.md
├── config/
├── data/
├── logs/
├── scripts/
├── docker-compose.yml
└── .env.example
```

规则：

- 运行数据、配置、日志、数据库、compose 文件放这里。
- 服务源码如果是自己维护的项目，可以在 `Projects`；`Services` 只保留部署实例。
- 服务源码如果只是外部项目，可以在 `Sources`；`Services` 记录如何运行它。
- 密钥文件不要进 Git；用 `.env`，并保留 `.env.example`。
- 每个服务应能回答：如何启动、如何停止、端口是什么、数据在哪里、如何备份。
- 不要把多个服务的数据混在同一个 `data/`。

## 三者分工

| 问题 | Projects | Sources | Services |
|---|---|---|---|
| 我是否维护代码 | 是 | 否/临时 | 不一定 |
| 是否关注上游源码 | 辅助 | 是 | 辅助 |
| 是否关注端口和运行状态 | 辅助 | 否 | 是 |
| 是否有持久化数据 | 少量 | 否 | 是 |
| 是否可以删除重拉 | 不一定 | 通常可以 | 谨慎，可能有数据 |

## 迁移流程

1. 扫描三个目录下的 Git 仓库、服务配置、数据库和日志。
2. 判断每个对象的角色：自有项目、外部源码、运行服务。
3. 先做 dry-run，列出移动计划。
4. 对 Git 仓库先检查 dirty 状态，避免移动未保存工作。
5. 对服务先记录端口、启动方式、数据目录，再移动。
6. 迁移后验证 remote、启动脚本、数据路径是否仍正常。

## 验证命令

```bash
# 找 Git 仓库
find /Users/mac/Repository/Projects /Users/mac/Repository/Sources /Users/mac/Repository/Services -name .git -type d -prune

# 检查 Projects 是否混入大量外部只读源码
find /Users/mac/Repository/Projects -name .git -type d -prune -print

# 检查 Services 的服务配置
find /Users/mac/Repository/Services -maxdepth 3 \( -name docker-compose.yml -o -name package.json -o -name pyproject.toml -o -name README.md \) -print

# 检查可能的运行数据
find /Users/mac/Repository/Services -maxdepth 3 \( -iname "data" -o -iname "logs" -o -iname "*.db" -o -iname "*.sqlite" \) -print
```

## 汇报重点

- 哪些目录是自有项目。
- 哪些目录只是外部源码收藏。
- 哪些目录是运行服务实例。
- 哪些服务有数据和端口风险。
- 哪些仓库 dirty，不能直接移动。
- 哪些对象需要用户决定归属。
