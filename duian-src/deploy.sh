#!/bin/sh
# 发布到 dylanhe.cn/duian：页面走 GitHub Pages，媒体走 jsDelivr（钉在某个 commit 上，国内快）。
# 用法：先把新媒体（duian/m/ 里新增的文件）提交并推送，然后
#   ./deploy.sh <那个 commit 的完整 hash>
# 再提交推送生成的 duian/index.html。jsDelivr 取不到的文件会自动退回 GitHub Pages 上的同一份。
set -e
cd "$(dirname "$0")"
[ -n "$1" ] || { echo "用法：./deploy.sh <commit hash>"; exit 1; }
python3 build.py "https://cdn.jsdelivr.net/gh/DDDylan123/dylan-he-films@$1/duian/"
