import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def final_polish():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Simplify weather description (e.g., '비 옴' -> '비', '구름조금' -> '구름')
    weather_pattern = re.compile(r'async function fetchWeather\(\) \{.*?\}', re.DOTALL)
    weather_logic_new = """        async function fetchWeather() {
            try {
                const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=31.2222&longitude=121.4581&current_weather=true');
                const data = await res.json();
                const cw = data.current_weather;
                const temp = Math.round(cw.temperature);
                const code = cw.weathercode;
                
                let icon = 'fa-sun';
                let desc = '맑음';
                
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
    content = weather_pattern.sub(weather_logic_new, content)

    # 2. Fix Itinerary not showing: More robust sorting and ensuring renderList is called correctly
    # If itineraryData exists but renderList doesn't show anything, it might be due to grouping logic.
    # Also ensuring basePath is correct.
    
    sort_logic_old = """                        itineraryData.sort((a, b) => {
                            const dateA = a.date ? a.date.replace(/[^0-9]/g, "") : "";
                            const dateB = b.date ? b.date.replace(/[^0-9]/g, "") : "";
                            const timeA = a.time || "";
                            const timeB = b.time || "";
                            return dateA.localeCompare(dateB) || timeA.localeCompare(timeB);
                        });"""

    sort_logic_new = """                        itineraryData.sort((a, b) => {
                            const dateA = String(a.date || "").replace(/[^0-9]/g, "");
                            const dateB = String(b.date || "").replace(/[^0-9]/g, "");
                            const timeA = String(a.time || "");
                            const timeB = String(b.time || "");
                            if (dateA !== dateB) return dateA.localeCompare(dateB);
                            return timeA.localeCompare(timeB);
                        });"""
    content = content.replace(sort_logic_old, sort_logic_new)

    # Ensure Firebase is initialized correctly with the right variable 'db'
    # Also checking if renderList has any potential JS errors.
    
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    final_polish()
    print("Done")
