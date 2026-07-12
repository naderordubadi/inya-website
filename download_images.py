import re
import os
import urllib.request
from urllib.parse import urlparse

def download_images():
    html_file = 'shopify_homepage.html'
    image_dir = 'public/images'
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all shopify CDN image links
    # example: //inyanewyork.com/cdn/shop/files/image.jpg
    pattern = r'//inyanewyork\.com/cdn/shop/files/[^"\s\?]+'
    matches = set(re.findall(pattern, content))
    
    print(f"Found {len(matches)} unique image links.")
    
    for url in matches:
        if not url.startswith('http'):
            full_url = 'https:' + url
        else:
            full_url = url
            
        filename = os.path.basename(urlparse(full_url).path)
        filepath = os.path.join(image_dir, filename)
        
        # Don't download if it already exists
        if not os.path.exists(filepath):
            try:
                print(f"Downloading {filename}...")
                import ssl
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, context=ctx) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Failed to download {full_url}: {e}")

if __name__ == '__main__':
    download_images()
