import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def update_spots_comprehensive():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update initialSpots with more complete list, clean addresses, and detailed subway info
    new_spots_data = '''        const initialSpots = [
            {cat: "핵심", nameKo: "푸동 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "지하철 2호선 浦东国际机场(Pudong Int'l Airport)역 | 자기부상 직결"},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "2/7/16/18호선 龙阳路(Longyang Rd)역"},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "2/14호선 陆家嘴(Lujiazui)역"},
            {cat: "핵심", nameKo: "숙소 (IFC Residence)", nameZh: "上海국金汇", addr: "", subway: "2/14호선 陆家嘴(Lujiazui)역 6번출구 도보 3분"},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "", subway: "2/10호선 南京东路(East Nanjing Rd)역 7번출구 도보 1분"},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "9호선 七宝(Qibao)역 2번출구 도보 5분 (400m)"},
            {cat: "명소", nameKo: "정안사", nameZh: "静安寺", addr: "", subway: "2/7/14호선 静安寺(Jing'an Temple)역 1번출구 도보 2분 (100m)"},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "", subway: "2/12/13호선 南京西路(West Nanjing Rd)역"},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "", subway: "시외지역 | 전용차량 또는 시외버스 이용"},
            {cat: "명소", nameKo: "주가각", nameZh: "朱家角", addr: "", subway: "17호선 朱家角(Zhujiajiao)역 1번출구 도보 15분 (1.1km)"},
            {cat: "명소", nameKo: "루쉰공원", nameZh: "鲁迅公园", addr: "", subway: "3/8호선 虹口足球场(Hongkou Football Stadium)역 1번출구 도보 5분 (450m)"},
            {cat: "명소", nameKo: "우캉멘션", nameZh: "武康大楼", addr: "", subway: "10/11호선 交通大学(Jiaotong Univ)역 1번출구 도보 5분 (400m)"},
            {cat: "명소", nameKo: "티엔즈팡", nameZh: "田子坊", addr: "", subway: "9호선 打浦桥(Dapuqiao)역 1번출구 도보 1분"},
            {cat: "명소", nameKo: "상하이 박물관", nameZh: "上海博物馆", addr: "", subway: "1/2/8호선 人민广场(People's Square)역 1번출구 도보 3분 (200m)"},
            {cat: "명소", nameKo: "도시계획 전시관", nameZh: "上海城市规划展示馆", addr: "", subway: "1/2/8호선 人민广场(People's Square)역 3번출구 도보 1분 (100m)"},
            {cat: "명소", nameKo: "윤봉길 기념관", nameZh: "梅园-尹奉길义士生平사적陈列室", addr: "", subway: "3/8호선 虹口足球场(Hongkou Football Stadium)역 1번출구 도보 7분 (500m)"},
            {cat: "명소", nameKo: "동방명주", nameZh: "东方明珠", addr: "", subway: "2/14호선 陆家嘴(Lujiazui)역 1번출구 도보 5분"},
            {cat: "명소", nameKo: "와이탄 야경", nameZh: "外滩", addr: "", subway: "2/10호선 南京东路(East Nanjing Rd)역 2번출구 도보 10분"},
            {cat: "맛집", nameKo: "점보시푸드 (IFC)", nameZh: "珍宝海鲜(国金中心店)", addr: "", subway: "2/14호선 陆家嘴(Lujiazui)역 6번출구 (IFC몰 3층)"},
            {cat: "맛집", nameKo: "게살국수", nameZh: "裕兴记(外滩店)", addr: "", subway: "2/10호선 南京东路(East Nanjing Rd)역 2번출구 도보 8분 (500m)"},
            {cat: "맛집", nameKo: "장씨네 게국수", nameZh: "庄氏隆兴·蟹粉面道", addr: "", subway: "2/10호선 南京东路(East Nanjing Rd)역 7번출구 도보 3분 (200m)"},
            {cat: "맛집", nameKo: "가정식 식당 (상해라오라오)", nameZh: "上海姥姥家常饭馆", addr: "", subway: "2/10호선 南京东路(East Nanjing Rd)역 2번출구 도보 10분 (650m)"},
            {cat: "맛집", nameKo: "샤오롱바오 (가가탕포)", nameZh: "佳家汤包", addr: "", subway: "1/2/8호선 人민广场(People's Square)역 8번출구 도보 5분 (400m)"},
            {cat: "맛집", nameKo: "생전 (샤오양)", nameZh: "小杨生煎", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 7번출구 인근"},
            {cat: "맛집", nameKo: "생전 맛집 (따후춘)", nameZh: "大壶春", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 6분 (400m)"},
            {cat: "맛집", nameKo: "상하이 전통요리 (老吉士)", nameZh: "老吉士酒家", addr: "", subway: "1/7호선 Changshu Rd(Changshu Lu)역 8번출구 도보 8분 (550m)"},
            {cat: "맛집", nameKo: "항저우 요리 (구이만롱)", nameZh: "桂满陇", addr: "", subway: "2/7/14호선 Jing'an Temple(Jing An Si)역 3번출구 도보 3분"},
            {cat: "맛집", nameKo: "생선구이 (강변성외)", nameZh: "江边城外烤全鱼", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 7번출구 직결"},
            {cat: "맛집", nameKo: "훠궈 (촉대협)", nameZh: "蜀大侠", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 6번출구 도보 5분 (300m)"},
            {cat: "맛집", nameKo: "훠궈 (홍지에)", nameZh: "鸿姐老火锅", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 3분 (200m)"},
            {cat: "쇼핑/기타", nameKo: "신세계백화점", nameZh: "新세계城", addr: "", subway: "1/2/8호선 People's Square(Renmin Guangchang)역 7번출구 바로앞"},
            {cat: "쇼핑/기타", nameKo: "제일백화점", nameZh: "第一百货商业中心", addr: "", subway: "1/2/8호선 People's Square(Renmin Guangchang)역 19번출구 바로앞"},
            {cat: "쇼핑/기타", nameKo: "미니소 (Miniso)", nameZh: "名创优品", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 도보 3분"},
            {cat: "쇼핑/기타", nameKo: "토끼사탕 (대백토)", nameZh: "大白兔", addr: "", subway: "예원/난징동루 상점가 내 위치"},
            {cat: "쇼핑/기타", nameKo: "로손 (Lawson)", nameZh: "罗森便利店", addr: "", subway: "상해 전역 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "패밀리마트", nameZh: "全家便利店", addr: "", subway: "상해 전역 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "대형마트 (따룬파)", nameZh: "大润发", addr: "", subway: "지하철역 연계 필요"},
            {cat: "쇼핑/기타", nameKo: "현지 마트", nameZh: "联华생활鲜", addr: "", subway: "상해 전역 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "도원향 (마사지)", nameZh: "桃源乡(南京东路店)", addr: "", subway: "2/10호선 East Nanjing Rd(Nanjing Dong Lu)역 2번출구 도보 2분 (100m)"}
        ];'''
    
    spots_pattern = re.compile(r'const initialSpots = \[.*?\];', re.DOTALL)
    content = spots_pattern.sub(new_spots_data, content)

    # 2. Ensure migration logic force-updates EXISTING items
    # Fixed to look for the exact loop structure
    migration_old = re.search(r'initialSpots\.forEach\(init => \{.*?\}\);', content, re.DOTALL).group(0)
    new_migration = """initialSpots.forEach(init => {
                        const existingItem = spotData.find(item => item.nameZh === init.nameZh);
                        if (!existingItem) {
                            db.ref(`${basePath}/spots`).push(init);
                        } else {
                            // Force update subway and clean up URL addresses for all items
                            db.ref(`${basePath}/spots/${existingItem.key}`).update({ 
                                subway: init.subway,
                                addr: init.addr
                            });
                        }
                    });"""
    content = content.replace(migration_old, new_migration)

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_spots_comprehensive()
