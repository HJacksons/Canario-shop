from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Mounting static files
app.mount("/static", StaticFiles(directory="./static"), name="static")

#SHOW_FLASHSALE = os.environ.get("SHOW_FLASHSALE", default=False)
#SHOW_PREMIUM = os.environ.get("SHOW_PREMIUM", default=False)
SHOW_FLASHSALE = os.environ.get("SHOW_FLASHSALE", default="0") == "1"
SHOW_PREMIUM = os.environ.get("SHOW_PREMIUM", default="0") == "1"


@app.get("/", response_class=HTMLResponse)
def shop_homepage():
    # Fetch feature flags from the dashboard
    # fetched_flags = fetch_feature_flags()
    # SHOW_FLASHSALE = fetched_flags.get("SHOW_FLASHSALE", False)
    # SHOW_PREMIUM = fetched_flags.get("SHOW_PREMIUM", False)

    header = "<header>Canario Shop</header>"
    title = "<h1>Welcome to Canario Shop</h1><p>Your one-stop shop for all things Canario.</p>"

    sidebar = """
    <div class="sidebar">
        <h2>Categories</h2>
        <ul>
            <li><a href="#"><span>📱</span> Electronics</a></li>
            <li><a href="#"><span>👗</span> Fashion</a></li>
            <li><a href="#"><span>🏠</span> Home & Living</a></li>
            <li><a href="#"><span>💄</span> Beauty & Health</a></li>
            <li><a href="#"><span>🏋️</span> Sports & Outdoors</a></li>
            <li><a href="#"><span>🎲</span> Toys & Hobbies</a></li>
            <li><a href="#"><span>📚</span> Books & Stationery</a></li>
            <li><a href="#"><span>🎉</span> Special Offers</a></li>
        </ul>
    </div>
    """

    product_grid = """
    <div class="product-grid">
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_dua_lipa_ixam.png" />
            </div>
            <div class="product-name">
                Canario
            </div>
            <div class="product-price">
                $100
            </div>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_dua_lipa_ixam.png" />
            </div>
            <div class="product-name">
                Canario
            </div>
            <div class="product-price">
                $100
            </div>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_Imagination_re_i0xi.png" />
            </div>
            <div class="product-name">
                Canario
            </div>
            <div class="product-price">
                $100
            </div>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_mobile_devices_k1ok.png" />
            </div>
            <div class="product-name">
                Canario
            </div>
            <div class="product-price">
                $100
            </div>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_ninja_e52b.png" />
            </div>
            <div class="product-name">
                Canario
            </div>
            <div class="product-price">
                $100
            </div>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_Smartwatch_re_59lx.png" />
            </div>
            <div class="product-name">
                Canario
            </div>
            <div class="product-price">
                $100
            </div>
        </div>
        </div>
    </div>
    """

    flash_sale = """
    <div class="product flash-sale" data-status="Flash Sale!">
        <div class="product-image">
            <img src="static/assets/special-offer.jpg" />
        </div>
        <div class="product-name">
            Special Product
        </div>
        <div class="product-price">
            Special Discount
        </div>
    </div>
    """ if SHOW_FLASHSALE else ""

    premium_offer = """
    <div class="product premium" data-status="Premium Offer!">
        <div class="product-image">
            <img src="static/assets/premium.jpeg" />
        </div>
        <div class="product-name">
            Exclusive Product
        </div>
        <div class="product-price">
            Exclusive Deal
        </div>
    </div>
    """ if SHOW_PREMIUM else ""

    footer = "<footer>Canario Shop 2023</footer>"

    full_page = f"""

    <html>
    <head>
        <link rel="stylesheet" href="static/styles.css">

    </head>
    <body>
        {header}
        {title}
        <div class="main-content">
        {sidebar}
        <div class="content-wrapper">
        {premium_offer}
        {product_grid}
        {flash_sale}
        </div>
        </div>
        {footer}
        
    </body>
    </html>
    
    """
    return HTMLResponse(content=full_page, status_code=200)
