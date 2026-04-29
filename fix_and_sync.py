import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'

def clean_and_sync():
    with codecs.open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up the corrupted loadSpots area
    # I'll replace everything from 'function loadSpots' to 'function renderPhrases' with a clean version.
    
    start_marker = 'function loadSpots()'
    end_marker = 'function renderPhrases()'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        clean_load_spots = """function loadSpots() {
            if(!db) return;
            db.ref(`${basePath}/spots`).on('value', s => {
                const data = s.val();
                if(data) {
                    spotData = Object.entries(data).map(([k, v]) => ({...v, key: k}));
                    // Migration: Add missing initial items by nameZh
                    initialSpots.forEach(init => {
                        const exists = spotData.some(item => item.nameZh === init.nameZh);
                        if (!exists) db.ref(`${basePath}/spots`).push(init);
                    });
                } else {
                    initialSpots.forEach(i => db.ref(`${basePath}/spots`).push(i));
                }
                renderSpots();
            });
        }

        """
        content = content[:start_idx] + clean_load_spots + content[end_idx:]

    # 2. Fix degree symbol and potential broken tags
    content = content.replace('째C', '°C')
    
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    clean_and_sync()
    print("Cleanup and Spot Sync logic applied.")
