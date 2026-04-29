import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def fix_subway_ui():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Spot Modal HTML to include Subway input
    old_modal_fields = '''            <input type="text" id="spot-name-zh" placeholder="중문 명칭 (예: 豫园)" class="w-full p-4 rounded-2xl bg-slate-100 dark:bg-slate-800 border-none font-black text-base outline-none">
            <input type="text" id="spot-addr" placeholder="상세 주소 (선택)" class="w-full p-4 rounded-2xl bg-slate-100 dark:bg-slate-800 border-none font-black text-base outline-none">'''

    new_modal_fields = '''            <input type="text" id="spot-name-zh" placeholder="중문 명칭 (예: 豫园)" class="w-full p-4 rounded-2xl bg-slate-100 dark:bg-slate-800 border-none font-black text-base outline-none">
            <input type="text" id="spot-subway" placeholder="지하철 정보 (예: 2호선 난징동루역)" class="w-full p-4 rounded-2xl bg-slate-100 dark:bg-slate-800 border-none font-black text-base outline-none">
            <input type="text" id="spot-addr" placeholder="상세 주소 (선택)" class="w-full p-4 rounded-2xl bg-slate-100 dark:bg-slate-800 border-none font-black text-base outline-none">'''

    if 'id="spot-subway"' not in content:
        content = content.replace(old_modal_fields, new_modal_fields)

    # 2. Update renderSpots to show subway info
    render_old = '<h4 class="font-black text-lg">${s.nameKo}</h4><p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p></div>'
    render_new = """<h4 class="font-black text-lg">${s.nameKo}</h4>
                            <p class="text-xs font-bold text-slate-400 mt-1">${s.nameZh}</p>
                            ${s.subway ? `<p class="text-[10px] font-bold text-indigo-600 mt-2 flex items-center bg-indigo-50 dark:bg-indigo-900/20 px-2 py-1.5 rounded-lg w-fit"><i class="fas fa-subway mr-1.5"></i>${s.subway}</p>` : ''}</div>"""

    if 's.subway ?' not in content:
        content = content.replace(render_old, render_new)

    # 3. Update openSpotModal to load subway value
    open_modal_old = "document.getElementById('spot-name-zh').value = s.nameZh;"
    open_modal_new = "document.getElementById('spot-name-zh').value = s.nameZh; document.getElementById('spot-subway').value = s.subway || '';"
    if "document.getElementById('spot-subway').value =" not in content:
        content = content.replace(open_modal_old, open_modal_new)

    # 4. Update saveSpot to save subway value
    save_old = "nameZh: document.getElementById('spot-name-zh').value,"
    save_new = "nameZh: document.getElementById('spot-name-zh').value, subway: document.getElementById('spot-subway').value,"
    if "subway: document.getElementById('spot-subway').value" not in content:
        content = content.replace(save_old, save_new)

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_subway_ui()
    print("UI update applied.")
