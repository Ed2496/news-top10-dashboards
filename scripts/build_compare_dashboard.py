# -*- coding: utf-8 -*-
"""國際比對儀表板：美/日/韓/英 vs 台灣，每日議題分布趨勢與偏差比較。
讀取 data/snapshots.csv → compare_stats.json + 國際比對儀表板.html
"""
import csv, json, os
from collections import Counter, defaultdict
from classifier import classify, ORDER

WS = os.path.dirname(os.path.abspath(__file__))
COUNTRIES = ["TW", "US", "JP", "KR", "UK"]
CNAME = {"TW": "台灣", "US": "美國", "JP": "日本", "KR": "韓國", "UK": "英國"}

rows = list(csv.DictReader(open(os.path.join(WS, "data", "snapshots.csv"), encoding="utf-8-sig")))
for r in rows:
    r["cat"] = classify(r["title"])

days = sorted({r["date"] for r in rows})

# 每日 × 國家 × 類別 筆數
cnt = defaultdict(Counter)          # cnt[(day,country)][cat]
per_country = defaultdict(Counter)  # 全期
for r in rows:
    cnt[(r["date"], r["country"])][r["cat"]] += 1
    per_country[r["country"]][r["cat"]] += 1

def shares(counter):
    tot = sum(counter.values()) or 1
    return {c: round(100 * counter.get(c, 0) / tot, 1) for c in ORDER}

# 各國全期佔比 + 對台偏差（百分點）+ 總變異距離
share_all = {c: shares(per_country[c]) for c in COUNTRIES}
tw = share_all["TW"]
deviation = {c: {cat: round(share_all[c][cat] - tw[cat], 1) for cat in ORDER} for c in COUNTRIES if c != "TW"}
tvd = {c: round(sum(abs(deviation[c][cat]) for cat in ORDER) / 2, 1) for c in deviation}

# 每日政治/科技佔比趨勢（五國）
def daily_share(cat):
    out = {}
    for c in COUNTRIES:
        arr = []
        for d in days:
            cc = cnt[(d, c)]
            tot = sum(cc.values()) or 1
            arr.append(round(100 * cc.get(cat, 0) / tot, 1))
        out[c] = arr
    return out

trend_pol = daily_share("政治")
trend_tech = daily_share("科技AI")
trend_eco = daily_share("經濟財經")

latest = days[-1]
latest_rows = [r for r in rows if r["date"] == latest]

