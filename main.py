from pyscript import document, window

products = {}
cart = {}

admin_name = ""
store_name = ""
store_type = ""

total_sales = 0
total_profit = 0

def sign_in(event=None):
    global admin_name, store_name, store_type
    admin_name = document.getElementById("admin").value.strip()
    store_name = document.getElementById("store_nm").value.strip()
    store_type = document.getElementById("store_type").value


    if admin_name == "" or store_name == "" or store_type == "":
        window.alert("Please fill in all fields.")
        return

    old_store = window.localStorage.getItem("store_name")
    if old_store != store_name:
            clear_prd()

    clear_prd()
    
    window.localStorage.setItem("admin_name", admin_name)
    window.localStorage.setItem("store_name", store_name)   
    window.localStorage.setItem("store_type", store_type)


    window.location.href = "dashboard.html"

def clear_prd():
    window.localStorage.removeItem("total_sales")
    window.localStorage.removeItem("total_profit")
    count = window.localStorage.getItem("product_count")

    if not count:
        return

    for index in range(int(count)):
        prefix = f"product_{str(index)}_"

        window.localStorage.removeItem(prefix + "name")
        window.localStorage.removeItem(prefix + "sku")
        window.localStorage.removeItem(prefix + "category")
        window.localStorage.removeItem(prefix + "variant")
        window.localStorage.removeItem(prefix + "model")
        window.localStorage.removeItem(prefix + "version")
        window.localStorage.removeItem(prefix + "brand")
        window.localStorage.removeItem(prefix + "price")
        window.localStorage.removeItem(prefix + "cost")
        window.localStorage.removeItem(prefix + "stock")
        

    window.localStorage.removeItem("product_count")

    

#Helper func
def display_store_info():
    global admin_name, store_name, store_type
    admin = window.localStorage.getItem("admin_name")
    store = window.localStorage.getItem("store_name")

    if admin:
        document.getElementById("show_admin").innerHTML = admin
    
    if store:
        document.getElementById("show_store_name").innerHTML = store

def display_sales_summary():

    sales = window.localStorage.getItem("total_sales")
    profit = window.localStorage.getItem("total_profit")

    if sales:
        document.getElementById("total_sl").innerHTML = f"Total Sales: P{float(sales):.2f}"
    else:
        document.getElementById("total_sl").innerHTML = "Total Sales: P0.00"

    if profit:
        document.getElementById("total_prft").innerHTML = f"Total Profit: P{float(profit):.2f}"
    else:
        document.getElementById("total_prft").innerHTML = "Total Profit: P0.00"

