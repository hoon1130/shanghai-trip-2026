import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def safe_reconstruct_v33():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix fetchWeather with Safe Encoding
    weather_logic = """        async function fetchWeather() {
            try {
                const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=31.2222&longitude=121.4581&current_weather=true');
                const data = await res.json();
                const cw = data.current_weather;
                const temp = Math.round(cw.temperature);
                const code = cw.weathercode;
                let icon = 'fa-sun'; let desc = '\\ub9d1\\uc74c';
                if (code >= 1 && code <= 3) { icon = 'fa-cloud-sun'; desc = '\\uad6c\\ub984'; }
                else if (code >= 45 && code <= 48) { icon = 'fa-smog'; desc = '\\uc548\\uac1c'; }
                else if (code >= 51 && code <= 67) { icon = 'fa-cloud-showers-heavy'; desc = '\\ube44'; }
                else if (code >= 71 && code <= 77) { icon = 'fa-snowflake'; desc = '\\ub208'; }
                else if (code >= 80 && code <= 82) { icon = 'fa-cloud-rain'; desc = '\\uc18c\\ub098\\uae30'; }
                else if (code >= 95) { icon = 'fa-bolt'; desc = '\\ub1cc\\uc6b0'; }
                const el = document.getElementById('weather-display');
                if(el) el.innerHTML = `<i class="fas ${icon} mr-2 text-indigo-500"></i>\\uc0c1\\ud574 ${temp}\\u00B0C / ${desc}`;
            } catch(e) {
                const el = document.getElementById('weather-display');
                if(el) el.innerText = 'Weather...';
            }
        }"""
    
    content = re.sub(r'async function fetchWeather\(\) \{.*?\}', weather_logic, content, flags=re.DOTALL)

    # 2. Fix translateAction with Safe Encoding
    translate_logic = """        async function translateAction() {
            const input = document.getElementById('trans-input').value.trim();
            const resultBox = document.getElementById('trans-result-box');
            const resultText = document.getElementById('trans-result-text');
            const speakBtn = document.getElementById('trans-speak-btn');
            const btnIcon = document.getElementById('trans-btn-icon');
            if (!input) return alert('\\ub124\\uc6a9\\uc744 \\uc785\\ub825\\ud574\\uc8fc\\uc138\\uc6a4.');
            btnIcon.className = 'fas fa-spinner fa-spin';
            resultBox.classList.remove('hidden');
            resultText.innerText = '...';
            try {
                const isKorean = /[\\u3131-\\u318E|\\uAC00-\\uD7A3]/.test(input);
                const target = isKorean ? 'zh-CN' : 'ko';
                const response = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${target}&dt=t&q=${encodeURIComponent(input)}`);
                const data = await response.json();
                const translated = data[0].map(item => item[0]).join('');
                resultText.innerText = translated;
                btnIcon.className = 'fas fa-paper-plane';
                if (target === 'zh-CN') {
                    speakBtn.classList.remove('hidden');
                    speakBtn.onclick = () => speak(translated);
                } else { speakBtn.classList.add('hidden'); }
            } catch (e) {
                resultText.innerText = 'Error';
                btnIcon.className = 'fas fa-paper-plane';
            }
        }"""
    
    # Remove any stray translate functions and inject clean one
    content = re.sub(r'async function translateAction\(\) \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'function goPapago\(src, tgt\) \{.*?\}', '', content, flags=re.DOTALL)
    
    # Find a safe insertion point: after fetchWeather
    content = content.replace(weather_logic, weather_logic + "\n\n" + translate_logic)

    # 3. Final Cleanup of any stray corrupted characters
    content = content.replace('째C', '°C')
    # Remove the broken 'else if' block that was leaking outside functions
    content = re.sub(r'\}\s*?else if \(code >= 45 && code <= 48\).*?鍮\s*?; \}', '}', content, flags=re.DOTALL)

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    safe_reconstruct_v33()
    print("Safe Reconstruction Applied.")
