from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from pymemcache.client import base
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
        memcache_client.delete("SHOW_PROMOTION")
        return {"status": "cache invalidated"}
    return {"status": "memcache not used"}


def fetch_feature_flags():
    try:
        if memcache_client:
            show_flashsale = memcache_client.get("SHOW_FLASHSALE")
            show_premium = memcache_client.get("SHOW_PREMIUM")
            show_promotion = memcache_client.get("SHOW_PROMOTION")

            if show_flashsale is None:
                show_flashsale = os.environ.get("SHOW_FLASHSALE", default="0")
                memcache_client.set(
                    "SHOW_FLASHSALE", show_flashsale, expire=int(MEMCACHE_TIMEOUT)
                )

            if show_premium is None:
                show_premium = os.environ.get("SHOW_PREMIUM", default="0")

                memcache_client.set(
                    "SHOW_PREMIUM", show_premium, expire=int(MEMCACHE_TIMEOUT)
                )

            if show_promotion is None:
                show_promotion = os.environ.get("SHOW_PROMOTION", default="0")
                memcache_client.set(
                    "SHOW_PROMOTION", show_promotion, expire=int(MEMCACHE_TIMEOUT)
                )

            logging.info(
                f"From Memcache - SHOW_FLASHSALE: {show_flashsale}, SHOW_PREMIUM: {show_premium}, SHOW_PROMOTION: {show_promotion}"
            )

            return {
                "SHOW_FLASHSALE": True
                if show_flashsale and show_flashsale.decode("utf-8") == "1"
                else False,
                "SHOW_PREMIUM": True
                if show_premium and show_premium.decode("utf-8") == "1"
                else False,
                "SHOW_PROMOTION": True
                if show_promotion and show_promotion.decode("utf-8") == "1"
                else False,
            }
    except Exception as e:
        logging.error(f"Error accessing Memcache: {e}")

    logging.info("Using environment variables for feature flags.")
    return {
        "SHOW_FLASHSALE": os.environ.get("SHOW_FLASHSALE", default="0") == "1",
        "SHOW_PREMIUM": os.environ.get("SHOW_PREMIUM", default="0") == "1",
        "SHOW_PROMOTION": os.environ.get("SHOW_PROMOTION", default="0") == "1",
    }


