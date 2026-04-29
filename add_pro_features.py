import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def add_pro_features():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Quick Buttons to Calculator
    cny_input_block = '''                    <div class="relative">
                        <span class="absolute left-5 top-5 text-white/50 font-black text-sm">CNY</span>
                        <input type="number" id="cny-input" placeholder="위안(¥) 입력" class="w-full p-5 pl-16 rounded-[1.5rem] bg-white/10 border border-white/10 text-white font-black outline-none text-2xl">
                    </div>'''
    quick_btns = '''
                    <div class="flex gap-2 pt-1 pb-2">
                        <button onclick="addCNY(10)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-2 rounded-xl font-bold text-sm transition-colors">+10¥</button>
                        <button onclick="addCNY(50)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-2 rounded-xl font-bold text-sm transition-colors">+50¥</button>
                        <button onclick="addCNY(100)" class="flex-1 bg-white/10 hover:bg-white/20 text-white py-2 rounded-xl font-bold text-sm transition-colors">+100¥</button>
                        <button onclick="clearCNY()" class="w-12 bg-red-500/80 text-white py-2 rounded-xl font-bold text-sm"><i class="fas fa-undo"></i></button>
                    </div>'''
    
    if "addCNY(10)" not in content:
        content = content.replace(cny_input_block, cny_input_block + quick_btns)

    # Add quick calc logic
    quick_logic = """        function addCNY(amt) {
            const el = document.getElementById('cny-input');
            const krwEl = document.getElementById('krw-input');
            const cur = parseFloat(el.value) || 0;
            el.value = cur + amt;
            krwEl.value = Math.round(el.value * exchangeRate);
        }
        function clearCNY() {
            document.getElementById('cny-input').value = '';
            document.getElementById('krw-input').value = '';
        }"""
    if "function addCNY(amt)" not in content:
        content = content.replace('// 🌟 Functions 🌟', '// 🌟 Functions 🌟\n' + quick_logic)

    # 2. Add Category to Expenses and Summary Bar
    exp_input_old = '''                <div class="flex gap-2 mb-6">
                    <input type="text" id="exp-desc"'''
    exp_input_new = '''                <!-- Expense Summary Bar -->
                <div id="expense-summary" class="flex w-full h-3 rounded-full bg-slate-100 dark:bg-slate-800 mb-6 overflow-hidden hidden"></div>
                <div id="expense-legend" class="flex flex-wrap gap-3 mb-6 text-[10px] font-black hidden"></div>

                <div class="flex gap-2 mb-6">
                    <select id="exp-cat" class="w-20 p-4 rounded-xl border dark:bg-slate-800 dark:text-white dark:border-slate-700 font-black text-[11px] outline-none bg-slate-50">
                        <option value="식비">🍔 식비</option>
                        <option value="교통">🚕 교통</option>
                        <option value="쇼핑">🛍️ 쇼핑</option>
                        <option value="기타">✨ 기타</option>
                    </select>
                    <input type="text" id="exp-desc"'''
    
    if 'id="exp-cat"' not in content:
        content = content.replace(exp_input_old, exp_input_new)

    # Update addExpense function
    add_exp_old = "function addExpense() { const d = document.getElementById('exp-desc').value, a = document.getElementById('exp-amt').value; if(d && a && db) { db.ref(`${basePath}/expenses`).push({desc: d, amt: Number(a), krwAmt: Math.round(Number(a) * exchangeRate)}); document.getElementById('exp-desc').value = ''; document.getElementById('exp-amt').value = ''; } }"
    add_exp_new = "function addExpense() { const c = document.getElementById('exp-cat') ? document.getElementById('exp-cat').value : '기타', d = document.getElementById('exp-desc').value, a = document.getElementById('exp-amt').value; if(d && a && db) { db.ref(`${basePath}/expenses`).push({cat: c, desc: d, amt: Number(a), krwAmt: Math.round(Number(a) * exchangeRate)}); document.getElementById('exp-desc').value = ''; document.getElementById('exp-amt').value = ''; } }"
    content = content.replace(add_exp_old, add_exp_new)

    # Update loadExpenses function with summary logic
    load_exp_old = "function loadExpenses() { if(db) db.ref(`${basePath}/expenses`).on('value', s => { const data = s.val() || {}; let tC = 0, tK = 0; document.getElementById('expense-list').innerHTML = Object.entries(data).map(([k, v]) => { tC += v.amt; const kAmt = v.krwAmt || Math.round(v.amt * exchangeRate); tK += kAmt; return `<div class=\"flex justify-between items-center bg-white dark:bg-slate-800 p-4 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs mb-2 shadow-sm\"><div class=\"flex flex-col\"><span class=\"font-bold\">${v.desc}</span><span class=\"text-[10px] text-slate-400\">${kAmt.toLocaleString()} ₩</span></div><span class=\"font-black text-indigo-500 text-sm\">${v.amt.toLocaleString()} ¥ <button onclick=\"db.ref('${basePath}/expenses/${k}').remove()\" class=\"ml-2 text-slate-300\">✕</button></span></div>`; }).join(''); document.getElementById('total-expense').innerHTML = `${tC.toLocaleString()} ¥ <span class=\"text-xs font-bold text-slate-400 ml-1\">(${tK.toLocaleString()} ₩)</span>`; }); }"
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

                // Render Summary Bar
                if (tC > 0) {
                    let barHtml = ''; let legendHtml = '';
                    for (const [c, amt] of Object.entries(cats)) {
                        if (amt > 0) {
                            const pct = (amt / tC * 100).toFixed(1);
                            barHtml += `<div class="h-full ${colors[c]}" style="width: ${pct}%"></div>`;
                            legendHtml += `<div class="flex items-center"><span class="w-2 h-2 rounded-full ${colors[c]} mr-1"></span>${c} <span class="opacity-60 ml-1">${pct}%</span></div>`;
                        }
                    }
                    const sumBar = document.getElementById('expense-summary');
                    const legBar = document.getElementById('expense-legend');
                    if(sumBar && legBar) {
                        sumBar.innerHTML = barHtml; sumBar.classList.remove('hidden');
                        legBar.innerHTML = legendHtml; legBar.classList.remove('hidden');
                    }
                } else {
                    const sumBar = document.getElementById('expense-summary');
                    const legBar = document.getElementById('expense-legend');
                    if(sumBar) sumBar.classList.add('hidden');
                    if(legBar) legBar.classList.add('hidden');
                }
            });
        }"""
    if "const cats =" not in content:
        content = content.replace(load_exp_old, load_exp_new)

    # 3. Add Checklist Progress Bar
    pack_title_old = '''<h3 class="font-black text-base flex items-center uppercase tracking-tighter italic text-brand-500"><i class="fas fa-check-circle mr-2 text-xl"></i>체크리스트</h3>'''
    pack_title_new = '''<div><h3 class="font-black text-base flex items-center uppercase tracking-tighter italic text-brand-500 mb-1"><i class="fas fa-check-circle mr-2 text-xl"></i>체크리스트</h3><div class="w-24 h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div id="packing-progress" class="h-full bg-brand-500 transition-all duration-500" style="width: 0%"></div></div></div>'''
    if 'id="packing-progress"' not in content:
        content = content.replace(pack_title_old, pack_title_new)

    # Update loadChecklist to update progress
    pack_progress_logic = """
                // Progress update
                const packItems = items.filter(i => i.type === 'packing');
                const pBar = document.getElementById('packing-progress');
                if (pBar && packItems.length > 0) {
                    const checked = packItems.filter(i => i.checked).length;
                    pBar.style.width = `${(checked / packItems.length) * 100}%`;
                }"""
    
    # We will inject this inside loadChecklist just before closing the 'value' event
    if "const pBar =" not in content:
        content = content.replace("if(shopEl) shopEl.innerHTML =", pack_progress_logic + "\n                if(shopEl) shopEl.innerHTML =")

    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    add_pro_features()
