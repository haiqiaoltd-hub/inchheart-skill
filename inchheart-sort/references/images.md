# 图片

图片分三类处理，不要混成一个标准。

| 图片类型 | 物理主轴 | 说明 |
|---|---|---|
| 日常照片 | Photos/Lightroom 软件库 | 不在 Finder 手动分类 |
| 设计/截图/壁纸素材 | 格式或 Eagle 库 | 格式利于批处理，Eagle 利于标签 |
| 项目图片素材 | 项目 | 服务具体项目时放进项目目录 |

手动图片库：

```
ImageLibrary/
├── GIF/
├── JPEG/
├── PNG/
├── SVG/
├── WEBP/
└── HEIC/
```

命名规则：

```text
YYYY-MM-DD_HH-MM-SS.ext
```

规则：

- 日常照片导入 Apple Photos 或 Lightroom。
- 非照片素材可以按格式存放，文件名使用创建时间。
- 项目相关图片放到项目目录，不塞进通用图片库。
- 不按“好看/灵感/重要/电影感”建物理目录。
- Eagle/Photos 负责标签、人物、地理位置、相册。

图片验证：

```bash
find ImageLibrary -mindepth 1 -maxdepth 1 -type d -print

find ImageLibrary -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.webp" -o -iname "*.heic" -o -iname "*.svg" \) ! -name "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[0-9][0-9]-[0-9][0-9]-[0-9][0-9].*" -print | head -5
```
