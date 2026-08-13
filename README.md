# STR Analysis · 短租经营分析工作台

汽车短租租赁业务的经营分析单页应用，纯前端、零构建、可离线打开。

在线地址：https://bd7ovy.github.io/STR-Analysis/

## 功能
- 顶部导航：`导入数据` / `订单分析` / `周数据环比` / `月数据环比` / `城市平台订单明细`，点击平滑滚动到对应板块。
- 月份筛选：切换任意月份，实时计算该月的订单数、GMV、客单价、环比、Top 城市/平台、状态分布、日趋势。
- 导入数据：上传归一化后的订单 Excel（统一表头）或 JSON 即可替换示例数据；数据在浏览器本地解析与计算，不上传任何服务器。

## 文件
- `index.html` — 应用本体（内联 CSS/JS，图表用内联 SVG，零外部依赖）。
- `data.json` — 示例数据（四平台归一化订单），由本地 Python 管线生成。

## 本地更新数据
示例数据来自本地管线 `数据分析工作台/2_运行脚本/generate_dashboard.py`：
```
python generate_dashboard.py   # 生成 3_报表产出/unified_orders.json
cp 3_报表产出/unified_orders.json data.json
git add data.json && git commit -m "update data" && git push
```
