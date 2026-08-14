# -*- coding: utf-8 -*-
"""
数据分析个人工作台 · 微信分享海报
================================
读取 3_报表产出/metrics.json，生成一张竖版分享海报 PNG（含指标卡 + 二维码）。

用法：
    python generate_poster.py
输出：
    3_报表产出/微信分享海报.png

二维码指向 config.json 的 share_url（默认本地服务 http://localhost:8080）。
若要手机扫码可看，需先把看板部署到可公网访问的地址并填入 share_url。
"""
import os
import io
import json

import segno
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTPUT = os.path.join(ROOT, '3_报表产出')
METRICS = os.path.join(OUTPUT, 'metrics.json')
POSTER = os.path.join(OUTPUT, '微信分享海报.png')
CFG = os.path.join(HERE, 'config.json')

# 中文字体（Windows 自带，优先 simhei；缺失则退回 msyh）
FONT_CANDIDATES = [
    r'C:\Windows\Fonts\simhei.ttf',
    r'C:\Windows\Fonts\msyh.ttc',
    r'C:\Windows\Fonts\simsun.ttc',
]
FONT = None
for fp in FONT_CANDIDATES:
    if os.path.exists(fp):
        FONT = fp
        break


def font(size, bold=False):
    """返回指定字号字体；bold 在 msyh.ttc 上用 index=1（粗体）。"""
    if not FONT:
        return ImageFont.load_default()
    try:
        if FONT.endswith('.ttc') and 'msyh' in FONT.lower():
            idx = 1 if bold else 0
            return ImageFont.truetype(FONT, size, index=idx)
        return ImageFont.truetype(FONT, size)
    except Exception:
        return ImageFont.load_default()


def text_w(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0]


def fmt_money(v):
    return f"{v:,.0f}元"


def pct_str(v):
    if v is None:
        return '—'
    if v == float('inf'):
        return '新增'
    return f"{v:+.1f}%"


def round_rect(draw, box, radius, fill, outline=None):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline)


def main():
    if not os.path.exists(METRICS):
        print('[错误] 未找到 metrics.json，请先运行 generate_dashboard.py')
        return
    with open(METRICS, 'r', encoding='utf-8') as f:
        m = json.load(f)

    cfg = {}
    if os.path.exists(CFG):
        try:
            with open(CFG, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
        except Exception:
            pass
    share_url = cfg.get('share_url') or f"http://localhost:{cfg.get('server_port', 8080)}"

    W, H = 720, 1280
    img = Image.new('RGB', (W, H), '#f8fafc')
    d = ImageDraw.Draw(img)

    # ---- 顶部色带 ----
    d.rectangle([0, 0, W, 200], fill='#1e293b')
    d.text((40, 60), '销售经营分析平台', font=font(40, bold=True), fill='#ffffff')
    d.text((40, 120), f"数据截至 {m['today_str']} · 按实际取车统计", font=font(20), fill='#cbd5e1')

    # ---- 三个核心指标卡 ----
    p = m['periods']
    g = m['growth']
    cards = [
        ('本月 GMV', p['this_month']['gmv'], g['month_over_month_gmv']),
        ('本周 GMV', p['this_week']['gmv'], g['week_over_week_gmv']),
        ('今日 GMV', p['today']['gmv'], g['day_over_day_gmv']),
    ]
    card_w = 200
    gap = 20
    x0 = (W - (card_w * 3 + gap * 2)) // 2
    y0 = 240
    for i, (label, val, pct) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        round_rect(d, [x, y0, x + card_w, y0 + 150], 14, '#ffffff', outline='#e2e8f0')
        d.text((x + 16, y0 + 18), label, font=font(18), fill='#64748b')
        d.text((x + 16, y0 + 48), fmt_money(val), font=font(30, bold=True), fill='#1e293b')
        pc = '#16a34a' if (pct is not None and pct >= 0) else ('#dc2626' if pct is not None else '#64748b')
        d.text((x + 16, y0 + 100), f"环比 {pct_str(pct)}", font=font(18), fill=pc)

    # ---- 环比对比文字 ----
    by = y0 + 200
    d.text((40, by), '环比对比', font=font(26, bold=True), fill='#1e293b')
    lines = [
        f"本月 GMV {fmt_money(p['this_month']['gmv'])}，环比 {pct_str(g['month_over_month_gmv'])}",
        f"本周 GMV {fmt_money(p['this_week']['gmv'])}，环比 {pct_str(g['week_over_week_gmv'])}",
        f"今日 GMV {fmt_money(p['today']['gmv'])}，环比 {pct_str(g['day_over_day_gmv'])}",
    ]
    yy = by + 44
    for ln in lines:
        d.text((40, yy), ln, font=font(20), fill='#334155')
        yy += 34

    # ---- Top 城市 / 平台 ----
    yy += 12
    d.text((40, yy), '赚钱城市 TOP3', font=font(26, bold=True), fill='#1e293b')
    yy += 44
    for i, c in enumerate(m.get('top_cities', [])[:3]):
        d.text((40, yy), f"{i+1}. {c['city']}", font=font(20), fill='#334155')
        d.text((360, yy), fmt_money(c['gmv']), font=font(20, bold=True), fill='#2563eb')
        yy += 34

    yy += 14
    d.text((40, yy), '赚钱平台 TOP3', font=font(26, bold=True), fill='#1e293b')
    yy += 44
    for i, pl in enumerate(m.get('top_platforms', [])[:3]):
        d.text((40, yy), f"{i+1}. {pl['platform']}", font=font(20), fill='#334155')
        d.text((360, yy), fmt_money(pl['gmv']), font=font(20, bold=True), fill='#16a34a')
        yy += 34

    # ---- 二维码（直接写入内存，避免临时文件）----
    qr = segno.make(share_url, error='m')
    buf = io.BytesIO()
    qr.save(buf, scale=10, border=2, kind='png')
    buf.seek(0)
    qr_img = Image.open(buf).convert('RGB')
    qsize = 200
    qr_img = qr_img.resize((qsize, qsize))
    qx, qy = (W - qsize) // 2, H - 270
    # 白底卡片
    round_rect(d, [qx - 16, qy - 16, qx + qsize + 16, qy + qsize + 16], 16, '#ffffff', outline='#e2e8f0')
    img.paste(qr_img, (qx, qy))
    d.text((W // 2, qy + qsize + 28), '扫码在看板查看完整报表', font=font(20), fill='#64748b', anchor='mm')
    d.text((W // 2, qy + qsize + 58), share_url, font=font(15), fill='#94a3b8', anchor='mm')

    img.save(POSTER, 'PNG')
    print(f'海报已生成：{POSTER}')


if __name__ == '__main__':
    main()
