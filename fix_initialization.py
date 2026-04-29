import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def fix_app():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Header (Remove time elements, rearrange weather)
    # Finding the header block more accurately
    header_pattern = re.compile(r'<header.*?</header>', re.DOTALL)
    header_new = '''    <header class="glass-header sticky top-0 z-50 px-4 py-3">
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
    content = header_pattern.sub(header_new, content)

    # 2. Fix fetchWeather function
    weather_pattern = re.compile(r'async function fetchWeather\(\) \{.*?\}', re.DOTALL)
    weather_new = '''        async function fetchWeather() {
            try {
                const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=31.2222&longitude=121.4581&current_weather=true');
                const data = await res.json();
                const cw = data.current_weather;
                const temp = Math.round(cw.temperature);
                const code = cw.weathercode;
                
                let icon = 'fa-sun';
                let desc = '맑음';
                
                if (code >= 1 && code <= 3) { icon = 'fa-cloud-sun'; desc = '구름조금'; }
                else if (code >= 45 && code <= 48) { icon = 'fa-smog'; desc = '안개'; }
                else if (code >= 51 && code <= 67) { icon = 'fa-cloud-showers-heavy'; desc = '비 옴'; }
                else if (code >= 71 && code <= 77) { icon = 'fa-snowflake'; desc = '눈 옴'; }
                else if (code >= 80 && code <= 82) { icon = 'fa-cloud-rain'; desc = '소나기'; }
                else if (code >= 95) { icon = 'fa-bolt'; desc = '뇌우'; }
                
                const el = document.getElementById('weather-display');
                if(el) el.innerHTML = `<i class="fas ${icon} mr-2 text-indigo-500"></i>상해 ${temp}°C / ${desc}`;
            } catch(e) {
                const el = document.getElementById('weather-display');
                if(el) el.innerText = '날씨 정보 오류';
            }
        }'''
    content = weather_pattern.sub(weather_new, content)

    # 3. Update initialSpots with subway info
    spots_pattern = re.compile(r'const initialSpots = \[.*?\];', re.DOTALL)
    spots_data_new = '''        const initialSpots = [
            {cat: "핵심", nameKo: "푸동공항 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "지하철 2호선 / 자기부상"},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路(地铁站)", addr: "", subway: "2/7/16/18호선 Longyang Rd역"},
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
            {cat: "맛집", nameKo: "가정식 식당 (상해라오라오)", nameZh: "上海姥姥家常饭馆", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "샤오롱바오 (가가탕포)", nameZh: "佳家汤包", addr: "", subway: "1/2/8호선 People's Square역 8번출구"},
            {cat: "맛집", nameKo: "생전 (샤오양)", nameZh: "小杨生煎", addr: "", subway: "체인점 (주요 역 근처 많음)"},
            {cat: "맛집", nameKo: "생전 맛집 (따후춘)", nameZh: "大壶春", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "상하이 전통요리 (라오지쓰)", nameZh: "老吉士酒家", addr: "", subway: "1/7호선 Changshu Rd역 8번출구"},
            {cat: "맛집", nameKo: "항저우 요리 (구이만롱)", nameZh: "桂满陇", addr: "", subway: "2/7/14호선 Jing'an Temple역 3번출구"},
            {cat: "맛집", nameKo: "생선구이 (강변성외)", nameZh: "江边城外烤全鱼", addr: "", subway: "2/10호선 East Nanjing Rd역 7번출구"},
            {cat: "맛집", nameKo: "훠궈 (촉대협)", nameZh: "蜀大侠", addr: "", subway: "2/10호선 East Nanjing Rd역 6번출구"},
            {cat: "맛집", nameKo: "훠궈 (홍지에)", nameZh: "鸿姐老火锅", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "쇼핑/기타", nameKo: "신세계백화점", nameZh: "新世界城", addr: "", subway: "1/2/8호선 People's Square역 7번출구"},
            {cat: "쇼핑/기타", nameKo: "제일백화점", nameZh: "第一百货商业中心", addr: "", subway: "1/2/8호선 People's Square역 19번출구"},
            {cat: "쇼핑/기타", nameKo: "미니소 (Miniso)", nameZh: "名创优品", addr: "", subway: "난징동루 거리 내 위치"},
            {cat: "쇼핑/기타", nameKo: "토끼사탕 (대백토)", nameZh: "大白兔", addr: "", subway: "예원/난징동루 상점가"},
            {cat: "쇼핑/기타", nameKo: "로손 (Lawson)", nameZh: "罗森便利店", addr: "", subway: ""},
            {cat: "쇼핑/기타", nameKo: "패밀리마트", nameZh: "全家便利店", addr: "", subway: ""},
            {cat: "쇼핑/기타", nameKo: "대형마트 (따룬파)", nameZh: "大润发", addr: "https://surl.amap.com/8IacSH7IcrX", subway: ""},
            {cat: "쇼핑/기타", nameKo: "롄화 마트 (현지)", nameZh: "联华生活鲜", addr: "", subway: ""},
            {cat: "쇼핑/기타", nameKo: "도원향 (마사지)", nameZh: "桃源乡(南京东路店)", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구 100m"}
        ];'''
    content = spots_pattern.sub(spots_data_new, content)

    # 4. Correct the DOMContentLoaded initialization line (Fixing the comment bug)
    init_pattern = re.compile(r'// startClock\(\); // Removed time from header.*?;', re.DOTALL)
    init_new = "fetchWeather(); renderPhrases(); loadItinerary(); loadExpenses(); loadChecklist(); loadSpots();"
    content = init_pattern.sub(init_new, content)

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_app()
