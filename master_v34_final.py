import codecs

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

full_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>상해 투어 가이드</title>
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#1e293b">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link rel="apple-touch-icon" href="icon.svg">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config = { darkMode: 'class', theme: { extend: { colors: { brand: { 50: '#f8fafc', 500: '#4f46e5', 600: '#4338ca', 900: '#0f172a' } } } } }</script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://www.gstatic.com/firebasejs/9.17.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.17.1/firebase-database-compat.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&display=swap');
        body { font-family: 'Pretendard', sans-serif; -webkit-tap-highlight-color: transparent; word-break: keep-all; user-select: none; letter-spacing: -0.03em; }
        .tab-content { display: none; } .tab-content.active { display: block; animation: fadeIn 0.2s ease-out; }
        .glass-header { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border-bottom: 1px solid #f1f5f9; }
        .dark .glass-header { background: rgba(15, 23, 42, 0.95); border-bottom: 1px solid #1e293b; }
        .bottom-nav { height: 60px; border-top: 1px solid #f1f5f9; box-shadow: 0 -10px 30px rgba(0,0,0,0.05); }
        .dark .bottom-nav { border-top: 1px solid #1e293b; box-shadow: 0 -10px 30px rgba(0,0,0,0.5); }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        ::-webkit-scrollbar { display: none; }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .card-grad { background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); }
        .dark .card-grad { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); }
        .category-chip { transition: all 0.2s; white-space: nowrap; border: 1px solid #e2e8f0; cursor: pointer; }
        .dark .category-chip { border-color: #1e293b; }
        .category-chip.active { background-color: #4f46e5 !important; color: white !important; border-color: #4f46e5 !important; }
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 pb-24 transition-colors duration-300 text-slate-900 dark:text-slate-100">

    <header class="glass-header sticky top-0 z-50 px-4 py-3">
        <div class="flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <button onclick="window.open('https://search.naver.com/search.naver?query=상해+날씨', '_blank')" id="weather-display" class="bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 px-4 py-2.5 rounded-2xl text-[11px] font-black flex items-center shadow-sm border border-indigo-100 dark:border-indigo-800/50">
                    <i class="fas fa-spinner fa-spin mr-2 text-indigo-500"></i>날씨 확인 중...
                </button>
            </div>
            <div class="flex items-center space-x-1">
                <button onclick="openSOSModal()" class="w-9 h-9 rounded-full bg-red-500 text-white flex items-center justify-center shadow-md active:scale-90 transition-transform mr-1">
                    <span class="animate-pulse">🚨</span>
                </button>
                <button onclick="location.href='alipays://platformapi/startapp?appId=20000056'" class="w-9 h-9 rounded-full bg-blue-500 text-white flex items-center justify-center shadow-md active:scale-90 transition-transform">
                    <i class="fab fa-alipay text-[16px]"></i>
                </button>
                <button onclick="toggleTheme()" class="w-9 h-9 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-500 shadow-sm border border-slate-200 dark:border-slate-700 ml-1">
                    <i id="theme-icon" class="fas fa-moon text-sm"></i>
                </button>
            </div>
        </div>
    </header>

    <main class="p-4">
        <!-- Schedule Tab -->
        <div id="schedule" class="tab-content active space-y-5">
            <div class="flex bg-slate-200/50 dark:bg-slate-800/50 p-1 rounded-2xl mb-4 shadow-inner border border-slate-100 dark:border-slate-800">
                <button onclick="toggleItineraryType('family')" id="btn-family" class="flex-1 py-3 rounded-xl text-[13px] font-black transition-all bg-white dark:bg-slate-700 shadow-sm text-brand-500">📍 실전 일정표</button>
                <button onclick="toggleItineraryType('guide')" id="btn-guide" class="flex-1 py-3 rounded-xl text-[13px] font-black transition-all text-slate-500 dark:text-slate-400">💎 가이드 브리핑</button>
            </div>
            <div id="family-itinerary" class="space-y-4">
                <div class="flex justify-between items-center px-1">
                    <h2 class="text-lg font-black uppercase tracking-tighter italic">Family Route</h2>
                    <button onclick="openItineraryForm()" class="bg-slate-900 dark:bg-brand-500 text-white px-4 py-2 rounded-lg text-[11px] font-black shadow-lg flex items-center active:scale-95 transition-transform"><i class="fas fa-plus mr-1"></i>일정 추가</button>
                </div>
                <div id="itinerary-list" class="space-y-6 pt-2">
                    <div class="text-center text-slate-400 text-sm py-10 font-bold"><i class="fas fa-spinner fa-spin mr-2"></i>일정 동기화 중...</div>
                </div>
            </div>
            <div id="guide-itinerary" class="hidden space-y-4">
                <div id="guide-itinerary-list" class="space-y-6 pt-2"></div>
            </div>
        </div>

        <!-- Spot Tab -->
        <div id="spot" class="tab-content space-y-5">
            <div class="flex justify-between items-center px-1">
                <h2 class="text-lg font-black uppercase tracking-tighter italic text-brand-500">Shanghai Spots</h2>
                <button onclick="openSpotModal()" class="bg-slate-900 dark:bg-brand-500 text-white px-4 py-2 rounded-lg text-[11px] font-black shadow-lg active:scale-95 transition-transform"><i class="fas fa-plus mr-1"></i>장소 추가</button>
            </div>
            <div class="relative">
                <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                <input type="text" id="spot-search" oninput="renderSpots()" placeholder="장소 검색" class="w-full p-4 pl-11 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 font-bold text-sm outline-none shadow-sm">
            </div>
            <div class="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
                <button onclick="filterSpots('내 주변')" class="category-chip px-5 py-2 rounded-full text-xs font-black shadow-sm bg-red-50 text-red-600 border-red-100" data-cat="내 주변">내 주변</button>
                <button onclick="filterSpots('전체')" class="category-chip active px-5 py-2 rounded-full text-xs font-black shadow-sm" data-cat="전체">전체</button>
                <button onclick="filterSpots('핵심')" class="category-chip px-5 py-2 rounded-full text-xs font-black shadow-sm bg-white dark:bg-slate-900" data-cat="핵심">핵심</button>
                <button onclick="filterSpots('명소')" class="category-chip px-5 py-2 rounded-full text-xs font-black shadow-sm bg-white dark:bg-slate-900" data-cat="명소">명소</button>
                <button onclick="filterSpots('맛집')" class="category-chip px-5 py-2 rounded-full text-xs font-black shadow-sm bg-white dark:bg-slate-900" data-cat="맛집">맛집</button>
                <button onclick="filterSpots('쇼핑/기타')" class="category-chip px-5 py-2 rounded-full text-xs font-black shadow-sm bg-white dark:bg-slate-900" data-cat="쇼핑/기타">쇼핑/기타</button>
            </div>
            <div id="spot-list" class="space-y-4"></div>
        </div>

        <!-- Ledger Tab -->
        <div id="ledger" class="tab-content space-y-5">
            <div class="bg-slate-900 text-white p-7 rounded-[2.5rem] shadow-xl relative overflow-hidden">
                <h2 class="text-4xl font-black mb-1 italic tracking-tighter" id="exchange-rate-display">1¥ = 215.94₩</h2>
                <div class="space-y-4 relative z-10 mt-6">
                    <div class="relative">
                        <span class="absolute left-5 top-5 text-white/50 font-black text-sm">CNY</span>
                        <input type="number" id="cny-input" placeholder="위안(¥) 입력" class="w-full p-5 pl-16 rounded-[1.5rem] bg-white/10 border border-white/10 text-white font-black outline-none text-2xl">
                    </div>
                    <div class="flex gap-2 mb-2">
                        <button onclick="addCNY(10)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-3 rounded-xl font-black text-xs transition-all active:scale-95">+10¥</button>
                        <button onclick="addCNY(50)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-3 rounded-xl font-black text-xs transition-all active:scale-95">+50¥</button>
                        <button onclick="addCNY(100)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-3 rounded-xl font-black text-xs transition-all active:scale-95">+100¥</button>
                        <button onclick="clearCNY()" class="w-12 bg-red-500/50 text-white py-3 rounded-xl font-black text-xs active:scale-95"><i class="fas fa-undo"></i></button>
                    </div>
                    <div class="relative">
                        <span class="absolute left-5 top-5 text-white/50 font-black text-sm">KRW</span>
                        <input type="number" id="krw-input" placeholder="원화(₩) 입력" class="w-full p-5 pl-16 rounded-[1.5rem] bg-indigo-600 border-none text-white font-black outline-none text-2xl placeholder:text-white/50">
                    </div>
                </div>
            </div>
            <div class="bg-white dark:bg-slate-900 p-6 rounded-[2.5rem] border border-slate-200 dark:border-slate-800 shadow-md">
                <div id="expense-summary" class="flex w-full h-3 rounded-full bg-slate-100 dark:bg-slate-800 mb-4 overflow-hidden hidden"></div>
                <div id="expense-legend" class="flex flex-wrap gap-3 mb-6 text-[10px] font-black hidden"></div>
                <div class="flex gap-2 mb-6">
                    <select id="exp-cat" class="w-20 p-4 rounded-xl border dark:bg-slate-800 dark:text-white dark:border-slate-700 font-black text-[11px] outline-none bg-slate-50">
                        <option value="식비">🍔 식비</option><option value="교통">🚕 교통</option><option value="쇼핑">🛍️ 쇼핑</option><option value="기타">✨ 기타</option>
                    </select>
                    <input type="text" id="exp-desc" placeholder="지출 내역" class="flex-1 min-w-0 p-4 rounded-xl border dark:bg-slate-800 dark:text-white dark:border-slate-700 font-bold text-sm outline-none">
                    <input type="number" id="exp-amt" placeholder="¥" class="w-16 p-4 rounded-xl border dark:bg-slate-800 dark:text-white dark:border-slate-700 font-bold text-sm outline-none text-center">
                    <button onclick="addExpense()" class="px-4 bg-slate-900 dark:bg-brand-500 text-white rounded-xl font-black text-sm shadow-md active:scale-95">저장</button>
                </div>
                <div id="expense-list" class="space-y-3 max-h-64 overflow-y-auto pr-1"></div>
                <div class="mt-6 pt-5 border-t-2 border-dashed border-slate-100 dark:border-slate-800 flex justify-between items-center px-1">
                    <span class="font-black text-slate-400 text-xs tracking-widest uppercase">Total Expense</span>
                    <span id="total-expense" class="text-3xl font-black text-brand-500 italic underline underline-offset-4 decoration-2">0 ¥</span>
                </div>
            </div>
        </div>

        <!-- Phrases Tab -->
        <div id="phrases" class="tab-content space-y-6">
            <div class="bg-indigo-600 text-white p-6 rounded-[2rem] shadow-lg mb-4 relative overflow-hidden">
                <h3 class="font-black mb-1 text-xl flex items-center italic uppercase tracking-tighter"><i class="fas fa-language mr-2"></i>Talk Helper</h3>
                <p class="text-sm opacity-90 font-bold mt-1 leading-relaxed">자동 번역기를 활용하세요.</p>
                <i class="fas fa-comment-dots absolute -right-4 -bottom-4 text-8xl opacity-10"></i>
            </div>
            <!-- Translator Section -->
            <div class="bg-white dark:bg-slate-900 p-6 rounded-[2.5rem] border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
                <div class="flex justify-between items-center px-1">
                    <h3 class="font-black text-brand-500 italic uppercase tracking-tighter flex items-center text-sm"><i class="fas fa-magic mr-2 text-xl"></i>In-App Translator</h3>
                    <button onclick="window.open('https://papago.naver.com/?sk=auto&tk=ko&hn=0&st=', '_blank')" class="text-[10px] font-black text-slate-400 underline uppercase flex items-center"><i class="fas fa-camera mr-1 text-[12px]"></i>Camera</button>
                </div>
                <div class="space-y-3">
                    <div class="relative">
                        <textarea id="trans-input" placeholder="한글 또는 중국어를 입력하세요" class="w-full p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border-none font-bold text-sm outline-none h-24 shadow-inner"></textarea>
                        <button onclick="translateAction()" class="absolute right-3 bottom-3 bg-slate-900 text-white w-10 h-10 rounded-xl shadow-lg active:scale-90 flex items-center justify-center transition-transform">
                            <i id="trans-btn-icon" class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                    <div id="trans-result-box" class="hidden p-5 rounded-2xl bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-100 dark:border-indigo-800 relative">
                        <p id="trans-result-text" class="font-black text-lg text-indigo-900 dark:text-indigo-100 leading-tight pr-8"></p>
                        <button id="trans-speak-btn" class="absolute right-4 top-1/2 -translate-y-1/2 text-indigo-400 hover:text-indigo-600 hidden"><i class="fas fa-volume-up text-xl"></i></button>
                    </div>
                </div>
            </div>
            <div id="phrase-list" class="space-y-6 pb-8"></div>
        </div>

        <!-- Packing Tab -->
        <div id="packing" class="tab-content space-y-6">
            <div class="bg-white dark:bg-slate-900 p-7 rounded-[2.5rem] border border-slate-200 dark:border-slate-800 shadow-sm">
                <div class="flex justify-between items-center mb-5">
                    <div>
                        <h3 class="font-black text-base flex items-center uppercase tracking-tighter italic text-brand-500 mb-1"><i class="fas fa-check-circle mr-2 text-xl"></i>체크리스트</h3>
                        <div class="w-24 h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div id="packing-progress" class="h-full bg-brand-500 transition-all duration-500" style="width: 0%"></div></div>
                    </div>
                    <button onclick="openChecklistModal('packing')" class="bg-slate-900 dark:bg-brand-500 text-white px-3 py-1 rounded-lg text-[10px] font-black shadow-md"><i class="fas fa-plus mr-1"></i>추가</button>
                </div>
                <div id="packing-list" class="space-y-2"></div>
            </div>
        </div>
    </main>

    <nav class="fixed bottom-0 left-0 right-0 glass-header flex bottom-nav z-50 shadow-2xl">
        <button onclick="showTab('schedule')" id="nav-schedule" class="tab-btn flex-1 flex flex-col items-center justify-center text-brand-500"><i class="fas fa-route text-[22px] mb-1"></i><span class="text-[9px] font-black uppercase tracking-tighter">Plan</span></button>
        <button onclick="showTab('spot')" id="nav-spot" class="tab-btn flex-1 flex flex-col items-center justify-center text-slate-400"><i class="fas fa-map-marked-alt text-[22px] mb-1"></i><span class="text-[9px] font-black uppercase tracking-tighter">Spot</span></button>
        <button onclick="showTab('ledger')" id="nav-ledger" class="tab-btn flex-1 flex flex-col items-center justify-center text-slate-400"><i class="fas fa-wallet text-[22px] mb-1"></i><span class="text-[9px] font-black uppercase tracking-tighter">Money</span></button>
        <button onclick="showTab('phrases')" id="nav-phrases" class="tab-btn flex-1 flex flex-col items-center justify-center text-slate-400"><i class="fas fa-comment-dots text-[22px] mb-1"></i><span class="text-[9px] font-black uppercase tracking-tighter">Talk</span></button>
        <button onclick="showTab('packing')" id="nav-packing" class="tab-btn flex-1 flex flex-col items-center justify-center text-slate-400"><i class="fas fa-suitcase text-[22px] mb-1"></i><span class="text-[9px] font-black uppercase tracking-tighter">Box</span></button>
    </nav>

    <!-- SOS Modal -->
    <div id="sos-modal" class="fixed inset-0 bg-black/70 z-[400] hidden flex items-center justify-center p-5 backdrop-blur-md">
        <div class="bg-white dark:bg-slate-900 p-7 rounded-[2.5rem] w-full max-w-md space-y-5 shadow-2xl border-t-[8px] border-red-500">
            <h3 class="font-black text-2xl text-red-500 text-center uppercase tracking-tighter">SOS</h3>
            <button onclick="showHotelCard()" class="w-full bg-slate-900 dark:bg-brand-500 text-white py-5 rounded-2xl font-black text-lg active:scale-95 transition-transform flex flex-col items-center">
                <span>🏠 숙소로 갑시다 (택시용)</span>
                <span class="text-[10px] opacity-70 uppercase mt-1">Show address to driver</span>
            </button>
            <div class="grid grid-cols-2 gap-2">
                <a href="tel:110" class="bg-red-50 text-red-600 p-4 rounded-xl text-center font-black">경찰 (110)</a>
                <a href="tel:120" class="bg-orange-50 text-orange-600 p-4 rounded-xl text-center font-black">구급차 (120)</a>
                <a href="tel:+86-21-6295-5000" class="col-span-2 bg-blue-50 text-blue-600 p-4 rounded-xl text-center font-black italic">🇰🇷 주상하이 영사관</a>
            </div>
            <button onclick="showHelpPhrase('길을 잃었습니다. 도와주세요.', '我迷路了, 请帮帮我。', '워 미루러, 칭 빵빵워')" class="w-full bg-slate-50 dark:bg-slate-800 p-4 rounded-2xl text-left font-bold flex justify-between items-center text-sm">
                <span>迷路了 (길을 잃었습니다)</span><i class="fas fa-chevron-right text-slate-300"></i>
            </button>
        </div>
    </div>

    <!-- Fullscreen Card -->
    <div id="hotel-card" class="fixed inset-0 bg-white z-[500] hidden flex flex-col items-center justify-center p-8 text-center" onclick="this.classList.add('hidden')">
        <p class="text-slate-500 font-black text-xl mb-10 text-center">기사님, 여기로 가주세요 (请帶我去这里)</p>
        <h2 class="text-7xl font-black text-slate-950 mb-6">上海国金汇</h2>
        <p class="text-3xl font-bold text-slate-700 leading-tight">上海市浦东新区<br>世纪大道8号</p>
        <div class="mt-20 bg-slate-100 px-6 py-3 rounded-full font-black text-slate-400 animate-pulse text-sm">Touch anywhere to close</div>
    </div>

    <!-- Edit Modals -->
    <div id="itinerary-modal" class="fixed inset-0 bg-black/60 z-[100] hidden flex items-center justify-center p-5 backdrop-blur-sm">
        <div class="bg-white dark:bg-slate-900 p-8 rounded-[2.5rem] w-full max-w-md space-y-4 shadow-2xl">
            <h3 class="font-black text-xl text-brand-500 text-center uppercase">Edit Plan</h3>
            <input type="hidden" id="edit-key"><select id="form-date" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black outline-none"><option value="05-05(화)">5월 5일 (화)</option><option value="05-06(수)">5월 6일 (수)</option><option value="05-07(목)">5월 7일 (목)</option><option value="05-08(금)">5월 8일 (금)</option><option value="05-09(토)">5월 9일 (토)</option></select>
            <input type="text" id="form-time" placeholder="시간" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black">
            <input type="text" id="form-place" placeholder="장소명" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black">
            <textarea id="form-memo" placeholder="내용" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black h-24 outline-none"></textarea>
            <div class="flex gap-2"><button onclick="saveItinerary()" class="flex-1 bg-slate-900 text-white py-4 rounded-xl font-black">SAVE</button><button onclick="closeItineraryModal()" class="flex-1 bg-slate-200 py-4 rounded-xl font-black">CLOSE</button></div>
            <button id="delete-btn" onclick="deleteItinerary()" class="w-full text-red-500 underline text-xs mt-2">Delete</button>
        </div>
    </div>

    <div id="spot-modal" class="fixed inset-0 bg-black/60 z-[100] hidden flex items-center justify-center p-5 backdrop-blur-sm">
        <div class="bg-white dark:bg-slate-900 p-8 rounded-[2.5rem] w-full max-w-md space-y-4 shadow-2xl">
            <h3 class="font-black text-xl text-brand-500 text-center uppercase">Spot Info</h3>
            <input type="hidden" id="spot-key"><select id="spot-cat" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black outline-none"><option value="핵심">핵심</option><option value="명소">명소</option><option value="맛집">맛집</option><option value="쇼핑/기타">쇼핑/기타</option></select>
            <input type="text" id="spot-name-ko" placeholder="한글 명칭" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black">
            <input type="text" id="spot-name-zh" placeholder="중문 명칭" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black">
            <input type="text" id="spot-subway" placeholder="지하철 정보" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black">
            <input type="text" id="spot-addr" placeholder="상세 주소" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black">
            <div class="flex gap-2"><button onclick="saveSpot()" class="flex-1 bg-slate-900 text-white py-4 rounded-xl font-black">저장</button><button onclick="closeSpotModal()" class="flex-1 bg-slate-200 py-4 rounded-xl font-black">닫기</button></div>
            <button id="spot-delete-btn" onclick="deleteSpot()" class="w-full text-red-500 underline text-xs mt-2">삭제</button>
        </div>
    </div>

    <div id="checklist-modal" class="fixed inset-0 bg-black/60 z-[100] hidden flex items-center justify-center p-5 backdrop-blur-sm">
        <div class="bg-white dark:bg-slate-900 p-8 rounded-[2.5rem] w-full max-w-md space-y-4 shadow-2xl">
            <h3 class="font-black text-xl text-brand-500 text-center">Item Add</h3>
            <input type="hidden" id="checklist-type"><input type="hidden" id="checklist-key">
            <input type="text" id="checklist-title" placeholder="항목 이름" class="w-full p-4 rounded-xl bg-slate-100 dark:bg-slate-800 font-black">
            <div class="flex gap-2"><button onclick="saveChecklist()" class="flex-1 bg-slate-900 dark:bg-brand-500 text-white py-4 rounded-xl font-black">저장</button><button onclick="closeChecklistModal()" class="flex-1 bg-slate-200 py-4 rounded-xl font-black">닫기</button></div>
        </div>
    </div>

    <script>
        const basePath = 'shanghai_2026_v30_final'; const exchangeRate = 215.94;
        let db = null, itineraryData = [], spotData = [], currentSpotCat = '전체';

        const smartMapDict = {"공항": {name: "浦东国际机场", addr: ""}, "루자쭈이": {name: "陆家嘴", addr: ""}, "ifc": {name: "上海国金汇", addr: ""}, "호텔": {name: "上海国金汇", addr: ""}};
        
        const initialSpots = [
            {cat: "핵심", nameKo: "푸동 T2", nameZh: "上海浦东国际机场2号航站楼", addr: "", subway: "浦东国际机场(Pudong Guoji Jichang) 푸동공항역 | 2호선/자기부상", lat: 31.144, lng: 121.808},
            {cat: "핵심", nameKo: "롱양루역", nameZh: "龙阳路站", addr: "", subway: "龙阳路(Longyang Lu) 롱양루역 | 2/7/16/18호선", lat: 31.203, lng: 121.558},
            {cat: "핵심", nameKo: "루자주이역", nameZh: "陆家嘴地铁站", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 2/14호선", lat: 31.239, lng: 121.501},
            {cat: "핵심", nameKo: "숙소", nameZh: "上海国金汇", addr: "", subway: "陆家嘴(Lujiazui) 루자주이역 | 6번출구 도보 3분", lat: 31.236, lng: 121.502},
            {cat: "명소", nameKo: "난징동루", nameZh: "南京东路", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 1분", lat: 31.238, lng: 121.484},
            {cat: "명소", nameKo: "치바오", nameZh: "七宝古镇", addr: "", subway: "七宝(Qi Bao) 치바오역 | 2번출구 도보 5분", lat: 31.155, lng: 121.352},
            {cat: "명소", nameKo: "정안사", nameZh: "静安寺", addr: "", subway: "静安寺(Jing An Si) 정안사역 | 1번출구 도보 2분", lat: 31.224, lng: 121.447},
            {cat: "명소", nameKo: "남경서로", nameZh: "南京西路", addr: "", subway: "南京西路(Nanjing Xi Lu) 남경서로역 | 2/12/13호선", lat: 31.230, lng: 121.460},
            {cat: "명소", nameKo: "우전", nameZh: "乌镇", addr: "", subway: "시외지역 | 전용차량 권장", lat: 30.751, lng: 120.485},
            {cat: "명소", nameKo: "주가각", nameZh: "朱家角", addr: "", subway: "朱家角(Zhu Jia Jiao) 주가각역 | 1번출구 도보 15분", lat: 31.111, lng: 121.053},
            {cat: "명소", nameKo: "루쉰공원", nameZh: "鲁迅公园", addr: "", subway: "虹口足球场(Hongkou Zuqiu Chang) 홍구축구장역 | 도보 5분", lat: 31.272, lng: 121.481},
            {cat: "명소", nameKo: "우캉멘션", nameZh: "武康大楼", addr: "", subway: "交通大学(Jiao Tong Da Xue) 교통대학역 | 도보 5분", lat: 31.203, lng: 121.434},
            {cat: "명소", nameKo: "티엔즈팡", nameZh: "田子坊", addr: "", subway: "打浦桥(Da Pu Qiao) 타포교역 | 도보 1분", lat: 31.209, lng: 121.468},
            {cat: "명소", nameKo: "신천지", nameZh: "上海新天地", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 6번출구 도보 2분", lat: 31.221, lng: 121.475},
            {cat: "명소", nameKo: "예원/예원상성", nameZh: "豫园商城", addr: "", subway: "豫园(Yu Yuan) 예원역 | 10/14호선 1번출구 도보 5분", lat: 31.227, lng: 121.492},
            {cat: "명소", nameKo: "임시정부 유적지", nameZh: "大韩민국临时政府旧址", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 6번출구 도보 3분", lat: 31.218, lng: 121.475},
            {cat: "명소", nameKo: "디즈니랜드", nameZh: "上海迪士尼度假区", addr: "", subway: "迪士尼(Di Shi Ni) 디즈니역 | 11호선 1번출구 도보 5분", lat: 31.141, lng: 121.662},
            {cat: "명소", nameKo: "인민광장", nameZh: "人民广场", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 1/2/8호선", lat: 31.232, lng: 121.475},
            {cat: "맛집", nameKo: "점도덕", nameZh: "点都德(新天地店)", addr: "", subway: "新天地(Xin Tian Di) 신천지역 | 2번출구 도보 5분", lat: 31.216, lng: 121.479},
            {cat: "맛집", nameKo: "양꼬치", nameZh: "很久以前羊肉串(南京东路)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 7번출구 도보 3분", lat: 31.235, lng: 121.484},
            {cat: "맛집", nameKo: "하이디라오", nameZh: "海底捞(人民广场店)", addr: "", subway: "人民广场(Renmin Guangchang) 인민광장역 | 19번출구 도보 2분", lat: 31.234, lng: 121.478},
            {cat: "쇼핑/기타", nameKo: "릴리안 베이커리", nameZh: "莉莲蛋挞(南京东路)", addr: "", subway: "南京东路(Nanjing Dong Lu) 난징동루역 | 2번출구 도보 1분", lat: 31.237, lng: 121.486}
        ];

        const initialShanghai = [
            {date: "05-05(화)", time: "04:50~07:00", place: "공항 이동", memo: "집 앞 리무진 예약 완료", tipkey: ""},
            {date: "05-05(화)", time: "09:00~10:05", place: "인천 공항 → 푸동 공항", memo: "OZ361 A350", tipkey: "flight"},
            {date: "05-05(화)", time: "11:00~12:00", place: "푸동공항 -> 숙소 이동", memo: "디디 비즈니스 호출", tipkey: "taxi"},
            {date: "05-05(화)", time: "14:00", place: "호텔 체크인", memo: "上海国金汇", tipkey: "hotel"}
        ];

        const phraseData = [{cat: "식당 (Order)", items: [{ko: "고수 빼주세요", zh: "不要香菜", py: "부야오 샹차이"}]}];
        const placeTipsData = {"flight": "✈️ **항공**\\n- 보조배터리 필수.", "taxi": "🚖 **디디**\\n- 6인승 비즈니스 추천."};

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
            btnIcon.className = 'fas fa-spinner fa-spin'; resultBox.classList.remove('hidden');
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
                    const searchKey = (s.subway.match(/\\(([^)]+)\\)/) || ['', ''])[1];
                    return `<div class="bg-white dark:bg-slate-900 p-5 rounded-[2rem] border border-slate-200 dark:border-slate-800 shadow-sm">
                        <div class="flex justify-between items-start mb-2">
                            <div><span class="text-[10px] font-black text-indigo-500 bg-indigo-50 px-2 py-1 rounded-md mb-2 inline-block">${s.cat}</span>
                            <h4 class="font-black text-lg">${s.nameKo}${s.dist && s.dist < 500 ? `<span class="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-1 rounded-md ml-2">${s.dist<1?Math.round(s.dist*1000)+'m':s.dist.toFixed(1)+'km'}</span>`:''}</h4>
                            <p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p>
                            ${s.subway ? `<div onclick="openMetro('${searchKey}')" class="text-[12px] font-black text-indigo-600 mt-3 flex items-start bg-indigo-50 dark:bg-indigo-900/30 px-3 py-2 rounded-xl border border-indigo-100 cursor-pointer"><i class="fas fa-subway mt-0.5 mr-2"></i><span class="flex-1 underline font-black">${s.subway}</span></div>`:''}</div>
                            <button onclick="openSpotModal('${s.key}')" class="text-slate-300 p-2"><i class="fas fa-edit text-sm"></i></button>
                        </div>
                        <div class="flex gap-2 mt-4"><button onclick="openAmap('${s.nameZh}')" class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 rounded-xl font-black text-[10px]">지도1</button><button onclick="openBaiduMap('${s.nameZh}')" class="flex-1 py-2.5 bg-slate-100 dark:bg-slate-800 rounded-xl font-black text-[10px]">지도2</button></div>
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
                    return `<div class="flex justify-between items-center bg-white dark:bg-slate-800 p-4 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs mb-2 shadow-sm"><div class="flex flex-col"><div class="flex items-center"><span class="w-2 h-2 rounded-full ${cName==='식비'?'bg-orange-400':cName==='교통'?'bg-blue-400':cName==='쇼핑'?'bg-purple-400':'bg-slate-400'} mr-2"></span><span class="font-bold">${v.desc}</span></div><span class="text-[10px] text-slate-400 ml-4">${kAmt.toLocaleString()} ₩</span></div><span class="font-black text-indigo-500 text-sm">${v.amt.toLocaleString()} ¥ <button onclick="db.ref('${basePath}/expenses/${k}').remove()" class="ml-3">&times;</button></span></div>`;
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
                            const shouldHide = ["기상", "조식", "정비", "자유 일정", "체크아웃", "인천공항", "집으로"].some(k => placeStr.includes(k));
                            return `
                            <div id="card-${item.key}" class="card-grad p-6 rounded-[2rem] border border-slate-200 dark:border-slate-800 shadow-sm">
                                <div class="flex justify-between items-center mb-3"><span class="text-[11px] font-black bg-indigo-500 text-white px-3 py-1.5 rounded-lg shadow-md">${item.time || ''}</span><button onclick="openItineraryForm('${item.key}')" class="text-slate-300"><i class="fas fa-ellipsis-h text-lg"></i></button></div>
                                <h4 class="font-black text-xl mb-3 leading-tight">${placeStr}</h4>
                                ${item.memo ? `<p class="text-[13px] font-bold text-slate-600 dark:text-slate-400 mb-5 leading-relaxed whitespace-pre-wrap">${item.memo}</p>` : ''}
                                ${shouldHide ? '' : `
                                <div class="flex gap-2 pt-1">
                                    <button onclick="openAmap('${placeStr}')" class="flex-1 py-3.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-2xl font-black text-[10px] shadow-sm border border-slate-200 dark:border-slate-700">지도1</button>
                                    <button onclick="openBaiduMap('${placeStr}')" class="flex-1 py-3.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-2xl font-black text-[10px] shadow-sm border border-slate-200 dark:border-slate-700">지도2</button>
                                    <button onclick="openDidi('${placeStr}')" class="flex-1 py-3.5 bg-slate-900 text-white rounded-2xl font-black text-[10px] shadow-lg">디디호출</button>
                                </div>`}
                            </div>`;
                        }).join('')}
                        </div>
                    </div>`).join('');
            }
        }

        function loadItinerary() { if(db) db.ref(`${basePath}/itinerary`).on('value', s => { const data = s.val(); if(data) { itineraryData = Object.entries(data).map(([k, v]) => ({...v, key: k})); itineraryData.sort((a,b) => String(a.date).localeCompare(String(b.date)) || String(a.time).localeCompare(String(b.time))); renderList(itineraryData); } else initialShanghai.forEach(i => db.ref(`${basePath}/itinerary`).push(i)); }); }

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
            const arrowMatch = input.match(/(?:->|→)\\s*([^(\\n]+)/);
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

        function renderPhrases() { 
            const pEl = document.getElementById('phrase-list');
            if(pEl) pEl.innerHTML = phraseData.map(group => `
                <div class="space-y-4 mb-6">
                    <h4 class="text-[12px] font-black text-slate-400 uppercase tracking-widest pl-1 italic border-b pb-2 dark:border-slate-800">${group.cat}</h4>
                    ${group.items.map(p => `<div class="bg-white dark:bg-slate-900 p-6 rounded-[2rem] shadow-sm border border-slate-100 dark:border-slate-800 flex justify-between items-center active:scale-[0.98] transition-transform" onclick="showFlashcard('${p.zh}', '${p.ko}', '${p.py}')"><div class="pr-3"><p class="text-base font-black dark:text-white leading-tight">${p.ko}</p><p class="text-[11px] text-indigo-500 font-bold mt-2 uppercase">${p.py}</p></div><button onclick="event.stopPropagation(); speak('${p.zh}')" class="w-12 h-12 rounded-2xl bg-slate-50 dark:bg-slate-800 text-slate-400 flex items-center justify-center text-xl active:text-indigo-500 shadow-inner border border-slate-100 dark:border-slate-700"><i class="fas fa-volume-up"></i></button></div>`).join('')}
                </div>`).join(''); 
        }

        function openChecklistModal(type, key = null) {
            document.getElementById('checklist-type').value = type; document.getElementById('checklist-key').value = key || '';
            document.getElementById('checklist-modal').classList.remove('hidden');
            if(key) { db.ref(`${basePath}/checklist/${key}`).once('value', s => { const d = s.val(); document.getElementById('checklist-title').value = d.title; document.getElementById('checklist-delete-btn').classList.remove('hidden'); }); }
            else { document.getElementById('checklist-title').value = ''; }
        }
        function closeChecklistModal() { document.getElementById('checklist-modal').classList.add('hidden'); }
        function saveChecklist() { const k = document.getElementById('checklist-key').value, t = document.getElementById('checklist-type').value, title = document.getElementById('checklist-title').value; if(!title) return; if(k) db.ref(`${basePath}/checklist/${k}`).update({title}); else db.ref(`${basePath}/checklist`).push({title, type: t, checked: false}); closeChecklistModal(); }

        function openItineraryForm(key = null) {
            document.getElementById('itinerary-modal').classList.remove('hidden');
            if(key) { const item = itineraryData.find(i => i.key === key); if(item) { document.getElementById('edit-key').value = key; document.getElementById('form-date').value = item.date; document.getElementById('form-time').value = item.time; document.getElementById('form-place').value = item.place; document.getElementById('form-memo').value = item.memo || ""; } }
            else { document.getElementById('edit-key').value = ''; }
        }
        function closeItineraryModal() { document.getElementById('itinerary-modal').classList.add('hidden'); }
        function saveItinerary() { const k = document.getElementById('edit-key').value, d = { date: document.getElementById('form-date').value, time: document.getElementById('form-time').value || "00:00", place: document.getElementById('form-place').value || "장소명", memo: document.getElementById('form-memo').value || "" }; if(k) db.ref(`${basePath}/itinerary/${k}`).update(d); else db.ref(`${basePath}/itinerary`).push(d); closeItineraryModal(); }
        function deleteItinerary() { const k = document.getElementById('edit-key').value; if(k && confirm("삭제?")) { db.ref(`${basePath}/itinerary/${k}`).remove(); closeItineraryModal(); } }

        function scrollToCurrentTask() {
            try {
                const now = new Date();
                const shTime = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Shanghai"}));
                const todayStr = `${(shTime.getMonth() + 1).toString().padStart(2, '0')}-${shTime.getDate().toString().padStart(2, '0')}`;
                const curM = shTime.getHours() * 60 + shTime.getMinutes();
                let targetId = null; let minD = Infinity;
                itineraryData.forEach(item => {
                    if (item.date && item.date.includes(todayStr) && item.time) {
                        const tArr = item.time.split('~');
                        if(tArr.length > 0) {
                            const [h, m] = (tArr[0].includes(':') ? tArr[0] : '00:00').split(':').map(Number);
                            const diff = (h * 60 + m) - curM;
                            if (diff >= -60 && diff < minD) { minD = diff; targetId = `card-${item.key}`; }
                        }
                    }
                });
                if (targetId) {
                    const el = document.getElementById(targetId);
                    if (el) setTimeout(() => { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); el.parentElement.classList.add('ring-2', 'ring-indigo-500', 'rounded-[2.5rem]', 'p-1'); }, 500);
                }
            } catch(e) {}
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
    </script>
</body>
</html>"""

with codecs.open(path, 'w', encoding='utf-8') as f:
    f.write(full_html)
print("Final Super Master Pro Build (v34) complete.")
