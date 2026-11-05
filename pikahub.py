import hmac
import io
import urllib.parse
from datetime import date

import pandas as pd
import streamlit as st
from supabase import create_client


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
# SUPABASE CONNECTION
# =========================================================

@st.cache_resource
def connect_to_supabase():
    """Connect to Supabase using Streamlit Cloud Secrets."""
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


supabase = connect_to_supabase()


def save_request_to_supabase(customer_name, product_name, quantity, total_price):
    """Save a customer request to the Supabase orders table."""
    try:
        order_data = {
            "customer_name": str(customer_name).strip(),
            "product": str(product_name),
            "quantity": int(quantity),
            "price": float(total_price),
        }

        response = supabase.table("orders").insert(order_data).execute()

        if response.data:
            return True, "Your request was saved successfully."

        return False, "Supabase did not return the saved request."

    except Exception as error:
        return False, f"The request could not be saved: {error}"


def load_orders_from_supabase():
    """Retrieve all order records for the authenticated admin."""
    try:
        response = (
            supabase.table("orders")
            .select("*")
            .order("order_date", desc=True)
            .execute()
        )
        return True, response.data or []
    except Exception as error:
        return False, f"Orders could not be loaded: {error}"


# =========================================================
# WHATSAPP FUNCTION
# =========================================================

def create_whatsapp_message(
    customer_name,
    product_name,
    unit_price,
    quantity,
    whatsapp_number,
):
    """Create a WhatsApp URL containing the order details."""
    total_price = float(unit_price) * int(quantity)

    message = (
        f"Hello! My name is {customer_name}.\n\n"
        "I would like to place the following order:\n\n"
        f"Customer Name: {customer_name}\n"
        f"Product: {product_name}\n"
        f"Quantity: {quantity}\n"
        f"Unit Price: GHS {unit_price:,.2f}\n"
        f"Total Price: GHS {total_price:,.2f}\n\n"
        "Please let me know about availability, delivery and payment options."
    )

    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{whatsapp_number}?text={encoded_message}"


# =========================================================
# ADMIN HELPERS
# =========================================================

def get_admin_credentials():
    """Read admin credentials from either supported Secrets format."""
    try:
        if "admin" in st.secrets:
            return (
                str(st.secrets["admin"]["username"]),
                str(st.secrets["admin"]["password"]),
            )

        return (
            str(st.secrets["ADMIN_USERNAME"]),
            str(st.secrets["ADMIN_PASSWORD"]),
        )
    except Exception:
        return None, None


def authenticate_admin(username, password):
    stored_username, stored_password = get_admin_credentials()

    if not stored_username or not stored_password:
        return False

    username_matches = hmac.compare_digest(username, stored_username)
    password_matches = hmac.compare_digest(password, stored_password)
    return username_matches and password_matches


