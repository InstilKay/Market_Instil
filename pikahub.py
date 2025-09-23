import streamlit as st
import pandas as pd
from PIL import Image
import urllib.parse

# Set page configuration
st.set_page_config(
    page_title="Pika StyleHub - Modern Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 48px;
        font-weight: 700;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: 600;
        color: #262730;
        margin-bottom: 20px;
    }
    .product-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s;
        height: 100%;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .product-image-container {
        position: relative;
        border-radius: 10px;
        margin-bottom: 12px;
        height: 200px;
        overflow: hidden;
        background-color: #f8f9fa;
    }
    .product-main-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 10px;
    }
    .image-counter {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
    }
    .product-title {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 8px;
        height: 40px;
        overflow: hidden;
    }
    .product-price {
        font-weight: 700;
        color: #FF4B4B;
        font-size: 18px;
        margin-bottom: 8px;
    }
    .product-description {
        font-weight: 400;
        color: #666;
        font-size: 14px;
        margin-bottom: 8px;
        font-style: italic;
    }
    .product-stock {
        font-weight: 500;
        color: #666;
        font-size: 14px;
        margin-bottom: 12px;
    }
    .low-stock {
        color: #FF4B4B;
        font-weight: 600;
    }
    .buy-button {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        width: 100%;
        border: none;
    }
    .buy-button:hover {
        background-color: #128C7E !important;
    }
    .buy-button:disabled {
        background-color: #CCCCCC !important;
        cursor: not-allowed;
    }
    .category-button {
        background-color: #F0F2F6;
        border-radius: 8px;
        padding: 12px 20px;
        margin: 8px 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        border: 2px solid transparent;
    }
    .category-button:hover {
        background-color: #FF4B4B;
        color: white;
        border-color: #FF4B4B;
        transform: scale(1.05);
    }
    .selected-category {
        background-color: #FF4B4B !important;
        color: white !important;
        border-color: #FF4B4B !important;
    }
    .stats-container {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    /* Style for WhatsApp link buttons */
    .whatsapp-link {
        display: inline-block;
        background-color: #25D366;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
        width: 100%;
        margin-top: 10px;
    }
    .whatsapp-link:hover {
        background-color: #128C7E;
        color: white;
    }
    .menu-header {
        font-size: 24px;
        font-weight: 700;
        color: #FF4B4B;
        margin-bottom: 15px;
        text-align: center;
        padding: 10px;
        background-color: #F8F9FA;
        border-radius: 8px;
    }
    .main-menu-button {
        background-color: #FF4B4B;
        color: white;
        padding: 15px 30px;
        font-size: 20px;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        margin: 20px auto;
        display: block;
        text-align: center;
    }
    .main-menu-button:hover {
        background-color: #E63B3B;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Sample product data with multiple images support
products = [
    {
        "id": 1,
        "name": "Premium Wireless Headphones",
        "price": 1150.00,
        "category": "Electronics",
        "stock": 15,
        "whatsapp_number": "233275696787",
        "image_urls": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8aGVhZHBob25lc3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8aGVhZHBob25lc3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60"
        ]
    },
    {
        "id": 2,
        "name": "Designer Leather Watch",
        "price": 920.00,
        "category": "Accessories",
        "stock": 8,
        "whatsapp_number": "233275696787",
        "image_urls": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2F0Y2h8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"
        ]
    },
    {
        "id": 3,
        "name": "Casual Summer Dress",
        "price": 290.00,
        "category": "Clothing",
        "stock": 22,
        "whatsapp_number": "233275696787",
        "image_urls": [
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZHJlc3N8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"
        ]
    },
    {
        "id": 4,
        "name": "Samsung Galaxy s22",
        "price": 5200.00,
        "category": "Electronics",
        "stock": 3,
        "whatsapp_number": "233246729676",
        "description": "8GB RAM and 256GB storage",
        "image_urls": [
            "https://i.imgur.com/HCfqBWJ.jpeg",
            "https://app.box.com/index.php?rm=box_download_shared_file&shared_name=fir7mmj0cdian7kyw5q5bxcifj7u4462&file_id=f_1993599277353",
            "https://app.box.com/index.php?rm=box_download_shared_file&shared_name=xks2f0cyxepasq7rcb4n3ebyru6okbyx&file_id=f_1993599956661"
        ]
    },
    {
        "id": 5,
        "name": "Toyota Corrolla 2007 model",
        "price": 65000.00,
        "category": "Electronics",
        "stock": 1,
        "whatsapp_number": "233275696787",
        "description": "Totoya Corrola 2012 registered with reverse camera and Alley rims",
        "image_urls": [
            "https://i.imgur.com/H0009Rv.jpeg",
            "https://i.imgur.com/8cBjcjA.jpeg",
            "https://i.imgur.com/es6AzB2.jpeg",
            "https://i.imgur.com/4CWA1LD.jpeg",
            "https://i.imgur.com/wdIpeE6.jpeg"
        ]
    }
]

# Function to create WhatsApp message
def create_whatsapp_message(product_name, product_price, whatsapp_number):
    message = f"Hello! I would like to buy the {product_name} for GHS {product_price:.2f}. Please let me know about availability and payment options."
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{whatsapp_number}?text={encoded_message}"

# Initialize session state for image selection
if 'selected_image_index' not in st.session_state:
    st.session_state.selected_image_index = {}

