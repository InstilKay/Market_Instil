import streamlit as st
import pandas as pd
from PIL import Image
import webbrowser

# Set page configuration
st.set_page_config(
    page_title="StyleHub - Modern Shopping",
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
    .product-image {
        border-radius: 10px;
        margin-bottom: 12px;
        height: 200px;
        object-fit: cover;
        width: 100%;
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
        padding: 10px 20px;
        margin: 5px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .category-button:hover {
        background-color: #FF4B4B;
        color: white;
    }
    .selected-category {
        background-color: #FF4B4B;
        color: white;
    }
    .stats-container {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sample product data with availability and prices in Ghana Cedis
products = [
    {
        "id": 1,
        "name": "Premium Wireless Headphones",
        "price": 1150.00,
        "original_price": 199.99,
        "category": "Electronics",
        "stock": 15,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8aGVhZHBob25lc3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 2,
        "name": "Designer Leather Watch",
        "price": 920.00,
        "original_price": 159.99,
        "category": "Accessories",
        "stock": 8,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2F0Y2h8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 3,
        "name": "Casual Summer Dress",
        "price": 290.00,
        "original_price": 49.99,
        "category": "Clothing",
        "stock": 22,
        "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZHJlc3N8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 4,
        "name": "Smart Fitness Tracker",
        "price": 520.00,
        "original_price": 89.99,
        "category": "Electronics",
        "stock": 3,
        "image_url": "https://images.unsplash.com/photo-1576243345690-4e4b79b63288?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGZpdG5lc3MlMjB0cmFja2VyfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 5,
        "name": "Luxury Perfume Collection",
        "price": 750.00,
        "original_price": 129.99,
        "category": "Beauty",
        "stock": 12,
        "image_url": "https://images.unsplash.com/photo-1592945403407-9de659572da9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cGVyZnVtZXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 6,
        "name": "Minimalist Sneakers",
        "price": 460.00,
        "original_price": 79.99,
        "category": "Footwear",
        "stock": 0,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c25lYWtlcnN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 7,
        "name": "Designer Handbag",
        "price": 1730.00,
        "original_price": 299.99,
        "category": "Accessories",
        "stock": 5,
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGFuZGJhZ3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60"
    },
    {
        "id": 8,
        "name": "Wireless Charging Pad",
        "price": 230.00,
        "original_price": 39.99,
        "category": "Electronics",
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1579118126029-8f2c813b5b82?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8d2lyZWxlc3MlMjBjaGFyZ2VyfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60"
    }
]

# Function to create WhatsApp message
def create_whatsapp_message(product_name, product_price):
    phone_number = "+233275696789"
    message = f"Hello! I would like to buy the {product_name} for GHS {product_price:.2f}. Please let me know about availability and payment options."
    encoded_message = message.replace(" ", "%20").replace("!", "%21")
    return f"https://wa.me/{phone_number}?text={encoded_message}"

# Header section
st.markdown('<h1 class="main-header">🛍️ PIKA Hub Ghana</h1>', unsafe_allow_html=True)
st.markdown("### Discover the latest trends and shop your favorite products")

# Sidebar with categories and statistics
st.sidebar.markdown("## 🔍 Categories")
categories = ["All", "Electronics", "Clothing", "Accessories", "Beauty", "Footwear"]
selected_category = st.sidebar.radio("", categories)

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
if selected_category != "All":
    filtered_products = [p for p in products if p["category"] == selected_category]
else:
    filtered_products = products

# Display category statistics
available_in_category = sum(1 for p in filtered_products if p["stock"] > 0)
st.markdown(f'<div class="stats-container">', unsafe_allow_html=True)
st.markdown(f"**{selected_category} Category:** {len(filtered_products)} products ({available_in_category} available, {len(filtered_products) - available_in_category} out of stock)")
st.markdown('</div>', unsafe_allow_html=True)

# Display products in a grid
st.markdown(f'<div class="sub-header">{selected_category} Products</div>', unsafe_allow_html=True)

# Create columns for product grid
cols = st.columns(4)

for index, product in enumerate(filtered_products):
    with cols[index % 4]:
        # Product card
        st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
        st.image(product["image_url"], use_column_width=True)
        st.markdown(f'<div class="product-title">{product["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="product-price">GHS {product["price"]:.2f}</div>', unsafe_allow_html=True)
        
        # Display stock information
        if product["stock"] > 0:
            stock_class = "low-stock" if product["stock"] < 5 else ""
            st.markdown(f'<div class="product-stock {stock_class}">In stock: {product["stock"]} available</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="product-stock low-stock">Out of stock</div>', unsafe_allow_html=True)
        
        # Buy button that opens WhatsApp (disabled if out of stock)
        if product["stock"] > 0:
            if st.button("Buy Now", key=product["id"]):
                whatsapp_url = create_whatsapp_message(product["name"], product["price"])
                webbrowser.open_new_tab(whatsapp_url)
                st.success("Redirecting to WhatsApp...")
        else:
            st.button("Out of Stock", key=product["id"], disabled=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        <p>© 2023 StyleHub Ghana - Modern Shopping Experience</p>
        <p>All prices in Ghana Cedis (GHS) | Contact us: +233 27 569 6789 | email@stylehub.com</p>
    </div>
    """,
    unsafe_allow_html=True
)
