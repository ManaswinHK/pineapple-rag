import urllib.request
import urllib.parse
from html.parser import HTMLParser

START_URL = "https://roots-and-rays.vercel.app/"
DOMAIN = urllib.parse.urlparse(START_URL).netloc

visited = set()
data = []

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.links = []
        self.in_script_or_style = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.in_script_or_style = True
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_script_or_style = False

    def handle_data(self, data):
        if not self.in_script_or_style:
            self.text_content.append(data)

def scrape(url):
    if url in visited:
        return
    visited.add(url)
    try:
        print(f"Scraping: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        parser = MyHTMLParser()
        parser.feed(html)
        
        text = ''.join(parser.text_content)
        # clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        data.append(f"URL: {url}\n\n{text}\n\n{'='*80}\n")
        
        for href in parser.links:
            if href:
                full_url = urllib.parse.urljoin(url, href)
                parsed_url = urllib.parse.urlparse(full_url)
                if parsed_url.netloc == DOMAIN and not full_url.endswith(('.png', '.jpg', '.pdf', '.svg')):
                    clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                    if clean_url not in visited:
                        scrape(clean_url)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

scrape(START_URL)

with open('knowledge_base.md', 'w', encoding='utf-8') as f:
    f.writelines(data)

print("Scraping complete. Data saved to knowledge_base.md.")