# Function to handle image selection
def get_selected_image_index(product_id):
    return st.session_state.selected_image_index.get(product_id, 0)

def set_selected_image_index(product_id, index):
    st.session_state.selected_image_index[product_id] = index

# Initialize session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "All"
if 'show_categories' not in st.session_state:
    st.session_state.show_categories = False

# Header section
st.markdown('<h1 class="main-header">🛍️ Pika Market Hub Ghana</h1>', unsafe_allow_html=True)
st.markdown("###Discover the latest trends and shop your favorite products")

# Main Menu Button on Homepage
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📋 OPEN MENU", key="main_menu_button", use_container_width=True):
        st.session_state.show_categories = not st.session_state.show_categories

# Display categories if menu is open
if st.session_state.show_categories:
    st.markdown("---")
    st.markdown("### 🏷️ Product Categories")
    
    categories = ["All", "Electronics", "Clothing", "Accessories", "Beauty", "Footwear","Food"]
    
    # Create a grid of category buttons
    cols = st.columns(3)
    for i, category in enumerate(categories):
        with cols[i % 3]:
            if st.button(f"📦 {category}", key=f"main_cat_{category}", use_container_width=True):
                st.session_state.selected_category = category
                st.session_state.show_categories = False
                st.rerun()

# Sidebar with categories and statistics
st.sidebar.markdown('<div class="menu-header">📋 QUICK MENU</div>', unsafe_allow_html=True)

categories = ["All", "Electronics", "Clothing", "Accessories", "Beauty", "Footwear","Food"]

# Create category buttons in sidebar
for category in categories:
    if st.sidebar.button(
        f"🏷️ {category}", 
        key=f"sidebar_cat_{category}",
        use_container_width=True
    ):
        st.session_state.selected_category = category
        st.rerun()

# Display selected category
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Selected Category:** {st.session_state.selected_category}")

# Display inventory statistics in sidebar
total_products = len(products)
available_products = sum(1 for p in products if p["stock"] > 0)
out_of_stock_products = total_products - available_products

st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Inventory Stats")
st.sidebar.metric("Total Products", total_products)
st.sidebar.metric("Available Products", available_products)
st.sidebar.metric("Out of Stock", out_of_stock_products)

# Filter products by category
if st.session_state.selected_category != "All":
    filtered_products = [p for p in products if p["category"] == st.session_state.selected_category]
else:
    filtered_products = products

# Display category statistics
available_in_category = sum(1 for p in filtered_products if p["stock"] > 0)
st.markdown(f'<div class="stats-container">', unsafe_allow_html=True)
st.markdown(f"**{st.session_state.selected_category} Category:** {len(filtered_products)} products ({available_in_category} available, {len(filtered_products) - available_in_category} out of stock)")
st.markdown('</div>', unsafe_allow_html=True)

# Display products in a grid
st.markdown(f'<div class="sub-header">{st.session_state.selected_category} Products</div>', unsafe_allow_html=True)

# Create columns for product grid
cols = st.columns(4)

for index, product in enumerate(filtered_products):
    with cols[index % 4]:
        # Product card
        st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
        
        # Handle multiple images with carousel
        if len(product["image_urls"]) > 0:
            current_index = get_selected_image_index(product["id"])
            total_images = len(product["image_urls"])
            
            # Image container with carousel
            st.markdown(f'''
            <div class="product-image-container">
                <img src="{product["image_urls"][current_index]}" class="product-main-image" alt="{product["name"]}">
                <div class="image-counter">{current_index + 1}/{total_images}</div>
            ''', unsafe_allow_html=True)
            
            # Navigation buttons (only show if multiple images)
            if total_images > 1:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("◀", key=f"prev_{product['id']}"):
                        new_index = (current_index - 1) % total_images
                        set_selected_image_index(product["id"], new_index)
                        st.rerun()
                
                with col3:
                    if st.button("▶", key=f"next_{product['id']}"):
                        new_index = (current_index + 1) % total_images
                        set_selected_image_index(product["id"], new_index)
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="product-title">{product["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-price">GHS {product["price"]:.2f}</div>', unsafe_allow_html=True)
        
        # Add description if it exists - MOVED INSIDE THE PRODUCT LOOP
        if "description" in product:
            st.markdown(f'<div class="product-description">{product["description"]}</div>', unsafe_allow_html=True)
        
        # Display stock information
        if product["stock"] > 0:
            stock_class = "low-stock" if product["stock"] < 5 else ""
            st.markdown(f'<div class="product-stock {stock_class}">In stock: {product["stock"]} available</div>', unsafe_allow_html=True)
            
            # Create WhatsApp link
            whatsapp_url = create_whatsapp_message(product["name"], product["price"], product["whatsapp_number"])
            st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-link">Buy Now on WhatsApp</a>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="product-stock low-stock">Out of stock</div>', unsafe_allow_html=True)
            st.markdown(f'<button class="buy-button" disabled>Out of Stock</button>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        <p>© 2023 StyleHub Ghana - Modern Shopping Experience</p>
        <p>All prices in Ghana Cedis (GHS) | Contact us: +233 27 569 6787 | instilpee@gmail.com</p>
        <p><strong>Disclaimer:</strong>Please note this application is solely responsible for connecting buyers to sellers only, any other due diligue is your responsiblity </p>
        <p>Click "Buy Now on WhatsApp" to contact us directly about your order</p>
    </div>
    """,
    unsafe_allow_html=True
)
