# -*- coding: utf-8 -*-
"""多語議題分類器：中(zh-TW) / 英(en) / 日(ja) / 韓(ko)
統一八大類：政治 / 科技AI / 經濟財經 / 國際地緣 / 社會 / 生活健康 / 娛樂 / 體育 / 其他
規則：命中關鍵字數最多的類別勝出；政治詞命中則優先歸政治（與台灣版方法一致）。
"""

CATS = {
    "科技AI": [
        # zh
        "AI", "人工智慧", "iPhone", "蘋果", "Apple", "機器人", "晶片", "半導體", "資安", "輝達", "台積電3奈米",
        # en
        "ai ", "artificial intelligence", "iphone", "apple", "google", "microsoft", "nvidia", "chip", "semiconductor",
        "robot", "spacex", "quantum", "tech", "chatgpt", "openai", "data center", "smartphone", "app",
        # ja
        "ai", "生成ai", "半導体", "スマホ", "iphone", "ロボット", "量子", "チップ", "it",
        # ko
        "ai", "반도체", "삼성", "스마트폰", "로봇", "챗gpt", "it ",
    ],
    "經濟財經": [
        # zh
        "台積電", "費半", "fed", "升息", "降息", "美股", "道瓊", "標普", "台指期", "adr", "原油", "油價",
        "匯率", "股價", "物價", "通膨", "關稅", "央行", "房市", "房價",
        # en
        "fed", "stocks", "stock market", "inflation", "gdp", "interest rate", "rate cut", "rate hike", "economy",
        "economic", "tariff", "oil price", "nasdaq", "dow jones", "wall street", "recession", "bank", "market",
        "yen", "dollar", "trade deal", "housing",
        # ja
        "日経", "株価", "円安", "円高", "金利", "物価", "経済", "日銀", "関税", "景気", "為替", "株",
        # ko
        "주가", "주식", "경제", "금리", "물가", "환율", "코스피", "원화", "관세", "증시",
    ],
    "娛樂": [
        # zh
        "演唱會", "金鐘", "金馬", "電影", "票房", "藝人", "女星", "男星", "偶像",
        # en
        "movie", "film", "netflix", "singer", "concert", "actor", "actress", "music", "album", "box office",
        "celebrity", "tv show", "drama series", "hollywood",
        # ja
        "映画", "芸能", "歌手", "アイドル", "ドラマ", "コンサート", "俳優", "女優",
        # ko
        "영화", "가수", "콘서트", "드라마", "아이돌", "연예", "배우",
    ],
    "體育": [
        # zh
        "棒球", "大聯盟", "nba", "plg", "羽球", "網球", "足球", "奧運", "世足", "中職", "職棒",
        # en
        "football", "nfl", "nba", "soccer", "world cup", "olympics", "baseball", "tennis", "golf", "mlb",
        "premier league", "f1", "formula 1", "boxing",
        # ja
        "野球", "サッカー", "大谷", "甲子園", "オリンピック", "テニス", "相撲", "プロ野球",
        # ko
        "야구", "축구", "올림픽", "월드컵", "테니스", "골프",
    ],
    "生活健康": [
        # zh
        "東北季風", "東北風", "颱風", "天氣", "氣象", "降雨", "高溫", "地震", "熱帶擾動", "聖嬰",
        "流感", "疫苗", "健康", "食安", "旅遊", "美食", "洪災", "水災", "重建",
        # en
        "weather", "storm", "hurricane", "typhoon", "heatwave", "heat wave", "flu", "covid", "vaccine",
        "health", "earthquake", "travel", "food", "diet", "cancer", "hospital",
        # ja
        "台風", "地震", "気象", "大雨", "猛暑", "健康", "インフルエンザ", "ワクチン", "病院", "食",
        # ko
        "태풍", "지진", "날씨", "폭염", "건강", "독감", "백신", "병원",
    ],
    "社會": [
        # zh
        "護理師", "肇逃", "輾斃", "羈押", "聲押", "槍", "毒", "殺", "棄屍", "凶嫌", "起訴", "法辦",
        "詐", "車禍", "火警", "大火", "墜", "命案", "不治", "送醫", "搶救",
        # en
        "shooting", "shot", "killed", "arrested", "police", "crash", "fire", "dies", "dead", "death",
        "trial", "court", "murder", "stabbing", "prison", "fraud", "scam", "missing",
        # ja
        "逮捕", "死亡", "事故", "火災", "殺人", "警察", "判決", "事件", "容疑", "詐欺",
        # ko
        "사망", "체포", "사고", "화재", "경찰", "살인", "사건", "판결", "구속",
    ],
    "國際地緣": [
        # zh
        "川普", "美軍", "伊朗", "胡塞", "葉門", "普亭", "普京", "烏克蘭", "俄羅斯", "英相", "金磚",
        "莫迪", "習近平", "川習會", "紅海", "沙烏地", "以色列", "加薩", "北約", "北韓", "沖繩",
        # en
        "ukraine", "russia", "gaza", "israel", "iran", "china", "nato", "war", "missile", "north korea",
        "putin", "zelensky", "middle east", "ceasefire", "taiwan strait", "xi jinping",
        # ja
        "ウクライナ", "ロシア", "ガザ", "イスラエル", "イラン", "中国", "北朝鮮", "ミサイル", "台湾",
        "プーチン", "中東", "停戦", "習近平",
        # ko
        "우크라이나", "러시아", "가자", "이스라엘", "이란", "중국", "북한", "미사일", "푸틴", "중동", "휴전",
    ],
}

# 政治詞（命中即歸政治，與台灣版方法一致）
POL_WORDS = [
    # zh-TW
    "賴清德", "蕭美琴", "卓榮泰", "林佳龍", "沈伯洋", "蔡英文", "柯建銘", "民進黨", "綠營", "綠委",
    "蔣萬安", "黃國昌", "柯文哲", "侯友宜", "韓國瑜", "盧秀燕", "徐巧芯", "國民黨", "藍營", "藍委",
    "民眾黨", "白營", "行政院", "立法院", "立委", "選舉", "市長", "議員", "民調", "內閣", "國防",
    "國安", "總統", "副總統", "政黨", "造勢", "不副署", "違憲", "監察院", "罷免", "兩岸", "部長",
    # en (US/UK)
    "trump", "white house", "president", "election", "senate", "congress", "democrat", "republican",
    "governor", "starmer", "parliament", "prime minister", "labour", "conservative", "cabinet",
    "minister", "mayor", "poll", "campaign", "vote", "voters", "impeach", "government shutdown",
    # ja
    "首相", "総理", "自民党", "立憲", "選挙", "国会", "内閣", "参議院", "衆議院", "石破", "高市",
    "政党", "都知事", "野党", "与党", "大臣", "官邸",
    # ko
    "대통령", "국회", "선거", "여당", "야당", "정부", "정치", "국민의힘", "민주당", "총리", "장관",
    "이재명", "탄핵", "청와대", "용산",
]

ORDER = ["政治", "科技AI", "經濟財經", "國際地緣", "社會", "生活健康", "娛樂", "體育", "其他"]


def classify(title: str) -> str:
    t = title.lower()
    best, best_score = "其他", 0
    for cat, kws in CATS.items():
        s = sum(1 for k in kws if k.lower() in t)
        if s > best_score:
            best, best_score = cat, s
    if any(k.lower() in t for k in POL_WORDS):
        return "政治"
    return best if best_score > 0 else "其他"
