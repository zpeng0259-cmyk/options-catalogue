# Options Catalogue

期权策略教学/复习手册（中文为主，英文术语保留）。

🌐 **Live**: https://zpeng0259-cmyk.github.io/options-catalogue/

## 第一期内容

- **CSP** — Cash-Secured Put 现金担保看跌
- **BPS** — Bull Put Spread 牛市看跌价差
- **CC**  — Covered Call 备兑看涨

每个策略统一 6 节：机制 / 适用 vs 不适用 / 损益图 / 极端场景表 / 真实案例 / 常见误区。

## 本地开发

```bash
npm install
npm run dev     # http://localhost:4321/options-catalogue/
npm run build   # 输出到 dist/
npm run preview # 本地预览 build 产物
```

## 重新生成损益图 SVG

修改 `scripts/gen_payoffs.py` 顶部参数后：

```bash
pip3 install matplotlib   # 首次需要
python3 scripts/gen_payoffs.py
```

输出到 `public/payoffs/*.svg`，commit 提交。

## 部署

Push 到 `main` 分支自动触发 GitHub Actions 部署到 GitHub Pages。
首次需在仓库 Settings → Pages → Source 选择 "GitHub Actions"。

## 项目结构

```
src/
├── pages/        # 每个策略一页 (.astro)
├── components/   # StrategyCard / PayoffSVG / ScenarioTable / ExampleCard / ProsConsList / Nav
├── layouts/      # BaseLayout / StrategyLayout
└── styles/       # global.css (Tailwind v4 + typography + dark theme tokens)

public/payoffs/   # 预生成的 SVG 损益图
scripts/          # gen_payoffs.py 一次性 SVG 生成器
```

## 免责

仅供教学/复习用。期权可损失全部本金。不构成投资建议。
