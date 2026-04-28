
        // 🌟 Configuration 🌟
        const basePath = 'shanghai_2026_v30_final'; 
        const exchangeRate = 215.94;
        let db = null;
        let itineraryData = [];

        // 주소 및 명칭 사전 (디디추싱 검색 최적화를 위해 정확한 POI 명칭과 주소 사용)
        const smartMapDict = {
            "공항": {name: "浦东国际机场", addr: "上海市浦东新区迎宾大道6000号"},
            "푸동공항": {name: "浦东国际机场", addr: "上海市浦东新区迎宾大道6000号"},
            "루자쭈이": {name: "陆家嘴", addr: "上海市浦东新区"},
            "ifc": {name: "国金汇IFC Residence", addr: "上海市浦东新区世纪大道8号"},
            "호텔": {name: "国金汇IFC Residence", addr: "上海市浦东新区世纪大道8号"},
            "숙소": {name: "国金汇IFC Residence", addr: "上海市浦东新区世纪大道8号"},
            "ifc몰": {name: "上海国金中心商场", addr: "上海市浦东新区世纪大道8号"},
            "점보시푸드": {name: "珍宝海鲜(国金中心店)", addr: "上海市浦东新区世纪大道8号国金中心L3"},
            "예원": {name: "豫园", addr: "上海市黄浦区福佑路168号"},
            "마시청": {name: "上海马戏城", addr: "上海市静安区共和新路2266号"},
            "궁연": {name: "宫宴(上海)", addr: "上海市静安区江宁路445号"},
            "징안쓰": {name: "静安寺", addr: "上海市静安区南京西路1686号"},
            "임시정부": {name: "大韩民国临时政府旧址", addr: "上海市黄浦区马当路306弄4号"},
            "신천지": {name: "上海新天地", addr: "上海市黄浦区太仓路181弄"},
            "점도덕": {name: "点都德(新天地店)", addr: "上海市黄浦区黄陂南路838弄中海环宇荟"},
            "디즈니": {name: "上海迪士尼度假区", addr: "上海市浦东新区川沙新镇"},
            "릴리안": {name: "莉莲蛋挞(新世界大丸百货店)", addr: "上海市黄浦区南京东路228号新世界大丸百货"},
            "양꼬치": {name: "很久以前羊肉串(南京东路店)", addr: "上海市黄浦区南京东路800号"},
            "동방명주": {name: "东方明珠广播电视塔", addr: "上海市浦东新区世纪大道1号"},
            "우캉멘션": {name: "武康大楼", addr: "上海市徐汇区淮海中路1850号"},
            "우캉루": {name: "武康路", addr: "上海市徐汇区武康路"},
            "티엔즈팡": {name: "田子坊", addr: "上海市黄浦区泰康路210弄"},
            "자연박물관": {name: "上海自然博物馆", addr: "上海市静安区北京西路510号"},
            "그린마사지": {name: "Green Massage青籁养身(K11店)", addr: "上海市黄浦区淮海中路300号K11购物艺术中心"},
            "드래곤플라이": {name: "Dragonfly蜻蜓(陆家嘴店)", addr: "上海市浦东新区陆家嘴环路1318号星展银行大厦"},
            "동방화건강": {name: "东方和健康(南京东路店)", addr: "上海市黄浦区南京东路479号"},
            "빈장다다오": {name: "滨江大道", addr: "上海市浦东新区滨江大道"},
            "와이탄": {name: "外滩", addr: "上海市黄浦区中山东一路"}
        };

        const initialShanghai = [
            {date: "05-05(화)", time: "04:50~07:00", place: "공항 이동", memo: "집 앞 공항 리무진\n예약 완료", tipkey: ""},
            {date: "05-05(화)", time: "09:00~10:05", place: "인천 공항 → 푸동 공항", memo: "OZ361 A350\n좌석: 34A, 34B, 35B, 35C", tipkey: "flight"},
            {date: "05-05(화)", time: "11:00~12:00", place: "숙소 이동", memo: "6인승 비즈니스 디디 추천", tipkey: "taxi"},
            {date: "05-05(화)", time: "12:00~14:00", place: "점심 (IFC몰)", memo: "점보시푸드\n지하 2층 컷팅 과일 추천", tipkey: "ifc"},
            {date: "05-05(화)", time: "14:00", place: "호텔 체크인", memo: "IFC Residence", tipkey: "hotel"},
            {date: "05-05(화)", time: "15:30~16:30", place: "예원 정원", memo: "명나라 정원\n16:30 입장 마감 주의", tipkey: "yuyuan"},
            {date: "05-05(화)", time: "16:30~18:00", place: "예원 상성", memo: "전통 상점거리 및 구곡교\n대백토 사탕 등 쇼핑", tipkey: "yuyuan_shop"},
            {date: "05-05(화)", time: "19:30~21:00", place: "마시청 서커스", memo: "100분 관람 (예매 완료)", tipkey: "circus"},
            {date: "05-06(수)", time: "10:30~14:00", place: "점심 (궁연)", memo: "전통의상 체험 및 식사/공연", tipkey: "gongyan"},
            {date: "05-06(수)", time: "14:30~15:30", place: "상해 임시 정부", memo: "우리나라 독립운동 역사지", tipkey: "history"},
            {date: "05-06(수)", time: "15:30~18:00", place: "신천지 구경", memo: "유럽풍 노천 카페 및 거리", tipkey: "xintiandi"},
            {date: "05-06(수)", time: "18:00~20:00", place: "석식 (점도덕)", memo: "딤섬 전문 식당", tipkey: "diandude"},
            {date: "05-07(목)", time: "10:00~20:00", place: "상해 디즈니랜드", memo: "주토피아 및 주요 퍼레이드\n디즈니 전용앱 확인 필수", tipkey: "disney"},
            {date: "05-08(금)", time: "10:00~13:00", place: "난징동루 관광", memo: "우캉멘션, 동방명주 조망", tipkey: "lilian"},
            {date: "05-08(금)", time: "13:00~13:30", place: "점심 (양꼬치)", memo: "현저우이치엔 (자동구이)", tipkey: "yang"},
            {date: "05-08(금)", time: "16:00~18:00", place: "오후 자유 일정", memo: "티엔즈팡 골목 투어", tipkey: "tianzifang"},
            {date: "05-09(토)", time: "16:20~19:20", place: "푸동 공항 → 인천 공항", memo: "OZ366 A330", tipkey: ""},
            {date: "05-09(토)", time: "20:00", place: "수하물 찾고 귀가", memo: "공항버스 6705A 탑승", tipkey: "home"}
        ];

        const guideItinerary = [
            {
                date: "Day 1 푸동 & 화려한 첫날", 
                items: [
                    { time: "12:30", place: "IFC 몰", memo: "아버지와 아이의 첫 식사는 '점보시푸드'를 추천합니다. 쾌적한 시설에서 여독을 풀기 좋습니다.", map: "점보시푸드" },
                    { time: "15:30", place: "예원 & 상성", memo: "아버지와 일행분들께 '효도 정원'이라 설명해 드리면 좋습니다. 아이와 구곡교에서 예쁜 사진을 남기세요.", map: "예원" },
                    { time: "18:30", place: "빈장다다오 야경", memo: "푸동 강변 산책로에서 건너편 와이탄 야경을 감상하세요. 관광객이 붐비지 않아 일행 모두 만족할 코스입니다.", map: "빈장다다오" },
                    { time: "20:00", place: "마시청 서커스", memo: "아이와 아버지 모두 즐길 수 있는 상해 최고의 공연입니다.", map: "마시청" },
                    { time: "22:00", place: "Dragonfly (푸동)", memo: "첫날 피로는 숙소 근처 드래곤플라이에서 푸세요. 한국보다 저렴하고 수준 높은 오일 관리를 추천합니다.", map: "드래곤플라이" }
                ]
            },
            {
                date: "Day 2 올드 상해 & 몰입 체험", 
                items: [
                    { time: "11:00", place: "궁연 (Gongyan)", memo: "전통 공연과 식사가 결합된 이색 식당입니다. 아이에게 당나라 전통의상 체험을 강력 추천합니다.", map: "궁연" },
                    { time: "15:00", place: "임시정부 & 신천지", memo: "역사 관람 후 신천지 노천 카페에서 차 한 잔의 여유를 가지며 쉬어가는 것이 포인트입니다.", map: "신천지" },
                    { time: "18:00", place: "우캉루 (조계지)", memo: "상해에서 가장 예쁜 거리입니다. 우캉멘션 앞에서 가족 단체 사진을 남기세요.", map: "우캉멘션" },
                    { time: "20:00", place: "Green Massage", memo: "상해 프리미엄 마사지의 기준! 청결하고 조용한 분위기여서 아버지와 함께 발 마사지를 받기 좋습니다.", map: "그린마사지" }
                ]
            },
            {
                date: "Day 3 꿈의 나라 디즈니랜드", 
                items: [
                    { time: "08:30", place: "상해 디즈니랜드", memo: "아이를 위한 날! 주토피아를 우선 공략하시고, 아버지를 위해 중간중간 실내 공연으로 휴식을 병행하는 것이 핵심입니다.", map: "디즈니" }
                ]
            },
            {
                date: "Day 4 마지막 밤의 야경", 
                items: [
                    { time: "10:30", place: "상해 자연박물관", memo: "아이가 가장 좋아할 거대한 공룡 전시물이 가득한 곳입니다.", map: "자연박물관" },
                    { time: "13:30", place: "현저우이치엔", memo: "자동으로 구워져 연기 걱정 없이 아버지도 쾌적하게 양꼬치를 즐기실 수 있습니다.", map: "양꼬치" },
                    { time: "16:00", place: "티엔즈팡", memo: "전통 골목 사이에서 아기자기한 기념품을 쇼핑하며 타이궤이러(너무 비싸요!)를 외쳐보세요.", map: "티엔즈팡" },
                    { time: "18:30", place: "와이탄 야경", memo: "상해 여행의 정점! 화려한 루자쭈이 야경을 배경으로 최고의 단체 사진을 찍으세요.", map: "와이탄" },
                    { time: "20:30", place: "Oriental Aroma", memo: "가성비 끝판왕 동방화건강에서 전신 마사지를 받으며 여행의 피로를 완전히 날려버리세요.", map: "동방화건강" }
                ]
            }
        ];

        const placeTipsData = {
            "flight": "액체류 반입 주의 및 보조배터 기내 소지 필수.",
            "taxi": "짐이 많으므로 반드시 6인승 비즈니스 디디를 호출하세요.",
            "hotel": "동방명주 뷰 객실 요청을 추천합니다.",
            "ifc": "점보시푸드는 쿠폰 구매 시 비용 절감이 가능합니다.",
            "yuyuan": "아버지를 위한 정원이라는 스토리를 강조해주세요.",
            "yuyuan_shop": "선물용으로는 대백토 우유사탕이 가성비 좋습니다.",
            "circus": "퇴장 시 인파가 많으니 아이 손을 꼭 잡아주세요.",
            "gongyan": "예약 시간 1시간 전 도착하여 의상 대여를 추천합니다.",
            "history": "실내 사진 촬영 금지, 아이에게 역사의 중요성을 들려주세요.",
            "xintiandi": "노천 카페에서 여유를 부리기 가장 좋은 곳입니다.",
            "diandude": "하가우, 창펀 등 인기 딤섬을 꼭 드셔보세요.",
            "disney": "미개봉 간식 반입 가능, 앱 대기시간 수시 확인 필수.",
            "lilian": "당이 떨어질 때 에그타르트 하나면 일행 모두가 행복해집니다.",
            "yang": "고기가 자동으로 구워져 옷에 냄새가 배지 않습니다.",
            "tianzifang": "골목이 복잡하니 아이와 떨어지지 않게 주의하세요.",
            "home": "공항버스 승차 위치를 미리 확인하세요."
        };

        const phraseData = [
            {cat: "식당 (Order)", items: [
                {ko: "고수 빼주세요", zh: "不要香菜", py: "부야오 샹차이"},
                {ko: "안 맵게 해주세요", zh: "不要辣", py: "부야오 라"},
                {ko: "메뉴판 주세요", zh: "请给我菜单", py: "칭 게이워 차이딴"},
                {ko: "시원한 물 주세요", zh: "请给我冰水", py: "칭 게이워 삥쉐이"},
                {ko: "따뜻한 물 주세요", zh: "请给我热水", py: "칭 게이워 러쉐이"},
                {ko: "얼음 주세요", zh: "请给我冰块", py: "칭 게이워 삥콰이"},
                {ko: "시원한 맥주 한병 주세요", zh: "请给我一瓶冰啤酒", py: "칭 게이워 이핑 삥피지우"},
                {ko: "계산할게요", zh: "买单", py: "마이딴"}
            ]},
            {cat: "교통 (Move)", items: [
                {ko: "여기로 가주세요", zh: "请去这里", py: "칭 취 저리"},
                {ko: "트렁크 열어주세요", zh: "请开一下后备箱", py: "칭 카이 이샤 호우뻬이샹"}
            ]},
            {cat: "긴급/쇼핑 (Help)", items: [
                {ko: "화장실 어디에요?", zh: "洗手间在哪儿？", py: "시쇼우지엔 짜이 날?"},
                {ko: "너무 비싸요 깎아주세요", zh: "太贵了, 便宜点吧", py: "타이 궤이러, 피엔이 디엔빠"}
            ]}
        ];

        const initialChecklist = [
            { title: "여권 & 비자", memo: "만료일 확인 필수", type: "packing" },
            { title: "알리페이 & 카카오페이", memo: "카드 등록 및 결제 테스트", type: "packing" },
            { title: "중국 유심 또는 로밍", memo: "VPN 포함 여부 확인", type: "packing" },
            { title: "상해 디즈니 앱 설치", memo: "미리 회원가입 및 여권 등록", type: "packing" },
            { title: "보조배터리", memo: "위탁수하물 불가, 기내 소지 필수", type: "packing" },
            { title: "개인 비상약", memo: "감기약, 소화제, 지사제 등", type: "packing" }
        ];

        const initialShopping = [
            { title: "대백토 우유사탕 🐰", memo: "상해 전통 사탕 (선물용 추천)", type: "shopping" },
            { title: "칭즈 핸드크림", memo: "향기가 좋은 선물 아이템", type: "shopping" },
            { title: "릴리안 에그타르트", memo: "현지 필수 디저트", type: "shopping" },
            { title: "화시쯔(Florasis) 화장품", memo: "패키지가 예쁜 고급 화장품", type: "shopping" }
        ];

        // 🌟 Core Logic 🌟
        try {
            firebase.initializeApp({ databaseURL: "https://nhatrang-trip-default-rtdb.asia-southeast1.firebasedatabase.app" });
            db = firebase.database();
        } catch (e) { console.error("Firebase init error:", e); }

        function speak(text) { try { const u = new SpeechSynthesisUtterance(text); u.lang = 'zh-CN'; u.rate = 0.8; window.speechSynthesis.speak(u); } catch(e){} }
        
        async function fetchWeather() {
            try {
                const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=31.2222&longitude=121.4581&current_weather=true');
                const data = await res.json();
                const el = document.getElementById('weather-display');
                if(el) el.innerHTML = `<i class="fas fa-sun mr-1"></i>${Math.round(data.current_weather.temperature)}°C`;
            } catch(e) {}
        }

        let autoDarkChecked = false;
        function startClock() { 
            setInterval(() => { 
                const now = new Date(); 
                const kr = document.getElementById('time-kr');
                const sh = document.getElementById('time-sh');
                if(kr) kr.innerText = 'KOR ' + now.toLocaleTimeString('ko-KR', {timeZone:'Asia/Seoul', hour:'2-digit', minute:'2-digit', hour12:false}); 
                const shTime = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Shanghai"}));
                if(sh) sh.innerText = 'SHA ' + shTime.toLocaleTimeString('ko-KR', {hour:'2-digit', minute:'2-digit', hour12:false}); 
                
                if (!autoDarkChecked) {
                    const hour = shTime.getHours();
                    if (hour >= 19 || hour < 6) { document.documentElement.classList.add('dark'); updateThemeUI(); }
                    autoDarkChecked = true;
                }
            }, 1000); 
        }

        function updateThemeUI() { const icon = document.getElementById('theme-icon'); if(icon) icon.className = document.documentElement.classList.contains('dark') ? 'fas fa-sun text-yellow-400 text-xs' : 'fas fa-moon text-slate-500 text-xs'; }
        function toggleTheme() { document.documentElement.classList.toggle('dark'); updateThemeUI(); }

        function getSmartInfo(input) {
            if(!input) return {name: "", addr: ""};
            const query = input.toLowerCase().replace(/\s+/g, '');
            for (let key in smartMapDict) { if (query.includes(key)) return smartMapDict[key]; }
            return {name: input, addr: ""};
        }

        function openAmap(place) {
            const info = getSmartInfo(place); const keyword = encodeURIComponent(info.name); const ua = navigator.userAgent.toLowerCase();
            if (ua.indexOf("iphone") > -1) window.location.href = `iosamap://poi?sourceApplication=sh_trip&name=${keyword}`;
            else if (ua.indexOf("android") > -1) window.location.href = `androidamap://poi?sourceApplication=sh_trip&keywords=${keyword}`;
            else window.open(`https://uri.amap.com/search?keyword=${keyword}`, '_blank');
        }

        function openDidi(place) {
            const info = getSmartInfo(place); navigator.clipboard.writeText(info.name).catch(()=>{});
            const encN = encodeURIComponent(info.name), encA = encodeURIComponent(info.addr);
            const appU = `OneTravel://route/?end_name=${encN}&end_address=${encA}`;
            const fallbackU = `diditaxi://route/?end_name=${encN}&end_address=${encA}`;
            const alipayU = `alipays://platformapi/startapp?appId=20000067&page=pages/index/index&query=end_name%3D${encN}%26end_address%3D${encA}`;
            const start = Date.now(); window.location.href = appU;
            setTimeout(() => { if (Date.now() - start < 1500) { window.location.href = fallbackU; setTimeout(() => { if (Date.now() - start < 3000) window.location.href = alipayU; }, 1500); } }, 1000);
        }

        function scrollToCurrentTask() {
            try {
                const now = new Date();
                const shTime = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Shanghai"}));
                const todayStr = `${(shTime.getMonth() + 1).toString().padStart(2, '0')}-${shTime.getDate().toString().padStart(2, '0')}`;
                const curM = shTime.getHours() * 60 + shTime.getMinutes();
                let targetId = null; let minD = Infinity;
                itineraryData.forEach(item => {
                    if (item.date && item.date.includes(todayStr) && item.time) {
                        const timeArr = item.time.split('~');
                        if(timeArr.length > 0) {
                            const [h, m] = timeArr[0].split(':').map(Number);
                            if(!isNaN(h)) {
                                const diff = (h * 60 + m) - curM;
                                if (diff >= -60 && diff < minD) { minD = diff; targetId = `card-${item.key}`; }
                            }
                        }
                    }
                });
                if (targetId) {
                    const el = document.getElementById(targetId);
                    if (el) setTimeout(() => { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); el.parentElement.classList.add('ring-2', 'ring-brand-500', 'rounded-[2.5rem]', 'p-1'); }, 500);
                }
            } catch(e) {}
        }

        function renderList(list) {
            const groups = {};
            list.forEach(item => { 
                if(item.date) {
                    if(!groups[item.date]) groups[item.date] = []; 
                    groups[item.date].push(item); 
                }
            });
            const listEl = document.getElementById('itinerary-list');
            if(listEl) {
                listEl.innerHTML = Object.keys(groups).map(date => `
                    <div class="mb-8">
                        <h3 class="day-header text-[18px] font-black text-slate-800 dark:text-slate-200 mb-4 border-l-4 border-brand-500 pl-3">${date}</h3>
                        <div class="space-y-4">${groups[date].map(item => {
                            const placeStr = item.place || '';
                            return `
                            <div id="card-${item.key}" class="card-grad p-6 rounded-[2rem] border border-slate-200 dark:border-slate-800 shadow-[0_4px_20px_rgba(0,0,0,0.04)] active:scale-[0.98] transition-transform">
                                <div class="flex justify-between items-center mb-3"><span class="text-[11px] font-black bg-brand-500 text-white px-3 py-1.5 rounded-lg tracking-tighter shadow-md">${item.time || ''}</span><button onclick="openItineraryForm('${item.key}')" class="text-slate-300 hover:text-brand-500 transition-colors"><i class="fas fa-ellipsis-h text-lg"></i></button></div>
                                <h4 class="font-black text-xl mb-3 leading-tight tracking-tight">${placeStr}</h4>
                                ${item.memo ? `<p class="text-[13px] font-bold text-slate-600 dark:text-slate-400 mb-5 leading-relaxed whitespace-pre-wrap">${item.memo}</p>` : ''}
                                ${placeStr.includes('공항 이동') ? '' : `
                                <div class="flex gap-2 pt-1">
                                    <button onclick="openAmap('${placeStr}')" class="flex-1 py-3.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-2xl font-black text-xs shadow-sm border border-slate-200 dark:border-slate-700"><i class="fas fa-map-marker-alt mr-1 text-brand-500"></i>지도</button>
                                    <button onclick="openDidi('${placeStr}')" class="flex-1 py-3.5 bg-slate-900 text-white rounded-2xl font-black text-xs shadow-lg"><i class="fas fa-taxi mr-1 text-yellow-400"></i>디디호출</button>
                                    ${item.tipkey ? `<button onclick="openTipModal('${item.tipkey}')" class="w-14 py-3.5 bg-amber-50 text-amber-600 rounded-2xl font-black text-xs border border-amber-200"><i class="fas fa-star"></i></button>` : ''}
                                </div>`}
                            </div>`;
                        }).join('')}
                        </div>
                    </div>`).join('');
            }
        }

        function renderGuideItinerary() {
            const guideEl = document.getElementById('guide-itinerary-list');
            if(guideEl) {
                guideEl.innerHTML = guideItinerary.map(day => `
                    <div class="mb-10">
                        <div class="flex items-center mb-5"><div class="w-10 h-10 bg-indigo-600 text-white rounded-full flex items-center justify-center font-black mr-3 shadow-lg">D</div><h3 class="text-[16px] font-black text-slate-800 dark:text-slate-100">${day.date}</h3></div>
                        <div class="space-y-6 ml-5 border-l-2 border-indigo-100 dark:border-slate-800 pl-6 relative">
                            ${day.items.map(item => `
                                <div class="relative">
                                    <div class="absolute -left-[31px] top-1 w-3 h-3 bg-indigo-600 rounded-full border-2 border-white dark:border-slate-900"></div>
                                    <div class="bg-white dark:bg-slate-900 p-5 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm">
                                        <span class="text-[10px] font-black text-indigo-600 bg-indigo-50 dark:bg-indigo-900/30 px-2 py-1 rounded-md mb-2 inline-block">${item.time}</span>
                                        <h4 class="font-black text-lg mb-2">${item.place}</h4><p class="text-[13px] font-medium text-slate-600 dark:text-slate-400 leading-relaxed mb-4">${item.memo}</p>
                                        <button onclick="openAmap('${item.map}')" class="w-full py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-black text-xs transition-active active:scale-95 border border-slate-200 dark:border-slate-700"><i class="fas fa-map-marked-alt mr-2 text-indigo-500"></i>가이드 추천 위치 확인</button>
                                    </div>
                                </div>`).join('')}
                        </div>
                    </div>`).join('');
            }
        }

        function renderPhrases() { 
            const pEl = document.getElementById('phrase-list');
            if(pEl && typeof phraseData !== 'undefined') {
                pEl.innerHTML = phraseData.map(group => `
                    <div class="space-y-4">
                        <h4 class="text-[12px] font-black text-slate-400 uppercase tracking-widest pl-1 italic border-b pb-2 dark:border-slate-800">${group.cat}</h4>
                        ${group.items.map(p => `
                            <div class="bg-white dark:bg-slate-900 p-6 rounded-[2rem] shadow-sm border border-slate-100 dark:border-slate-800 flex justify-between items-center active:scale-[0.98] transition-transform" onclick="showFlashcard('${p.zh}', '${p.ko}', '${p.py}')">
                                <div class="pr-3">
                                    <p class="text-base font-black dark:text-white leading-tight">${p.ko}</p>
                                    <p class="text-[11px] text-brand-500 font-bold mt-2 uppercase">${p.py}</p>
                                </div>
                                <button onclick="event.stopPropagation(); speak('${p.zh}')" class="w-12 h-12 rounded-2xl bg-slate-50 dark:bg-slate-800 text-slate-400 flex items-center justify-center text-xl active:text-brand-500 shadow-inner border border-slate-100 dark:border-slate-700"><i class="fas fa-volume-up"></i></button>
                            </div>`).join('')}
                    </div>`).join(''); 
            }
        }

        function showTab(id) { document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active')); document.getElementById(id).classList.add('active'); document.querySelectorAll('.tab-btn').forEach(b => b.classList.replace('text-brand-500', 'text-slate-400')); event.currentTarget.classList.replace('text-slate-400', 'text-brand-500'); window.scrollTo(0,0); if(id === 'schedule') scrollToCurrentTask(); }
        function toggleItineraryType(type) { const isFm = type === 'family'; document.getElementById('btn-family').className = `flex-1 py-3 rounded-xl text-[13px] font-black transition-all ${isFm ? 'bg-white dark:bg-slate-700 shadow-sm text-brand-500' : 'text-slate-500'}`; document.getElementById('btn-guide').className = `flex-1 py-3 rounded-xl text-[13px] font-black transition-all ${!isFm ? 'bg-white dark:bg-slate-700 shadow-sm text-purple-600' : 'text-slate-500'}`; document.getElementById('family-itinerary').classList.toggle('hidden', !isFm); document.getElementById('guide-itinerary').classList.toggle('hidden', isFm); if(!isFm) renderGuideItinerary(); }
        function openTipModal(tipkey) { document.getElementById('tip-content').innerHTML = placeTipsData[tipkey] || "안전한 여행 되세요!"; document.getElementById('tip-modal').classList.remove('hidden'); }
        function closeTipModal() { document.getElementById('tip-modal').classList.add('hidden'); }
        function showFlashcard(zh, ko, py) { document.getElementById('flash-zh').innerText = zh; document.getElementById('flash-ko').innerText = ko; document.getElementById('flash-py').innerText = `[ ${py} ]`; document.getElementById('flashcard').classList.remove('hidden'); }

        function addExpense() { const d = document.getElementById('exp-desc').value, a = document.getElementById('exp-amt').value; if(d && a && db) { db.ref(`${basePath}/expenses`).push({desc: d, amt: Number(a), krwAmt: Math.round(Number(a) * exchangeRate)}); document.getElementById('exp-desc').value = ''; document.getElementById('exp-amt').value = ''; } }
        function loadExpenses() { if(db) db.ref(`${basePath}/expenses`).on('value', s => { const data = s.val() || {}; let tC = 0, tK = 0; document.getElementById('expense-list').innerHTML = Object.entries(data).map(([k, v]) => { tC += v.amt; const kAmt = v.krwAmt || Math.round(v.amt * exchangeRate); tK += kAmt; return `<div class="flex justify-between items-center bg-white dark:bg-slate-800 p-4 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs mb-2 shadow-sm"><div class="flex flex-col"><span class="font-bold">${v.desc}</span><span class="text-[10px] text-slate-400">${kAmt.toLocaleString()} ₩</span></div><span class="font-black text-brand-500 text-sm">${v.amt.toLocaleString()} ¥ <button onclick="db.ref('${basePath}/expenses/${k}').remove()" class="ml-2 text-slate-300">✕</button></span></div>`; }).join(''); document.getElementById('total-expense').innerHTML = `${tC.toLocaleString()} ¥ <span class="text-xs font-bold text-slate-400 ml-1">(${tK.toLocaleString()} ₩)</span>`; }); }

        function loadChecklist() {
            if(!db) return;
            db.ref(`${basePath}/checklist`).on('value', s => {
                const data = s.val() || {}; const items = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                if(items.length === 0) { [...initialChecklist, ...initialShopping].forEach(i => db.ref(`${basePath}/checklist`).push(i)); return; }
                const packEl = document.getElementById('packing-list'), shopEl = document.getElementById('shopping-list');
                if(packEl) packEl.innerHTML = items.filter(i => i.type === 'packing').map(i => `<div class="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 mb-2"><div onclick="openChecklistModal('packing', '${i.key}')" class="flex-1"><p class="font-bold text-sm">${i.title}</p>${i.memo ? `<p class="text-[10px] text-slate-400">${i.memo}</p>` : ''}</div><input type="checkbox" ${i.checked ? 'checked' : ''} onchange="db.ref('${basePath}/checklist/${i.key}').update({checked: this.checked})" class="w-5 h-5 accent-brand-500"></div>`).join('');
                if(shopEl) shopEl.innerHTML = items.filter(i => i.type === 'shopping').map(i => `<div class="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-2xl border border-slate-100 dark:border-slate-700 mb-2"><div onclick="openChecklistModal('shopping', '${i.key}')" class="flex-1"><p class="font-black text-sm">${i.title}</p>${i.memo ? `<p class="text-[11px] text-slate-500 mt-1">${i.memo}</p>` : ''}</div><input type="checkbox" ${i.checked ? 'checked' : ''} onchange="db.ref('${basePath}/checklist/${i.key}').update({checked: this.checked})" class="w-5 h-5 accent-purple-500"></div>`).join('');
            });
        }

        function openChecklistModal(type, key = null) {
            document.getElementById('checklist-type').value = type; document.getElementById('checklist-key').value = key || '';
            document.getElementById('checklist-modal').classList.remove('hidden');
            if(key) { db.ref(`${basePath}/checklist/${key}`).once('value', s => { const d = s.val(); document.getElementById('checklist-title').value = d.title; document.getElementById('checklist-memo').value = d.memo || ''; document.getElementById('checklist-delete-btn').classList.remove('hidden'); }); }
            else { document.getElementById('checklist-title').value = ''; document.getElementById('checklist-memo').value = ''; document.getElementById('checklist-delete-btn').classList.add('hidden'); }
        }
        function closeChecklistModal() { document.getElementById('checklist-modal').classList.add('hidden'); }
        function saveChecklist() { const k = document.getElementById('checklist-key').value, t = document.getElementById('checklist-type').value, title = document.getElementById('checklist-title').value, memo = document.getElementById('checklist-memo').value; if(!title) return; if(k) db.ref(`${basePath}/checklist/${k}`).update({title, memo}); else db.ref(`${basePath}/checklist`).push({title, memo, type: t, checked: false}); closeChecklistModal(); }
        function deleteChecklist() { const k = document.getElementById('checklist-key').value; if(k && confirm("삭제하시겠습니까?")) { db.ref(`${basePath}/checklist/${k}`).remove(); closeChecklistModal(); } }

        function openItineraryForm(key = null) {
            document.getElementById('itinerary-modal').classList.remove('hidden');
            if(key) { const item = itineraryData.find(i => i.key === key); if(item) { document.getElementById('edit-key').value = key; document.getElementById('form-date').value = item.date; document.getElementById('form-time').value = item.time; document.getElementById('form-place').value = item.place; document.getElementById('form-memo').value = item.memo || ""; document.getElementById('delete-btn').classList.remove('hidden'); } }
            else { document.getElementById('edit-key').value = ''; document.getElementById('itinerary-modal').querySelectorAll('input, textarea').forEach(i => i.value = ''); document.getElementById('delete-btn').classList.add('hidden'); }
        }
        function closeItineraryModal() { document.getElementById('itinerary-modal').classList.add('hidden'); }
        function saveItinerary() { const k = document.getElementById('edit-key').value, d = { date: document.getElementById('form-date').value, time: document.getElementById('form-time').value || "00:00", place: document.getElementById('form-place').value || "장소명", memo: document.getElementById('form-memo').value || "" }; if(k) db.ref(`${basePath}/itinerary/${k}`).update(d); else db.ref(`${basePath}/itinerary`).push(d); closeItineraryModal(); }
        function deleteItinerary() { const k = document.getElementById('edit-key').value; if(k && confirm("삭제할까요?")) { db.ref(`${basePath}/itinerary/${k}`).remove(); closeItineraryModal(); } }

        function loadItinerary() {
            renderList(initialShanghai);
            if (db) {
                db.ref(`${basePath}/itinerary`).on('value', s => {
                    const data = s.val(); 
                    if(data) { 
                        itineraryData = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                        itineraryData.sort((a, b) => {
                            const dateA = a.date ? a.date.replace(/[^0-9]/g, "") : "";
                            const dateB = b.date ? b.date.replace(/[^0-9]/g, "") : "";
                            const timeA = a.time || "";
                            const timeB = b.time || "";
                            return dateA.localeCompare(dateB) || timeA.localeCompare(timeB);
                        });
                        renderList(itineraryData); scrollToCurrentTask();
                    } else initialShanghai.forEach(i => db.ref(`${basePath}/itinerary`).push(i));
                });
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            const cny = document.getElementById('cny-input'), krw = document.getElementById('krw-input');
            if(cny && krw) {
                cny.addEventListener('input', (e) => krw.value = e.target.value ? Math.round(e.target.value * exchangeRate) : '');
                krw.addEventListener('input', (e) => cny.value = e.target.value ? (e.target.value / exchangeRate).toFixed(2) : '');
            }
            startClock(); fetchWeather(); renderPhrases(); loadItinerary(); loadExpenses(); loadChecklist();
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('sw.js').then(reg => {
                    reg.onupdatefound = () => {
                        const installingWorker = reg.installing;
                        installingWorker.onstatechange = () => {
                            if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                window.location.reload();
                            }
                        };
                    };
                }).catch(()=>{});
            }
        });
    