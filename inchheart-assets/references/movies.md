# 电影

这里指电影/剧集收藏，需要 Plex/Infuse/Emby 等播放器识别海报和元数据。

物理结构：

```
VideoLibrary/
├── Movies/
│   └── 三峡好人 (2006)/
│       └── 三峡好人 (2006).mkv
└── TV Shows/
    └── 剧集名称/
        └── Season 01/
            └── S01E01.mkv
```

规则：

- 电影和剧集必须分开。
- 电影使用 `片名 (年份)`。
- 剧集使用 `Season 01/S01E01`。
- 不按导演、类型、国家、年代建物理目录。
- 导演、流派、年代、主题用播放器 Collection、标签或 Obsidian MOC 表达。

电影验证：

```bash
ls VideoLibrary/

find VideoLibrary/Movies -type f \( -iname "*.mkv" -o -iname "*.mp4" -o -iname "*.m4v" -o -iname "*.avi" \) ! -name "*([0-9][0-9][0-9][0-9])*" -print | head -5

find "VideoLibrary/TV Shows" -type f \( -iname "*.mkv" -o -iname "*.mp4" -o -iname "*.m4v" -o -iname "*.avi" \) ! -name "S[0-9][0-9]E[0-9][0-9]*" -print | head -5
```
