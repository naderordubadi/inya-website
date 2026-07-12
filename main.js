document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('product-grid');
  
  try {
    const response = await fetch('/products.json');
    const products = await response.json();
    
    products.forEach(product => {
      const sku = product.sku;
      const tiktokId = product.tiktok_id;
      const title = product.title;
      const handle = product.handle;
      const imgSrc = product.image || '/images/beyaz_zemin.jpg'; // Fallback
      
      const price = product.price ? `$${product.price}` : '';
      
      const card = document.createElement('div');
      card.className = 'product-card';
      
      card.innerHTML = `
        <a href="/products/${handle}.html" style="text-decoration: none; color: inherit; display: block;">
          <div class="image-wrapper">
            <img src="${imgSrc}" alt="${title}" class="product-image" onerror="this.src='https://via.placeholder.com/400x400?text=Image+Coming+Soon'">
          </div>
          <h3 class="product-title">${title}</h3>
          <span class="product-sku">${sku}</span>
          <span class="product-price">${price}</span>
        </a>
        <a href="https://www.tiktok.com/view/product/${tiktokId}" target="_blank" rel="noopener noreferrer" class="buy-btn">Buy on TikTok</a>
      `;
      
      grid.appendChild(card);
    });
    
  } catch (error) {
    console.error('Error loading products:', error);
    grid.innerHTML = '<p>Error loading collection.</p>';
  }
});
