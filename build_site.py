import json
import os
import shutil

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, 'public', 'products.json')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'product_template.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'public', 'products')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
with open(PRODUCTS_FILE, 'r') as f:
    products = json.load(f)

with open(TEMPLATE_FILE, 'r') as f:
    template = f.read()

# Generate pages
generated_count = 0
for product in products:
    handle = product.get('handle')
    if not handle:
        continue
        
    html = template
    html = html.replace('{{title}}', str(product.get('title', '')))
    html = html.replace('{{sku}}', str(product.get('sku', '')))
    html = html.replace('{{price}}', str(product.get('price', '')))
    
    images = product.get('images', [])
    if not images and product.get('image'):
        images = [product.get('image')]
        
    images_html = ''
    for img in images:
        images_html += f'<img src="{img}" alt="{product.get("title", "")}" class="gallery-image">'
    html = html.replace('{{images_html}}', images_html)
    html = html.replace('{{tiktok_id}}', str(product.get('tiktok_id', '')))
    
    # Body HTML
    body_html = product.get('body_html', '')
    if body_html is None:
        body_html = ''
    html = html.replace('{{body_html}}', str(body_html))
    
    output_file = os.path.join(OUTPUT_DIR, f"{handle}.html")
    with open(output_file, 'w') as f:
        f.write(html)
    generated_count += 1

print(f"Successfully generated {generated_count} product pages.")
