# Obsidian 笔记

Obsidian 的核心不是文件夹，而是链接。文件夹只负责操作边界。

推荐结构：

```
Vault/
├── Inbox/
├── Notes/
├── MOC/
├── Projects/
├── Attachments/
├── Templates/
└── Archive/
```

规则：

- 不按“哲学/电影/技术/心理学”建大型主题文件夹。
- 主题关系用 MOC、标签、双链表达。
- 项目笔记可以进 `Projects/项目名/`，因为项目有交付边界。
- 附件统一放 `Attachments/`，避免散落。

验证：

```bash
find Vault -mindepth 1 -maxdepth 1 -type d -print

find Vault -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.pdf" -o -iname "*.mp4" \) ! -path "*/Attachments/*" -print | head -10
```
