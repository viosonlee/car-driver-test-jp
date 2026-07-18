# 日本驾照笔试练习

Vue 3 + TypeScript + Vite 构建的离线练习应用，题库以中文版《交通规则教程》为主要校对来源。

## 开发与检查

```bash
npm install
npm run audit:questions
npm run build
```

`audit:questions` 会检查题目 ID、题型结构、图片文件、图片题中日文案、真/假配对和 PDF 来源页标签。

## PDF 图片题维护

仓库根目录放置参考 PDF 后，可重新生成经人工核对的标志和标线素材，并幂等修复题库：

```bash
python -m pip install -r requirements-audit.txt
python scripts/extract_pdf_quiz_assets.py
python scripts/repair_image_question_bank.py
npm run audit:questions
```

图片题的覆盖率按唯一图片知识点统计，不按同图的真/假题数量重复计算。
