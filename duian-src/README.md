# 《对岸》原型源文件

- `build.py`：剧情树（剧本 v2）和每格素材 → 生成 `../duian/index.html` 和 `配音清单.txt`
- `index.tpl.html`：播放器模板
- `media_map.json`：素材名 → `duian/m/NN` 的固定编号（已有文件永不改号）
- `deploy.sh <commit>`：生成媒体走 jsDelivr 的线上版

加新素材：把文件按 `img_*.webp` / `vid_*.mp4` / `aud_*.mp3` 命名放进 `new/`（不进 git），在 `build.py` 里引用，运行 `python3 build.py`，它会复制进 `duian/m/` 并分配新编号。
