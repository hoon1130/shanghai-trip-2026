import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def apply_updates():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update initialSpots with the full list
    new_spots_data = '''        const initialSpots = [
            {cat: "핵심", nameKo: "푸동공항 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "지하철 2호선 / 자기부상"},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "2/7/16/18호선 Longyang Rd역"},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "2/14호선 Lujiazui역"},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "https://surl.amap.com/1raycs1Tfz8", subway: "2/10호선 East Nanjing Rd역 7번출구"},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "9호선 Qibao역 2번출구"},
            {cat: "명소", nameKo: "정안사", nameZh: "静안寺", addr: "https://surl.amap.com/1M5SBkJie2Z", subway: "2/7/14호선 Jing'an Temple역 1번출구"},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "https://surl.amap.com/1uSLDCN1o9iV", subway: "2/12/13호선 West Nanjing Rd역"},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "https://surl.amap.com/1Ord7Ml1z6OW", subway: "시외 지역 (전용 차량 권장)"},
            {cat: "명소", nameKo: "상하이 박물관", nameZh: "上海博物馆", addr: "", subway: "1/2/8호선 People's Square역 1번출구"},
            {cat: "명소", nameKo: "도시계획 전시관", nameZh: "上海城市规划展示馆", addr: "", subway: "1/2/8호선 People's Square역 3번출구"},
            {cat: "명소", nameKo: "윤봉길 기념관", nameZh: "梅园-尹奉길义士生平사적陈列室", addr: "https://surl.amap.com/1W3f3i9H89v", subway: "3/8호선 Hongkou Football Stadium역 1번출구"},
            {cat: "맛집", nameKo: "게살국수", nameZh: "裕兴记(外滩店)", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "장씨네 게국수", nameZh: "庄氏隆兴·蟹粉面道", addr: "", subway: "2/10호선 East Nanjing Rd역 7번출구"},
            {cat: "맛집", nameKo: "가정식 식당 (상해라오라오)", nameZh: "上海姥姥家常饭馆", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "샤오롱바오 (가가탕포)", nameZh: "佳家탕包", addr: "", subway: "1/2/8호선 People's Square역 8번출구"},
            {cat: "맛집", nameKo: "생전 (샤오양)", nameZh: "小杨生煎", addr: "", subway: "체인점 (주요 역 근처 많음)"},
            {cat: "맛집", nameKo: "생전 맛집 (따후춘)", nameZh: "大壶春", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구"},
            {cat: "맛집", nameKo: "상하이 전통요리 (老吉士)", nameZh: "老吉士酒家", addr: "", subway: "1/7호선 Changshu Rd역 8번출구"},
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
            {cat: "쇼핑/기타", nameKo: "롄화 마트 (현지)", nameZh: "联华생활鲜", addr: "", subway: ""},
            {cat: "쇼핑/기타", nameKo: "도원향 (마사지)", nameZh: "桃源乡(南京东路店)", addr: "", subway: "2/10호선 East Nanjing Rd역 2번출구 100m"}
        ];'''
    
    spots_pattern = re.compile(r'const initialSpots = \[.*?\];', re.DOTALL)
    content = spots_pattern.sub(new_spots_data, content)

    # 2. Update renderSpots function UI
    render_spots_old = '<h4>${s.nameKo}</h4><p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p></div>'
    render_spots_new = """<h4>${s.nameKo}</h4>
                            <p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p>
                            ${s.subway ? `<p class="text-[10px] font-bold text-indigo-600 mt-2 flex items-center bg-indigo-50 dark:bg-indigo-900/20 px-2 py-1.5 rounded-lg w-fit"><i class="fas fa-subway mr-1.5"></i>${s.subway}</p>` : ''}</div>"""
    content = content.replace(render_spots_old, render_spots_new)

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    apply_updates()
