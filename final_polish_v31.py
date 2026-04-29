import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def final_polish_v31():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean the duplicated/broken loop block in loadSpots
    broken_pattern = re.compile(r'initialSpots\.forEach\(init => \{.*?\}\);\s*?\}\s*?\}\s*?\}\s*?\);', re.DOTALL)
    # This is risky. Let's just rebuild the loadSpots function from scratch to be 100% safe.
    
    load_spots_start = content.find('function loadSpots()')
    render_phrases_start = content.find('function renderPhrases()')
    
    if load_spots_start != -1 and render_phrases_start != -1:
        clean_load_spots = """function loadSpots() {
            if(!db) return;
            db.ref(`${basePath}/spots`).on('value', s => {
                const data = s.val();
                if(data) {
                    spotData = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                    initialSpots.forEach(init => {
                        const existingItem = spotData.find(item => item.nameZh === init.nameZh || item.nameKo === init.nameKo);
                        if (!existingItem) {
                            db.ref(`${basePath}/spots`).push(init);
                        } else {
                            db.ref(`${basePath}/spots/${existingItem.key}`).update({ 
                                subway: init.subway,
                                addr: init.addr
                            });
                        }
                    });
                } else {
                    initialSpots.forEach(i => db.ref(`${basePath}/spots`).push(i));
                }
                renderSpots();
            });
        }

        """
        content = content[:load_spots_start] + clean_load_spots + content[render_phrases_start:]

    # 2. Re-verify degree symbols and Pinyin keywords
    content = content.replace('째C', '°C')
    
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    final_polish_v31()
    print("Final polish applied.")
