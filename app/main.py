from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import random
import requests
from pymemcache.client import base
import logging

import logging

logging.basicConfig(level=logging.INFO)

VERSION = "0.3"

USE_MEMCACHE = os.environ.get("USE_MEMCACHE", default="N")
MEMCACHE_SERVER = os.environ.get("MEMCACHE_SERVER")
MEMCACHE_TIMEOUT = os.environ.get("MEMCACHE_TIMEOUT", default=60)

app = FastAPI()

# Mounting static files
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Create memcache client if USE_MEMCACHE is set to Y
memcache_client = None
if USE_MEMCACHE == "Y":
    memcache_client = base.Client((MEMCACHE_SERVER, 11211))

    # Fetch feature flags from memcache or env vars

@app.post("/invalidate_cache")
def invalidate_cache():
    if memcache_client:
        memcache_client.delete("SHOW_FLASHSALE")
        memcache_client.delete("SHOW_PREMIUM")
        return {"status": "cache invalidated"}
    return {"status": "memcache not used"}

    
def fetch_feature_flags():
    try:
        if memcache_client:
            show_flashsale = memcache_client.get("SHOW_FLASHSALE")
            show_premium = memcache_client.get("SHOW_PREMIUM")

            logging.info(f"Type of show_flashsale: {type(show_flashsale)}, Value: {show_flashsale}")
            logging.info(f"Type of show_premium: {type(show_premium)}, Value: {show_premium}")

            if show_flashsale is None:
                show_flashsale = os.environ.get("SHOW_FLASHSALE", default="0")
                memcache_client.set("SHOW_FLASHSALE", show_flashsale, expire=int(MEMCACHE_TIMEOUT))

            if show_premium is None:
                show_premium = os.environ.get("SHOW_PREMIUM", default="0")
                memcache_client.set("SHOW_PREMIUM", show_premium, expire=int(MEMCACHE_TIMEOUT))

            logging.info(f"From Memcache - SHOW_FLASHSALE: {show_flashsale}, SHOW_PREMIUM: {show_premium}")
            return {
                "SHOW_FLASHSALE": True if show_flashsale and show_flashsale.decode('utf-8') == "1" else False,
                "SHOW_PREMIUM": True if show_premium and show_premium.decode('utf-8') == "1" else False,
            }
    except Exception as e:
        logging.error(f"Error accessing Memcache: {e}")

    logging.info("Using environment variables for feature flags.")
    return {
        "SHOW_FLASHSALE": os.environ.get("SHOW_FLASHSALE", default="0") == "1",
        "SHOW_PREMIUM": os.environ.get("SHOW_PREMIUM", default="0") == "1"
    }



@app.get("/", response_class=HTMLResponse)
def shop_homepage():
    server_info = f"Served by FastAPI on port {os.environ.get('INFO_PORT', 'unknown')}"
    # Fetch feature flags from  memcache or env vars
    feature_flags = fetch_feature_flags()
    SHOW_FLASHSALE = feature_flags["SHOW_FLASHSALE"]
    SHOW_PREMIUM = feature_flags["SHOW_PREMIUM"]

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

    footer = f"<footer>Canario Shop 2023, Oslo, Norway | {server_info}</footer>"

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
