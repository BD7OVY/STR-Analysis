# 销售经营分析平台

一个通用的**订单分析平台**：导入任意渠道的订单 Excel/JSON → 自动识别平台、统一表头、按城市/平台聚合 → 用图表与 3D 地图直观展示订单与应收。

纯前端单文件应用，**数据只在浏览器本地解析计算，不上传任何服务器**。可直接双击 `index.html` 打开，或部署到任意静态托管（GitHub Pages 等）。

## 目录结构

```
index.html          主程序（纯前端工作台：导入 / 处理 / 展示）
china-geo.js        本地化中国地图数据（省份边界 + 城市质心，离线可用）
xlsx.full.min.js    本地化 SheetJS（解析 Excel，离线可用）
schema_mapping.json 表头统一「单一映射配置」（前端导入与 Python 管线共用）
data.json           内置示例数据（页面默认载入，方便一目了然）
README.md           本说明
sample-data/        示例原始 Excel（哈啰/滴滴/悟空/携程，表头各不相同，自动识别）——仅作样例
tools/              Python 离线刷新管线（可选，非部署必需）
  generate_dashboard.py   读 Excel → 统一 schema → 算指标 → 生成 data.json 与看板
  generate_poster.py      生成微信分享海报
  server.py                本地预览服务（http://localhost:8080）
  config.json              数据源 / 输出目录 / 端口等配置
  sample_outputs/          管线产出（分析看板.html / metrics.json / unified_orders.json / 微信分享海报.png）
启动看板.bat        一键启动本地管线 + 服务（Windows）
```

> GitHub Pages 部署只需 `index.html` + `china-geo.js` + `xlsx.full.min.js` + `schema_mapping.json` + `data.json` 五个文件，其余为本地开发/刷新工具。

## 数据源不再受限（通用性）

平台定位为**数据处理平台**，数据源**不再局限于任何固定文件夹**：

- **前端导入**：点「选择文件 / 选择文件夹」即可导入任意目录下的订单 Excel/JSON；表头由 `schema_mapping.json` 的「分词规则 + 平台标识词」自动识别，与文件名、固定目录无关。
- **Python 管线**：`generate_dashboard.py` 默认读取 `sample-data/`，但可用 `python generate_dashboard.py <任意文件夹>` 指向任何目录；也可用 `config.json` 的 `data_source` 配置。`sample-data/` 只是随仓库附带的样例。

## 筛选月份：新增「全部月份」

月份下拉框新增 **全部月份** 选项（默认选中），用于一键查看**整体累计数据**：

- KPI 显示为「累计订单数 / 累计 GMV / 客单价」；
- 趋势图切换为**各月 GMV 趋势**；
- 「各周 GMV 与环比」板块自动变为**各月 GMV 与环比**（含月环比增速）；
- 城市 3D 地图展示全部城市的累计订单与应收；
- 明细表与洞察文案同步适配累计口径。

## 表头统一是怎么做的（核心）

各平台后台下载的订单 Excel **表头各不相同**。统一逻辑全部收敛在 `schema_mapping.json` 一份文件里：
- 每个平台的「列名 → 统一字段」分词规则、城市映射、状态映射、车型归一、节假日；
- 平台识别**不依赖文件名**，而是按「专属标识词 + 列特征」自动判断；
- Python 管线（`generate_dashboard.py`）和前端「导入数据」按钮**读同一份配置**，行为一致。

新增平台或调整列名，只改 `schema_mapping.json`，不用动代码。

## 一键本地运行（可选）

双击：`启动看板.bat`

或手动：
```bash
cd tools
python generate_dashboard.py    # 读 sample-data → 生成 data.json 与看板
python server.py                # 本地服务 http://localhost:8080
```

## 配置项（tools/config.json）

- `data_source`：原始 Excel 目录（相对路径基于项目根；留空则用默认 `sample-data`）
- `output_dir`：报表产出目录（默认 `tools/sample_outputs`）
- `server_port`：本地服务端口（默认 8080）
- `share_url`：海报二维码地址
- `platforms`：各平台登录地址/账号/密码（后续自动下载时填）

## 设计原则

- **不过度工程化**：前端单文件、管线脚本少而清晰。
- **harness 优先**：识别、去重、聚合、环比全由代码保证。
- **离线可用**：地图与 Excel 解析库均本地化，`file://` 双击与静态托管都能跑。
- **配色克制**：整体仅用 绿 `#0FBA81` / 橙 `#FB9C0D` / 青 `#0EA5A4` + 深浅灰。
