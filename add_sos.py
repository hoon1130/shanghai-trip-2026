import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def update_sos_features():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Header: Add Emergency Button (🚨)
    old_header_btns = """<button onclick="toggleTheme()" class="w-9 h-9 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-500 shadow-sm border border-slate-200 dark:border-slate-700">"""
    
    new_header_btns = """<button onclick="openSOSModal()" class="w-9 h-9 rounded-full bg-red-500 text-white flex items-center justify-center shadow-md active:scale-90 transition-transform">
                    <span class="animate-pulse">🚨</span>
                </button>
                """ + old_header_btns

    if 'openSOSModal()' not in content:
        content = content.replace(old_header_btns, new_header_btns)

    # 2. SOS Modal and Huge Card HTML
    sos_modal_html = """
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
    </div>
"""
    if 'id="sos-modal"' not in content:
        content = content.replace('</body>', sos_modal_html + '\n</body>')

    # 3. Add JS Logic for SOS
    js_sos_logic = """
        function openSOSModal() { document.getElementById('sos-modal').classList.remove('hidden'); }
        function closeSOSModal() { document.getElementById('sos-modal').classList.add('hidden'); }
        function showHotelCard() { document.getElementById('hotel-card').classList.remove('hidden'); closeSOSModal(); }
        function showHelpPhrase(ko, zh, py) { if(typeof showFlashcard === 'function') showFlashcard(zh, ko, py); closeSOSModal(); }
"""
    if 'function openSOSModal()' not in content:
        # Injecting into the script area
        content = content.replace('function openMetro(keyword) {', js_sos_logic + '\n\n        function openMetro(keyword) {')

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_sos_features()
