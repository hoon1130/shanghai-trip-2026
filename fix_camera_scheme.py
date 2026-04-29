import codecs
import re

path = r'C:\Users\변지훈\Downloads\shanghai-trip\index.html'
with codecs.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# naverpapago://image 는 카메라 번역 화면으로 바로 들어가는 스킴입니다.
new_func = """
        function openPapagoCamera() {
            const appUrl = 'naverpapago://image';
            const webUrl = 'https://papago.naver.com/?sk=auto&tk=ko&hn=0&st=';
            const start = Date.now();
            window.location.href = appUrl;
            setTimeout(() => {
                if (Date.now() - start < 3000) {
                    window.open(webUrl, '_blank');
                }
            }, 2500);
        }
"""

# Replace the existing function
content = re.sub(r'function openPapagoCamera\(\) \{.*?\}', new_func, content, flags=re.DOTALL)

with codecs.open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html logic updated to use naverpapago://image")
