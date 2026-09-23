# -*- coding: utf-8 -*-
"""五國 Google News 焦點新聞 RSS 快照抓取。
用法: python fetch_snapshot.py
輸出: data/snapshots.csv 追加（date, ts, country, rank, title, source）
"""
import csv, os, sys, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime

WS = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(WS, "data")
os.makedirs(DATA, exist_ok=True)
CSV_PATH = os.path.join(DATA, "snapshots.csv")

COUNTRIES = {
    "TW": ("zh-TW", "TW", "TW:zh-Hant"),
    "US": ("en-US", "US", "US:en"),
    "JP": ("ja-JP", "JP", "JP:ja"),
    "KR": ("ko-KR", "KR", "KR:ko"),
    "UK": ("en-GB", "GB", "GB:en"),
}
TOP_N = 10


def fetch(country, hl, gl, ceid):
    url = f"https://news.google.com/rss?hl={hl}&gl={gl}&ceid={ceid}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read()
    root = ET.fromstring(raw)
    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        # Google News 標題格式「標題 - 來源」
        src = ""
        s = it.find("source")
        if s is not None and s.text:
            src = s.text.strip()
        elif " - " in title:
            title, src = title.rsplit(" - ", 1)
        items.append((title.strip(), src))
        if len(items) >= TOP_N:
            break
    return items


def main():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    new_rows = []
    for c, (hl, gl, ceid) in COUNTRIES.items():
        try:
            items = fetch(c, hl, gl, ceid)
            for i, (title, src) in enumerate(items, 1):
                new_rows.append([date, ts, c, i, title, src])
            print(f"{c}: {len(items)} 則")
        except Exception as e:
            print(f"{c}: 失敗 {e}", file=sys.stderr)
    exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        if not exists:
            w.writerow(["date", "ts", "country", "rank", "title", "source"])
        w.writerows(new_rows)
    print(f"寫入 {CSV_PATH}，新增 {len(new_rows)} 筆")


if __name__ == "__main__":
    main()
