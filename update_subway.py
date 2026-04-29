import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def update_subway_info():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update initialSpots with detailed subway information
    new_spots_data = '''        const initialSpots = [
            {cat: "핵심", nameKo: "푸동 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "지하철 2호선 / 자기부상 (Pudong Airport)"},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "2/7/16/18호선 Longyang Rd역"},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "2/14호선 Lujiazui역"},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "https://surl.amap.com/1raycs1Tfz8", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 7번출구"},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "9호선 Qibao(Qi Bao)역 2번출구 도보 5분(400m)"},
            {cat: "명소", nameKo: "정안사", nameZh: "静安寺", addr: "https://surl.amap.com/1M5SBkJie2Z", subway: "2/7/14호선 Jing'an Temple(Jing An Si)역 1번출구 도보 2분(100m)"},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "https://surl.amap.com/1uSLDCN1o9iV", subway: "2/12/13호선 West Nanjing Rd(Nanjing Xi Lu)역"},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "https://surl.amap.com/1Ord7Ml1z6OW", subway: "시외 지역 (전용 차량/버스 권장)"},
            {cat: "명소", nameKo: "상하이 박물관", nameZh: "上海博物馆", addr: "", subway: "1/2/8호선 People's Square(Renmin Guangchang)역 1번출구 도보 3분(200m)"},
            {cat: "명소", nameKo: "도시계획 전시관", nameZh: "上海城市规划展示馆", addr: "", subway: "1/2/8호선 People's Square(Renmin Guangchang)역 3번출구 도보 1분(100m)"},
            {cat: "명소", nameKo: "윤봉길 기념관", nameZh: "梅园-尹奉길义士生平사적陈列室", addr: "https://surl.amap.com/1W3f3i9H89v", subway: "3/8호선 Hongkou Football Stadium(Hongkou Zuqiu Chang)역 1번출구 도보 7분(500m)"},
            {cat: "맛집", nameKo: "게살국수", nameZh: "裕兴记(外滩店)", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 8분(500m)"},
            {cat: "맛집", nameKo: "장씨네 게국수", nameZh: "庄氏隆兴·蟹粉面道", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 7번출구 도보 3분(200m)"},
            {cat: "맛집", nameKo: "가정식 식당 (상해라오라오)", nameZh: "上海姥姥家常饭馆", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 10분(600m)"},
            {cat: "맛집", nameKo: "샤오롱바오 (가가탕포)", nameZh: "佳家탕包", addr: "", subway: "1/2/8호선 People's Square(Renmin Guangchang)역 8번출구 도보 5분(400m)"},
            {cat: "맛집", nameKo: "생전 (샤오양)", nameZh: "小杨生煎", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 7번출구 인근 도보 3분"},
            {cat: "맛집", nameKo: "생전 맛집 (따후춘)", nameZh: "大壶春", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 6분(400m)"},
            {cat: "맛집", nameKo: "상하이 전통요리 (老吉士)", nameZh: "老吉士酒家", addr: "", subway: "1/7호선 Changshu Rd(Changshu Lu)역 8번출구 도보 8분(550m)"},
            {cat: "맛집", nameKo: "항저우 요리 (구이만롱)", nameZh: "桂满陇", addr: "", subway: "2/7/14호선 Jing'an Temple(Jing An Si)역 3번출구 도보 3분"},
            {cat: "맛집", nameKo: "생선구이 (강변성외)", nameZh: "江边城外烤全鱼", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 7번출구 직결 (애플스토어 옆)"},
            {cat: "맛집", nameKo: "훠궈 (촉대협)", nameZh: "蜀大侠", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 6번출구 도보 5분(300m)"},
            {cat: "맛집", nameKo: "훠궈 (홍지에)", nameZh: "鸿姐老火锅", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 3분(200m)"},
            {cat: "쇼핑/기타", nameKo: "신세계백화점", nameZh: "新世界城", addr: "", subway: "1/2/8호선 People's Square(Renmin Guangchang)역 7번출구 바로앞"},
            {cat: "쇼핑/기타", nameKo: "제일백화점", nameZh: "第一百货商业中心", addr: "", subway: "1/2/8호선 People's Square(Renmin Guangchang)역 19번출구 바로앞"},
            {cat: "쇼핑/기타", nameKo: "미니소 (Miniso)", nameZh: "名创优品", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 도보 3분"},
            {cat: "쇼핑/기타", nameKo: "토끼사탕 (대백토)", nameZh: "大白兔", addr: "", subway: "예원/난징동루 상점가 내 위치"},
            {cat: "쇼핑/기타", nameKo: "로손 (Lawson)", nameZh: "罗森便利店", addr: "", subway: "시내 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "패밀리마트", nameZh: "全家便利店", addr: "", subway: "시내 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "대형마트 (따룬파)", nameZh: "大润发", addr: "https://surl.amap.com/8IacSH7IcrX", subway: "지하철역 연계 필요"},
            {cat: "쇼핑/기타", nameKo: "현지 마트", nameZh: "联华생활鲜", addr: "", subway: "시내 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "도원향 (마사지)", nameZh: "桃源乡(南京东路店)", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 2분(100m)"}
        ];'''
    
    spots_pattern = re.compile(r'const initialSpots = \[.*?\];', re.DOTALL)
    content = spots_pattern.sub(new_spots_data, content)

    # 2. Update renderSpots UI to show subway info properly
    # Check if subway info is already in the UI code
    if 's.subway ?' not in content:
        render_spots_old = '<h4>${s.nameKo}</h4>\n                            <p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p></div>'
        render_spots_new = """<h4>${s.nameKo}</h4>
                            <p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p>
                            ${s.subway ? `<p class="text-[10px] font-bold text-indigo-600 mt-2 flex items-center bg-indigo-50 dark:bg-indigo-900/20 px-2 py-1.5 rounded-lg w-fit"><i class="fas fa-subway mr-1.5"></i>${s.subway}</p>` : ''}</div>"""
        content = content.replace(render_spots_old, render_spots_new)

    # 3. Ensure the migration logic handles the updated 'subway' field for existing items
    migration_old = """// Migration: Add missing initial items by nameZh
                    initialSpots.forEach(init => {
                        const exists = spotData.some(item => item.nameZh === init.nameZh);
                        if (!exists) db.ref(`${basePath}/spots`).push(init);
                    });"""
    
    migration_new = """// Migration: Add missing initial items or update subway info
                    initialSpots.forEach(init => {
                        const existingItem = spotData.find(item => item.nameZh === init.nameZh);
                        if (!existingItem) {
                            db.ref(`${basePath}/spots`).push(init);
                        } else if (!existingItem.subway && init.subway) {
                            // Update subway info if it's missing in DB
                            db.ref(`${basePath}/spots/${existingItem.key}`).update({ subway: init.subway });
                        }
                    });"""
    content = content.replace(migration_old, migration_new)

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_subway_info()
    print("Subway information added to spots.")
