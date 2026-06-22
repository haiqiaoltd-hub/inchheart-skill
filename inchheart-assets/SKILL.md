---
name: inchheart-assets
description: "Use when organizing or refactoring personal digital assets: ebook libraries, project repositories, source repositories, local services, folders, images, videos, movies, browser bookmarks, and Obsidian notes. Applies single-axis physical placement, discipline-specific book taxonomy, and graph/tag indexing."
tags: [assets, file-organization, repo, source-repo, local-service, ebook, folder, video, movie, image, bookmark, obsidian, taxonomy]
---

# 数字资产分类整理

本技能用于整理个人数字资产：书库、项目仓库、源码收藏、本地服务、通用文件夹、图片、普通视频、电影/剧集、浏览器书签、Obsidian 笔记。

核心判断：

> 文件夹负责唯一归位；块茎/图谱负责多重抵达。前者是分类，后者是索引。

不要说“块茎分类”。块茎是关系拓扑，用来表达多重入口；它不能决定一个文件物理上放在哪里。

## 适用场景

- 用户要整理、重构、迁移个人文件体系。
- 文件夹混用了主题、时间、项目、格式、状态、来源。
- 书库、图片、视频、电影、书签等资产需要分开定标准。
- 跨主题文件不知道放哪，需要物理层和逻辑层分离。

## 不适用场景

- 工作项目代码：按项目边界组织即可。
- 系统配置文件：不是个人数字资产。
- 应用数据库：Calibre/Eagle/Photos 等数据库由应用自己管理。
- 临时下载：进待整理区或直接删除。

## 先读哪个文档

根据用户正在整理的资产类型，只读取对应 reference，不要一次性加载全部文档。

| 用户任务 | 读取文档 |
|---|---|
| 整理电子书、书库、学科分类、哲学/文学/历史等藏书 | `references/book-library.md` |
| 整理项目仓库、源码收藏、本地部署服务、Git 仓库目录 | `references/repositories.md` |
| 整理普通文件夹、下载目录、资料库、项目素材根目录 | `references/folders.md` |
| 整理图片、截图、壁纸、设计素材、照片导出 | `references/images.md` |
| 整理普通视频、课程、教程、网络视频、项目素材视频 | `references/videos.md` |
| 整理电影/剧集、Plex/Infuse/Emby 媒体库 | `references/movies.md` |
| 整理浏览器书签、HTML 书签导出、入口/资料源分工 | `references/browser-bookmarks.md` |
| 整理 Obsidian 笔记库、MOC、附件、双链结构 | `references/obsidian-notes.md` |
| 讨论块茎、图谱、多入口索引、树和图的分工 | `references/rhizome-file-management.md` |

## 通用原则

### 单一主轴

一个物理文件夹，在同一层级内，只能使用一个分类维度。

坏例子：

```text
资料/
├── 哲学/
├── 2026/
├── 已读/
└── AI/
```

这里混用了主题、时间、状态、领域，后续必然出现“同一个文件到底放哪”的问题。

### 物理/逻辑分离

| 层 | 职责 | 允许的结构 |
|---|---|---|
| 物理层 | 决定文件唯一位置 | 文件夹、文件名、少量固定目录 |
| 元数据层 | 记录客观属性 | 作者、年份、格式、来源、评分 |
| 索引层 | 提供多个入口 | 标签、MOC、书单、播放列表、Collection |
| 关联层 | 表达跨领域关系 | Obsidian 双链、图谱、研究笔记 |

物理层要稳定、死板、可批量处理；逻辑层可以自由、多义、不断生长。

### 主轴选择顺序

1. 软件协议优先：Plex/Infuse/Emby/Calibre/Photos 有固定规范时，服从软件。
2. 项目边界优先：素材明确服务某个项目时，项目是主轴。
3. 载体属性优先：格式、创建时间、媒体类型足够稳定时，用载体属性。
4. 受控分类优先：必须按主题放置时，只能用固定分类表。
5. 工作流状态优先：书签、待处理资料等入口型对象，按状态分类。

### 命名偏好

- 默认不使用数字前缀作为排序手段。
- 不建“重要”“有用”“以后看”“喜欢”这类情绪目录。
- 来源、状态、主题、时间不要混在同一层。
- 跨主题归属交给标签、MOC、Collection 或笔记，不强塞进物理目录。

## 块茎的正确位置

| 问题 | 用文件夹树 | 用块茎/图谱 |
|---|---|---|
| 这个文件物理上放哪 | 是 | 否 |
| 这个文件属于哪些主题 | 否 | 是 |
| 如何批量备份/同步/迁移 | 是 | 否 |
| 如何从灵感找到素材 | 否 | 是 |
| 如何给软件识别 | 是 | 否 |
| 如何表达跨领域关系 | 否 | 是 |

判断句：

> 如果问题需要唯一答案，用树；如果问题需要多个入口，用图。

## 工作流程

1. 确认资产段落：书库、项目仓库、源码收藏、本地服务、文件夹、图片、视频、电影、浏览器书签、Obsidian 笔记。
2. 读取该资产段落对应的 reference 文档。
3. 确认是否有软件协议：Plex、Infuse、Calibre、Photos、Eagle 等。
4. 若是书库，先判断学科类型，再使用该学科的内部主轴。
5. 选择唯一物理主轴，并明确拒绝其他主轴进入同一层级。
6. 给出新目录树或书签树。
7. 先做 dry-run 或列出迁移计划，再执行批量移动/重命名/HTML 改写。
8. 迁移后运行对应 reference 里的验证检查。
9. 汇报物理路径、逻辑索引建议、残留风险。

不要在没有确认资产类型和根目录时直接移动用户文件。

## 汇报模板

1. 资产段落：本次处理书库/项目仓库/源码收藏/本地服务/文件夹/图片/视频/电影/书签/笔记？
2. 混乱诊断：混用了哪些主轴？
3. 物理主轴：最终选择哪个唯一主轴，为什么？
4. 新结构：目录树。
5. 迁移动作：dry-run、移动、重命名、跳过项。
6. 逻辑层建议：标签、MOC、Collection、软件库。
7. 验证结果：对应段落的检查输出。
8. 残留风险：无法自动判断或需要用户决策的部分。

## 用户偏好

| 项 | 值 |
|---|---|
| 用户 | Wang Donghong（王东洪） |
| Obsidian 笔记库 | `/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/笔记本/寸心` |
| 项目仓库 | `/Users/mac/Repository/Projects` |
| 源码收藏 | `/Users/mac/Repository/Sources` |
| 本地服务 | `/Users/mac/Repository/Services` |
| 图片库路径 | `/Users/mac/Pictures/ImageLibrary` |
| 偏好工具 | 本地部署优先；脚本化批量操作 |
| 目录命名 | 默认不用数字前缀 |

## 参考

- `references/book-library.md`
- `references/repositories.md`
- `references/folders.md`
- `references/images.md`
- `references/videos.md`
- `references/movies.md`
- `references/browser-bookmarks.md`
- `references/obsidian-notes.md`
- `references/rhizome-file-management.md`
- EPUB 元数据优化：`inchheart-epub`
