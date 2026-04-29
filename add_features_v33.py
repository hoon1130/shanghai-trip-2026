import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def add_nearby_and_translator():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update initialSpots with Lat/Lng coordinates for main spots
    # I will add approximate coordinates for major Shanghai locations
    new_spots_data = '''        const initialSpots = [
            {cat: "핵심", nameKo: "푸동 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "浦东国际机场(Pudong Guoji Jichang) 푸동공항역 | 2호선/자기부상", lat: 31.144, lng: 121.808},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "龙阳路(Longyang Lu) 롱양루역 | 2/7/16/18호선", lat: 31.203, lng: 121.558},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 2/14호선", lat: 31.239, lng: 121.501},
            {cat: "핵심", nameKo: "숙소 (IFC Residence)", nameZh: "上海国金汇", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 6번출구 도보 3분", lat: 31.236, lng: 121.502},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 1분", lat: 31.238, lng: 121.484},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "七宝(Qi Bao) 치바오역 | 2번출구 도보 5분(400m)", lat: 31.155, lng: 121.352},
            {cat: "명소", nameKo: "정안사", nameZh: "静安寺", addr: "", subway: "静安寺(Jing An Si) 정안사역 | 1번출구 도보 2분(100m)", lat: 31.224, lng: 121.447},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "", subway: "南京西路(Nanjing Xi Lu) 남경서로역 | 2/12/13호선", lat: 31.230, lng: 121.460},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "", subway: "시외지역 | 전용차량 이용 권장", lat: 30.751, lng: 120.485},
            {cat: "명소", nameKo: "주가각", nameZh: "朱家角", addr: "", subway: "朱家角(Zhu Jia Jiao) 주가각역 | 1번출구 도보 15분(1.1km)", lat: 31.111, lng: 121.053},
            {cat: "명소", nameKo: "루쉰공원", nameZh: "鲁迅公园", addr: "", subway: "虹口足球场(Hongkou Zuqiu Chang) 홍구축구장역 | 1번출구 도보 5분", lat: 31.272, lng: 121.481},
            {cat: "명소", nameKo: "우캉멘션", nameZh: "武康大楼", addr: "", subway: "交通大学(Jiao Tong Da Xue) 교통대학역 | 1번출구 도보 5분", lat: 31.203, lng: 121.434},
            {cat: "명소", nameKo: "티엔즈팡", nameZh: "田子坊", addr: "", subway: "打浦桥(Da Pu Qiao) 타포교역 | 9호선 1번출구 도보 1분", lat: 31.209, lng: 121.468},
            {cat: "명소", nameKo: "상하이 박물관", nameZh: "上海博物馆", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 1번출구 도보 3분", lat: 31.230, lng: 121.474},
            {cat: "명소", nameKo: "도시계획 전시관", nameZh: "上海城市规划展示馆", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 3번출구 도보 1분", lat: 31.232, lng: 121.478},
            {cat: "명소", nameKo: "윤봉길 기념관", nameZh: "梅园-尹奉길义士生平사적陈列室", addr: "", subway: "虹口足球场(Hongkou Zuqiu Chang) 홍구축구장역 | 1번출구 도보 7분", lat: 31.270, lng: 121.485},
            {cat: "명소", nameKo: "동방명주", nameZh: "东方明珠", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 1번출구 도보 5분", lat: 31.242, lng: 121.495},
            {cat: "명소", nameKo: "와이탄 야경", nameZh: "外滩", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 10분", lat: 31.239, lng: 121.490},
            {cat: "명소", nameKo: "신천지", nameZh: "上海新天地", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 6번출구 도보 2분", lat: 31.221, lng: 121.475},
            {cat: "명소", nameKo: "예원/예원상성", nameZh: "豫园商城", addr: "", subway: "豫园(Yu Yuan) 예원역 | 1번출구 도보 5분", lat: 31.227, lng: 121.492},
            {cat: "명소", nameKo: "임시정부 유적지", nameZh: "大韩민국临时政府旧址", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 6번출구 도보 3분", lat: 31.218, lng: 121.475},
            {cat: "명소", nameKo: "디즈니랜드", nameZh: "上海迪士尼度假区", addr: "", subway: "迪士尼(Di Shi Ni) 디즈니역 | 1번출구 도보 5분", lat: 31.141, lng: 121.662},
            {cat: "명소", nameKo: "인민광장", nameZh: "人民广场", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 1/2/8호선", lat: 31.232, lng: 121.475},
            {cat: "맛집", nameKo: "점보시푸드 (IFC)", nameZh: "珍宝海鲜(国金中心店)", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 6번출구 직결", lat: 31.236, lng: 121.503},
            {cat: "맛집", nameKo: "게살국수", nameZh: "裕兴记(外滩店)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 8분", lat: 31.235, lng: 121.488},
            {cat: "맛집", nameKo: "장씨네 게국수", nameZh: "庄氏隆兴·蟹粉面道", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 3분", lat: 31.236, lng: 121.483},
            {cat: "맛집", nameKo: "가정식 식당 (상해라오라오)", nameZh: "上海姥姥家常饭馆", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 10분", lat: 31.237, lng: 121.489},
            {cat: "맛집", nameKo: "샤오롱바오 (가가탕포)", nameZh: "佳家汤包", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 8번출구 도보 5분", lat: 31.234, lng: 121.473},
            {cat: "맛집", nameKo: "생전 (샤오양)", nameZh: "小杨生煎", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 인근", lat: 31.236, lng: 121.484},
            {cat: "맛집", nameKo: "생전 맛집 (따후춘)", nameZh: "大壶春", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 6분", lat: 31.235, lng: 121.486},
            {cat: "맛집", nameKo: "상하이 전통요리 (老吉士)", nameZh: "老吉士酒家", addr: "", subway: "常숙路(Changshu Lu) 상숙로역 | 8번출구 도보 8분", lat: 31.213, lng: 121.448},
            {cat: "맛집", nameKo: "항저우 요리 (구이만롱)", nameZh: "桂满陇", addr: "", subway: "静安寺(Jing An Si) 정안사역 | 3번출구 도보 3분", lat: 31.224, lng: 121.449},
            {cat: "맛집", nameKo: "생선구이 (강변성외)", nameZh: "江边城外烤全鱼", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 직결", lat: 31.236, lng: 121.483},
            {cat: "맛집", nameKo: "훠궈 (촉대협)", nameZh: "蜀大侠", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 6번출구 도보 5분", lat: 31.235, lng: 121.481},
            {cat: "맛집", nameKo: "훠궈 (홍지에)", nameZh: "鸿姐老火锅", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 3분", lat: 31.234, lng: 121.485},
            {cat: "맛집", nameKo: "점도덕 (신천지)", nameZh: "点都德(新天地店)", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 2번출구 도보 5분", lat: 31.216, lng: 121.479},
            {cat: "맛집", nameKo: "양꼬치 (난징동루)", nameZh: "很久以前羊肉串(南京东路)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 3분", lat: 31.235, lng: 121.484},
            {cat: "맛집", nameKo: "하이디라오 (인민광장)", nameZh: "海底捞(人民广场店)", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 19번출구 도보 2분", lat: 31.234, lng: 121.478},
            {cat: "쇼핑/기타", nameKo: "신세계백화점", nameZh: "新세계城", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 7번출구 바로앞", lat: 31.235, lng: 121.473},
            {cat: "쇼핑/기타", nameKo: "제일백화점", nameZh: "第一百货商业中心", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 19번출구 바로앞", lat: 31.236, lng: 121.476},
            {cat: "쇼핑/기타", nameKo: "미니소 (Miniso)", nameZh: "名创优品", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 도보 3분", lat: 31.237, lng: 121.484},
            {cat: "쇼핑/기타", nameKo: "토끼사탕 (대백토)", nameZh: "大白兔", addr: "", subway: "豫园(Yuyuan) 예원역 | 1번출구 도보 5분", lat: 31.228, lng: 121.491},
            {cat: "쇼핑/기타", nameKo: "도원향 (마사지)", nameZh: "桃源乡(南京东路店)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 2분", lat: 31.235, lng: 121.485},
            {cat: "쇼핑/기타", nameKo: "릴리안 베이커리 (난징동루)", nameZh: "莉莲蛋挞(南京东路)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 1분", lat: 31.237, lng: 121.486}
        ];'''
    
    spots_pattern = re.compile(r'const initialSpots = \[.*?\];', re.DOTALL)
    content = spots_pattern.sub(new_spots_data, content)

    # 2. Add "Nearby" Button to Spot Filters
    cat_chips_old = '<button onclick="filterSpots(\'전체\')" class="category-chip active px-5 py-2 rounded-full text-xs font-black shadow-sm" data-cat="전체">전체</button>'
    cat_chips_new = '<button onclick="filterSpots(\'내 주변\')" class="category-chip px-5 py-2 rounded-full text-xs font-black shadow-sm bg-red-50 text-red-600 border-red-100" data-cat="내 주변"><i class="fas fa-location-arrow mr-1"></i>내 주변</button>\n                ' + cat_chips_old
    
    if 'data-cat="내 주변"' not in content:
        content = content.replace(cat_chips_old, cat_chips_new)

    # 3. Add Distance Calculation and Nearby Logic to JS
    distance_logic = """
        function getDistance(lat1, lon1, lat2, lon2) {
            if (!lat1 || !lon1 || !lat2 || !lon2) return Infinity;
            const R = 6371; const dLat = (lat2 - lat1) * Math.PI / 180; const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        }

        async function filterSpots(cat) { 
            currentSpotCat = cat; 
            document.querySelectorAll('.category-chip').forEach(btn => btn.classList.toggle('active', btn.dataset.cat === cat));
            
            if (cat === '내 주변') {
                navigator.geolocation.getCurrentPosition(pos => {
                    const { latitude, longitude } = pos.coords;
                    spotData.forEach(s => { s.dist = getDistance(latitude, longitude, s.lat, s.lng); });
                    spotData.sort((a, b) => a.dist - b.dist);
                    renderSpots();
                }, () => { alert('GPS 기능을 켜주세요.'); currentSpotCat = '전체'; renderSpots(); });
            } else {
                renderSpots(); 
            }
        }
    """
    # Replace existing filterSpots and add getDistance
    content = re.sub(r'function filterSpots\(cat\) \{.*?\}', distance_logic, content, flags=re.DOTALL)

    # Update renderSpots to show distance badge
    dist_badge_logic = '${s.dist && s.dist !== Infinity ? `<span class="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-1 rounded-md ml-2"><i class="fas fa-walking mr-1"></i>${s.dist < 1 ? Math.round(s.dist * 1000) + "m" : s.dist.toFixed(1) + "km"}</span>` : ""}'
    content = content.replace('<h4 class="font-black text-lg">${s.nameKo}</h4>', '<h4 class="font-black text-lg">${s.nameKo}' + dist_badge_logic + '</h4>')

    # 4. Phrases Tab: Add Translator Section
    translator_html = """
            <!-- Translator Section -->
            <div class="bg-white dark:bg-slate-900 p-6 rounded-[2.5rem] border border-slate-200 dark:border-slate-800 shadow-md space-y-4 mb-6">
                <div class="flex justify-between items-center px-1">
                    <h3 class="font-black text-brand-500 italic uppercase tracking-tighter flex items-center"><i class="fas fa-language mr-2 text-xl"></i>Smart Translator</h3>
                    <button onclick="window.open('https://papago.naver.com/', '_blank')" class="text-[10px] font-black text-slate-400 underline uppercase">Papago Web</button>
                </div>
                <div class="space-y-3">
                    <textarea id="trans-input" placeholder="번역할 문장을 입력하세요" class="w-full p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border-none font-bold text-sm outline-none h-24"></textarea>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="goPapago('ko', 'zh-CN')" class="bg-slate-900 text-white py-4 rounded-xl font-black text-sm shadow-md active:scale-95 transition-transform flex flex-col items-center">
                            <span>🇰🇷 한국어 → 🇨🇳 중국어</span>
                        </button>
                        <button onclick="goPapago('zh-CN', 'ko')" class="bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-white py-4 rounded-xl font-black text-sm active:scale-95 transition-transform flex flex-col items-center">
                            <span>🇨🇳 중국어 → 🇰🇷 한국어</span>
                        </button>
                    </div>
                    <button onclick="window.open('https://papago.naver.com/?sk=auto&tk=ko&hn=0&st=', '_blank')" class="w-full bg-indigo-500 text-white py-4 rounded-xl font-black text-sm shadow-lg active:scale-95 transition-transform flex items-center justify-center">
                        <i class="fas fa-camera mr-2"></i>실시간 카메라 번역 열기 (Papago)
                    </button>
                </div>
            </div>
    """
    if 'id="trans-input"' not in content:
        content = content.replace('<!-- Phrases Tab -->\n        <div id="phrases" class="tab-content space-y-6">', '<!-- Phrases Tab -->\n        <div id="phrases" class="tab-content space-y-6">\n' + translator_html)

    # Add translation logic to JS
    trans_logic = """
        function goPapago(src, tgt) {
            const txt = document.getElementById('trans-input').value;
            if(!txt) return alert('문장을 입력해주세요.');
            window.open(`https://papago.naver.com/?sk=${src}&tk=${tgt}&st=${encodeURIComponent(txt)}`, '_blank');
        }
    """
    if 'function goPapago' not in content:
        content = content.replace('function openSOSModal()', trans_logic + '\n\n        function openSOSModal()')

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    add_nearby_and_translator()
    print("Nearby and Translator features added.")
