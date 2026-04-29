import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def update_spots_v30():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update initialSpots with the requested format: 한자(Pinyin) 한글명, 출구, 거리
    new_spots_data = '''        const initialSpots = [
            {cat: "핵심", nameKo: "푸동 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "浦东国际机场(Pudong Guoji Jichang) 푸동공항역 | 2호선/자기부상"},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "龙阳路(Longyang Lu) 롱양루역 | 2/7/16/18호선"},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 2/14호선"},
            {cat: "핵심", nameKo: "숙소 (IFC Residence)", nameZh: "上海国金汇", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 6번출구 도보 3분"},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 1분"},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "七宝(Qi Bao) 치바오역 | 2번출구 도보 5분(400m)"},
            {cat: "명소", nameKo: "정안사", nameZh: "静安寺", addr: "", subway: "静安寺(Jing An Si) 정안사역 | 1번출구 도보 2분(100m)"},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "", subway: "南京西路(Nanjing Xi Lu) 남경서로역 | 2/12/13호선"},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "", subway: "시외지역 | 전용차량 이용 권장"},
            {cat: "명소", nameKo: "주가각", nameZh: "朱家角", addr: "", subway: "朱家角(Zhu Jia Jiao) 주가각역 | 1번출구 도보 15분(1.1km)"},
            {cat: "명소", nameKo: "루쉰공원", nameZh: "鲁迅公园", addr: "", subway: "虹口足球场(Hongkou Zuqiu Chang) 홍구축구장역 | 1번출구 도보 5분"},
            {cat: "명소", nameKo: "우캉멘션", nameZh: "武康大楼", addr: "", subway: "交通大学(Jiao Tong Da Xue) 교통대학역 | 1번출구 도보 5분"},
            {cat: "명소", nameKo: "티엔즈팡", nameZh: "田子坊", addr: "", subway: "打浦桥(Da Pu Qiao) 타포교역 | 1번출구 도보 1분"},
            {cat: "명소", nameKo: "상하이 박물관", nameZh: "上海博物馆", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 1번출구 도보 3분"},
            {cat: "명소", nameKo: "도시계획 전시관", nameZh: "上海城市规划展示馆", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 3번출구 도보 1분"},
            {cat: "명소", nameKo: "윤봉길 기념관", nameZh: "梅园-尹奉길义士生平사적陈列室", addr: "", subway: "虹口足球场(Hongkou Zuqiu Chang) 홍구축구장역 | 1번출구 도보 7분"},
            {cat: "명소", nameKo: "동방명주", nameZh: "东方明珠", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 1번출구 도보 5분"},
            {cat: "명소", nameKo: "와이탄 야경", nameZh: "外滩", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 10분"},
            {cat: "맛집", nameKo: "점보시푸드 (IFC)", nameZh: "珍宝海鲜(国金中心店)", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 6번출구 직결"},
            {cat: "맛집", nameKo: "게살국수", nameZh: "裕兴记(外滩店)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 8분"},
            {cat: "맛집", nameKo: "장씨네 게국수", nameZh: "庄氏隆兴·蟹粉面道", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 3분"},
            {cat: "맛집", nameKo: "가정식 식당 (상해라오라오)", nameZh: "上海姥姥家常饭馆", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 10분"},
            {cat: "맛집", nameKo: "샤오롱바오 (가가탕포)", nameZh: "佳家汤包", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 8번출구 도보 5분"},
            {cat: "맛집", nameKo: "생전 (샤오양)", nameZh: "小杨生煎", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 인근"},
            {cat: "맛집", nameKo: "생전 맛집 (따후춘)", nameZh: "大壶春", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 6분"},
            {cat: "맛집", nameKo: "상하이 전통요리 (老吉士)", nameZh: "老吉士酒家", addr: "", subway: "常熟路(Changshu Lu) 상숙로역 | 8번출구 도보 8분"},
            {cat: "맛집", nameKo: "항저우 요리 (구이만롱)", nameZh: "桂满陇", addr: "", subway: "静安寺(Jing An Si) 정안사역 | 3번출구 도보 3분"},
            {cat: "맛집", nameKo: "생선구이 (강변성외)", nameZh: "江边城外烤全鱼", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 직결"},
            {cat: "맛집", nameKo: "훠궈 (촉대협)", nameZh: "蜀大侠", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 6번출구 도보 5분"},
            {cat: "맛집", nameKo: "훠궈 (홍지에)", nameZh: "鸿姐老火锅", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 3분"},
            {cat: "쇼핑/기타", nameKo: "신세계백화점", nameZh: "新世界城", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 7번출구 바로앞"},
            {cat: "쇼핑/기타", nameKo: "제일백화점", nameZh: "第一百货商业中心", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 19번출구 바로앞"},
            {cat: "쇼핑/기타", nameKo: "미니소 (Miniso)", nameZh: "名创优品", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 도보 3분"},
            {cat: "쇼핑/기타", nameKo: "토끼사탕 (대백토)", nameZh: "大白兔", addr: "", subway: "豫园(Yuyuan) 예원역 | 1번출구 도보 5분"},
            {cat: "쇼핑/기타", nameKo: "로손 (Lawson)", nameZh: "罗森便利店", addr: "", subway: "상해 시내 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "패밀리마트", nameZh: "全家便利店", addr: "", subway: "상해 시내 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "대형마트 (따룬파)", nameZh: "大润发", addr: "", subway: "지하철역 연계 필요"},
            {cat: "쇼핑/기타", nameKo: "현지 마트", nameZh: "联华생활鲜", addr: "", subway: "상해 시내 곳곳 위치"},
            {cat: "쇼핑/기타", nameKo: "도원향 (마사지)", nameZh: "桃源乡(南京东路店)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 2분"}
        ];'''
    
    spots_pattern = re.compile(r'const initialSpots = \[.*?\];', re.DOTALL)
    content = spots_pattern.sub(new_spots_data, content)

    # 2. Update renderSpots UI logic
    # Clean up the function to include Metro search and clipboard
    render_spots_new = """        function renderSpots() {
            const search = document.getElementById('spot-search').value.toLowerCase();
            const filtered = spotData.filter(s => (currentSpotCat === '전체' || s.cat === currentSpotCat) && (s.nameKo.toLowerCase().includes(search) || s.nameZh.toLowerCase().includes(search) || (s.addr && s.addr.toLowerCase().includes(search))));
            const listEl = document.getElementById('spot-list');
            if(listEl) {
                listEl.innerHTML = filtered.map(s => {
                    const subwayPinyinMatch = s.subway ? s.subway.match(/\\(([^)]+)\\)/) : null;
                    const searchKey = subwayPinyinMatch ? subwayPinyinMatch[1] : (s.subway ? s.subway.split(' ')[0] : '');
                    return `
                    <div class="bg-white dark:bg-slate-900 p-5 rounded-[2rem] border border-slate-200 dark:border-slate-800 shadow-sm active:scale-[0.98] transition-transform">
                        <div class="flex justify-between items-start mb-2">
                            <div><span class="text-[10px] font-black text-indigo-500 bg-indigo-50 px-2 py-1 rounded-md mb-2 inline-block">${s.cat}</span>
                            <h4 class="font-black text-lg">${s.nameKo}</h4>
                            <p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p>
                            ${s.subway ? `<div onclick="openMetro('${searchKey}')" class="text-[13px] font-black text-indigo-600 mt-3 flex items-start bg-indigo-50 dark:bg-indigo-900/30 px-3 py-2 rounded-xl border border-indigo-100 dark:border-indigo-800 cursor-pointer active:scale-95 transition-transform"><i class="fas fa-subway mt-0.5 mr-2"></i><span class="flex-1">${s.subway}</span></div>` : ''}</div>
                            <button onclick="openSpotModal('${s.key}')" class="text-slate-300 p-2"><i class="fas fa-edit text-sm"></i></button>
                        </div>
                        <p class="text-[12px] font-medium text-slate-500 mb-3">${s.addr || ''}</p>
                        <div class="flex gap-2">
                            <button onclick="openAmap('${s.nameZh}')" class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-700 rounded-xl font-black text-[10px]">고덕지도</button>
                            <button onclick="openBaiduMap('${s.nameZh}')" class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-700 rounded-xl font-black text-[10px]">바이두</button>
                        </div>
                    </div>`;
                }).join('') || '<div class="text-center text-slate-400 py-10 font-bold">검색 결과가 없습니다.</div>';
            }
        }
        function openMetro(keyword) {
            if(keyword) { navigator.clipboard.writeText(keyword).catch(()=>{}); }
            window.open('https://metro.nuua.travel/ko/shanghai', '_blank');
        }"""
    
    content = re.sub(r'function renderSpots\(\) \{.*?\}', render_spots_new, content, flags=re.DOTALL)

    # 3. Fix loadSpots to MERGE subway info properly
    load_spots_new = """        function loadSpots() {
            if(!db) return;
            db.ref(`${basePath}/spots`).on('value', s => {
                const data = s.val();
                if(data) {
                    spotData = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                    initialSpots.forEach(init => {
                        const existingItem = spotData.find(item => item.nameZh === init.nameZh);
                        if (!existingItem) {
                            db.ref(`${basePath}/spots`).push(init);
                        } else {
                            db.ref(`${basePath}/spots/${existingItem.key}`).update({ 
                                subway: init.subway,
                                addr: init.addr
                            });
                        }
                    });
                } else {
                    initialSpots.forEach(i => db.ref(`${basePath}/spots`).push(i));
                }
                renderSpots();
            });
        }"""
    content = re.sub(r'function loadSpots\(\) \{.*?\}', load_spots_new, content, flags=re.DOTALL)

    # 4. Cleanup any stray degree symbol corruption
    content = content.replace('째C', '°C')

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_spots_v30()
