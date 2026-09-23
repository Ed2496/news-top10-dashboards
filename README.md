# 新聞輿情儀表板 · 台灣專注版 + 五國比對版

每日抓取 **台灣 / 美國 / 日本 / 韓國 / 英國** Google News 焦點新聞 Top 10（RSS），以多語（中/英/日/韓）關鍵字規則分類為八大類（政治 / 科技AI / 經濟財經 / 國際地緣 / 社會 / 生活健康 / 娛樂 / 體育 / 其他），產生兩個單檔互動儀表板：

| 頁面 | 內容 |
|---|---|
| [`taiwan.html`](./taiwan.html) | 台灣專注版：議題比重/聲量、逐日趨勢、執政 vs 在野批判聲量、立場結構、媒體來源（歷史區間 2026/09/09–09/21 經人工逐則覆核） |
| [`international.html`](./international.html) | 五國比對版：議題佔比 100% 堆疊、對台偏差熱力表（百分點差）、TVD 差異指數、政治/科技/經濟佔比每日趨勢 |

## 檔案結構

```
index.html            入口頁（兩個儀表板的連結）
taiwan.html           台灣新聞儀表板（產物）
international.html    國際比對儀表板（產物）
scripts/
  fetch_snapshot.py         五國 RSS 快照抓取（手動版）
  classifier.py             多語關鍵字分類器（中英日韓）
  tw_analyze.py             台灣版統計（含人工覆寫表）
  tw_build_dashboard.py     台灣版 HTML 產生器
  build_compare_dashboard.py 國際比對 HTML 產生器
data/
  snapshots.csv             五國逐日快照累積（date, ts, country, rank, title, source）
  tw_stats.json             台灣版統計
  tw_classified_all.csv     台灣版明細（含類別/立場）
  compare_stats.json        國際比對統計
```

## 方法論與限制

- 每國取 Google News 焦點新聞 RSS 前 10 則；榜單反映 Google 熱度演算法，非全媒體版面。
- 分類為關鍵字規則（命中政治詞庫優先歸「政治」），跨語比對存在誤判率。
- 「對台偏差」= 該國類別佔比 − 台灣類別佔比（百分點）；TVD = Σ|差| ÷ 2。
- 台灣版立場判定（批執政/批在野/互批/正面）僅適用台灣政黨語境，不套用於他國。

## 自動更新

由本機 Kimi Work 定時任務「五國新聞儀表板 · 每日更新」每日 10:15（Asia/Taipei）抓取並重建兩個儀表板。
