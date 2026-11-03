# Qinyu Luo 个人站

这是独立的 Astro 静态新站，用于替代原来的 Jekyll 模板。生产地址为 https://logic-10.github.io/，本地预览地址为 http://127.0.0.1:4174/。

## 本地使用

需要 Node.js 24 或更新版本、npm 和 Python 3.10 或更新版本；内容完整性检查使用固定版本的 `pypdf`。

```sh
npm ci
python3 -m pip install -r requirements-dev.txt
npm run build
npm run verify
npm run preview
```

打开 <http://127.0.0.1:4174/>。预览只提供 `dist/` 中的构建文件；修改源码后需重新运行 `npm run build`。离线检查覆盖生成页面中的本地资源与页内、跨页锚点，不访问外部链接。

## 主要文件

- `src/pages/`：首页、研究、产品与笔记等页面。
- `src/components/`、`src/layouts/`：共享组件与页面框架。
- `src/styles/`：全站样式。
- `public/`：公开图片与项目附件。
- `scripts/`：本地预览与构建结果检查。

完整成果列表记录在 `src/data/research.ts` 与 `scholar-additions.ts`，依据 2026-11-03 读取的 Google Scholar 23 条记录整理为 14 项成果，含 Seed2.0 与 Seed2.1 Model Card。旧题名和重复版本保留在对应详情页。原始记录保存在 `src/data/scholar-records.json`；`npm run verify` 会核对每条记录的覆盖及配图。

论文的核心方法图、结果图与来源在 `src/data/publication-images.json` 中维护，卡片使用正文图而非整页首页缩略图。数学预印本没有插图，使用早稿核心不等式的原文局部，图注保留早期版本及未审稿说明。听诊器保留在二级项目页面，通过 Projects 页下方的 Other explorations 入口访问。

首页与 Research 共用 `displayPublications` 顺序：Seed2.1、Seed2.0 优先展示，其余成果按发表年月从新到旧。`src/data/publication-dates.json` 保存每项年月、依据和来源；会议成果用正式出版月（ICLR 使用会议月），预印本和技术报告用公开发布月，项目报告使用初始公开版本月。同月保留既有相对顺序；卡片显示年月。

两个页面共用论文检索与分页组件，每页 10 项，列表上下均可点击页码、上一页/下一页或下拉选择页码。关键词检索覆盖全部成果的题名、旧题名、作者、摘要、领域、场合和年月；先筛选再分页，修改关键词或领域时回到第一页。关闭 JavaScript 时仍可阅读完整列表。

所有阅读材料在网站内呈现：13 份论文及报告全文、35 页 RepoAgent 幻灯片和 1 页海报使用 PDF.js 阅读器，支持翻页、全文搜索和缩放；XAgent 官方项目报告以网页正文显示。文档清单、页数及来源记录在 `src/data/document-assets.json`，共 505 页。数学论文全文是明确标注的公开 v1 早稿；现有出版记录仍指向 v2。图片可在页面内放大，视频使用内嵌播放器。CV 不发布，页面不提供文件下载入口。

## 来源与版权

内容、头像、项目图片和笔记来源于 [LOGIC-10 的公开个人站仓库](https://github.com/LOGIC-10/LOGIC-10.github.io)，按站点所有者授权用于本次重设计。原仓库的 MIT 许可证对应旧主题；图片与文章的其他许可不作推断。

字体使用固定版本 `@fontsource-variable/newsreader@5.3.0` 与 `@fontsource-variable/dm-sans@5.3.0`，许可见依赖包内的 OFL 文件。

文档阅读使用 `pdfjs-dist@6.5.438`（Apache 2.0）；构建时将字体、字符映射和解码资源复制到站点，无需外部阅读服务。论文版权归各作者及出版方所有。XAgent 报告保留 OpenBMB / XAgent Team 署名及 Apache 2.0 来源链接。

## 发布

`master` 保存 Astro 源码，`gh-pages` 保存经过核验的 `dist/` 静态文件。GitHub Pages 使用 `gh-pages` 根目录，`.nojekyll` 保证完整保留 `_astro/` 资源。发布前必须完成构建及全部核验；论文全文、封面和 PDF.js 支持文件均随构建一起发布。