def update_product_options():
    selected_store = window.localStorage.getItem("store_type") or ""
    category = document.getElementById("prd_category")
    variant = document.getElementById("prd_variant")
    models = document.getElementById("prd_model")
    version = document.getElementById("prd_version")
    
    if category is None:
        return
    
    category.innerHTML = ""
    variant.innerHTML = ""
    models.innerHTML = ""
    version.innerHTML = ""

    categories = []

    if selected_store == "Clothing":
        categories = ["Shirts", "Pants", "Dresses", "Shoes", "Jackets", "Accessories"]
        variants = ["Standard", "Premium", "Limited Edition"]
        models = ["S", "M", "L", "XL"]
        versions = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]

    elif selected_store == "F&B":
        categories = ["Beverages", "Snacks", "Meals", "Desserts"]
        variants = ["Seasonal", "Static", "Cycle", "A la carte"]
        models = ["Large", "Medium", "Small"]
        versions = ["Good for 1", "Good for 2", "Good for many"]

    elif selected_store == "Electronics":
        categories = ["Phones", "Laptops", "Tablets", "Accessories", "Audio", "Devices"]
        variants = ["Standard", "Premium"]
        models = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
        versions = ["64GB", "128GB", "256GB"]


    elif selected_store == "Cosmetics & Skincare":
        categories = ["Skincare", "Makeup", "Haircare", "Fragrances", "Personal Hygiene"]
        variants = ["Standard", "Premium", "Limited Edition"]
        models = ["Gel", "Moisturizer", "Foundation", "Lipstick"]
        versions = ["50ml", "100ml","200ml"]

    elif selected_store == "Sports":
        categories = ["Fitness Equipment", "Outdoor Gear", "Sports Apparel", "Footwear", "Accessories"]
        variants = ["Beginner", "Advanced", "Professional"]
        models = ["Individual", "Dual", "Team", "Indoor", "Outdoor"]
        versions = ["S", "M", "L","XL"]

    elif selected_store == "Home & Living":
        categories = ["Furniture", "Decor", "Kitchen", "Bedding", "Lighting", "Appliances", "Storage"]
        variants = ["Everyday", "Luxury", "Artisanal"]
        models = ["Large", "Medium", "Small"]
        versions = ["Wood", "Metal", "Stainless"]

    elif selected_store == "School & Office":
        categories = ["Stationery", "Notebooks", "Writing Instruments", "Art Supplies", "Office Supplies"]
        variants = ["Corporate", "Back-to-school"]
        models = ["erasable", "Mechanical", "Oil", "Glue"]
        versions = ["Short", "Long", "Black", "Red"]

    elif selected_store == "Toys and Games":
        categories = ["Action Figures", "Board Games", "Puzzles", "Dolls", "Educational Toys", "Collectibles", "Card Games"]
        variants = ["Standard", "Premium", "Limited Edition"]
        models = ["Fashion Doll", "Superhero", "Teddy Bear", "Toy Car", "Jigsaw Puzzle"]
        versions = ["Classic", "Deluxe", "Junior"]


    elif selected_store == "Grocery":
        categories = ["Fruits", "Vegetables", "Dairy", "Meat", "Beverages", "Snacks"]
        variants = ["Generic", "Premium", "Raw"]
        models = ["Soft Drink", "Instant Foods", "Canned Goods", "Sauce", "Chips"]
        versions = ["ml", "pack", "g", "kg", "L"]

    else:
        categories = ["General", "Product", "Accessory", "Other"]
        variants = ["Standard", "Premium", "Limited Edition"]
        models = ["Model A", "Model B", "Model C", "Other"]
        versions = ["1.0", "2.0", "3.0", "Other"]



    fill_dropdown("prd_category", categories)

    fill_dropdown("prd_variant", variants)
    fill_dropdown("prd_model", models)
    fill_dropdown("prd_version", versions)

def fill_dropdown(element_id, options):
    dropdown = document.getElementById(element_id)

    if dropdown is None:
        return

    for option in options:
        opt = document.createElement("option")
        opt.value = option
        opt.innerHTML = option
        dropdown.appendChild(opt)

def generate_sku():
    category = document.getElementById("prd_category").value
    variant = document.getElementById("prd_variant").value.strip()
    model = document.getElementById("prd_model").value
    version = document.getElementById("prd_version").value

    category_sku = category[:3].upper()
    variant_sku = variant[:3].upper()
    model_sku = model[:3].upper()
    version_sku = version[:3].upper()

    sku_parts = [category_sku, variant_sku, model_sku, version_sku]
    sku = "-".join(sku_parts)
    
    document.getElementById("show_sku").innerHTML = f"Generated SKU: {sku}"
    return sku

def add_prd(event=None):
    name = document.getElementById("prd_name").value.strip()
    category = document.getElementById("prd_category").value.strip()
    variant = document.getElementById("prd_variant").value.strip()
    model = document.getElementById("prd_model").value.strip()
    version = document.getElementById("prd_version").value.strip()
    brand = document.getElementById("prd_brand").value.strip()

    price_text = document.getElementById("prd_price").value
    cost_text = document.getElementById("prd_cost").value
    stock_text = document.getElementById("prd_stock").value

    if (name == "" or category == "" or variant == "" or model == "" or version == "" or brand == "" or price_text == "" or cost_text == "" or stock_text == ""):
        document.getElementById("prd_msg").innerHTML = "Please fill in all Product fields."
        return
    
    try:
        price = float(price_text)
        cost = float(cost_text)
        stock = int(stock_text)
    except ValueError:
        document.getElementById("prd_msg").innerHTML = "Enter Valid Values"
        return

    if price < 0 or cost < 0 or stock < 0:
        document.getElementById("prd_msg").innerHTML = "Price, Cost, and Stock must be non-negative."
        return

    sku = generate_sku()

    product = {
        "name": name,
        "sku": sku,
        "category": category,
        "variant": variant,
        "model": model,
        "version": version,
        "brand": brand,
        "price": price,
        "cost": cost,
        "stock": stock,
    }

    products[sku] = product
    save_products()

    display_inventory()

    document.getElementById("prd_msg").innerHTML = f"Product '{name}' added successfully."

