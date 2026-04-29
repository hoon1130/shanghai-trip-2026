import codecs

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'
with codecs.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """
        function openPapagoCamera() {
            const webUrl = 'https://papago.naver.com/?sk=auto&tk=ko&hn=0&st=';
            const appUrl = 'naverpapago://image_translate';
            const start = Date.now();
            window.location.href = appUrl;
            setTimeout(() => {
                if (Date.now() - start < 2500) {
                    window.open(webUrl, '_blank');
                }
            }, 2000);
        }
"""

if 'function openPapagoCamera()' not in content:
    # Insert after toggleTheme
    target = 'function toggleTheme() {'
    idx = content.find(target)
    if idx != -1:
        end_idx = content.find('}', idx) + 1
        content = content[:end_idx] + new_func + content[end_idx:]
        with codecs.open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success")
    else:
        print("ToggleTheme not found")
else:
    print("Already exists")
