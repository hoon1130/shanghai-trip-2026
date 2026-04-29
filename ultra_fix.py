import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def ultra_fix():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean the duplicated logic between fetchWeather and openAmap
    # Find the problematic fetchWeather function and replace the WHOLE block carefully.
    
    start_point = content.find('async function fetchWeather()')
    end_point = content.find('function getSmartInfo(input)')
    
    if start_point != -1 and end_point != -1:
        fresh_functions = """async function fetchWeather() {
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

        """
        content = content[:start_point] + fresh_functions + content[end_point:]

    # 2. Re-apply the renderSpots and loadSpots logic completely clean
    render_start = content.find('function renderSpots()')
    render_end = content.find('function renderPhrases()')
    
    if render_start != -1 and render_end != -1:
        clean_spots_logic = """function renderSpots() {
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
        }

        """
        content = content[:render_start] + clean_spots_logic + content[render_end:]

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    ultra_fix()
    print("Ultra Fix applied.")