def create_excel_report(dataframe):
    """Create an in-memory Excel workbook for downloading."""
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Orders")
        worksheet = writer.sheets["Orders"]
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        for column_cells in worksheet.columns:
            max_length = max(
                len(str(cell.value)) if cell.value is not None else 0
                for cell in column_cells
            )
            column_letter = column_cells[0].column_letter
            worksheet.column_dimensions[column_letter].width = min(
                max(max_length + 2, 12),
                45,
            )

    output.seek(0)
    return output.getvalue()


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
            margin: 5px 0 10px 0;
            border-radius: 8px;
            font-size: 17px;
            font-weight: 700;
            text-align: center;
        }
        .whatsapp-link {
            display: block;
            box-sizing: border-box;
            background-color: #25D366;
            color: white !important;
            padding: 11px 15px;
            text-decoration: none !important;
            border-radius: 8px;
            font-weight: 600;
            text-align: center;
            width: 100%;
            margin: 10px 0;
        }
        .whatsapp-link:hover {
            background-color: #128C7E;
            color: white !important;
        }
        .out-of-stock-button {
            display: block;
            box-sizing: border-box;
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
        .admin-header {
            font-size: 25px;
            font-weight: 700;
            color: #FF4B4B;
            margin-bottom: 8px;
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
        "description": "Can be used on both sides. Silver and black with four mats.",
        "image_urls": [
            "https://i.imgur.com/3TJlx72.jpeg",
            "https://i.imgur.com/VGZJ8iM.jpeg",
        ],
    },
    {
        "id": 2,
        "name": " Electric Car Washing Machine Water Spray",
        "price": 425.00,
        "category": "Accessories",
        "stock": 4,
        "whatsapp_number": "233275696787",
        "description": "Colour: Black.48VH 12000 mAh",
        "image_urls": [
            "https://github.com/InstilKay/Market_Instil/blob/main/spraygun.jpg?raw=true",
            "https://github.com/InstilKay/Market_Instil/blob/main/spraygun2.jpg?raw=true",

        ],
    },
    {
        "id": 3,
        "name": "Windshield Sun Shade UV Protector",
        "price": 145.00,
        "category": "Accessories",
        "stock": 5,
        "whatsapp_number": "233275696787",
        "description": "L27.56 × W57 inches.",
        "image_urls": [
            "https://github.com/InstilKay/Market_Instil/blob/main/psolfg-800x1091.jpg?raw=true",
            "https://github.com/InstilKay/Market_Instil/blob/main/a2-800x1091.jpg?raw=true",
            "https://github.com/InstilKay/Market_Instil/blob/main/edf-800x1091.jpg?raw=true",
        ],
    },
    {
        "id": 4,
        "name": "Foldable Windshield Sun UV Rays Blocking Shade Umbrella",
        "price": 155.00,
        "category": "Accessories",
        "stock": 5,
        "whatsapp_number": "233246729676",
        "description": "(L6.5 × W12.5) cm / (L2.55 × W4.9) inches, Small/B Style.",
        "image_urls": [
            "https://github.com/InstilKay/Market_Instil/blob/main/foldsunsheild.jpg?raw=true",
            "https://github.com/InstilKay/Market_Instil/blob/main/foldsunshieldlength.jpg?raw=true",
        ],
    },
    {
        "id": 5,
        "name": "Electric Car Washing Machine Water Spray",
        "price": 425.00,
        "category": "Electronics",
        "stock": 5,
        "whatsapp_number": "233275696787",
        "description": "48VH 12000 mAh ,Colour: Black, suitable for car washing.",
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
            "https://github.com/InstilKay/Market_Instil/blob/main/tomatoes.jpg?raw=true",
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
            "https://github.com/InstilKay/Market_Instil/blob/main/Pepper.jpg?raw=true",
        ],
    },
    {
        "id": 8,
        "name": "Seat Massager",
        "price": 395.00,
        "category": "Electronics",
        "stock": 30,
        "whatsapp_number": "233547568955",
        "description": (
            "2 in 1 Electronic Heated Vibrating Massage Mat "
            "& Home Car Massage Cushion with 4 Modes."
        ),
        "image_urls": [
            "https://github.com/InstilKay/Market_Instil/blob/main/seatmassage.jpg?raw=true",
            "https://github.com/InstilKay/Market_Instil/blob/main/seatmassager2.jpg?raw=true",
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
if "show_name_form" not in st.session_state:
    st.session_state.show_name_form = {}
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


def get_selected_image_index(product_id):
    return st.session_state.selected_image_index.get(product_id, 0)


def set_selected_image_index(product_id, image_index):
    st.session_state.selected_image_index[product_id] = image_index


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
        Discover exciting products and place your request directly with the seller.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MAIN MENU
# =========================================================

menu_col1, menu_col2, menu_col3 = st.columns([1, 2, 1])
with menu_col2:
    if st.button("📋 OPEN MENU", key="main_menu_button", use_container_width=True):
        st.session_state.show_categories = not st.session_state.show_categories

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
st.sidebar.markdown(f"**Selected Category:** {st.session_state.selected_category}")

total_products = len(products)
available_products = sum(1 for product in products if product["stock"] > 0)
out_of_stock_products = total_products - available_products

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
        if product["category"] == st.session_state.selected_category
    ]

available_in_category = sum(
    1 for product in filtered_products if product["stock"] > 0
)
out_of_stock_in_category = len(filtered_products) - available_in_category

st.markdown(
    f"""
    <div class="stats-container">
        <strong>{st.session_state.selected_category} Category:</strong>
        {len(filtered_products)} product(s), {available_in_category} available and
        {out_of_stock_in_category} out of stock.
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="sub-header">{st.session_state.selected_category} Products</div>',
    unsafe_allow_html=True,
)


# =========================================================
# DISPLAY PRODUCTS
# =========================================================

if not filtered_products:
    st.info("There are currently no products in this category.")
else:
    product_columns = st.columns(4)

    for index, product in enumerate(filtered_products):
        with product_columns[index % 4]:
            with st.container(border=True):
                image_urls = product.get("image_urls", [])

                if image_urls:
                    current_index = get_selected_image_index(product["id"])
                    total_images = len(image_urls)

                    if current_index >= total_images:
                        current_index = 0
                        set_selected_image_index(product["id"], 0)

                    st.image(image_urls[current_index], use_container_width=True)
                    st.caption(f"Image {current_index + 1} of {total_images}")

                    if total_images > 1:
                        previous_column, next_column = st.columns(2)
                        with previous_column:
                            if st.button(
                                "◀ Previous",
                                key=f"previous_{product['id']}",
                                use_container_width=True,
                            ):
                                set_selected_image_index(
                                    product["id"],
                                    (current_index - 1) % total_images,
                                )
                                st.rerun()
                        with next_column:
                            if st.button(
                                "Next ▶",
                                key=f"next_{product['id']}",
                                use_container_width=True,
                            ):
                                set_selected_image_index(
                                    product["id"],
                                    (current_index + 1) % total_images,
                                )
                                st.rerun()
                else:
                    st.info("No product image available.")

                st.markdown(
                    f'<div class="product-title">{product["name"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="product-price">GHS {product["price"]:,.2f}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="product-description">{product["description"]}</div>',
                    unsafe_allow_html=True,
                )

                if product["stock"] > 0:
                    stock_class = "low-stock" if product["stock"] < 5 else ""
                    st.markdown(
                        f'<div class="product-stock {stock_class}">'
                        f'In stock: {product["stock"]} available</div>',
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
                    total_price = float(product["price"]) * int(quantity)
                    st.markdown(
                        f'<div class="total-price">Total: GHS {total_price:,.2f}</div>',
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "🛒 Submit Request",
                        key=f"submit_request_{product['id']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        st.session_state.show_name_form[product["id"]] = True

                    if st.session_state.show_name_form.get(product["id"], False):
                        customer_name = st.text_input(
                            "Your full name",
                            placeholder="Enter your full name",
                            key=f"customer_name_{product['id']}",
                        )

                        if st.button(
                            "✅ Confirm Request",
                            key=f"confirm_request_{product['id']}",
                            use_container_width=True,
                        ):
                            cleaned_customer_name = customer_name.strip()

                            if len(cleaned_customer_name) < 2:
                                st.warning(
                                    "Please enter a valid full name before confirming the request."
                                )
                            else:
                                success, message = save_request_to_supabase(
                                    customer_name=cleaned_customer_name,
                                    product_name=product["name"],
                                    quantity=quantity,
                                    total_price=total_price,
                                )

                                if success:
                                    st.session_state.submitted_requests[product["id"]] = {
                                        "customer_name": cleaned_customer_name,
                                        "quantity": int(quantity),
                                        "unit_price": float(product["price"]),
                                        "total_price": float(total_price),
                                    }
                                    st.session_state.show_name_form[product["id"]] = False
                                    st.success(
                                        f"Thank you, {cleaned_customer_name}! "
                                        "Your request was saved successfully."
                                    )
                                else:
                                    st.error(message)

                    submitted_request = st.session_state.submitted_requests.get(
                        product["id"]
                    )

                    if submitted_request:
                        submitted_customer_name = submitted_request["customer_name"]
                        submitted_quantity = submitted_request["quantity"]
                        submitted_total = submitted_request["total_price"]

                        whatsapp_url = create_whatsapp_message(
                            customer_name=submitted_customer_name,
                            product_name=product["name"],
                            unit_price=product["price"],
                            quantity=submitted_quantity,
                            whatsapp_number=product["whatsapp_number"],
                        )

                        st.info(
                            f"Order for {submitted_customer_name}: "
                            f"{submitted_quantity} item(s), "
                            f"GHS {submitted_total:,.2f}"
                        )
                        st.markdown(
                            f'<a href="{whatsapp_url}" target="_blank" '
                            f'rel="noopener noreferrer" class="whatsapp-link">'
                            f'Continue Order on WhatsApp</a>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.markdown(
                        '<div class="product-stock low-stock">Out of stock</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        '<div class="out-of-stock-button">Out of Stock</div>',
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
        <p>© 2026 Pika Market Hub Ghana. A modern shopping experience.</p>
        <p>Call or email us to advertise your products here.</p>
        <p>
            All prices are in Ghana Cedis (GHS).<br>
            Contact: +233 27 569 6787 | instilpee@gmail.com
        </p>
        <p>
            <strong>Disclaimer:</strong> This application is solely responsible for
            connecting buyers with sellers. Buyers and sellers are responsible for
            conducting the necessary due diligence before completing any transaction.
        </p>
        <p>
            Select a quantity, click “Submit Request”, enter your name when prompted,
            confirm the request and continue the order on WhatsApp.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# ADMIN ACCESS - END OF PAGE
# =========================================================

st.markdown("---")

with st.expander("🔐 Admin Access", expanded=False):
    st.markdown(
        '<div class="admin-header">Admin Order Reports</div>',
        unsafe_allow_html=True,
    )

    stored_username, stored_password = get_admin_credentials()

    if not stored_username or not stored_password:
        st.error(
            "Admin credentials are missing. Add the [admin] username and password "
            "to your Streamlit Secrets."
        )

    elif not st.session_state.admin_authenticated:
        with st.form("admin_login_form", clear_on_submit=True):
            admin_username = st.text_input("Admin username")
            admin_password = st.text_input("Admin password", type="password")
            login_submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if login_submitted:
            if authenticate_admin(admin_username.strip(), admin_password):
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect admin username or password.")

    else:
        action_col1, action_col2 = st.columns([3, 1])
        with action_col1:
            st.success("Admin access granted.")
        with action_col2:
            if st.button("Logout", key="admin_logout", use_container_width=True):
                st.session_state.admin_authenticated = False
                st.rerun()

        orders_loaded, orders_result = load_orders_from_supabase()

        if not orders_loaded:
            st.error(orders_result)
        elif not orders_result:
            st.info("There are currently no orders to display or download.")
        else:
            orders_df = pd.DataFrame(orders_result)

            preferred_columns = [
                "id",
                "customer_name",
                "product",
                "quantity",
                "price",
                "order_date",
            ]
            available_columns = [
                column for column in preferred_columns if column in orders_df.columns
            ]
            other_columns = [
                column for column in orders_df.columns if column not in available_columns
            ]
            orders_df = orders_df[available_columns + other_columns]

            if "order_date" in orders_df.columns:
                orders_df["order_date"] = pd.to_datetime(
                    orders_df["order_date"],
                    errors="coerce",
                    utc=True,
                )

            if "quantity" in orders_df.columns:
                orders_df["quantity"] = pd.to_numeric(
                    orders_df["quantity"], errors="coerce"
                ).fillna(0)

            if "price" in orders_df.columns:
                orders_df["price"] = pd.to_numeric(
                    orders_df["price"], errors="coerce"
                ).fillna(0.0)

            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("Total Orders", len(orders_df))
            metric_col2.metric(
                "Total Quantity",
                int(orders_df["quantity"].sum())
                if "quantity" in orders_df.columns
                else 0,
            )
            metric_col3.metric(
                "Total Order Value",
                f"GHS {orders_df['price'].sum():,.2f}"
                if "price" in orders_df.columns
                else "GHS 0.00",
            )

            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                if "product" in orders_df.columns:
                    product_options = sorted(
                        orders_df["product"].dropna().astype(str).unique().tolist()
                    )
                    selected_products = st.multiselect(
                        "Filter by product",
                        options=product_options,
                        default=[],
                    )
                else:
                    selected_products = []

            with filter_col2:
                customer_search = st.text_input(
                    "Search customer name",
                    placeholder="Type part of a customer name",
                    key="admin_customer_search",
                )

            filtered_orders = orders_df.copy()

            if selected_products and "product" in filtered_orders.columns:
                filtered_orders = filtered_orders[
                    filtered_orders["product"].astype(str).isin(selected_products)
                ]

            if customer_search.strip() and "customer_name" in filtered_orders.columns:
                filtered_orders = filtered_orders[
                    filtered_orders["customer_name"]
                    .fillna("")
                    .astype(str)
                    .str.contains(customer_search.strip(), case=False, regex=False)
                ]

            if "order_date" in filtered_orders.columns:
                valid_dates = filtered_orders["order_date"].dropna()

                if not valid_dates.empty:
                    minimum_date = valid_dates.min().date()
                    maximum_date = valid_dates.max().date()

                    selected_date_range = st.date_input(
                        "Filter by order date",
                        value=(minimum_date, maximum_date),
                        min_value=minimum_date,
                        max_value=maximum_date,
                        key="admin_date_filter",
                    )

                    if isinstance(selected_date_range, (tuple, list)):
                        if len(selected_date_range) == 2:
                            start_date, end_date = selected_date_range
                            order_dates = filtered_orders["order_date"].dt.date
                            filtered_orders = filtered_orders[
                                (order_dates >= start_date)
                                & (order_dates <= end_date)
                            ]
                        elif len(selected_date_range) == 1:
                            selected_date = selected_date_range[0]
                            filtered_orders = filtered_orders[
                                filtered_orders["order_date"].dt.date
                                == selected_date
                            ]

            display_df = filtered_orders.copy()
            if "order_date" in display_df.columns:
                display_df["order_date"] = display_df["order_date"].dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            st.caption(f"Showing {len(display_df)} order record(s).")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            csv_data = display_df.to_csv(index=False).encode("utf-8-sig")
            excel_data = create_excel_report(display_df)
            report_date = date.today().strftime("%Y%m%d")

            download_col1, download_col2 = st.columns(2)
            with download_col1:
                st.download_button(
                    "⬇️ Download CSV Report",
                    data=csv_data,
                    file_name=f"pika_market_orders_{report_date}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with download_col2:
                st.download_button(
                    "⬇️ Download Excel Report",
                    data=excel_data,
                    file_name=f"pika_market_orders_{report_date}.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    use_container_width=True,
                )
