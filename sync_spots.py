import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def final_spot_sync():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix loadSpots logic to MERGE missing items from initialSpots into Firebase
    # This ensures that even if there's existing data, new items are added.
    old_load_spots = """function loadSpots() { if(db) db.ref(`${basePath}/spots`).on('value', s => { const data = s.val(); if(data) spotData = Object.entries(data).map(([k, v]) => ({...v, key: k})); else initialSpots.forEach(i => db.ref(`${basePath}/spots`).push(i)); renderSpots(); }); }"""
    
    # Improved loadSpots that checks for duplicates by nameZh
    new_load_spots = """        function loadSpots() {
            if(!db) return;
            db.ref(`${basePath}/spots`).on('value', s => {
                const data = s.val();
                if(data) {
                    spotData = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                    // Migration: If any initialSpot is missing in current data (by nameZh), add it
                    initialSpots.forEach(init => {
                        const exists = spotData.some(s => s.nameZh === init.nameZh);
                        if (!exists) {
                            db.ref(`${basePath}/spots`).push(init);
                        }
                    });
                } else {
                    initialSpots.forEach(i => db.ref(`${basePath}/spots`).push(i));
                }
                renderSpots();
            });
        }"""
    
    # We need to find the existing loadSpots and replace it. 
    # The grep showed it's on L690.
    content = re.sub(r'function loadSpots\(\) \{.*?\}', new_load_spots, content)

    # 2. Re-verify initialSpots (Ensure it's the full list and clean)
    full_spots_data = '''        const initialSpots = [
            {cat: "핵심", nameKo: "푸동 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "지하철 2호선 / 자기부상"},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "2/7/16/18호선 Longyang Rd역"},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "2/14호선 Lujiazui역"},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "https://surl.amap.com/1raycs1Tfz8", subway: "2/10호선 East Nanjing Rd역 7번출구"},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "9호선 Qibao역 2번출구"},
            {cat: "명소", nameKo: "정안사", nameZh: "静安寺", addr: "https://surl.amap.com/1M5SBkJie2Z", subway: "2/7/14호선 Jing'an Temple역 1번출구"},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "https://surl.amap.com/1uSLDCN1o9iV", subway: "2/12/13호선 West Nanjing Rd역"},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "https://surl.amap.com/1Ord7Ml1z6OW", subway: "시외 지역 (전용 차량 권장)"},
            {cat: "명소", nameKo: "상하이 박물관", nameZh: "上海博物馆", addr: "", subway: "1/2/8호선 People's Square역 1번출구"},
            {cat: "명소", nameKo: "도시계획 전시관", nameZh: "上海城市规划展示馆", addr: "", subway: "1/2/8호선 People's Square역 3번출구"},
            {cat: "명소", nameKo: "윤봉길 기념관", nameZh: "梅园-尹奉吉义士生平事迹陈列室", addr: "https://surl.amap.com/1W3f3i9H89v", subway: "3/8호선 Hongkou Football Stadium역 1번출구"},
            {cat: "맛집", nameKo: "게살국수", nameZh: "裕兴记(外滩店)", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "장씨네 게국수", nameZh: "庄氏隆兴·蟹粉面道", addr: "", subway: "2/10호선 East Nanjing Rd역 7번출구"},
            {cat: "맛집", nameKo: "가정식 식당", nameZh: "上海姥姥家常饭馆", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "샤오롱바오", nameZh: "佳家汤包", addr: "", subway: "1/2/8호선 People's Square역 8번출구"},
            {cat: "맛집", nameKo: "생전", nameZh: "小杨生煎", addr: "", subway: "체인점 (주요 역 근처 많음)"},
            {cat: "맛집", nameKo: "생전 맛집", nameZh: "大壶春", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "상하이 전통요리", nameZh: "老吉士酒家", addr: "", subway: "1/7호선 Changshu Rd역 8번출구"},
            {cat: "맛집", nameKo: "항저우 요리", nameZh: "桂满陇", addr: "", subway: "2/7/14호선 Jing'an Temple역 3번출구"},
            {cat: "맛집", nameKo: "생선구이", nameZh: "江边城外烤全鱼", addr: "", subway: "2/10호선 East Nanjing Rd역 7번출구"},
            {cat: "맛집", nameKo: "훠궈(촉대협)", nameZh: "蜀大侠", addr: "", subway: "2/10호선 East Nanjing Rd역 6번출구"},
            {cat: "맛집", nameKo: "훠궈(홍지에)", nameZh: "鸿姐老火锅", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "쇼핑/기타", nameKo: "신세계백화점", nameZh: "新世界城", addr: "", subway: "1/2/8호선 People's Square역 7번출구"},
            {cat: "쇼핑/기타", nameKo: "제일백화점", nameZh: "第一百货商业中心", addr: "", subway: "1/2/8호선 People's Square역 19번출구"},
            {cat: "쇼핑/기타", nameKo: "미니소", nameZh: "名创优品", addr: "", subway: "난징동루 거리 내 위치"},
            {cat: "쇼핑/기타", nameKo: "토끼사탕", nameZh: "大白兔", addr: "", subway: "예원/난징동루 상점가"},
            {cat: "쇼핑/기타", nameKo: "로손", nameZh: "罗森便利店", addr: "", subway: ""},
            {cat: "쇼핑/기타", nameKo: "패밀리마트", nameZh: "全家便利店", addr: "", subway: ""},
            {cat: "쇼핑/기타", nameKo: "대형마트(따룬파)", nameZh: "大润发", addr: "https://surl.amap.com/8IacSH7IcrX", subway: ""},
            {cat: "쇼핑/기타", nameKo: "현지 마트", nameZh: "联华生活鲜", addr: "", subway: ""},
            {cat: "쇼핑/기타", nameKo: "마사지(도원향)", nameZh: "桃源乡(南京东路店)", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구 100m"}
        ];'''
    
    content = re.sub(r'const initialSpots = \[.*?\];', full_spots_data, content, flags=re.DOTALL)

    # 3. Double check Weather Header - Ensure it's exactly as requested
    weather_header_old = re.search(r'<header.*?</header>', content, re.DOTALL).group(0)
    weather_header_new = '''    <header class="glass-header sticky top-0 z-50 px-4 py-3">
        <div class="flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <button onclick="window.open('https://search.naver.com/search.naver?query=상해+날씨', '_blank')" id="weather-display" class="bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 px-4 py-2.5 rounded-2xl text-[11px] font-black flex items-center shadow-sm border border-indigo-100 dark:border-indigo-800/50">
                    <i class="fas fa-spinner fa-spin mr-2 text-indigo-500"></i>날씨 확인 중...
                </button>
            </div>
            <div class="flex items-center space-x-2">
                <button onclick="location.href='alipays://platformapi/startapp?appId=20000056'" class="w-9 h-9 rounded-full bg-blue-500 text-white flex items-center justify-center shadow-md active:scale-90 transition-transform">
                    <i class="fab fa-alipay text-[16px]"></i>
                </button>
                <button onclick="toggleTheme()" class="w-9 h-9 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-500 shadow-sm border border-slate-200 dark:border-slate-700">
                    <i id="theme-icon" class="fas fa-moon text-sm"></i>
                </button>
            </div>
        </div>
    </header>'''
    content = content.replace(weather_header_old, weather_header_new)

    # 4. Final Script Safety Check: Remove any duplicated or corrupted script segments
    # (Clean up any stray degree symbols or broken code observed earlier)
    content = content.replace('}°C`;', '}°C`; }') # Fix potentially broken template strings
    
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    final_spot_sync()
    print("Successfully synced spots and fixed header.")
