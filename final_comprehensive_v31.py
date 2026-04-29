import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def deep_clean_js():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Rebuild the core functions block completely
    # We'll replace from 'function speak' to 'document.addEventListener'
    
    start_marker = 'function speak(text)'
    end_marker = "document.addEventListener('DOMContentLoaded'"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        clean_js_block = """function speak(text) { try { const u = new SpeechSynthesisUtterance(text); u.lang = 'zh-CN'; u.rate = 0.8; window.speechSynthesis.speak(u); } catch(e){} }
        
        async function fetchWeather() {
            try {
                const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=31.2222&longitude=121.4581&current_weather=true');
                const data = await res.json();
                const cw = data.current_weather;
                const temp = Math.round(cw.temperature);
                const code = cw.weathercode;
                let icon = 'fa-sun'; let desc = '맑음';
                if (code >= 1 && code <= 3) { icon = 'fa-cloud-sun'; desc = '구름'; }
                else if (code >= 45 && code <= 48) { icon = 'fa-smog'; desc = '안개'; }
                else if (code >= 51 && code <= 67) { icon = 'fa-cloud-showers-heavy'; desc = '비'; }
                else if (code >= 71 && code <= 77) { icon = 'fa-snowflake'; desc = '눈'; }
                else if (code >= 80 && code <= 82) { icon = 'fa-cloud-rain'; desc = '소나기'; }
                else if (code >= 95) { icon = 'fa-bolt'; desc = '뇌우'; }
                const el = document.getElementById('weather-display');
                if(el) el.innerHTML = `<i class="fas ${icon} mr-2 text-indigo-500"></i>상해 ${temp}°C / ${desc}`;
            } catch(e) {
                const el = document.getElementById('weather-display');
                if(el) el.innerText = '날씨 확인 중...';
            }
        }

        function toggleTheme() { document.documentElement.classList.toggle('dark'); const icon = document.getElementById('theme-icon'); if(icon) icon.className = document.documentElement.classList.contains('dark') ? 'fas fa-sun text-yellow-400 text-sm' : 'fas fa-moon text-slate-500 text-sm'; }

        function getSmartInfo(input) {
            if(!input) return {name: "", addr: ""};
            let destination = input;
            const arrowMatch = input.match(/(?:->|→)\\s*([^(\\n]+)/);
            if (arrowMatch) destination = arrowMatch[1].trim();
            else if (input.includes("->")) { const parts = input.split("->"); destination = parts[parts.length - 1].trim(); }
            const query = destination.toLowerCase().replace(/\\s+/g, '');
            for (let key in smartMapDict) { if (query.includes(key)) return smartMapDict[key]; }
            return {name: destination, addr: ""};
        }

        function openAmap(place) {
            const info = getSmartInfo(place); navigator.clipboard.writeText(info.name).catch(()=>{});
            if (info.addr && info.addr.startsWith('http')) {
                const link = document.createElement('a'); link.href = info.addr; link.target = '_blank'; link.rel = 'noopener noreferrer';
                document.body.appendChild(link); link.click(); document.body.removeChild(link);
                return;
            }
            const keyword = encodeURIComponent(info.name); const ua = navigator.userAgent.toLowerCase();
            if (ua.indexOf("iphone") > -1) window.location.href = `iosamap://poi?sourceApplication=sh_trip&name=${keyword}`;
            else if (ua.indexOf("android") > -1) window.location.href = `androidamap://poi?sourceApplication=sh_trip&keywords=${keyword}`;
            else window.open(`https://uri.amap.com/search?keyword=${keyword}`, '_blank');
        }

        function openBaiduMap(place) {
            const info = getSmartInfo(place); navigator.clipboard.writeText(info.name).catch(()=>{});
            const keyword = encodeURIComponent(info.name);
            const webUrl = `https://map.baidu.com/mobile/webapp/search/search/qt=s&wd=${keyword}`;
            const link = document.createElement('a'); link.href = webUrl; link.target = '_blank'; link.rel = 'noopener noreferrer';
            document.body.appendChild(link); link.click(); document.body.removeChild(link);
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

        function showTab(id) { 
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active')); 
            document.getElementById(id).classList.add('active'); 
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.replace('text-brand-500', 'text-slate-400')); 
            const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(id));
            if(targetBtn) targetBtn.classList.replace('text-slate-400', 'text-brand-500');
            window.scrollTo(0,0); 
            if(id === 'schedule') scrollToCurrentTask(); 
            if(id === 'spot') renderSpots(); 
        }

        function toggleItineraryType(type) { 
            const isFm = type === 'family'; 
            document.getElementById('btn-family').className = `flex-1 py-3 rounded-xl text-[13px] font-black transition-all ${isFm ? 'bg-white dark:bg-slate-700 shadow-sm text-brand-500' : 'text-slate-500'}`; 
            document.getElementById('btn-guide').className = `flex-1 py-3 rounded-xl text-[13px] font-black transition-all ${!isFm ? 'bg-white dark:bg-slate-700 shadow-sm text-brand-500' : 'text-slate-500'}`; 
            document.getElementById('family-itinerary').classList.toggle('hidden', !isFm); 
            document.getElementById('guide-itinerary').classList.toggle('hidden', isFm); 
            if(!isFm) renderGuideItinerary(); 
        }

        function renderList(list) {
            const groups = {};
            list.forEach(item => { if(item.date) { if(!groups[item.date]) groups[item.date] = []; groups[item.date].push(item); } });
            const listEl = document.getElementById('itinerary-list');
            if(listEl) {
                listEl.innerHTML = Object.keys(groups).map(date => `
                    <div class="mb-8">
                        <h3 class="day-header text-[18px] font-black text-indigo-600 mb-4 border-l-4 border-indigo-500 pl-3">${date}</h3>
                        <div class="space-y-4">${groups[date].map(item => {
                            const placeStr = item.place || '';
                            const hideKeywords = ["기상", "조식", "정비", "자유 일정", "체크아웃", "인천공항", "집으로", "인천 공항", "공항 이동"];
                            const shouldHide = hideKeywords.some(k => placeStr.includes(k));
                            return `
                            <div id="card-${item.key}" class="card-grad p-6 rounded-[2rem] border border-slate-200 dark:border-slate-800 shadow-sm">
                                <div class="flex justify-between items-center mb-3"><span class="text-[11px] font-black bg-indigo-500 text-white px-3 py-1.5 rounded-lg shadow-md">${item.time || ''}</span><button onclick="openItineraryForm('${item.key}')" class="text-slate-300 hover:text-indigo-500"><i class="fas fa-ellipsis-h text-lg"></i></button></div>
                                <h4 class="font-black text-xl mb-3 leading-tight">${placeStr}</h4>
                                ${item.memo ? `<p class="text-[13px] font-bold text-slate-600 dark:text-slate-400 mb-5 leading-relaxed whitespace-pre-wrap">${item.memo}</p>` : ''}
                                ${shouldHide ? '' : `
                                <div class="flex gap-2 pt-1">
                                    <button onclick="openAmap('${placeStr}')" class="flex-1 py-3.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-2xl font-black text-[10px] shadow-sm border border-slate-200 dark:border-slate-700">지도1</button>
                                    <button onclick="openBaiduMap('${placeStr}')" class="flex-1 py-3.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-2xl font-black text-[10px] shadow-sm border border-slate-200 dark:border-slate-700">지도2</button>
                                    <button onclick="openDidi('${placeStr}')" class="flex-1 py-3.5 bg-slate-900 text-white rounded-2xl font-black text-[10px] shadow-lg">디디호출</button>
                                    ${item.tipkey ? `<button onclick="openTipModal('${item.tipkey}')" class="w-12 py-3.5 bg-amber-50 text-amber-600 rounded-2xl font-black text-xs border border-amber-200"><i class="fas fa-star"></i></button>` : ''}
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
                guideEl.innerHTML = `
                    <div class="bg-gradient-to-br from-indigo-950 to-slate-900 text-white p-6 rounded-[2.5rem] shadow-xl relative overflow-hidden mb-6 border border-slate-700">
                        <h2 class="text-2xl font-black mb-1 text-yellow-400 italic">Pro Guide Pick</h2>
                        <p class="text-[12px] font-bold opacity-80 leading-snug uppercase tracking-widest mt-1">아버지와 아이를 위한 동선 최적화</p>
                        <i class="fas fa-gem absolute -right-4 -bottom-4 text-7xl opacity-10"></i>
                    </div>
                ` + guideItinerary.map(day => `
                    <div class="mb-10">
                        <div class="flex items-center mb-5"><div class="w-10 h-10 bg-indigo-600 text-white rounded-full flex items-center justify-center font-black mr-3 shadow-lg">D</div><h3 class="text-[16px] font-black text-slate-800 dark:text-slate-100">${day.date}</h3></div>
                        <div class="space-y-6 ml-5 border-l-2 border-indigo-100 dark:border-slate-800 pl-6 relative">
                            ${day.items.map(item => `
                                <div class="relative">
                                    <div class="absolute -left-[31px] top-1 w-3 h-3 bg-indigo-600 rounded-full border-2 border-white dark:border-slate-900"></div>
                                    <div class="bg-white dark:bg-slate-900 p-5 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm">
                                        <span class="text-[10px] font-black text-indigo-600 bg-indigo-50 dark:bg-indigo-900/30 px-2 py-1 rounded-md mb-2 inline-block">${item.time}</span>
                                        <div class="flex justify-between items-start mb-2">
                                            <h4 class="font-black text-lg leading-tight">${item.place}</h4>
                                            ${item.tipkey ? `<button onclick="openTipModal('${item.tipkey}')" class="text-amber-500 active:scale-90 transition-transform"><i class="fas fa-star text-lg"></i></button>` : ''}
                                        </div>
                                        <p class="text-[13px] font-medium text-slate-600 dark:text-slate-400 leading-relaxed mb-4">${item.memo}</p>
                                        <div class="flex gap-2">
                                            <button onclick="openAmap('${item.map}')" class="flex-1 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-black text-[10px] border border-slate-200 dark:border-slate-700">지도1</button>
                                            <button onclick="openBaiduMap('${item.map}')" class="flex-1 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-black text-[10px] border border-slate-200 dark:border-slate-700">지도2</button>
                                        </div>
                                    </div>
                                </div>`).join('')}
                        </div>
                    </div>`).join('');
            }
        }

        function filterSpots(cat) { currentSpotCat = cat; document.querySelectorAll('.category-chip').forEach(btn => btn.classList.toggle('active', btn.dataset.cat === cat)); renderSpots(); }
        
        function renderSpots() {
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
                            ${s.subway ? `<div onclick="openMetro('${searchKey}')" class="text-[13px] font-black text-indigo-600 mt-3 flex items-start bg-indigo-50 dark:bg-indigo-900/30 px-3 py-2 rounded-xl border border-indigo-100 dark:border-indigo-800 cursor-pointer active:scale-95 transition-transform"><i class="fas fa-subway mt-0.5 mr-2"></i><span class="flex-1 font-black underline underline-offset-4">${s.subway}</span></div>` : ''}</div>
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
            if(keyword) { 
                const el = document.createElement('textarea');
                el.value = keyword;
                document.body.appendChild(el);
                el.select();
                document.execCommand('copy');
                document.body.removeChild(el);
            }
            window.open('https://metro.nuua.travel/ko/shanghai', '_blank');
        }

        function openSpotModal(key = null) {
            document.getElementById('spot-key').value = key || ''; document.getElementById('spot-modal').classList.remove('hidden');
            if(key) { const s = spotData.find(i => i.key === key); if(s) { document.getElementById('spot-cat').value = s.cat; document.getElementById('spot-name-ko').value = s.nameKo; document.getElementById('spot-name-zh').value = s.nameZh; document.getElementById('spot-addr').value = s.addr || ''; document.getElementById('spot-delete-btn').classList.remove('hidden'); } }
            else { document.getElementById('spot-modal').querySelectorAll('input').forEach(i => i.value = ''); document.getElementById('spot-delete-btn').classList.add('hidden'); }
        }
        function closeSpotModal() { document.getElementById('spot-modal').classList.add('hidden'); }
        function saveSpot() {
            const k = document.getElementById('spot-key').value, d = { cat: document.getElementById('spot-cat').value, nameKo: document.getElementById('spot-name-ko').value, nameZh: document.getElementById('spot-name-zh').value, addr: document.getElementById('spot-addr').value };
            if(!d.nameKo || !d.nameZh) return alert('명칭을 입력해주세요.');
            if(k) db.ref(`${basePath}/spots/${k}`).update(d); else db.ref(`${basePath}/spots`).push(d);
            closeSpotModal();
        }
        function deleteSpot() { const k = document.getElementById('spot-key').value; if(k && confirm("삭제하시겠습니까?")) { db.ref(`${basePath}/spots/${k}`).remove(); closeSpotModal(); } }
        
        function loadSpots() {
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
                            if (existingItem.subway !== init.subway || existingItem.addr !== init.addr) {
                                db.ref(`${basePath}/spots/${existingItem.key}`).update({ 
                                    subway: init.subway,
                                    addr: init.addr
                                });
                            }
                        }
                    });
                } else {
                    initialSpots.forEach(i => db.ref(`${basePath}/spots`).push(i));
                }
                renderSpots();
            });
        }

        function renderPhrases() { 
            const pEl = document.getElementById('phrase-list');
            if(pEl && typeof phraseData !== 'undefined') {
                pEl.innerHTML = phraseData.map(group => `
                    <div class="space-y-4 mb-6">
                        <h4 class="text-[12px] font-black text-slate-400 uppercase tracking-widest pl-1 italic border-b pb-2 dark:border-slate-800">${group.cat}</h4>
                        ${group.items.map(p => `
                            <div class="bg-white dark:bg-slate-900 p-6 rounded-[2rem] shadow-sm border border-slate-100 dark:border-slate-800 flex justify-between items-center active:scale-[0.98] transition-transform" onclick="showFlashcard('${p.zh}', '${p.ko}', '${p.py}')">
                                <div class="pr-3">
                                    <p class="text-base font-black dark:text-white leading-tight">${p.ko}</p>
                                    <p class="text-[11px] text-brand-500 font-bold mt-2 uppercase">${p.py}</p>
                                </div>
                                <button onclick="event.stopPropagation(); speak('${p.zh}')" class="w-12 h-12 rounded-2xl bg-slate-50 dark:bg-slate-800 text-slate-400 flex items-center justify-center text-xl active:text-indigo-500 shadow-inner border border-slate-100 dark:border-slate-700"><i class="fas fa-volume-up"></i></button>
                            </div>`).join('')}
                    </div>`).join(''); 
            }
        }

        function openTipModal(tipkey) { document.getElementById('tip-content').innerHTML = (placeTipsData[tipkey] || "안전한 여행 되세요!").replace(/\\n/g, '<br>'); document.getElementById('tip-modal').classList.remove('hidden'); }
        function closeTipModal() { document.getElementById('tip-modal').classList.add('hidden'); }
        function showFlashcard(zh, ko, py) { document.getElementById('flash-zh').innerText = zh; document.getElementById('flash-ko').innerText = ko; document.getElementById('flash-py').innerText = `[ ${py} ]`; document.getElementById('flashcard').classList.remove('hidden'); }

        function addExpense() { const d = document.getElementById('exp-desc').value, a = document.getElementById('exp-amt').value; if(d && a && db) { db.ref(`${basePath}/expenses`).push({desc: d, amt: Number(a), krwAmt: Math.round(Number(a) * exchangeRate)}); document.getElementById('exp-desc').value = ''; document.getElementById('exp-amt').value = ''; } }
        function loadExpenses() { if(db) db.ref(`${basePath}/expenses`).on('value', s => { const data = s.val() || {}; let tC = 0, tK = 0; document.getElementById('expense-list').innerHTML = Object.entries(data).map(([k, v]) => { tC += v.amt; const kAmt = v.krwAmt || Math.round(v.amt * exchangeRate); tK += kAmt; return `<div class="flex justify-between items-center bg-white dark:bg-slate-800 p-4 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs mb-2 shadow-sm"><div class="flex flex-col"><span class="font-bold">${v.desc}</span><span class="text-[10px] text-slate-400">${kAmt.toLocaleString()} ₩</span></div><span class="font-black text-indigo-500 text-sm">${v.amt.toLocaleString()} ¥ <button onclick="db.ref('${basePath}/expenses/${k}').remove()" class="ml-2 text-slate-300">✕</button></span></div>`; }).join(''); document.getElementById('total-expense').innerHTML = `${tC.toLocaleString()} ¥ <span class="text-xs font-bold text-slate-400 ml-1">(${tK.toLocaleString()} ₩)</span>`; }); }

        function openChecklistModal(type, key = null) {
            document.getElementById('checklist-type').value = type; document.getElementById('checklist-key').value = key || '';
            document.getElementById('checklist-modal').classList.remove('hidden');
            if(key) { db.ref(`${basePath}/checklist/${key}`).once('value', s => { const d = s.val(); document.getElementById('checklist-title').value = d.title; document.getElementById('checklist-memo').value = d.memo || ''; document.getElementById('checklist-delete-btn').classList.remove('hidden'); }); }
            else { document.getElementById('checklist-title').value = ''; document.getElementById('checklist-memo').value = ''; document.getElementById('checklist-delete-btn').classList.add('hidden'); }
        }
        function closeChecklistModal() { document.getElementById('checklist-modal').classList.add('hidden'); }
        function saveChecklist() { const k = document.getElementById('checklist-key').value, t = document.getElementById('checklist-type').value, title = document.getElementById('checklist-title').value, memo = document.getElementById('checklist-memo').value; if(!title) return; if(k) db.ref(`${basePath}/checklist/${k}`).update({title, memo}); else db.ref(`${basePath}/checklist`).push({title, memo, type: t, checked: false}); closeChecklistModal(); }
        function deleteChecklist() { const k = document.getElementById('checklist-key').value; if(k && confirm("삭제하시겠습니까?")) { db.ref(`${basePath}/checklist/${k}`).remove(); closeChecklistModal(); } }
        function loadChecklist() {
            if(!db) return;
            db.ref(`${basePath}/checklist`).on('value', s => {
                const data = s.val() || {}; const items = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                if(items.length === 0) { [...initialChecklist, ...initialShopping].forEach(i => db.ref(`${basePath}/checklist`).push(i)); return; }
                const packEl = document.getElementById('packing-list'), shopEl = document.getElementById('shopping-list');
                if(packEl) packEl.innerHTML = items.filter(i => i.type === 'packing').map(i => `<div class="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-800 mb-2"><div onclick="openChecklistModal('packing', '${i.key}')" class="flex-1"><p class="font-bold text-sm">${i.title}</p>${i.memo ? `<p class="text-[10px] text-slate-400">${i.memo}</p>` : ''}</div><input type="checkbox" ${i.checked ? 'checked' : ''} onchange="db.ref('${basePath}/checklist/${i.key}').update({checked: this.checked})" class="w-5 h-5 accent-indigo-500"></div>`).join('');
                if(shopEl) shopEl.innerHTML = items.filter(i => i.type === 'shopping').map(i => `<div class="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-2xl border border-slate-100 dark:border-slate-800 mb-2"><div onclick="openChecklistModal('shopping', '${i.key}')" class="flex-1"><p class="font-black text-sm">${i.title}</p>${i.memo ? `<p class="text-[11px] text-slate-500 mt-1">${i.memo}</p>` : ''}</div><input type="checkbox" ${i.checked ? 'checked' : ''} onchange="db.ref('${basePath}/checklist/${i.key}').update({checked: this.checked})" class="w-5 h-5 accent-purple-500"></div>`).join('');
            });
        }

        function openItineraryForm(key = null) {
            document.getElementById('itinerary-modal').classList.remove('hidden');
            if(key) { const item = itineraryData.find(i => i.key === key); if(item) { document.getElementById('edit-key').value = key; document.getElementById('form-date').value = item.date; document.getElementById('form-time').value = item.time; document.getElementById('form-place').value = item.place; document.getElementById('form-memo').value = item.memo || ""; document.getElementById('delete-btn').classList.remove('hidden'); } }
            else { document.getElementById('edit-key').value = ''; document.getElementById('itinerary-modal').querySelectorAll('input, textarea').forEach(i => i.value = ''); document.getElementById('delete-btn').classList.add('hidden'); }
        }
        function closeItineraryModal() { document.getElementById('itinerary-modal').classList.add('hidden'); }
        function saveItinerary() { const k = document.getElementById('edit-key').value, d = { date: document.getElementById('form-date').value, time: document.getElementById('form-time').value || "00:00", place: document.getElementById('form-place').value || "장소명", memo: document.getElementById('form-memo').value || "" }; if(k) db.ref(`${basePath}/itinerary/${k}`).update(d); else db.ref(`${basePath}/itinerary`).push(d); closeItineraryModal(); }
        function deleteItinerary() { const k = document.getElementById('edit-key').value; if(k && confirm("삭제할까요?")) { db.ref(`${basePath}/itinerary/${k}`).remove(); closeItineraryModal(); } }
        function loadItinerary() {
            if (db) {
                db.ref(`${basePath}/itinerary`).on('value', s => {
                    const data = s.val(); 
                    if(data) { 
                        itineraryData = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                        itineraryData.sort((a, b) => {
                            const dateA = String(a.date || "").replace(/[^0-9]/g, "");
                            const dateB = String(b.date || "").replace(/[^0-9]/g, "");
                            if (dateA !== dateB) return dateA.localeCompare(dateB);
                            return String(a.time || "").localeCompare(String(b.time || ""));
                        });
                        renderList(itineraryData); scrollToCurrentTask();
                    } else initialShanghai.forEach(i => db.ref(`${basePath}/itinerary`).push(i));
                });
            }
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
                            const tStr = timeArr[0].includes(':') ? timeArr[0] : '00:00';
                            const [h, m] = tStr.split(':').map(Number);
                            if(!isNaN(h)) {
                                const diff = (h * 60 + m) - curM;
                                if (diff >= -60 && diff < minD) { minD = diff; targetId = `card-${item.key}`; }
                            }
                        }
                    }
                });
                if (targetId) {
                    const el = document.getElementById(targetId);
                    if (el) setTimeout(() => { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); el.parentElement.classList.add('ring-2', 'ring-indigo-500', 'rounded-[2.5rem]', 'p-1'); }, 500);
                }
            } catch(e) {}
        }
        
        """
        content = content[:start_idx] + clean_js_block + content[end_idx:]

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    deep_clean_js()
    print("JS cleaned and spots updated.")
