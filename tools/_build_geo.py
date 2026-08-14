import json, urllib.request, time

PROV = {
 "110000":"北京市","120000":"天津市","130000":"河北省","140000":"山西省","150000":"内蒙古自治区",
 "210000":"辽宁省","220000":"吉林省","230000":"黑龙江省","310000":"上海市","320000":"江苏省",
 "330000":"浙江省","340000":"安徽省","350000":"福建省","360000":"江西省","370000":"山东省",
 "410000":"河南省","420000":"湖北省","430000":"湖南省","440000":"广东省","450000":"广西壮族自治区",
 "460000":"海南省","500000":"重庆市","510000":"四川省","520000":"贵州省","530000":"云南省",
 "540000":"西藏自治区","610000":"陕西省","620000":"甘肃省","630000":"青海省","640000":"宁夏回族自治区",
 "650000":"新疆维吾尔自治区","710000":"台湾省","810000":"香港特别行政区","820000":"澳门特别行政区"
}
SUFFIXES=["市","地区","自治州","盟","区","县","特别行政区","自治区","省","回族自治州","土家族苗族自治州","壮族自治区","维吾尔自治区","回族自治区"]

def short(name):
    n=name
    # special full-name regions
    for full,sh in [("内蒙古自治区","内蒙古"),("广西壮族自治区","广西"),("新疆维吾尔自治区","新疆"),
                    ("宁夏回族自治区","宁夏"),("西藏自治区","西藏"),("香港特别行政区","香港"),
                    ("澳门特别行政区","澳门"),("台湾省","台湾")]:
        if n==full: return sh
    # municipalities
    for m in ["北京市","上海市","天津市","重庆市"]:
        if n==m: return m[:-1]
    for s in SUFFIXES:
        if n.endswith(s):
            n=n[:-len(s)]
            break
    return n

def fetch(code):
    url=f"https://geo.datav.aliyun.com/areas_v3/bound/{code}_full.json"
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt==2:
                print("FAIL",code,e)
            time.sleep(0.4)
    return None

prov_centroid={}
city_coord={}
city_prov={}

# province centroids from the already-downloaded 100000_full
prov_full=json.load(open("china_geo_tmp.json",encoding="utf-8"))
for f in prov_full["features"]:
    p=f["properties"]; name=p["name"]; cen=p.get("centroid") or p.get("center")
    if cen:
        prov_centroid[short(name)]=[round(cen[0],4),round(cen[1],4)]

for code,pname in PROV.items():
    d=fetch(code)
    if not d: 
        # fallback: use province centroid for the province itself
        continue
    for f in d["features"]:
        p=f["properties"]; name=p["name"]; cen=p.get("centroid") or p.get("center")
        if not cen: continue
        sh=short(name)
        city_coord[sh]=[round(cen[0],4),round(cen[1],4)]
        city_prov[sh]=short(pname)

# manual safety for municipalities / SARs / Taiwan in case fetch missed them
manual={
 "北京":[116.4053,39.9049],"上海":[121.4726,31.2317],"天津":[117.1902,39.1256],"重庆":[106.5516,29.5630],
 "香港":[114.1734,22.3200],"澳门":[113.5491,22.1987],"台湾":[120.9712,23.6995],"台北":[121.5654,25.0320]
}
for k,v in manual.items():
    city_coord.setdefault(k,v); city_prov.setdefault(k, "台湾" if k in ("台湾","台北") else k)

out={"coord":city_coord,"prov":prov_centroid,"cityProv":city_prov}
json.dump(out,open("china_cities_tmp.json","w",encoding="utf-8"),ensure_ascii=False)
print("城市坐标数:",len(city_coord))
print("省份质心数:",len(prov_centroid))
# quick check on data cities
data_cities=["重庆","西安","广州","北京","武汉","汕尾","汕头","昆明","厦门","佛山","东莞","珠海","中山","杭州","深圳"]
miss=[c for c in data_cities if c not in city_coord]
print("数据城市缺失:",miss if miss else "无")