@app.get("/", response_class=HTMLResponse)
def shop_homepage():
    server_info = f"Served by FastAPI on port {os.environ.get('INFO_PORT', 'unknown')}"
    # Fetch feature flags from  memcache or env vars
    feature_flags = fetch_feature_flags()
    SHOW_FLASHSALE = feature_flags["SHOW_FLASHSALE"]
    SHOW_PREMIUM = feature_flags["SHOW_PREMIUM"]
    SHOW_PROMOTION = feature_flags["SHOW_PROMOTION"]

    header = "<header>Canario Shop</header>"
    title = "<div class='title'><h1>Welcome to Canario Shop</h1><p>Your one-stop shop for all things Canario.</p></div>"

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
        <!-- <button id="toggle-sidebar">Toggle Sidebar</button> -->       
    </div>
    """

    product_grid = """
    <div class="product-grid">
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_Camera_re_cnp4.png" />
            </div>
            <div class="product-name">
                AI Camera
            </div>
            <div class="product-price">
                $359
            </div>
            <button class="btn" onclick="alert('Added to cart!')">Add to Cart</button>
            <button class="btn" onclick="alert('More details!')">View Details</button>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_dua_lipa_ixam.png" />
            </div>
            <div class="product-name">
              AI Speaker
            </div>
            <div class="product-price">
                $429
            </div>
            <button class="btn" onclick="alert('Added to cart!')">Add to Cart</button>
            <button class="btn" onclick="alert('More details!')">View Details</button>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_Imagination_re_i0xi.png" />
            </div>
            <div class="product-name">
                AI Headphones
            </div>
            <div class="product-price">
                $319
            </div>
            <button class="btn" onclick="alert('Added to cart!')">Add to Cart</button>
            <button class="btn" onclick="alert('More details!')">View Details</button>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_mobile_devices_k1ok.png" />
            </div>
            <div class="product-name">
                Smart Phone
            </div>
            <div class="product-price">
                $449
            </div>
            <button class="btn" onclick="alert('Added to cart!')">Add to Cart</button>
            <button class="btn" onclick="alert('More details!')">View Details</button>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_ninja_e52b.png" />
            </div>
            <div class="product-name">
                VR Gaming
            </div>
            <div class="product-price">
                $199
            </div>
            <button class="btn" onclick="alert('Added to cart!')">Add to Cart</button>
            <button class="btn" onclick="alert('More details!')">View Details</button>
        </div>
        <div class="product">
            <div class="product-image">
                <img src="static/assets/undraw_Smartwatch_re_59lx.png" />
            </div>
            <div class="product-name">
                Smart Watch
            </div>
            <div class="product-price">
                $600
            </div>
            <button class="btn" onclick="alert('Added to cart!')">Add to Cart</button>
            <button class="btn" onclick="alert('More details!')">View Details</button>
        </div>
        </div>
    </div>
    """

    flash_sale = (
        """
    <div class="product flash-sale" data-status="Flash Sale!">
        <div class="product-image">
            <img src="static/assets/undraw_discount_d4bd.png" />
        </div>
        <div class="product-name">
            Smart Watch
        </div>
        <div class="product-price">
            Special Discount
        </div>
        <button class="btn" onclick="alert('Grabbing the deal!')">Grab now!</button>
    </div>
    """
        if SHOW_FLASHSALE
        else ""
    )

    premium_offer = (
        """
    <div class="product premium" data-status="Premium Offer!">
        <div class="product-image">
            <img src="static/assets/undraw_product_hunt_n3f5.png" />
        </div>
        <div class="product-name">
            VR Gaming
        </div>
        <div class="product-price">
            Exclusive Deal
        </div>
        <button class="btn" onclick="alert('Grabbing the deal!')">Grab now!</button>
    </div>
    """
        if SHOW_PREMIUM
        else ""
    )

    hourly_promotion = (
        """

    <div class="product hourly-promotion" data-status="Christmas Offer!"!>
        <div class="product-image">
            <img src="static/assets/undraw_Gifts_0ceh.png" />
        </div>
        <div class="product-name">
            Shop one, Score Two! 
            <div class="banner">
                <span class="rotating-text">20th Dec</span>
            </div>
        </div>
        <div class="product-price">
            Our Mega Deal for Christmas!
        </div>
        <div class="hourly-promotion-timer">Time Left: <span id="time">58</span> mins</div>
       
        <script>
        // ################## COUNT UNTIL CHRISTMAS OFFER ################## 
        // Set the date we're counting down to
        const countDownDate = new Date("December 20, 2023 00:00:00").getTime();

        // Update the countdown every second
        const timer = setInterval(() => {
            const now = new Date().getTime();

            // Find the time difference between now and the countdown date
            const distance = countDownDate - now;

            // Calculate days, hours, minutes, and seconds
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Display the result
            document.querySelector(".hourly-promotion-timer").textContent = days + " days " + hours + " hours " + minutes + " minutes " + seconds + " seconds"

            // If the countdown is finished, display a message
            if (distance < 0) {
                clearInterval(timer);
                document.querySelector(".hourly-promotion-timer").textContent = "Grab the deal now!";
            }
        }, 1000);  // 1000 milliseconds (1 second)
        
        // ################## END OF COUNT UNTIL CHRISTMAS OFFER ##################
        </script>
        <button class="btn" onclick="alert('Grabbing the deal!')">Grab the deal now!</button>
    </div>
    
    <script>
    document.addEventListener('DOMContentLoaded', (event) => {
    // Function to toggle sidebar visibility
    const toggleSidebar = () => {
        const sidebarElement = document.querySelector('.sidebar');
        sidebarElement.classList.toggle('hidden');
    };

    // Event listener for your toggle button, assuming it has an id of 'toggle-sidebar'
    document.getElementById('toggle-sidebar').addEventListener('click', toggleSidebar);
    });

    </script>
    """
        if SHOW_PROMOTION
        else ""
    )
    special_offers_section = f"""
    <div class="special-offers">
        {premium_offer}
        {flash_sale}
        {hourly_promotion}
    </div>
    """

    footer = f"<footer>Canario Shop 2023, Oslo, Norway | {server_info}</footer>"

    full_page = f"""
    <html>
    <head>
        <link rel="stylesheet" href="static/styles.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {header}
        {title}
    </head>
    <body>
        <div class="main-content">
        {sidebar}
        <div class="content-wrapper">
            {special_offers_section}
            {product_grid}
        </div>
        </div>
        {footer}
    </body>
    </html>
    
    """
    # TODO: Add a button to invalidate cache

    return HTMLResponse(content=full_page, status_code=200)