def save_products():
    window.localStorage.setItem("product_count", str(len(products)))
    index = 0
    
    for sku, product in products.items():
        window.localStorage.setItem(f"product_{str(index)}_name", product["name"])
        window.localStorage.setItem(f"product_{str(index)}_sku", sku)
        window.localStorage.setItem(f"product_{str(index)}_category", product["category"])
        window.localStorage.setItem(f"product_{str(index)}_variant", product["variant"])
        window.localStorage.setItem(f"product_{str(index)}_model", product["model"])
        window.localStorage.setItem(f"product_{str(index)}_version", product["version"])
        window.localStorage.setItem(f"product_{str(index)}_brand", product["brand"])
        window.localStorage.setItem(f"product_{str(index)}_price", str(product["price"]))
        window.localStorage.setItem(f"product_{str(index)}_cost", str(product["cost"]))
        window.localStorage.setItem(f"product_{str(index)}_stock", str(product["stock"]))
        index += 1

def load_products():
    global products
    products = {}
    product_count = window.localStorage.getItem("product_count")
    
    if not product_count:
        return
    
    count = int(product_count)
    
    for index in range(count):
        prefix = f"product_{str(index)}_"

        sku = window.localStorage.getItem(prefix + "sku")

        if not sku:
            continue

        product = {
            "name": window.localStorage.getItem(prefix + "name"),
            "sku": sku,
            "category": window.localStorage.getItem(prefix + "category"),
            "variant": window.localStorage.getItem(prefix + "variant"),
            "model": window.localStorage.getItem(prefix + "model"),
            "version": window.localStorage.getItem(prefix + "version"),
            "brand": window.localStorage.getItem(prefix + "brand"),
            "price": float(window.localStorage.getItem(prefix + "price")) or 0,
            "cost": float(window.localStorage.getItem(prefix + "cost")) or 0,
            "stock": int(window.localStorage.getItem(prefix + "stock")) or 0,
        }

        products[sku] = product

def display_inventory():
    inventory = document.getElementById("inv_list")

    if inventory is None:
        return
    inventory.innerHTML = ""

    for sku, product in products.items():
        row = document.createElement("tr")
        prd_cell = document.createElement("td")
        prd_cell.innerHTML = product["name"]

        sku_cell = document.createElement("td")
        sku_cell.innerHTML = product["sku"]

        category_cell = document.createElement("td")
        category_cell.innerHTML = product["category"]

        price_cell = document.createElement("td")
        price_cell.innerHTML = f"P{product['price']:.2f}"

        stock_cell = document.createElement("td")
        mins_btn = document.createElement("button")
        mins_btn.type = "button"
        mins_btn.innerHTML = "-"

        stock_display = document.createElement("span")
        stock_display.innerHTML = str(product["stock"])

        plus_btn = document.createElement("button")
        plus_btn.type = "button"
        plus_btn.innerHTML = "+"

        rmv_btn = document.createElement("button")
        rmv_btn.type = "button"
        rmv_btn.innerHTML = "Remove"

        mins_btn.onclick = lambda event, product_sku=sku: decrease_stock(product_sku)
        plus_btn.onclick = lambda event, product_sku=sku: increase_stock(product_sku)
        rmv_btn.onclick = lambda event, product_sku=sku: remove_product(product_sku)

        stock_cell.appendChild(mins_btn)
        stock_cell.appendChild(stock_display)
        stock_cell.appendChild(plus_btn)
        stock_cell.appendChild(rmv_btn)

        row.appendChild(prd_cell)
        row.appendChild(sku_cell) 
        row.appendChild(category_cell)
        row.appendChild(price_cell)
        row.appendChild(stock_cell)
        inventory.appendChild(row)

def increase_stock(sku):
    if sku not in products:
        return
    
    products[sku]["stock"] += 1
    save_products()
    display_inventory()

