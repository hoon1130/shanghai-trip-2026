import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def final_fix():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, identify if we have the Spot Tab structure.
    # If not, it's a very old version.
    
    # Let's just do a surgical cleanup of the broken script area first.
    # The broken area starts with async function fetchWeather() and ends with some corrupted logic.
    
    # Remove all duplicated fetchWeather blocks
    content = re.sub(r'async function fetchWeather\(\) \{.*?\}\s*?\}\s*?\}°C`;.*?\} catch\(e\) \{\}', '', content, flags=re.DOTALL)
    # The above is too specific. Let's try to find the whole script block and fix it.
    
    script_start = content.find('<script>')
    script_end = content.rfind('</script>')
    
    if script_start != -1 and script_end != -1:
        # I'll keep the script start tag and replace the inside.
        # But wait, I need to preserve the data if it's there.
        pass

    # Actually, the user wants me to NOT lose content.
    # The most problematic area is between "function speak" and "function toggleTheme".
    
    speak_pos = content.find('function speak(text)')
    theme_pos = content.find('function toggleTheme()')
    
    if speak_pos != -1 and theme_pos != -1:
        clean_weather = """function speak(text) { try { const u = new SpeechSynthesisUtterance(text); u.lang = 'zh-CN'; u.rate = 0.8; window.speechSynthesis.speak(u); } catch(e){} }
        
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
                if(el) el.innerHTML = `<i class="fas ${icon} mr-2 text-indigo-500"></i>상해 ${temp}\\u00B0C / ${desc}`;
            } catch(e) {
                const el = document.getElementById('weather-display');
                if(el) el.innerText = '날씨 확인 중...';
            }
        }

        """
        content = content[:speak_pos] + clean_weather + content[theme_pos:]

    # Fix initialization block (DOMContentLoaded)
    init_start = content.find("document.addEventListener('DOMContentLoaded'")
    if init_start != -1:
        # Replace the entire DOMContentLoaded block with a fresh one
        new_init = """document.addEventListener('DOMContentLoaded', () => {
            const firebaseConfig = { databaseURL: "https://nhatrang-trip-default-rtdb.asia-southeast1.firebasedatabase.app" };
            try { if (!firebase.apps.length) firebase.initializeApp(firebaseConfig); db = firebase.database(); } catch(e) { console.error(e); }
            
            const cny = document.getElementById('cny-input'), krw = document.getElementById('krw-input');
            if(cny && krw) {
                cny.addEventListener('input', (e) => krw.value = e.target.value ? Math.round(e.target.value * exchangeRate) : '');
                krw.addEventListener('input', (e) => cny.value = e.target.value ? (e.target.value / exchangeRate).toFixed(2) : '');
            }
            const erEl = document.getElementById('exchange-rate-display');
            if (erEl) erEl.innerText = `1¥ = ${exchangeRate}₩`;
            
            fetchWeather(); renderPhrases(); loadItinerary(); loadExpenses(); loadChecklist(); loadSpots();
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('sw.js').then(reg => {
                    reg.onupdatefound = () => {
                        const installingWorker = reg.installing;
                        installingWorker.onstatechange = () => {
                            if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                console.log('New content available.');
                            }
                        };
                    };
                }).catch(()=>{});
                let refreshing;
                navigator.serviceWorker.addEventListener('controllerchange', () => { if (refreshing) return; window.location.reload(); refreshing = true; });
            }
        });"""
        
        # Finding the end of the current DOMContentLoaded
        # This is tricky, I'll search for the last }); before </body>
        last_body = content.find('</body>')
        init_end = content.rfind('});', 0, last_body)
        if init_end != -1:
            content = content[:init_start] + new_init + content[init_end+3:]

    # Remove any stray characters or corrupted patterns outside tags
    content = content.replace('\\u00B0', u'\u00B0')

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    final_fix()
