import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def upgrade_translator():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Reconstruct Translator HTML Section
    translator_old_pattern = re.compile(r'<!-- Translator Section -->.*?</div>\s*?</div>\s*?</div>', re.DOTALL)
    
    translator_new_html = """<!-- Translator Section -->
            <div class="bg-white dark:bg-slate-900 p-6 rounded-[2.5rem] border border-slate-200 dark:border-slate-800 shadow-md space-y-4 mb-6">
                <div class="flex justify-between items-center px-1">
                    <h3 class="font-black text-brand-500 italic uppercase tracking-tighter flex items-center text-sm"><i class="fas fa-magic mr-2 text-xl"></i>Auto Translator</h3>
                    <button onclick="window.open('https://papago.naver.com/?sk=auto&tk=ko&hn=0&st=', '_blank')" class="text-[10px] font-black text-slate-400 underline uppercase flex items-center"><i class="fas fa-camera mr-1"></i>Camera Translate</button>
                </div>
                <div class="space-y-3">
                    <div class="relative">
                        <textarea id="trans-input" placeholder="한글 또는 중국어를 입력하세요" class="w-full p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border-none font-bold text-sm outline-none h-24 shadow-inner"></textarea>
                        <button onclick="translateAction()" class="absolute right-3 bottom-3 bg-slate-900 text-white w-10 h-10 rounded-xl shadow-lg active:scale-90 transition-transform flex items-center justify-center">
                            <i id="trans-btn-icon" class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                    
                    <!-- Result Area -->
                    <div id="trans-result-box" class="hidden p-5 rounded-2xl bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-100 dark:border-indigo-800 relative group animate-pulse">
                        <p id="trans-result-text" class="font-black text-lg text-indigo-900 dark:text-indigo-100 leading-tight pr-8"></p>
                        <button id="trans-speak-btn" class="absolute right-4 top-1/2 -translate-y-1/2 text-indigo-400 hover:text-indigo-600 hidden">
                            <i class="fas fa-volume-up text-xl"></i>
                        </button>
                    </div>
                </div>
            </div>"""
    
    # We need to find the correct end of the translator section.
    # Looking at the previous read_file, it's roughly lines 210-240.
    content = translator_old_pattern.sub(translator_new_html, content)

    # 2. Update JS Logic: Remove goPapago and add translateAction
    # I'll replace the block from goPapago to openSOSModal
    
    js_old_pattern = re.compile(r'function goPapago\(src, tgt\) \{.*?\}', re.DOTALL)
    
    js_new_logic = """async function translateAction() {
            const input = document.getElementById('trans-input').value.trim();
            const resultBox = document.getElementById('trans-result-box');
            const resultText = document.getElementById('trans-result-text');
            const speakBtn = document.getElementById('trans-speak-btn');
            const btnIcon = document.getElementById('trans-btn-icon');

            if (!input) return alert('문장을 입력해주세요.');

            // Loading state
            btnIcon.className = 'fas fa-spinner fa-spin';
            resultBox.classList.remove('hidden', 'animate-pulse');
            resultText.innerText = '번역 중...';
            speakBtn.classList.add('hidden');

            try {
                // Auto Detect: If contains Hangul, target is Chinese, else Korean
                const isKorean = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(input);
                const target = isKorean ? 'zh-CN' : 'ko';
                const source = isKorean ? 'ko' : 'zh-CN';

                const response = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=${source}&tl=${target}&dt=t&q=${encodeURIComponent(input)}`);
                const data = await response.json();
                const translated = data[0].map(item => item[0]).join('');

                resultText.innerText = translated;
                btnIcon.className = 'fas fa-paper-plane';
                
                // Show Speak button if result is Chinese
                if (target === 'zh-CN') {
                    speakBtn.classList.remove('hidden');
                    speakBtn.onclick = () => speak(translated);
                } else {
                    speakBtn.classList.add('hidden');
                }
            } catch (e) {
                resultText.innerText = '번역 실패 (네트워크 확인 필요)';
                btnIcon.className = 'fas fa-paper-plane';
            }
        }"""
    
    content = js_old_pattern.sub(js_new_logic, content)

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    upgrade_translator()
    print("Translator upgraded to In-App Auto mode.")
