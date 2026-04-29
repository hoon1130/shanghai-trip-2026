import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def apply_all_pro_features():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. Header: Add SOS Button (🚨) ---
    if 'openSOSModal()' not in content:
        header_old = 'alipays://platformapi/startapp?appId=20000056\'" class="w-9 h-9 rounded-full bg-blue-500 text-white flex items-center justify-center shadow-md active:scale-90 transition-transform">'
        header_new = header_old.replace('bg-blue-500', 'bg-blue-500 mr-2').replace('</button>', '') # Just a marker
        # More reliable: find toggleTheme button
        theme_btn_marker = '<button onclick="toggleTheme()"'
        sos_btn = """<button onclick="openSOSModal()" class="w-9 h-9 rounded-full bg-red-500 text-white flex items-center justify-center shadow-md active:scale-90 transition-transform mr-2">
                    <span class="animate-pulse">🚨</span>
                </button>"""
        content = content.replace(theme_btn_marker, sos_btn + theme_btn_marker)

    # --- 2. Spot Tab: Add Nearby Button ---
    if 'data-cat="내 주변"' not in content:
        all_btn_marker = '<button onclick="filterSpots(\'전체\')"'
        nearby_btn = '<button onclick="filterSpots(\'내 주변\')" class="category-chip px-5 py-2 rounded-full text-xs font-black shadow-sm bg-red-50 text-red-600 border-red-100" data-cat="내 주변"><i class="fas fa-location-arrow mr-1 text-[10px]"></i>내 주변</button>\n                '
        content = content.replace(all_btn_marker, nearby_btn + all_btn_marker)

    # --- 3. Money Tab: Add Quick Buttons & Categories & Stats ---
    if 'id="exp-cat"' not in content:
        # Quick Buttons
        cny_input_marker = 'id="cny-input" placeholder="위안(¥) 입력" class="w-full p-5 pl-16 rounded-[1.5rem] bg-white/10 border border-white/10 text-white font-black outline-none text-2xl">'
        quick_calc_btns = """
                    <div class="flex gap-2 pt-1 pb-2">
                        <button onclick="addCNY(10)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-2 rounded-xl font-bold text-xs">+10¥</button>
                        <button onclick="addCNY(50)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-2 rounded-xl font-bold text-xs">+50¥</button>
                        <button onclick="addCNY(100)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-2 rounded-xl font-bold text-xs">+100¥</button>
                        <button onclick="clearCNY()" class="w-10 bg-red-500/80 text-white py-2 rounded-xl font-bold text-xs"><i class="fas fa-undo"></i></button>
                    </div>"""
        content = content.replace(cny_input_marker, cny_input_marker + quick_calc_btns)

        # Expense Stat Bar and Category Select
        exp_input_marker = '<div class="flex gap-2 mb-6">'
        stat_bar = """<!-- Expense Statistics -->
                <div id="expense-summary" class="flex w-full h-3 rounded-full bg-slate-100 dark:bg-slate-800 mb-4 overflow-hidden hidden"></div>
                <div id="expense-legend" class="flex flex-wrap gap-3 mb-6 text-[10px] font-black hidden"></div>

                """
        cat_select = """<select id="exp-cat" class="w-20 p-4 rounded-xl border dark:bg-slate-800 dark:text-white dark:border-slate-700 font-black text-[11px] outline-none bg-slate-50">
                        <option value="식비">🍔 식비</option>
                        <option value="교통">🚕 교통</option>
                        <option value="쇼핑">🛍️ 쇼핑</option>
                        <option value="기타">✨ 기타</option>
                    </select>"""
        content = content.replace(exp_input_marker, stat_bar + exp_input_marker + cat_select)

    # --- 4. Talk Tab: Add Translator Section ---
    if 'id="trans-input"' not in content:
        talk_header_end = '<p class="text-sm opacity-70 font-bold mt-2 leading-relaxed">카드를 누르면 화면 가득 중국어가 뜹니다.<br>스피커 버튼을 누르면 원어민 발음이 나옵니다.</p>'
        translator_html = """
            </div>
            <!-- Translator Section -->
            <div class="bg-white dark:bg-slate-900 p-6 rounded-[2.5rem] border border-slate-200 dark:border-slate-800 shadow-md space-y-4 mb-6">
                <div class="flex justify-between items-center px-1">
                    <h3 class="font-black text-indigo-500 italic uppercase tracking-tighter flex items-center text-sm"><i class="fas fa-language mr-2 text-xl"></i>Smart Translator</h3>
                    <button onclick="window.open('https://papago.naver.com/', '_blank')" class="text-[10px] font-black text-slate-400 underline uppercase">Papago Web</button>
                </div>
                <div class="space-y-3">
                    <textarea id="trans-input" placeholder="번역할 문장을 입력하세요" class="w-full p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border-none font-bold text-sm outline-none h-24"></textarea>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="goPapago('ko', 'zh-CN')" class="bg-slate-900 text-white py-4 rounded-xl font-black text-xs shadow-md active:scale-95 transition-transform flex flex-col items-center">
                            <span>🇰🇷 한국어 → 🇨🇳 중국어</span>
                        </button>
                        <button onclick="goPapago('zh-CN', 'ko')" class="bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-white py-4 rounded-xl font-black text-xs active:scale-95 transition-transform flex flex-col items-center">
                            <span>🇨🇳 중국어 → 🇰🇷 한국어</span>
                        </button>
                    </div>
                    <button onclick="window.open('https://papago.naver.com/?sk=auto&tk=ko&hn=0&st=', '_blank')" class="w-full bg-indigo-500 text-white py-4 rounded-xl font-black text-sm shadow-lg active:scale-95 transition-transform flex items-center justify-center">
                        <i class="fas fa-camera mr-2"></i>실시간 카메라 번역 열기 (Papago)
                    </button>
                </div>
            </div>"""
        content = content.replace(talk_header_end + '\n                </div>', talk_header_end + translator_html)

    # --- 5. Box Tab: Add Progress Bar ---
    if 'id="packing-progress"' not in content:
        checklist_title_old = '<h3 class="font-black text-base flex items-center uppercase tracking-tighter italic text-brand-500"><i class="fas fa-check-circle mr-2 text-xl"></i>체크리스트</h3>'
        checklist_title_new = '<div><h3 class="font-black text-base flex items-center uppercase tracking-tighter italic text-brand-500 mb-1"><i class="fas fa-check-circle mr-2 text-xl"></i>체크리스트</h3><div class="w-24 h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div id="packing-progress" class="h-full bg-brand-500 transition-all duration-500" style="width: 0%"></div></div></div>'
        content = content.replace(checklist_title_old, checklist_title_new)

    # --- 6. JS Logic: Add all needed functions at once ---
    # We will inject these before the DOMContentLoaded listener
    js_pro_logic = """
        // 🚀 Pro Features Logic 🚀
        function addCNY(amt) {
            const el = document.getElementById('cny-input');
            const krwEl = document.getElementById('krw-input');
            const cur = parseFloat(el.value) || 0;
            el.value = cur + amt;
            krwEl.value = Math.round(el.value * exchangeRate);
        }
        function clearCNY() {
            document.getElementById('cny-input').value = '';
            document.getElementById('krw-input').value = '';
        }
        function goPapago(src, tgt) {
            const txt = document.getElementById('trans-input').value;
            if(!txt) return alert('문장을 입력해주세요.');
            window.open(`https://papago.naver.com/?sk=${src}&tk=${tgt}&st=${encodeURIComponent(txt)}`, '_blank');
        }
        function openSOSModal() { document.getElementById('sos-modal').classList.remove('hidden'); }
        function closeSOSModal() { document.getElementById('sos-modal').classList.add('hidden'); }
        function showHotelCard() { document.getElementById('hotel-card').classList.remove('hidden'); closeSOSModal(); }
        function showHelpPhrase(ko, zh, py) { if(typeof showFlashcard === 'function') showFlashcard(zh, ko, py); closeSOSModal(); }

        function getDistance(lat1, lon1, lat2, lon2) {
            if (!lat1 || !lon1 || !lat2 || !lon2) return Infinity;
            const R = 6371; const dLat = (lat2 - lat1) * Math.PI / 180; const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        }
    """
    
    if 'function addCNY(amt)' not in content:
        content = content.replace("document.addEventListener('DOMContentLoaded'", js_pro_logic + "\n\n        document.addEventListener('DOMContentLoaded'")

    # --- 7. Update UI Functions (renderSpots, loadExpenses, loadChecklist) ---
    # These replacements need to be precise.
    
    # 7.1. renderSpots with Distance Badge
    if 's.dist && s.dist !== Infinity' not in content:
        content = content.replace('<h4 class="font-black text-lg">${s.nameKo}</h4>', '<h4 class="font-black text-lg">${s.nameKo}${s.dist && s.dist !== Infinity ? `<span class="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-1 rounded-md ml-2"><i class="fas fa-walking mr-1"></i>${s.dist < 1 ? Math.round(s.dist * 1000) + "m" : s.dist.toFixed(1) + "km"}</span>` : ""}</h4>')

    # 7.2. Update filterSpots to handle GPS
    filter_nearby_logic = """        async function filterSpots(cat) { 
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
        }"""
    content = re.sub(r'function filterSpots\(cat\) \{.*?\}', filter_nearby_logic, content, flags=re.DOTALL)

    # 7.3. Update addExpense for categories
    if 'id="exp-cat"' in content and 'push({cat: c' not in content:
        add_exp_old = re.search(r'function addExpense\(\) \{.*?\}', content, re.DOTALL).group(0)
        add_exp_new = "function addExpense() { const c = document.getElementById('exp-cat') ? document.getElementById('exp-cat').value : '기타', d = document.getElementById('exp-desc').value, a = document.getElementById('exp-amt').value; if(d && a && db) { db.ref(`${basePath}/expenses`).push({cat: c, desc: d, amt: Number(a), krwAmt: Math.round(Number(a) * exchangeRate)}); document.getElementById('exp-desc').value = ''; document.getElementById('exp-amt').value = ''; } }"
        content = content.replace(add_exp_old, add_exp_new)

    # 7.4. Update loadExpenses with Stat Bar
    if 'expense-summary' in content and 'Render Summary Bar' not in content:
        load_exp_start = content.find('function loadExpenses() {')
        load_exp_end = content.find('function openChecklistModal') # Marker for next function
        
        load_exp_new = """        function loadExpenses() {
            if(!db) return;
            db.ref(`${basePath}/expenses`).on('value', s => {
                const data = s.val() || {};
                let tC = 0, tK = 0;
                const cats = { '식비': 0, '교통': 0, '쇼핑': 0, '기타': 0 };
                const colors = { '식비': 'bg-orange-400', '교통': 'bg-blue-400', '쇼핑': 'bg-purple-400', '기타': 'bg-slate-400' };
                
                const listHtml = Object.entries(data).map(([k, v]) => {
                    tC += v.amt;
                    const kAmt = v.krwAmt || Math.round(v.amt * exchangeRate);
                    tK += kAmt;
                    const cName = v.cat ? v.cat.replace(/[🍔🚕🛍️✨ ]/g, '') : '기타';
                    if (cats[cName] !== undefined) cats[cName] += v.amt; else cats['기타'] += v.amt;
                    const badgeColor = colors[cName] || 'bg-slate-400';
                    return `<div class="flex justify-between items-center bg-white dark:bg-slate-800 p-4 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs mb-2 shadow-sm">
                        <div class="flex flex-col">
                            <div class="flex items-center"><span class="w-2 h-2 rounded-full ${badgeColor} mr-2"></span><span class="font-bold">${v.desc}</span></div>
                            <span class="text-[10px] text-slate-400 ml-4 mt-0.5">${kAmt.toLocaleString()} ₩</span>
                        </div>
                        <span class="font-black text-indigo-500 text-sm">${v.amt.toLocaleString()} ¥ <button onclick="db.ref('${basePath}/expenses/${k}').remove()" class="ml-3 text-slate-300 text-base active:scale-90">&times;</button></span>
                    </div>`;
                }).join('');
                
                document.getElementById('expense-list').innerHTML = listHtml;
                document.getElementById('total-expense').innerHTML = `${tC.toLocaleString()} ¥ <span class="text-xs font-bold text-slate-400 ml-1">(${tK.toLocaleString()} ₩)</span>`;

                const sumBar = document.getElementById('expense-summary');
                const legBar = document.getElementById('expense-legend');
                if (tC > 0 && sumBar && legBar) {
                    let barHtml = ''; let legendHtml = '';
                    for (const [c, amt] of Object.entries(cats)) {
                        if (amt > 0) {
                            const pct = (amt / tC * 100).toFixed(1);
                            barHtml += `<div class="h-full ${colors[c]}" style="width: ${pct}%"></div>`;
                            legendHtml += `<div class="flex items-center"><span class="w-2 h-2 rounded-full ${colors[c]} mr-1"></span>${c} <span class="opacity-60 ml-1">${pct}%</span></div>`;
                        }
                    }
                    sumBar.innerHTML = barHtml; sumBar.classList.remove('hidden');
                    legBar.innerHTML = legendHtml; legBar.classList.remove('hidden');
                } else if(sumBar && legBar) {
                    sumBar.classList.add('hidden'); legBar.classList.add('hidden');
                }
            });
        }
        """
        if load_exp_start != -1 and load_exp_end != -1:
            content = content[:load_exp_start] + load_exp_new + content[load_exp_end:]

    # 7.5. Update loadChecklist for Progress Bar
    if 'packing-progress' in content and 'const packItems =' not in content:
        checklist_injection = """
                // Progress update
                const packItems = items.filter(i => i.type === 'packing');
                const pBar = document.getElementById('packing-progress');
                if (pBar && packItems.length > 0) {
                    const checked = packItems.filter(i => i.checked).length;
                    pBar.style.width = `${(checked / packItems.length) * 100}%`;
                }"""
        content = content.replace("if(shopEl) shopEl.innerHTML =", checklist_injection + "\n                if(shopEl) shopEl.innerHTML =")

    # --- 8. Modals (SOS and Hotel Card) ---
    if 'id="sos-modal"' not in content:
        sos_modals = """
    <!-- SOS / Emergency Modal -->
    <div id="sos-modal" class="fixed inset-0 bg-black/70 z-[400] hidden flex items-center justify-center p-5 backdrop-blur-md">
        <div class="bg-white dark:bg-slate-900 p-7 rounded-[2.5rem] w-full max-w-md space-y-5 shadow-2xl border-t-[8px] border-red-500">
            <div class="flex justify-between items-center border-b pb-4 dark:border-slate-800">
                <h3 class="font-black text-2xl tracking-tighter italic uppercase text-red-500 flex items-center"><i class="fas fa-exclamation-triangle mr-2"></i>SOS</h3>
                <button onclick="closeSOSModal()" class="text-slate-400"><i class="fas fa-times text-xl"></i></button>
            </div>
            <button onclick="showHotelCard()" class="w-full bg-slate-900 dark:bg-brand-500 text-white py-5 rounded-2xl font-black text-lg shadow-lg flex flex-col items-center justify-center space-y-1 active:scale-95 transition-transform">
                <span>🏠 숙소로 갑시다 (택시용)</span>
                <span class="text-[10px] opacity-70 font-bold uppercase tracking-widest">Show address to driver</span>
            </button>
            <div class="space-y-3">
                <p class="text-[11px] font-black text-slate-400 uppercase tracking-widest">Emergency Calls</p>
                <div class="grid grid-cols-2 gap-2">
                    <a href="tel:110" class="bg-red-50 text-red-600 p-4 rounded-2xl text-center font-black text-sm border border-red-100">경찰 (110)</a>
                    <a href="tel:120" class="bg-orange-50 text-orange-600 p-4 rounded-2xl text-center font-black text-sm border border-orange-100">구급차 (120)</a>
                    <a href="tel:+86-21-6295-5000" class="col-span-2 bg-blue-50 text-blue-600 p-4 rounded-2xl text-center font-black text-sm border border-blue-100">🇰🇷 주상하이 영사관</a>
                </div>
            </div>
            <div class="space-y-3">
                <p class="text-[11px] font-black text-slate-400 uppercase tracking-widest">Help Me</p>
                <button onclick="showHelpPhrase('길을 잃었습니다. 도와주세요.', '我迷路了, 请帮帮我。', '워 미루러, 칭 빵빵워')" class="w-full bg-slate-50 dark:bg-slate-800 p-4 rounded-2xl text-left font-bold text-sm border border-slate-100 dark:border-slate-700 flex justify-between items-center">
                    <span>迷路了 (길을 잃었습니다)</span>
                    <i class="fas fa-chevron-right text-slate-300"></i>
                </button>
            </div>
        </div>
    </div>
    <!-- Huge Hotel Card Overlay -->
    <div id="hotel-card" class="fixed inset-0 bg-white z-[500] hidden flex flex-col items-center justify-center p-8 text-center" onclick="this.classList.add('hidden')">
        <p class="text-slate-500 font-black text-xl mb-10">기사님, 여기로 가주세요 (请带我去这里)</p>
        <h2 class="text-7xl font-black text-slate-950 mb-6">上海国金汇</h2>
        <p class="text-3xl font-bold text-slate-700 leading-tight mb-12">上海市浦东新区<br>世纪大道8号</p>
        <div class="bg-slate-100 px-6 py-3 rounded-full font-black text-slate-400 animate-pulse text-sm">Touch anywhere to close</div>
    </div>"""
        content = content.replace('</body>', sos_modals + '\n</body>')

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    apply_all_pro_features()
    print("All Pro features integrated into local index.html.")
