import json
import os
import shutil
from collections import defaultdict

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, 'public', 'products.json')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'product_template.html')
GRID_TEMPLATE_FILE = os.path.join(BASE_DIR, 'grid_template.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'public', 'products')
COLLECTIONS_DIR = os.path.join(BASE_DIR, 'public', 'collections')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(COLLECTIONS_DIR, exist_ok=True)

# Load data
with open(PRODUCTS_FILE, 'r') as f:
    products = json.load(f)

with open(TEMPLATE_FILE, 'r') as f:
    template = f.read()

with open(GRID_TEMPLATE_FILE, 'r') as f:
    grid_template = f.read()

# Generate pages
generated_count = 0
collections = defaultdict(list)

for product in products:
    handle = product.get('handle')
    if not handle:
        continue
    
    title = str(product.get('title', '')).strip()
    words = title.split()
    if not words: continue
    
    # Group by collection (first word of title, case-insensitive)
    first_word = words[0].upper()
    
    # Special case for Broadway N°1 and N°2
    if first_word == 'BROADWAY' and len(words) > 1 and words[1].upper().startswith('N°'):
        collection_name = f"BROADWAY {words[1].upper()}"
    else:
        collection_name = first_word
        
    collections[collection_name].append(product)
        
    html = template
    html = html.replace('{{title}}', title)
    html = html.replace('{{sku}}', str(product.get('sku', '')))
    html = html.replace('{{price}}', str(product.get('price', '')))
    
    images = product.get('images', [])
    if not images and product.get('image'):
        images = [product.get('image')]
        
    images_html = ''
    for img in images:
        images_html += f'<img src="{img}" alt="{title}" class="gallery-image">'
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

# Generate Collection Pages
for collection_name, col_products in collections.items():
    grid_html = ""
    for p in col_products:
        handle = p.get('handle')
        title = p.get('title', '')
        price = p.get('price', '')
        images = p.get('images', [])
        img = images[0] if images else p.get('image', '')
        
        grid_html += f"""
        <a href="/products/{handle}.html" class="product-card">
            <div class="image-wrapper">
                <img src="{img}" alt="{title}" class="product-image">
            </div>
            <h3 class="product-title">{title}</h3>
            <span class="product-price">${price}</span>
        </a>
        """
    
    # Create a URL-safe slug for the collection
    slug = collection_name.lower().replace(' ', '-').replace('°', '')
    
    col_html = grid_template.replace('{{page_title}}', collection_name + " Collection")
    col_html = col_html.replace('{{heading}}', collection_name.upper() + " COLLECTION")
    col_html = col_html.replace('{{grid_html}}', grid_html)
    
    col_file = os.path.join(COLLECTIONS_DIR, f"{slug}.html")
    with open(col_file, 'w') as f:
        f.write(col_html)

print(f"Successfully generated {len(collections)} collection pages.")

# Generate Master Collections Page (all.html)
master_grid_html = ""
for collection_name, col_products in collections.items():
    # Use the first product's image as the collection cover
    slug = collection_name.lower().replace(' ', '-').replace('°', '')
    img = col_products[0].get('images', [col_products[0].get('image', '')])[0] if col_products else ''
    
    master_grid_html += f"""
    <a href="/collections/{slug}.html" class="product-card">
        <div class="image-wrapper">
            <img src="{img}" alt="{collection_name} Collection" class="product-image">
        </div>
        <h3 class="product-title" style="text-align: center; font-size: 1.5rem;">{collection_name} COLLECTION</h3>
    </a>
    """
    
master_html = grid_template.replace('{{page_title}}', "All Collections")
master_html = master_html.replace('{{heading}}', "OUR COLLECTIONS")
master_html = master_html.replace('{{grid_html}}', master_grid_html)

master_file = os.path.join(COLLECTIONS_DIR, "all.html")
with open(master_file, 'w') as f:
    f.write(master_html)

print("Successfully generated master collections page.")