def decrease_stock(sku):
    if sku not in products:
        return
    
    if products[sku]["stock"] > 0:
        products[sku]["stock"] -= 1
        save_products()
        display_inventory()

def remove_product(sku):
    if sku not in products:
        return
    
    del products[sku]
    save_products()
    display_inventory()

def open_cashier(event=None):
    load_products()

    if len(products) == 0:
        document.getElementById("prd_msg").innerHTML = "No products available. Please add products first."
        return

    window.location.href = "cashier.html"

def display_products():
    container = document.getElementById("cashier_prd")

    if container is None:
        return
    
    container.innerHTML = ""

    for sku, product in products.items():
        prd_div = document.createElement("div")

        name_span = document.createElement("h3")
        name_span.innerHTML = product["name"]

        sku_span = document.createElement("p")
        sku_span.innerHTML = f"SKU: {product['sku']}"

        price_span = document.createElement("p")
        price_span.innerHTML = f"P{product['price']:.2f}"

        stock_span = document.createElement("p")
        stock_span.innerHTML = f"Stock: {product['stock']}"
        
        checkbox = document.createElement("input")
        checkbox.type = "checkbox"
        checkbox.value = sku

        checkbox.onchange = lambda event, product_sku=sku:select_product(event, product_sku)

        label = document.createElement("label")
        label.innerHTML = "Select"

        label.prepend(checkbox)

        prd_div.appendChild(name_span)
        prd_div.appendChild(sku_span)
        prd_div.appendChild(price_span)
        prd_div.appendChild(stock_span)
        prd_div.appendChild(label)

        container.appendChild(prd_div)

def select_product(event, sku):
    if event.target.checked:
        add_to_cart(sku)
    else:
        remove_from_cart(sku)

def add_to_cart(sku):
    if sku not in products:
        return
    
    product = products[sku]

    if product["stock"] <= 0:
        document.getElementById("cart_msg").innerHTML = f"Product '{product['name']}' is out of stock."
        return

    if sku in cart:
        return
    
    cart[sku] = {"quantity": 1}

    document.getElementById("cart_msg").innerHTML = ""
    update_cart_table()
    calculate_total()

def increase_quantity(sku):
    if sku not in cart:
        return

    if sku not in products:
        return
    
    curr_quantity = cart[sku]["quantity"]
    avail_stock = products[sku]["stock"]

    if curr_quantity >= avail_stock:
        document.getElementById("cart_msg").innerHTML = f"Cannot add more of '{products[sku]['name']}' to the cart."
        return

    cart[sku]["quantity"] += 1
    update_cart_item(sku)

def decrease_quantity(sku):
    if sku not in cart:
        return

    if cart[sku]["quantity"] > 1:
        cart[sku]["quantity"] -= 1
        update_cart_item(sku)
    else:
        remove_from_cart(sku)

def update_cart_item(sku):
    if sku not in cart:
        return

    update_cart_table()
    calculate_total()

def remove_from_cart(sku):
    if sku in cart:
        del cart[sku]
    update_cart_table()
    calculate_total()

def reset_checkbox():
    boxes = document.querySelectorAll("#cashier_prd input[type='checkbox']")

    for box in boxes:
        box.checked = box.value in cart

def update_cart_table():
    container = document.getElementById("cart_items")

    if container is None:
        return
    container.innerHTML = ""

    reset_checkbox()

    if len(cart) == 0:
        document.getElementById("cart_msg").innerHTML = "Cart is empty."
        return
    
    document.getElementById("cart_msg").innerHTML = ""

    for sku, item in cart.items():
        if sku not in products:
            continue
        
        product = products[sku]

        quantity = item["quantity"]
        subtotal = product["price"] * quantity

        row = document.createElement("tr")

        name_cell = document.createElement("td")
        name_cell.innerHTML = product["name"]

        sku_cell = document.createElement("td")
        sku_cell.innerHTML = product["sku"]

        price_cell = document.createElement("td")
        price_cell.innerHTML = f"P{product['price']:.2f}"

        quantity_cell = document.createElement("td")

        dec_btn = document.createElement("button")
        dec_btn.type = "button"
        dec_btn.innerHTML = "-"

        quantity_display = document.createElement("span")
        quantity_display.innerHTML = str(quantity)

        inc_btn = document.createElement("button")
        inc_btn.type = "button"
        inc_btn.innerHTML = "+"

        action_cell = document.createElement("td")
        rmv_btn = document.createElement("button")
        rmv_btn.type = "button"
        rmv_btn.innerHTML = "Remove"

        dec_btn.onclick = lambda event, product_sku=sku: decrease_quantity(product_sku)
        inc_btn.onclick = lambda event, product_sku=sku: increase_quantity(product_sku)
        rmv_btn.onclick = lambda event, product_sku=sku: remove_from_cart(product_sku)

        quantity_cell.appendChild(dec_btn)
        quantity_cell.appendChild(quantity_display)
        quantity_cell.appendChild(inc_btn)
        action_cell.appendChild(rmv_btn)

        subtotal_cell = document.createElement("td")
        subtotal_cell.innerHTML = f"P{subtotal:.2f}"

        row.appendChild(name_cell)
        row.appendChild(sku_cell)
        row.appendChild(price_cell)
        row.appendChild(quantity_cell)
        row.appendChild(subtotal_cell)
        row.appendChild(action_cell)

        container.appendChild(row)