stats = {
    "days": days, "latest": latest, "countries": COUNTRIES, "cname": CNAME,
    "order": ORDER, "share_all": share_all, "deviation": deviation, "tvd": tvd,
    "trend_pol": trend_pol, "trend_tech": trend_tech, "trend_eco": trend_eco,
    "n_rows": len(rows),
    "latest_rows": [{"country": r["country"], "rank": int(r["rank"]), "title": r["title"],
                     "source": r["source"], "cat": r["cat"]} for r in latest_rows],
    "daily_counts": {f"{d}|{c}": dict(cnt[(d, c)]) for d in days for c in COUNTRIES},
}
json.dump(stats, open(os.path.join(WS, "compare_stats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

DATA = json.dumps(stats, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>國際媒體比對 Dashboard · 美/日/韓/英 vs 台灣</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#eef3f8;--card:#fff;--line:#d3dfeb;--fg:#12305b;--mut:#5b7290;}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font-family:"Microsoft JhengHei","Noto Sans TC",sans-serif;padding:24px;max-width:1280px;margin:0 auto}
h1{font-size:22px;margin-bottom:4px}
.sub{color:var(--mut);font-size:13px;margin-bottom:20px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:20px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;box-shadow:0 1px 3px rgba(18,48,91,.06)}
.kpi .v{font-size:24px;font-weight:700}
.kpi .l{color:var(--mut);font-size:12px;margin-top:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:16px;box-shadow:0 1px 3px rgba(18,48,91,.06)}
.card h2{font-size:15px;margin-bottom:10px}
.card .note{color:var(--mut);font-size:12px;margin-top:8px;line-height:1.7}
canvas{max-height:320px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-weight:600;font-size:12px;white-space:nowrap}
td.num,th.num{text-align:right}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;white-space:nowrap;background:#eaf1f9;color:#12305b}
.footer{color:var(--mut);font-size:12px;margin-top:8px;line-height:1.8}
</style>
</head>
<body>
<h1>國際媒體比對 Dashboard</h1>
<div class="sub" id="sub"></div>

<div class="kpis" id="kpis"></div>

<div class="grid">
  <div class="card"><h2>各國議題分布（佔比 %,100% 堆疊）</h2><canvas id="cShare"></canvas>
    <div class="note">台灣與美/日/韓/英同日的 Google News 焦點 Top 10 議題結構。佔比 = 該類則數 ÷ 當日上榜則數。</div></div>
  <div class="card"><h2>對台偏差指數（總變異距離 TVD）</h2><canvas id="cTvd"></canvas>
    <div class="note">TVD = Σ|該國佔比 − 台灣佔比| ÷ 2。數值越大,代表該國媒體議題結構與台灣差異越大(0=完全一致,100=完全無交集)。</div></div>
  <div class="card"><h2>政治佔比 · 每日趨勢</h2><canvas id="cPol"></canvas>
    <div class="note" id="nTrend">每日快照累積後,此圖呈現五國政治新聞佔比的逐日走勢。</div></div>
  <div class="card"><h2>科技AI / 經濟財經佔比 · 每日趨勢</h2><canvas id="cTech"></canvas><canvas id="cEco" style="margin-top:10px"></canvas></div>
</div>

<div class="card"><h2>偏差熱力表：各國類別佔比 − 台灣（百分點）</h2>
  <div style="overflow-x:auto"><table id="tDev"></table></div>
  <div class="note">紅色 = 該國比台灣更偏重此類;藍色 = 台灣比該國更偏重此類。例如「政治 +20」表示該國政治佔比比台灣高 20 個百分點。</div></div>

<div class="card"><h2>最新快照明細（<span id="latestDay"></span>）</h2>
  <div style="overflow-x:auto"><table id="tRows"></table></div></div>

<div class="footer" id="foot"></div>

<script>
const S = __DATA__;
const CN = S.cname, ORDER = S.order, CS = S.countries;
const CCOL = {"政治":"#bc8cff","科技AI":"#ff9e64","經濟財經":"#d29922","國際地緣":"#58a6ff","社會":"#f85149","生活健康":"#3fb950","娛樂":"#f778ba","體育":"#39c5cf","其他":"#8b949e"};
const CCOL5 = {TW:"#0d9488",US:"#0284c7",JP:"#e11d48",KR:"#7c3aed",UK:"#d97706"};
Chart.defaults.color="#3f5878";Chart.defaults.borderColor="#d3dfeb";Chart.defaults.font.family='"Microsoft JhengHei",sans-serif';

document.getElementById("sub").textContent =
  `資料來源:Google News 焦點新聞 RSS 快照(每國 Top 10)· 國家:台灣/美國/日本/韓國/英國 · 期間 ${S.days[0]}–${S.latest}(${S.days.length} 天)· 共 ${S.n_rows} 筆`;

// KPI
const tvdSorted = Object.entries(S.tvd).sort((a,b)=>b[1]-a[1]);
const most = tvdSorted[0], least = tvdSorted[tvdSorted.length-1];
document.getElementById("kpis").innerHTML = [
  [S.days.length, "累積天數"], [S.n_rows, "累積上榜筆數"],
  [CN[most[0]]+" "+most[1], "與台灣差異最大(TVD)"],
  [CN[least[0]]+" "+least[1], "與台灣最接近(TVD)"],
].map(k=>`<div class="kpi"><div class="v">${k[0]}</div><div class="l">${k[1]}</div></div>`).join("");

// 100% stacked share
new Chart(cShare,{type:"bar",data:{labels:CS.map(c=>CN[c]),
  datasets:ORDER.map(cat=>({label:cat,data:CS.map(c=>S.share_all[c][cat]),backgroundColor:CCOL[cat]}))},
  options:{scales:{x:{stacked:true},y:{stacked:true,max:100,ticks:{callback:v=>v+"%"}}},plugins:{legend:{position:"right"}}}});

// TVD bar
const tvdKeys=Object.keys(S.tvd);
new Chart(cTvd,{type:"bar",data:{labels:tvdKeys.map(c=>CN[c]),datasets:[{data:tvdKeys.map(c=>S.tvd[c]),backgroundColor:tvdKeys.map(c=>CCOL5[c])}]},
  options:{plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,max:100}}}});

// trends
function trendChart(el, data, label){
  new Chart(el,{type:"line",data:{labels:S.days.map(d=>d.slice(5).replace("-","/")),
    datasets:CS.map(c=>({label:CN[c],data:data[c],borderColor:CCOL5[c],backgroundColor:CCOL5[c],tension:.3,spanGaps:true}))},
    options:{scales:{y:{beginAtZero:true,ticks:{callback:v=>v+"%"}}},plugins:{legend:{position:"right"}}}});
}
trendChart(cPol, S.trend_pol, "政治");
trendChart(cTech, S.trend_tech, "科技AI");
trendChart(cEco, S.trend_eco, "經濟財經");
if(S.days.length<3) document.getElementById("nTrend").textContent =
  `目前僅累積 ${S.days.length} 天快照,趨勢線會隨每日抓取逐漸成形(建議掛每日定時任務)。`;

// deviation heat table
const cats = ORDER.filter(c=>c!=="其他");
let h = "<tr><th>類別</th>"+tvdKeys.map(c=>`<th class="num">${CN[c]}</th>`).join("")+"</tr>";
for(const cat of cats){
  h += `<tr><td>${cat}</td>`;
  for(const c of tvdKeys){
    const v = S.deviation[c][cat];
    const a = Math.min(Math.abs(v)/40,1);
    const bg = v>0 ? `rgba(225,29,72,${0.08+0.5*a})` : v<0 ? `rgba(2,132,199,${0.08+0.5*a})` : "transparent";
    h += `<td class="num" style="background:${bg}">${v>0?"+":""}${v}</td>`;
  }
  h += "</tr>";
}
document.getElementById("tDev").innerHTML = h;

// latest rows
document.getElementById("latestDay").textContent = S.latest;
document.getElementById("tRows").innerHTML =
  "<tr><th>國家</th><th>#</th><th>標題</th><th>來源</th><th>類別</th></tr>" +
  S.latest_rows.map(r=>`<tr><td>${CN[r.country]}</td><td>${r.rank}</td><td>${r.title}</td><td>${r.source}</td><td><span class="badge" style="background:${CCOL[r.cat]}22;color:${CCOL[r.cat]}">${r.cat}</span></td></tr>`).join("");

document.getElementById("foot").innerHTML =
 `方法說明:每國取 Google News 焦點新聞 RSS 前 10 則;分類為多語(中/英/日/韓)關鍵字規則,命中政治詞庫優先歸「政治」。<br>`+
 `佔比以當日上榜則數為分母;偏差為百分點差。關鍵字分類存在誤判率,跨語比對解讀時請留意語言特性差異。<br>`+
 `台灣歷史深度分析請見「台灣新聞儀表板.html」。`;
</script>
</body>
</html>"""

html = HTML.replace("__DATA__", DATA)
out = os.path.join(WS, "國際比對儀表板.html")
open(out, "w", encoding="utf-8").write(html)
print("國際比對儀表板.html written,", len(html), "bytes")
