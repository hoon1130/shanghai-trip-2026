
        const basePath = 'shanghai_2026_v30_final'; const exchangeRate = 215.94;
        let db = null, itineraryData = [], spotData = [], currentSpotCat = '전체';

        const initialSpots = [
            {cat: "핵심", nameKo: "푸동 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "浦东国际机场(Pudong Guoji Jichang) 푸동공항역 | 2호선/자기부상", lat: 31.144, lng: 121.808},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "龙阳路(Longyang Lu) 롱양루역 | 2/7/16/18호선", lat: 31.203, lng: 121.558},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 2/14호선", lat: 31.239, lng: 121.501},
            {cat: "핵심", nameKo: "숙소 (IFC Residence)", nameZh: "上海国金汇", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 6번출구 도보 3분", lat: 31.236, lng: 121.502},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 1분", lat: 31.238, lng: 121.484},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "七宝(Qi Bao) 치바오역 | 2번출구 도보 5분", lat: 31.155, lng: 121.352},
            {cat: "명소", nameKo: "정안사", nameZh: "静安寺", addr: "", subway: "静安寺(Jing An Si) 정안사역 | 1번출구 도보 2분", lat: 31.224, lng: 121.447},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "", subway: "南京西路(Nanjing Xi Lu) 남경서로역 | 2/12/13호선", lat: 31.230, lng: 121.460},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "", subway: "시외지역 | 전용차량 권장", lat: 30.751, lng: 120.485},
            {cat: "명소", nameKo: "주가각", nameZh: "朱家角", addr: "", subway: "朱家角(Zhu Jia Jiao) 주가각역 | 도보 15분", lat: 31.111, lng: 121.053},
            {cat: "명소", nameKo: "루쉰공원", nameZh: "鲁迅公园", addr: "", subway: "虹口足球场(Hongkou Zuqiu Chang) 홍구축구장역 | 도보 5분", lat: 31.272, lng: 121.481},
            {cat: "명소", nameKo: "우캉멘션", nameZh: "武康大楼", addr: "", subway: "交通大学(Jiao Tong Da Xue) 교통대학역 | 도보 5분", lat: 31.203, lng: 121.434},
            {cat: "명소", nameKo: "티엔즈팡", nameZh: "田子坊", addr: "", subway: "打浦桥(Da Pu Qiao) 타포교역 | 도보 1분", lat: 31.209, lng: 121.468},
            {cat: "명소", nameKo: "신천지", nameZh: "上海新天地", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 6번출구 도보 2분", lat: 31.221, lng: 121.475},
            {cat: "명소", nameKo: "예원/예원상성", nameZh: "豫园商城", addr: "", subway: "豫园(Yu Yuan) 예원역 | 10/14호선 1번출구 도보 5분", lat: 31.227, lng: 121.492},
            {cat: "명소", nameKo: "디즈니랜드", nameZh: "上海迪士尼度假区", addr: "", subway: "迪士尼(Di Shi Ni) 디즈니역 | 도보 5분", lat: 31.141, lng: 121.662},
            {cat: "명소", nameKo: "인민광장", nameZh: "人民广场", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 1/2/8호선", lat: 31.232, lng: 121.475},
            {cat: "명소", nameKo: "임시정부 유적지", nameZh: "大韩민국临时政府旧址", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 6번출구 도보 3분", lat: 31.218, lng: 121.475},
            {cat: "맛집", nameKo: "점도덕", nameZh: "点都德(新天地店)", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 2번출구 도보 5분", lat: 31.216, lng: 121.479},
            {cat: "맛집", nameKo: "양꼬치", nameZh: "很久以前羊肉串(南京东路)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 3분", lat: 31.235, lng: 121.484},
            {cat: "맛집", nameKo: "하이디라오", nameZh: "海底捞(人民广场店)", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 19번출구 도보 2분", lat: 31.234, lng: 121.478},
            {cat: "쇼핑/기타", nameKo: "릴리안 베이커리", nameZh: "莉莲蛋挞(南京东路)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 1분", lat: 31.237, lng: 121.486}
        ];

        const phraseData = [{cat: "식당 (Order)", items: [{ko: "고수 빼주세요", zh: "不要香菜", py: "부야오 샹차이"},{ko: "안 맵게 해주세요", zh: "不要辣", py: "부야오 라"}]}];
        const placeTipsData = {"flight": "✈️ **항공**\n- 보조배터리 기내 소지 필수."};

        function speak(text) { try { const u = new SpeechSynthesisUtterance(text); u.lang = 'zh-CN'; u.rate = 0.8; window.speechSynthesis.speak(u); } catch(e){} }
        
        async function fetchWeather() {
            try {
                const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=31.2222&longitude=121.4581&current_weather=true');
                const data = await res.json(), cw = data.current_weather, temp = Math.round(cw.temperature), code = cw.weathercode;
                let icon = 'fa-sun', desc = '맑음';
                if (code >= 1 && code <= 3) desc = '구름'; else if (code >= 45 && code <= 48) desc = '안개';
                else if (code >= 51 && code <= 67) { icon = 'fa-cloud-showers-heavy'; desc = '비'; }
                else if (code >= 71 && code <= 77) desc = '눈'; else if (code >= 80 && code <= 82) desc = '소나기';
                else if (code >= 95) desc = '뇌우';
                document.getElementById('weather-display').innerHTML = `<i class="fas ${icon} mr-2 text-indigo-500"></i>상해 ${temp}°C / ${desc}`;
            } catch(e) {}
        }

        function toggleTheme() { document.documentElement.classList.toggle('dark'); const icon = document.getElementById('theme-icon'); if(icon) icon.className = document.documentElement.classList.contains('dark') ? 'fas fa-sun text-yellow-400 text-sm' : 'fas fa-moon text-slate-500 text-sm'; }

        async function translateAction() {
            const input = document.getElementById('trans-input').value.trim(), resultBox = document.getElementById('trans-result-box'), resultText = document.getElementById('trans-result-text'), speakBtn = document.getElementById('trans-speak-btn'), btnIcon = document.getElementById('trans-btn-icon');
            if (!input) return alert('문장을 입력해주세요.');
            btnIcon.className = 'fas fa-spinner fa-spin'; resultBox.classList.remove('hidden'); resultText.innerText = '...';
            try {
                const isKorean = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(input), target = isKorean ? 'zh-CN' : 'ko';
                const res = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${target}&dt=t&q=${encodeURIComponent(input)}`);
                const data = await res.json(), translated = data[0].map(item => item[0]).join('');
                resultText.innerText = translated; btnIcon.className = 'fas fa-paper-plane';
                if (target === 'zh-CN') { speakBtn.classList.remove('hidden'); speakBtn.onclick = () => speak(translated); } else speakBtn.classList.add('hidden');
            } catch (e) { resultText.innerText = 'Error'; btnIcon.className = 'fas fa-paper-plane'; }
        }

        function getDistance(lat1, lon1, lat2, lon2) {
            if (!lat1 || !lon1 || !lat2 || !lon2) return Infinity;
            const R = 6371; const dLat = (lat2-lat1)*Math.PI/180, dLon = (lon2-lon1)*Math.PI/180;
            const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        }

        async function filterSpots(cat) { 
            currentSpotCat = cat; document.querySelectorAll('.category-chip').forEach(btn => btn.classList.toggle('active', btn.dataset.cat === cat));
            if (cat === '내 주변') {
                navigator.geolocation.getCurrentPosition(pos => {
                    const { latitude, longitude } = pos.coords; spotData.forEach(s => { s.dist = getDistance(latitude, longitude, s.lat, s.lng); });
                    spotData.sort((a, b) => a.dist - b.dist); renderSpots();
                }, () => { alert('GPS 필수'); renderSpots(); });
            } else renderSpots();
        }

        function renderSpots() {
            const search = document.getElementById('spot-search').value.toLowerCase();
            const listEl = document.getElementById('spot-list');
            if(listEl) {
                listEl.innerHTML = spotData.filter(s => (currentSpotCat === '전체' || s.cat === currentSpotCat || currentSpotCat === '내 주변') && (s.nameKo.toLowerCase().includes(search) || s.nameZh.toLowerCase().includes(search))).map(s => {
                    const searchKey = (s.subway.match(/\(([^)]+)\)/) || ['', ''])[1];
                    return `<div class="bg-white dark:bg-slate-900 p-5 rounded-[2rem] border border-slate-200 dark:border-slate-800 shadow-sm">
                        <div class="flex justify-between items-start mb-2">
                            <div><span class="text-[10px] font-black text-indigo-500 bg-indigo-50 px-2 py-1 rounded-md mb-2 inline-block">${s.cat}</span>
                            <h4 class="font-black text-lg">${s.nameKo}${s.dist && s.dist < 500 ? `<span class="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-1 rounded-md ml-2">${s.dist<1?Math.round(s.dist*1000)+'m':s.dist.toFixed(1)+'km'}</span>`:''}</h4>
                            <p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p>
                            ${s.subway ? `<div onclick="openMetro('${searchKey}')" class="text-[12px] font-black text-indigo-600 mt-3 flex items-start bg-indigo-50 dark:bg-indigo-900/30 px-3 py-2 rounded-xl border border-indigo-100 cursor-pointer"><i class="fas fa-subway mt-0.5 mr-2"></i><span class="flex-1 underline">${s.subway}</span></div>`:''}</div>
                            <button onclick="openSpotModal('${s.key}')" class="text-slate-300 p-2"><i class="fas fa-edit text-sm"></i></button>
                        </div>
                        <div class="flex gap-2 mt-4"><button onclick="openAmap('${s.nameZh}')" class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 rounded-xl font-black text-[10px]">고덕지도</button><button onclick="openBaiduMap('${s.nameZh}')" class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 rounded-xl font-black text-[10px]">바이두</button></div>
                    </div>`;
                }).join('') || '<div class="text-center py-10 font-bold">결과 없음</div>';
            }
        }

        function openMetro(keyword) {
            if(keyword) { const el = document.createElement('textarea'); el.value = keyword; document.body.appendChild(el); el.select(); document.execCommand('copy'); document.body.removeChild(el); }
            window.open('https://metro.nuua.travel/ko/shanghai', '_blank');
        }

        function openSOSModal() { document.getElementById('sos-modal').classList.remove('hidden'); }
        function closeSOSModal() { document.getElementById('sos-modal').classList.add('hidden'); }
        function showHotelCard() { document.getElementById('hotel-card').classList.remove('hidden'); closeSOSModal(); }
        function showHelpPhrase(ko, zh, py) { if(typeof showFlashcard === 'function') showFlashcard(zh, ko, py); closeSOSModal(); }

        function openSpotModal(key = null) {
            document.getElementById('spot-key').value = key || ''; document.getElementById('spot-modal').classList.remove('hidden');
            if(key) { const s = spotData.find(i => i.key === key); if(s) { document.getElementById('spot-cat').value = s.cat; document.getElementById('spot-name-ko').value = s.nameKo; document.getElementById('spot-name-zh').value = s.nameZh; document.getElementById('spot-subway').value = s.subway || ''; document.getElementById('spot-addr').value = s.addr || ''; } }
            else { document.getElementById('spot-modal').querySelectorAll('input').forEach(i => i.value = ''); }
        }
        function closeSpotModal() { document.getElementById('spot-modal').classList.add('hidden'); }
        function saveSpot() {
            const k = document.getElementById('spot-key').value, d = { cat: document.getElementById('spot-cat').value, nameKo: document.getElementById('spot-name-ko').value, nameZh: document.getElementById('spot-name-zh').value, subway: document.getElementById('spot-subway').value, addr: document.getElementById('spot-addr').value };
            if(!d.nameKo || !d.nameZh) return alert('명칭 필수');
            if(k) db.ref(`${basePath}/spots/${k}`).update(d); else db.ref(`${basePath}/spots`).push(d);
            closeSpotModal();
        }
        function deleteSpot() { const k = document.getElementById('spot-key').value; if(k && confirm("삭제?")) { db.ref(`${basePath}/spots/${k}`).remove(); closeSpotModal(); } }

        function addCNY(amt) { const el = document.getElementById('cny-input'), krwEl = document.getElementById('krw-input'); const cur = parseFloat(el.value) || 0; el.value = cur + amt; krwEl.value = Math.round(el.value * exchangeRate); }
        function clearCNY() { document.getElementById('cny-input').value = ''; document.getElementById('krw-input').value = ''; }

        function addExpense() { const c = document.getElementById('exp-cat').value, d = document.getElementById('exp-desc').value, a = document.getElementById('exp-amt').value; if(d && a && db) { db.ref(`${basePath}/expenses`).push({cat: c, desc: d, amt: Number(a), krwAmt: Math.round(Number(a) * exchangeRate)}); document.getElementById('exp-desc').value = ''; document.getElementById('exp-amt').value = ''; } }
        function loadExpenses() {
            if(!db) return;
            db.ref(`${basePath}/expenses`).on('value', s => {
                const data = s.val() || {}; let tC = 0, tK = 0; const cats = {'식비':0,'교통':0,'쇼핑':0,'기타':0};
                const listHtml = Object.entries(data).map(([k, v]) => {
                    tC += v.amt; const kAmt = v.krwAmt || Math.round(v.amt * exchangeRate); tK += kAmt;
                    const cName = v.cat ? v.cat.replace(/[🍔🚕🛍️✨ ]/g, '') : '기타';
                    if(cats[cName]!==undefined) cats[cName]+=v.amt; else cats['기타']+=v.amt;
                    return `<div class="flex justify-between items-center bg-white dark:bg-slate-800 p-4 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs mb-2 shadow-sm"><div class="flex flex-col"><span class="font-bold">${v.desc}</span><span class="text-[10px] text-slate-400">${kAmt.toLocaleString()} ₩</span></div><span class="font-black text-indigo-500 text-sm">${v.amt.toLocaleString()} ¥ <button onclick="db.ref('${basePath}/expenses/${k}').remove()" class="ml-3">&times;</button></span></div>`;
                }).join('');
                document.getElementById('expense-list').innerHTML = listHtml; document.getElementById('total-expense').innerHTML = `${tC.toLocaleString()} ¥ <span class="text-xs font-bold text-slate-400 ml-1">(${tK.toLocaleString()} ₩)</span>`;
                const sumBar = document.getElementById('expense-summary'), legBar = document.getElementById('expense-legend');
                if (tC > 0 && sumBar && legBar) {
                    let barHtml = '', legendHtml = '';
                    const colors = {'식비':'bg-orange-400','교통':'bg-blue-400','쇼핑':'bg-purple-400','기타':'bg-slate-400'};
                    for (const [c, amt] of Object.entries(cats)) { if(amt>0) { const pct = (amt/tC*100).toFixed(1); barHtml += `<div class="h-full ${colors[c]}" style="width: ${pct}%"></div>`; legendHtml += `<div class="flex items-center mr-3"><span class="w-2 h-2 rounded-full ${colors[c]} mr-1"></span>${c} ${pct}%</div>`; } }
                    sumBar.innerHTML = barHtml; sumBar.classList.remove('hidden'); legBar.innerHTML = legendHtml; legBar.classList.remove('hidden');
                } else if(sumBar) { sumBar.classList.add('hidden'); legBar.classList.add('hidden'); }
            });
        }

        function loadChecklist() {
            if(!db) return;
            db.ref(`${basePath}/checklist`).on('value', s => {
                const data = s.val() || {}; const items = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                const packEl = document.getElementById('packing-list');
                if(packEl) packEl.innerHTML = items.filter(i => i.type === 'packing').map(i => `<div class="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-800 mb-2"><div onclick="openChecklistModal('packing', '${i.key}')" class="flex-1"><p class="font-bold text-sm">${i.title}</p></div><input type="checkbox" ${i.checked ? 'checked' : ''} onchange="db.ref('${basePath}/checklist/${i.key}').update({checked: this.checked})" class="w-5 h-5 accent-indigo-500"></div>`).join('');
                const pItems = items.filter(i => i.type === 'packing'), pBar = document.getElementById('packing-progress');
                if(pBar && pItems.length > 0) pBar.style.width = `${(pItems.filter(i => i.checked).length / pItems.length) * 100}%`;
            });
        }

        function loadSpots() {
            if(!db) return;
            db.ref(`${basePath}/spots`).on('value', s => {
                const data = s.val();
                if(data) {
                    spotData = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                    initialSpots.forEach(init => {
                        const existing = spotData.find(item => item.nameZh === init.nameZh || item.nameKo === init.nameKo);
                        if (!existing) db.ref(`${basePath}/spots`).push(init);
                        else if (existing.subway !== init.subway) db.ref(`${basePath}/spots/${existing.key}`).update({ subway: init.subway, lat: init.lat, lng: init.lng });
                    });
                } else initialSpots.forEach(i => db.ref(`${basePath}/spots`).push(i));
                renderSpots();
            });
        }

        function loadItinerary() { if(db) db.ref(`${basePath}/itinerary`).on('value', s => { const data = s.val(); if(data) { itineraryData = Object.entries(data).map(([k, v]) => ({...v, key: k})); itineraryData.sort((a,b) => String(a.date).localeCompare(String(b.date)) || String(a.time).localeCompare(String(b.time))); renderList(itineraryData); } }); }

        function showTab(id) { 
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active')); 
            document.getElementById(id).classList.add('active'); 
            document.querySelectorAll('.tab-btn').forEach(b => { b.classList.remove('text-brand-500'); b.classList.add('text-slate-400'); });
            const targetBtn = document.getElementById('nav-' + id);
            if(targetBtn) { targetBtn.classList.remove('text-slate-400'); targetBtn.classList.add('text-brand-500'); }
            window.scrollTo(0,0); if(id === 'spot') renderSpots(); 
        }

        function toggleItineraryType(type) { 
            const isFm = type === 'family'; 
            document.getElementById('btn-family').className = `flex-1 py-3 rounded-xl text-[13px] font-black transition-all ${isFm ? 'bg-white dark:bg-slate-700 shadow-sm text-brand-500' : 'text-slate-500'}`; 
            document.getElementById('btn-guide').className = `flex-1 py-3 rounded-xl text-[13px] font-black transition-all ${!isFm ? 'bg-white dark:bg-slate-700 shadow-sm text-brand-500' : 'text-slate-500'}`; 
            document.getElementById('family-itinerary').classList.toggle('hidden', !isFm); 
            document.getElementById('guide-itinerary').classList.toggle('hidden', isFm); 
        }

        function getSmartInfo(input) {
            if(!input) return {name: "", addr: ""};
            let destination = input;
            const arrowMatch = input.match(/(?:->|→)\s*([^(\n]+)/);
            if (arrowMatch) destination = arrowMatch[1].trim();
            for (let key in smartMapDict) { if (destination.toLowerCase().includes(key)) return smartMapDict[key]; }
            return {name: destination, addr: ""};
        }

        function openAmap(place) {
            const info = getSmartInfo(place); navigator.clipboard.writeText(info.name).catch(()=>{});
            window.open(`https://uri.amap.com/search?keyword=${encodeURIComponent(info.name)}`, '_blank');
        }

        function openBaiduMap(place) {
            const info = getSmartInfo(place); navigator.clipboard.writeText(info.name).catch(()=>{});
            window.open(`https://map.baidu.com/mobile/webapp/search/search/qt=s&wd=${encodeURIComponent(info.name)}`, '_blank');
        }

        function openDidi(place) {
            const info = getSmartInfo(place); navigator.clipboard.writeText(info.name).catch(()=>{});
            window.location.href = `alipays://platformapi/startapp?appId=20000067&page=pages/index/index&query=end_name%3D${encodeURIComponent(info.name)}%26end_address%3D${encodeURIComponent(info.addr)}`;
        }

        document.addEventListener('DOMContentLoaded', () => {
            const firebaseConfig = { databaseURL: "https://nhatrang-trip-default-rtdb.asia-southeast1.firebasedatabase.app" };
            if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
            db = firebase.database();
            const cny = document.getElementById('cny-input'), krw = document.getElementById('krw-input');
            if(cny && krw) {
                cny.addEventListener('input', (e) => krw.value = e.target.value ? Math.round(e.target.value * exchangeRate) : '');
                krw.addEventListener('input', (e) => cny.value = e.target.value ? (e.target.value / exchangeRate).toFixed(2) : '');
            }
            fetchWeather(); renderPhrases(); loadItinerary(); loadExpenses(); loadChecklist(); loadSpots();
        });
    