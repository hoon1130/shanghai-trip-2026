import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def final_cleanup_v33():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix fetchWeather (Simplify desc and icon logic)
    weather_logic = """        async function fetchWeather() {
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
        }"""
    
    content = re.sub(r'async function fetchWeather\(\) \{.*?\}', weather_logic, content, flags=re.DOTALL)

    # 2. Add translateAction and clean up residue
    # We replace from goPapago or any translate-related function to openSOSModal
    translate_logic = """        async function translateAction() {
            const input = document.getElementById('trans-input').value.trim();
            const resultBox = document.getElementById('trans-result-box');
            const resultText = document.getElementById('trans-result-text');
            const speakBtn = document.getElementById('trans-speak-btn');
            const btnIcon = document.getElementById('trans-btn-icon');
            if (!input) return alert('문장을 입력해주세요.');
            btnIcon.className = 'fas fa-spinner fa-spin';
            resultBox.classList.remove('hidden');
            resultText.innerText = '번역 중...';
            speakBtn.classList.add('hidden');
            try {
                const isKorean = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/.test(input);
                const target = isKorean ? 'zh-CN' : 'ko';
                const source = isKorean ? 'ko' : 'zh-CN';
                const response = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=${source}&tl=${target}&dt=t&q=${encodeURIComponent(input)}`);
                const data = await response.json();
                const translated = data[0].map(item => item[0]).join('');
                resultText.innerText = translated;
                btnIcon.className = 'fas fa-paper-plane';
                if (target === 'zh-CN') {
                    speakBtn.classList.remove('hidden');
                    speakBtn.onclick = () => speak(translated);
                } else { speakBtn.classList.add('hidden'); }
            } catch (e) {
                resultText.innerText = '번역 실패 (네트워크 확인 필요)';
                btnIcon.className = 'fas fa-paper-plane';
            }
        }"""
    
    # Precise replacement of any goPapago residue
    content = re.sub(r'function goPapago\(src, tgt\) \{.*?\}`,\s*?\'_blank\'\);', translate_logic, content, flags=re.DOTALL)
    # If the regex above didn't catch it, try a more general one
    content = re.sub(r'function goPapago\(src, tgt\) \{.*?\}', translate_logic, content, flags=re.DOTALL)

    # 3. Final Encoding/Symbol Clean
    content = content.replace('째C', '°C')

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    final_cleanup_v33()
    print("In-App Translator Logic fixed.")
