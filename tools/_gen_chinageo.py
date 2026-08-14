import json
geo=json.load(open("china_geo_tmp.json",encoding="utf-8"))
def rnd(o):
    if isinstance(o,list):
        if o and isinstance(o[0],(int,float)):
            return [round(o[0],2),round(o[1],2)]
        return [rnd(x) for x in o]
    return o
geo["features"]=[{**f,"geometry":rnd(f["geometry"])} for f in geo["features"]]
cities=json.load(open("china_cities_tmp.json",encoding="utf-8"))
with open("china-geo.js","w",encoding="utf-8") as f:
    f.write("/* 中国地图数据（本地化，非 CDN）。省份边界来自 DataV.GeoAtlas 100000_full，\n")
    f.write("   城市质心由各省 prefecture 级 GeoJSON 自动提取。纯前端离线可用。 */\n")
    f.write("window.CHINA_GEO=")
    json.dump(geo,f,ensure_ascii=False,separators=(",",":"))
    f.write(";\nwindow.CHINA_CITIES=")
    json.dump(cities,f,ensure_ascii=False,separators=(",",":"))
    f.write(";\n")
import os
print("china-geo.js size(KB):",round(os.path.getsize('china-geo.js')/1024,1))
print("features:",len(geo["features"]))