def calculate_total():
    total = 0.0

    for sku, item in cart.items():
        if sku not in products:
            continue
        
        quantity = item["quantity"]
        price = products[sku]["price"]
        total += price * quantity


    document.getElementById("cart_total").innerHTML = f"Total: P{total:.2f}"
    return total


def complete_sale(event=None):
    global total_sales, total_profit

    if len(cart) == 0:
        document.getElementById("sales_msg").innerHTML = "Cart is empty. Cannot complete sale."
        return

    sale_total = 0.0
    sale_profit = 0.0

    for sku, item in cart.items():
        if sku not in products:
            continue
        
        quantity = item["quantity"]
        product = products[sku]

        sale_total += product["price"] * quantity
        sale_profit += (product["price"] - product["cost"]) * quantity

    for sku, item in cart.items():
        if sku in products:
            products [sku]["stock"] -= item["quantity"]

            if products[sku]["stock"] < 0:
                products[sku]["stock"] = 0
    old_sales = window.localStorage.getItem("total_sales")
    old_profit = window.localStorage.getItem("total_profit")

    try:
        total_sales = float(old_sales) or 0.0
    except (ValueError, TypeError):
        total_sales = 0.0
    
    try:
        total_profit = float(old_profit) or 0.0
    except (ValueError, TypeError):
        total_profit = 0.0

    total_sales += sale_total
    total_profit += sale_profit


    window.localStorage.setItem("total_sales", str(total_sales))
    window.localStorage.setItem("total_profit", str(total_profit))

    save_products()

    update_receipt(sale_total, sale_profit)

    clear_cart()

    display_products()
    
    document.getElementById("sales_msg").innerHTML = f"Sale completed"

def clear_cart(event=None):
    cart.clear()
    update_cart_table()
    calculate_total()

    document.getElementById("cart_msg").innerHTML = "Cart is Cleared."

def update_receipt(sale_total, sale_profit):
    receipt = document.getElementById("receipt")

    if receipt is None:
        return
    
    receipt.innerHTML = ""
    
    total = document.createElement("p")
    total.innerHTML = f"Total Sale: P{sale_total:.2f}"

    profit = document.createElement("p")
    profit.innerHTML = f"Profit: P{sale_profit:.2f}"

    receipt.appendChild(total)
    receipt.appendChild(profit)

def back_inv(event=None):
    if len(cart) > 0:
        document.getElementById("cart_msg").innerHTML = ("Can't return to inventory while there are items in the cart")
        return
    window.location.href = "dashboard.html"

def log_out(event=None):
    global cart

    cart.clear()

    window.location.href = "index.html"

def initialize():
    global admin_name, store_name, store_type
    admin_name = window.localStorage.getItem("admin_name") or ""
    store_name = window.localStorage.getItem("store_name") or ""
    store_type = window.localStorage.getItem("store_type") or ""
    load_products()

    if document.getElementById("prd_builder") is not None:
        display_store_info()
        display_sales_summary()
        update_product_options()
        display_inventory()

    if document.getElementById("cashier_prd") is not None:
        display_store_info()
        display_products()
        update_cart_table()
        calculate_total()

initialize()
