import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Pika Market Hub Ghana",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# WHATSAPP FUNCTION
# =========================================================

def create_whatsapp_message(
    product_name,
    unit_price,
    quantity,
    whatsapp_number,
):
    """
    Create a WhatsApp order link containing the product,
    quantity, unit price and total price.
    """

    total_price = unit_price * quantity

    message = (
        "Hello! I would like to place the following order:\n\n"
        f"Product: {product_name}\n"
        f"Quantity: {quantity}\n"
        f"Unit Price: GHS {unit_price:,.2f}\n"
        f"Total Price: GHS {total_price:,.2f}\n\n"
        "Please let me know about availability, delivery "
        "and payment options."
    )

    encoded_message = urllib.parse.quote(message)

    return (
        f"https://wa.me/{whatsapp_number}"
        f"?text={encoded_message}"
    )


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
        .main-header {
            font-size: 48px;
            font-weight: 700;
            color: #FF4B4B;
            text-align: center;
            margin-bottom: 10px;
        }

        .main-description {
            text-align: center;
            color: #666666;
            font-size: 18px;
            margin-bottom: 25px;
        }

        .sub-header {
            font-size: 24px;
            font-weight: 600;
            color: #262730;
            margin-bottom: 20px;
        }

        .product-title {
            font-weight: 750;
            font-size: 16px;
            margin-bottom: 9px;
            min-height: 70px;
            overflow: hidden;
        }

        .product-price {
            font-weight: 700;
            color: #FF4B4B;
            font-size: 18px;
            margin-bottom: 8px;
        }

        .product-description {
            font-weight: 480;
            color: #666666;
            font-size: 14px;
            margin-bottom: 8px;
            font-style: italic;
            min-height: 42px;
        }

        .product-stock {
            font-weight: 500;
            color: #666666;
            font-size: 14px;
            margin-bottom: 12px;
        }

        .low-stock {
            color: #FF4B4B;
            font-weight: 600;
        }

        .stats-container {
            background-color: #F0F2F6;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .total-price {
            background-color: #F8F9FA;
            color: #FF4B4B;
            padding: 12px;
            margin-top: 5px;
            margin-bottom: 10px;
            border-radius: 8px;
            font-size: 17px;
            font-weight: 700;
            text-align: center;
        }

        .whatsapp-link {
            display: block;
            background-color: #25D366;
            color: white !important;
            padding: 10px 15px;
            text-decoration: none !important;
            border-radius: 8px;
            font-weight: 600;
            text-align: center;
            width: 100%;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .whatsapp-link:hover {
            background-color: #128C7E;
            color: white !important;
        }

        .out-of-stock-button {
            display: block;
            background-color: #CCCCCC;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: 600;
            text-align: center;
            width: 100%;
            margin-top: 10px;
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

        div[data-testid="stImage"] img {
            height: 220px;
            object-fit: cover;
            border-radius: 10px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PRODUCT DATA
# =========================================================

products = [
    {
        "id": 1,
        "name": "Car Door Mat",
        "price": 255.00,
        "category": "Accessories",
        "stock": 5,
        "whatsapp_number": "233275696787",
        "description": (
            "Can be used on both sides. Silver and black "
            "with four mats."
        ),
        "image_urls": [
            "https://i.imgur.com/3TJlx72.jpeg",
            "https://i.imgur.com/VGZJ8iM.jpeg",
        ],
    },
    {
        "id": 2,
        "name": (
            "48VH 12000 mAh Electric Car Washing "
            "Machine Water Spray"
        ),
        "price": 425.00,
        "category": "Accessories",
        "stock": 4,
        "whatsapp_number": "233275696787",
        "description": "Colour: Black",
        "image_urls": [
            "https://i.imgur.com/IptLBNh.jpeg",
            "https://i.imgur.com/TE9aAh6.jpeg",
            "https://i.imgur.com/zpHfaab.jpeg",
            "https://i.imgur.com/xLfWrez.jpeg",
            "https://i.imgur.com/hu121Vg.jpeg",
        ],
    },
    {
        "id": 3,
        "name": "Windshield Sun Shade UV Protector",
        "price": 145.00,
        "category": "Accessories",
        "stock": 5,
        "whatsapp_number": "233275696787",
        "description": "L27.56 × W57 inches",
        "image_urls": [
            (
                "https://github.com/InstilKay/Market_Instil/"
                "blob/main/psolfg-800x1091.jpg?raw=true"
            ),
            (
                "https://github.com/InstilKay/Market_Instil/"
                "blob/main/a2-800x1091.jpg?raw=true"
            ),
            (
                "https://github.com/InstilKay/Market_Instil/"
                "blob/main/edf-800x1091.jpg?raw=true"
            ),
        ],
    },
    {
        "id": 4,
        "name": (
            "Foldable Windshield Sun UV Rays "
            "Blocking Shade Umbrella"
        ),
        "price": 155.00,
        "category": "Accessories",
        "stock": 5,
        "whatsapp_number": "233246729676",
        "description": (
            "(L6.5 × W12.5) cm / "
            "(L2.55 × W4.9) inches, Small/B Style"
        ),
        "image_urls": [
            (
                "https://github.com/InstilKay/Market_Instil/"
                "blob/main/foldsunsheild.jpg?raw=true"
            ),
            (
                "https://github.com/InstilKay/Market_Instil/"
                "blob/main/foldsunshieldlength.jpg?raw=true"
            ),
        ],
    },
    {
        "id": 5,
        "name": (
            "48VH 12000 mAh Electric Car Washing "
            "Machine Water Spray"
        ),
        "price": 425.00,
        "category": "Electronics",
        "stock": 5,
        "whatsapp_number": "233275696787",
        "description": "Colour: Black, suitable for car washing.",
        "image_urls": [
            "https://i.imgur.com/IptLBNh.jpeg",
            "https://i.imgur.com/TE9aAh6.jpeg",
            "https://i.imgur.com/zpHfaab.jpeg",
            "https://i.imgur.com/xLfWrez.jpeg",
            "https://i.imgur.com/hu121Vg.jpeg",
        ],
    },
    {
        "id": 6,
        "name": "Tomatoes",
        "price": 50.00,
        "category": "Food Stuff",
        "stock": 30,
        "whatsapp_number": "233547568955",
        "description": "Price per Olonka rubber.",
        "image_urls": [
            (
                "https://github.com/InstilKay/Market_Instil/"
                "blob/main/tomatoes.jpg?raw=true"
            ),
        ],
    },
    {
        "id": 7,
        "name": "Pepper",
        "price": 15.00,
        "category": "Food Stuff",
        "stock": 30,
        "whatsapp_number": "233547568955",
        "description": "Price per Olonka rubber.",
        "image_urls": [
            (
                "https://github.com/InstilKay/Market_Instil/"
                "blob/main/Pepper.jpg?raw=true"
            ),
        ],
    },
]


# =========================================================
# SESSION STATE
# =========================================================

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"

if "show_categories" not in st.session_state:
    st.session_state.show_categories = False

if "selected_image_index" not in st.session_state:
    st.session_state.selected_image_index = {}

if "submitted_requests" not in st.session_state:
    st.session_state.submitted_requests = {}


def get_selected_image_index(product_id):
    return st.session_state.selected_image_index.get(
        product_id,
        0,
    )


def set_selected_image_index(product_id, index):
    st.session_state.selected_image_index[product_id] = index


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<h1 class="main-header">🛍️ Pika Market Hub Ghana</h1>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="main-description">
        Discover exciting products and place your request
        directly with the seller.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MAIN MENU
# =========================================================

menu_col1, menu_col2, menu_col3 = st.columns([1, 2, 1])

with menu_col2:
    if st.button(
        "📋 OPEN MENU",
        key="main_menu_button",
        use_container_width=True,
    ):
        st.session_state.show_categories = (
            not st.session_state.show_categories
        )


category_list = [
    "All",
    "Electronics",
    "Clothing",
    "Accessories",
    "Beauty",
    "Footwear",
    "Food Stuff",
]


if st.session_state.show_categories:
    st.markdown("---")
    st.markdown("### 🏷️ Product Categories")

    category_columns = st.columns(3)

    for category_index, category in enumerate(category_list):
        with category_columns[category_index % 3]:
            if st.button(
                f"📦 {category}",
                key=f"main_category_{category}",
                use_container_width=True,
            ):
                st.session_state.selected_category = category
                st.session_state.show_categories = False
                st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    '<div class="menu-header">📋 QUICK MENU</div>',
    unsafe_allow_html=True,
)

for category in category_list:
    if st.sidebar.button(
        f"🏷️ {category}",
        key=f"sidebar_category_{category}",
        use_container_width=True,
    ):
        st.session_state.selected_category = category
        st.rerun()


st.sidebar.markdown("---")
st.sidebar.markdown(
    f"**Selected Category:** "
    f"{st.session_state.selected_category}"
)


total_products = len(products)

available_products = sum(
    1 for product in products
    if product["stock"] > 0
)

out_of_stock_products = (
    total_products - available_products
)


st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Inventory Statistics")
st.sidebar.metric("Total Products", total_products)
st.sidebar.metric("Available Products", available_products)
st.sidebar.metric("Out of Stock", out_of_stock_products)


# =========================================================
# FILTER PRODUCTS
# =========================================================

if st.session_state.selected_category == "All":
    filtered_products = products
else:
    filtered_products = [
        product
        for product in products
        if product["category"]
        == st.session_state.selected_category
    ]


available_in_category = sum(
    1 for product in filtered_products
    if product["stock"] > 0
)

out_of_stock_in_category = (
    len(filtered_products) - available_in_category
)


st.markdown(
    f"""
    <div class="stats-container">
        <strong>
            {st.session_state.selected_category} Category:
        </strong>
        {len(filtered_products)} product(s),
        {available_in_category} available and
        {out_of_stock_in_category} out of stock.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="sub-header">
        {st.session_state.selected_category} Products
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DISPLAY PRODUCTS
# =========================================================

if not filtered_products:
    st.info(
        "There are currently no products in this category."
    )

else:
    product_columns = st.columns(4)

    for index, product in enumerate(filtered_products):
        with product_columns[index % 4]:


            with st.container(border=True):

                # -----------------------------------------
                # PRODUCT IMAGE CAROUSEL
                # -----------------------------------------

                image_urls = product.get("image_urls", [])

                if image_urls:
                    current_index = get_selected_image_index(
                        product["id"]
                    )

                    total_images = len(image_urls)

                    # Prevent an invalid image index.
                    if current_index >= total_images:
                        current_index = 0
                        set_selected_image_index(
                            product["id"],
                            0,
                        )

                    st.image(
                        image_urls[current_index],
                        use_container_width=True,
                    )

                    st.caption(
                        f"Image {current_index + 1} "
                        f"of {total_images}"
                    )

                    if total_images > 1:
                        previous_column, next_column = st.columns(2)

                        with previous_column:
                            if st.button(
                                "◀ Previous",
                                key=f"previous_{product['id']}",
                                use_container_width=True,
                            ):
                                new_index = (
                                    current_index - 1
                                ) % total_images

                                set_selected_image_index(
                                    product["id"],
                                    new_index,
                                )

                                st.rerun()

                        with next_column:
                            if st.button(
                                "Next ▶",
                                key=f"next_{product['id']}",
                                use_container_width=True,
                            ):
                                new_index = (
                                    current_index + 1
                                ) % total_images

                                set_selected_image_index(
                                    product["id"],
                                    new_index,
                                )

                                st.rerun()

                else:
                    st.info("No product image available.")

                # -----------------------------------------
                # PRODUCT INFORMATION
                # -----------------------------------------

                st.markdown(
                    f"""
                    <div class="product-title">
                        {product["name"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="product-price">
                        GHS {product["price"]:,.2f}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="product-description">
                        {product["description"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # -----------------------------------------
                # QUANTITY AND REQUEST SUBMISSION
                # -----------------------------------------

                if product["stock"] > 0:

                    stock_class = (
                        "low-stock"
                        if product["stock"] < 5
                        else ""
                    )

                    st.markdown(
                        f"""
                        <div class="product-stock {stock_class}">
                            In stock: {product["stock"]} available
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    quantity = st.number_input(
                        "Select quantity",
                        min_value=1,
                        max_value=int(product["stock"]),
                        value=1,
                        step=1,
                        key=f"quantity_{product['id']}",
                    )

                    total_price = (
                        product["price"] * quantity
                    )

                    st.markdown(
                        f"""
                        <div class="total-price">
                            Total: GHS {total_price:,.2f}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "🛒 Submit Request",
                        key=(
                            f"submit_request_"
                            f"{product['id']}"
                        ),
                        type="primary",
                        use_container_width=True,
                    ):
                        success, message = (
                            def save_request_to_supabase(
    product_name,
    quantity,
    unit_price,
    total_price
):
    try:

        supabase.table("orders").insert({
            "product": product_name,
            "quantity": quantity,
            "unit_price": float(unit_price),
            "total_price": float(total_price)
        }).execute()

        return True, "Request saved successfully."

    except Exception as e:
        return False, str(e)
                        )

                        if success:
                            st.session_state.submitted_requests[
                                product["id"]
                            ] = {
                                "quantity": int(quantity),
                                "unit_price": product["price"],
                                "total_price": total_price,
                            }

                            st.success(message)

                        else:
                            st.error(message)

                    # Retrieve the latest successfully
                    # submitted request for this product.
                    submitted_request = (
                        st.session_state
                        .submitted_requests
                        .get(product["id"])
                    )

                    if submitted_request:
                        submitted_quantity = (
                            submitted_request["quantity"]
                        )

                        submitted_total = (
                            submitted_request["total_price"]
                        )

                        whatsapp_url = (
                            create_whatsapp_message(
                                product_name=product["name"],
                                unit_price=product["price"],
                                quantity=submitted_quantity,
                                whatsapp_number=(
                                    product[
                                        "whatsapp_number"
                                    ]
                                ),
                            )
                        )

                        st.info(
                            "Saved order: "
                            f"{submitted_quantity} item(s), "
                            f"GHS {submitted_total:,.2f}"
                        )

                        st.markdown(
                            f"""
                            {whatsapp_url}
                                Continue Order on WhatsApp
                            </a>
                            """,
                            unsafe_allow_html=True,
                        )

                else:
                    st.markdown(
                        """
                        <div class="product-stock low-stock">
                            Out of stock
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        """
                        <div class="out-of-stock-button">
                            Out of Stock
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

st.markdown(
    """
    <div style="text-align: center; color: #666666;">
        <p>
            © 2026 Pika Market Hub Ghana.
            A modern shopping experience.
        </p>

      
            Call or email us to advertise your products here.
        </p>

   
            All prices are in Ghana Cedis (GHS).
            Contact: +233 27 569 6787 |
            instilpee@gmail.com
        </p>

        <p>
            <strong>Disclaimer:</strong>
            This application is solely responsible for
            connecting buyers with sellers. Buyers and sellers
            are responsible for conducting the necessary due
            diligence before completing any transaction.
        </p>

        <p>
            Select a quantity, submit the request and click
            “Continue Order on WhatsApp” to contact the seller.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
