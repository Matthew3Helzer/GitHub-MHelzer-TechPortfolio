import datetime
import os

# --- CONFIGURATION ---
TAX_RATE = 0.0825  # 8.25% Midland, TX Standard Sales Tax
LOG_FILE = "past_orders.txt"
FUDGE_PRICE_PER_HALF_LB = 12.00
FUDGE_PRICE_PER_LB = 24.00  # ($12 per 0.5 lb)

# Main Menu
MENU = {
    "1":  {"name": "Ice Cream (Cup/Cone/Bowl)", "price": 0.00},  # Opens nested sub-menu
    "2":  {"name": "Dubai Sundae", "price": 13.99},
    "3":  {"name": "Other Sundae", "price": 11.99},
    "4":  {"name": "Quart", "price": 18.99},
    "5":  {"name": "Milkshake", "price": 10.99},
    "6":  {"name": "Kooler", "price": 10.99},                   # Opens flavor sub-menu
    "7":  {"name": "Gourmet Apple", "price": 0.00},             # Opens apple sub-menu
    "8":  {"name": "Fudge (By Weight - B2G1 Free Promo)", "price": 0.00}, # Opens fudge sub-menu
    "9":  {"name": "Toppings", "price": 1.00},
    "10": {"name": "Water", "price": 1.99},
    "11": {"name": "Soda", "price": 2.29},
    "12": {"name": "Custom / Misc Item", "price": 0.00}        # Triggers dynamic notes
}

# Ice Cream Sub-Menu Tiers
ICE_CREAM_OPTIONS = {
    "1":  {"name": "Small Cup", "price": 5.99},
    "2":  {"name": "Regular Cup", "price": 7.99},
    "3":  {"name": "Large Cup", "price": 8.80},
    "4":  {"name": "Small Cake Cone", "price": 5.99},
    "5":  {"name": "Large Cake Cone", "price": 9.49},
    "6":  {"name": "Small Waffle Bowl", "price": 7.99},
    "7":  {"name": "Regular Waffle Bowl", "price": 9.49},
    "8":  {"name": "Large Waffle Bowl", "price": 10.99},
    "9":  {"name": "Small Waffle Cone", "price": 7.99},
    "10": {"name": "Regular Waffle Cone", "price": 9.49},
    "11": {"name": "Large Waffle Cone", "price": 10.99},
    "12": {"name": "Heritage Small Waffle Bowl", "price": 8.99},
    "13": {"name": "Heritage Regular Waffle Bowl", "price": 10.49},
    "14": {"name": "Heritage Large Waffle Bowl", "price": 11.99},
    "15": {"name": "Heritage Small Waffle Cone", "price": 8.99},
    "16": {"name": "Heritage Regular Waffle Cone", "price": 10.49},
    "17": {"name": "Heritage Large Waffle Cone", "price": 11.99}
}

KOOLER_FLAVORS = {
    "L": "Lemon", "M": "Mango", "R": "Raspberry", "X": "Mix (Lemon & Raspberry)"
}

FUDGE_FLAVORS = {
    "1": "Chocolate",
    "2": "Chocolate Peanut Butter",
    "3": "Peanut Butter",
    "4": "Lemon",
    "5": "Key Lime Pie",
    "6": "Cookies and Cream"
}

APPLE_VARIETIES = {
    "1":  {"flavor": "Regular", "price": 9.99},
    "2":  {"flavor": "Pecan", "price": 10.99},
    "3":  {"flavor": "Peanut", "price": 10.99},
    "4":  {"flavor": "Apple Pie", "price": 11.99},
    "5":  {"flavor": "Toffee", "price": 11.99},
    "6":  {"flavor": "Sea Salt Milk", "price": 11.99},
    "7":  {"flavor": "Sea Salt Dark", "price": 11.99},
    "8":  {"flavor": "Pecan Turtle", "price": 12.99},
    "9":  {"flavor": "M&M", "price": 12.99},
    "10": {"flavor": "Striped Pecan", "price": 13.99},
    "11": {"flavor": "Everything Peanut", "price": 13.99},
    "12": {"flavor": "Oreo", "price": 13.99}
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n" + "="*60)
    print("              ICE CREAM EMERGENCY TERMINAL              ")
    print("="*60)
    for k, item in MENU.items():
        if item['price'] > 0:
            print(f"  [{k:>2}] {item['name']:<35} ${item['price']:.2f}")
        elif k in ["1", "6", "7", "8"]:
            print(f"  [{k:>2}] {item['name']:<35} (Opens Sub-Menu)")
        elif k == "12":
            print(f"  [{k:>2}] {item['name']:<35} (Custom Price + Note)")
    print("  ----------------------------------------------------------")
    print("  [13] ⚙️  MENU & PRICE MANAGER (Add/Edit Items)")
    print("-" * 60)
    print("  [C] Checkout   |   [S] Saved Orders   |   [Q] Quit")
    print("="*60)

def manage_main_menu_items():
    clear_screen()
    print("\n--- STANDARD MENU ITEMS ---")
    editable_items = {k: v for k, v in MENU.items() if v['price'] > 0 or k == "6"}
    for k, v in editable_items.items():
        print(f"  [{k:>2}] {v['name']:<32} ${v['price']:.2f}")
    print("\n  [A] Add New Item")
    print("  [B] Back to Management Center")
    
    choice = input("\nEnter item code, [A]dd, or [B]ack: ").strip().upper()
    if choice == 'B':
        return
    elif choice == 'A':
        name = input("Enter new item name (or 'B' to cancel): ").strip()
        if not name or name.upper() == 'B':
            return
        try:
            price = float(input(f"Enter price for '{name}': $"))
            if price < 0:
                print("❌ Price cannot be negative.")
                input("Press Enter to continue...")
                return
            new_key = str(max([int(k) for k in MENU.keys() if k.isdigit()] + [0]) + 1)
            MENU[new_key] = {"name": name, "price": price}
            print(f"✔️ Added '{name}' as item [{new_key}] for ${price:.2f}!")
        except ValueError:
            print("❌ Invalid price input.")
        input("Press Enter to continue...")
    elif choice in editable_items:
        try:
            new_p = float(input(f"Enter new price for '{MENU[choice]['name']}': $"))
            if new_p >= 0:
                MENU[choice]['price'] = new_p
                print("✔️ Price updated successfully!")
            else:
                print("❌ Price cannot be negative.")
        except ValueError:
            print("❌ Invalid price entered.")
        input("Press Enter to continue...")

def manage_ice_cream_prices():
    clear_screen()
    print("\n--- ICE CREAM OPTIONS & PRICING ---")
    for k, v in ICE_CREAM_OPTIONS.items():
        print(f"  [{k:>2}] {v['name']:<35} ${v['price']:.2f}")
    print("\n  [A] Add New Ice Cream Size/Option")
    print("  [B] Back to Management Center")
    
    choice = input("\nEnter option code to edit, [A]dd, or [B]ack: ").strip().upper()
    if choice == 'B':
        return
    elif choice == 'A':
        name = input("Enter new option name (e.g., Jumbo Waffle Cone) (or 'B' to cancel): ").strip()
        if not name or name.upper() == 'B':
            return
        try:
            price = float(input(f"Enter price for '{name}': $"))
            if price < 0:
                print("❌ Price cannot be negative.")
                input("Press Enter to continue...")
                return
            new_key = str(max([int(k) for k in ICE_CREAM_OPTIONS.keys()] + [0]) + 1)
            ICE_CREAM_OPTIONS[new_key] = {"name": name, "price": price}
            print(f"✔️ Added '{name}' as option [{new_key}] for ${price:.2f}!")
        except ValueError:
            print("❌ Invalid price input.")
        input("Press Enter to continue...")
    elif choice in ICE_CREAM_OPTIONS:
        try:
            item_name = ICE_CREAM_OPTIONS[choice]['name']
            curr_price = ICE_CREAM_OPTIONS[choice]['price']
            new_p = float(input(f"Enter new price for '{item_name}' (Current: ${curr_price:.2f}): $"))
            if new_p >= 0:
                ICE_CREAM_OPTIONS[choice]['price'] = new_p
                print(f"✔️ Price updated! '{item_name}' is now ${new_p:.2f}")
            else:
                print("❌ Price cannot be negative.")
        except ValueError:
            print("❌ Invalid price entered.")
        input("Press Enter to continue...")

def manage_fudge_prices():
    global FUDGE_PRICE_PER_HALF_LB, FUDGE_PRICE_PER_LB
    clear_screen()
    print("\n--- FUDGE PRICING & FLAVORS ---")
    print(f"Current Base Price: ${FUDGE_PRICE_PER_HALF_LB:.2f} per 1/2 lb (${FUDGE_PRICE_PER_LB:.2f}/lb)")
    print("\nFlavors Available:")
    for k, v in FUDGE_FLAVORS.items():
        print(f"  [{k}] {v}")
    print("\n  [E] Edit Price per 1/2 lb")
    print("  [A] Add New Fudge Flavor")
    print("  [B] Back to Management Center")
    
    choice = input("\nSelect action ([E]dit price, [A]dd flavor, or [B]ack): ").strip().upper()
    if choice == 'B':
        return
    elif choice == 'E':
        try:
            new_half_p = float(input(f"Enter new price for 1/2 lb (Current: ${FUDGE_PRICE_PER_HALF_LB:.2f}): $"))
            if new_half_p >= 0:
                FUDGE_PRICE_PER_HALF_LB = new_half_p
                FUDGE_PRICE_PER_LB = new_half_p * 2
                print(f"✔️ Fudge price updated to ${FUDGE_PRICE_PER_HALF_LB:.2f} per 1/2 lb!")
            else:
                print("❌ Price cannot be negative.")
        except ValueError:
            print("❌ Invalid price entered.")
        input("Press Enter to continue...")
    elif choice == 'A':
        new_flav = input("Enter new fudge flavor name (or 'B' to cancel): ").strip()
        if new_flav and new_flav.upper() != 'B':
            new_key = str(max([int(k) for k in FUDGE_FLAVORS.keys()] + [0]) + 1)
            FUDGE_FLAVORS[new_key] = new_flav
            print(f"✔️ Added '{new_flav}' as option [{new_key}]!")
            input("Press Enter to continue...")

def manage_apple_prices():
    clear_screen()
    print("\n--- GOURMET APPLE PRICING ---")
    for k, v in APPLE_VARIETIES.items():
        print(f"  [{k:>2}] Apple ({v['flavor']}):{'' :<18} ${v['price']:.2f}")
    print("\n  [A] Add New Gourmet Apple Variety")
    print("  [B] Back to Management Center")
    
    choice = input("\nEnter option code to edit, [A]dd, or [B]ack: ").strip().upper()
    if choice == 'B':
        return
    elif choice == 'A':
        flavor = input("Enter new apple flavor/variety name (or 'B' to cancel): ").strip()
        if not flavor or flavor.upper() == 'B':
            return
        try:
            price = float(input(f"Enter price for Apple ({flavor}): $"))
            if price < 0:
                print("❌ Price cannot be negative.")
                input("Press Enter to continue...")
                return
            new_key = str(max([int(k) for k in APPLE_VARIETIES.keys()] + [0]) + 1)
            APPLE_VARIETIES[new_key] = {"flavor": flavor, "price": price}
            print(f"✔️ Added 'Apple ({flavor})' as option [{new_key}] for ${price:.2f}!")
        except ValueError:
            print("❌ Invalid price input.")
        input("Press Enter to continue...")
    elif choice in APPLE_VARIETIES:
        try:
            new_p = float(input(f"Enter new price for 'Apple ({APPLE_VARIETIES[choice]['flavor']})': $"))
            if new_p >= 0:
                APPLE_VARIETIES[choice]['price'] = new_p
                print("✔️ Price updated successfully!")
            else:
                print("❌ Price cannot be negative.")
        except ValueError:
            print("❌ Invalid price entered.")
        input("Press Enter to continue...")

def manage_menu_prices():
    """Main Price and Menu Management Center."""
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("            ⚙️  MENU & PRICE MANAGEMENT CENTER            ")
        print("="*60)
        print("  Select category to add or edit items:\n")
        print("  [1] Standard Menu Items (Sundaes, Drinks, Misc, etc.)")
        print("  [2] Ice Cream Sizes & Options (Cups, Cones, Bowls)")
        print("  [3] Fudge Prices & Flavors")
        print("  [4] Gourmet Apple Varieties")
        print("  [B] Back to Main Menu")
        print("="*60)
        
        cat_choice = input("\nSelect Category (1-4) or [B] to go back: ").strip().upper()
        
        if cat_choice == 'B':
            break
        elif cat_choice == '1':
            manage_main_menu_items()
        elif cat_choice == '2':
            manage_ice_cream_prices()
        elif cat_choice == '3':
            manage_fudge_prices()
        elif cat_choice == '4':
            manage_apple_prices()

def handle_ice_cream_selection():
    while True:
        print("\n  ================= SELECT ICE CREAM TIER =================")
        items = list(ICE_CREAM_OPTIONS.items())
        for i in range(0, len(items), 2):
            k1, v1 = items[i]
            col1 = f"  [{k1:>2}] {v1['name']:<28} ${v1['price']:.2f}"
            if i + 1 < len(items):
                k2, v2 = items[i+1]
                col2 = f"    [{k2:>2}] {v2['name']:<28} ${v2['price']:.2f}"
                print(col1 + col2)
            else:
                print(col1)
        print("  ---------------------------------------------------------")
        print("  [B] Back to Main Menu")
        print("  =========================================================")
        choice = input(f"  Select item code (1-{len(ICE_CREAM_OPTIONS)}) or [B]ack: ").strip().upper()
        if choice == 'B':
            return None, None
        if choice in ICE_CREAM_OPTIONS:
            return ICE_CREAM_OPTIONS[choice]['name'], ICE_CREAM_OPTIONS[choice]['price']
        print("  Invalid selection. Please try again.")

def handle_kooler_selection():
    while True:
        print("\n  --- Select Kooler Flavor ---")
        print("  [L] Lemon  |  [M] Mango  |  [R] Raspberry  |  [X] Mix")
        print("  [B] Back to Main Menu")
        flav_choice = input("  Select flavor letter or [B]ack: ").strip().upper()
        if flav_choice == 'B':
            return None
        if flav_choice in KOOLER_FLAVORS:
            return f"Kooler ({KOOLER_FLAVORS[flav_choice]})"
        print("  Invalid flavor selection.")

def handle_fudge_selection():
    while True:
        print("\n  ==================== SELECT FUDGE FLAVOR ====================")
        print(f"  PRICING: ${FUDGE_PRICE_PER_HALF_LB:.2f} / 0.5 lb (${FUDGE_PRICE_PER_LB:.2f} / lb)")
        print("  SPECIAL PROMO: Buy 2 Get 1 FREE (Mix & Match pieces!)")
        print("  -------------------------------------------------------------")
        for k, name in FUDGE_FLAVORS.items():
            print(f"  [{k}] {name}")
        print("  -------------------------------------------------------------")
        print("  [B] Back to Main Menu")
        print("  =============================================================")
        choice = input(f"  Select flavor code (1-{len(FUDGE_FLAVORS)}) or [B]ack: ").strip().upper()
        if choice == 'B':
            return None, None, None
        if choice in FUDGE_FLAVORS:
            try:
                weight_in = input(f"  Enter weight in lbs for {FUDGE_FLAVORS[choice]} Fudge (or [B]ack): ").strip().upper()
                if weight_in == 'B':
                    continue
                weight = float(weight_in)
                if weight <= 0:
                    print("  Weight must be greater than zero.")
                    continue
                cost = weight * FUDGE_PRICE_PER_LB
                return f"Fudge ({FUDGE_FLAVORS[choice]} - {weight:.2f} lbs)", cost, weight
            except ValueError:
                print("  Invalid weight entered.")
                continue
        print("  Invalid flavor choice.")

def handle_apple_selection():
    while True:
        print("\n  ================ SELECT GOURMET APPLE ================")
        items = list(APPLE_VARIETIES.items())
        for i in range(0, len(items), 2):
            k1, v1 = items[i]
            col1 = f"  [{k1:>2}] {v1['flavor']:<18} ${v1['price']:.2f}"
            if i + 1 < len(items):
                k2, v2 = items[i+1]
                col2 = f"    [{k2:>2}] {v2['flavor']:<18} ${v2['price']:.2f}"
                print(col1 + col2)
            else:
                print(col1)
        print("  ------------------------------------------------------")
        print("  [B] Back to Main Menu")
        print("  ======================================================")
        choice = input(f"  Select apple option number (1-{len(APPLE_VARIETIES)}) or [B]ack: ").strip().upper()
        if choice == 'B':
            return None, None
        if choice in APPLE_VARIETIES:
            return f"Apple ({APPLE_VARIETIES[choice]['flavor']})", APPLE_VARIETIES[choice]['price']
        print("  Invalid selection.")

def calculate_fudge_discount(cart):
    """
    Breaks down all fudge purchases into individual pieces/entries,
    finds the total pieces qualifying for B2G1, and subtracts the exact
    cost of the piece(s) with the lowest cost/weight.
    """
    fudge_pieces = []
    for item in cart:
        if 'Fudge' in item['name'] and item.get('weight', 0) > 0:
            fudge_pieces.append(item['price'])
            
    if len(fudge_pieces) < 3:
        return 0.0

    fudge_pieces.sort()
    free_items_count = len(fudge_pieces) // 3
    return sum(fudge_pieces[:free_items_count])

def process_payment(grand_total):
    """Prompts cashier for payment method and handles cash change logic."""
    while True:
        print("\n  ============= PAYMENT METHOD =============")
        print("  [1] Cash")
        print("  [2] Card")
        print("  [B] Back to Cart")
        print("  ==========================================")
        choice = input("  Select payment method (1-2) or [B]ack: ").strip().upper()
        
        if choice == 'B':
            return None, None, None
        elif choice == '2':
            return "Card", grand_total, 0.0
        elif choice == '1':
            while True:
                try:
                    cash_in = input(f"  Enter cash amount tendered (Total Due: ${grand_total:.2f}) [or 'B' to back]: $").strip().upper()
                    if cash_in == 'B':
                        break
                    cash_tendered = float(cash_in)
                    if cash_tendered < grand_total:
                        print(f"  ❌ Insufficient cash. Customer still owes ${grand_total - cash_tendered:.2f}")
                        continue
                    change_due = cash_tendered - grand_total
                    return "Cash", cash_tendered, change_due
                except ValueError:
                    print("  ❌ Invalid amount. Please enter a valid number.")
        else:
            print("  ❌ Invalid selection. Choose 1, 2, or B.")

def log_order(order_id, items, subtotal, discount, tax, total, pay_type, cash_tendered, change_due):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"ORDER ID: {order_id}\n")
            f.write(f"TIMESTAMP: {timestamp}\n")
            f.write(f"PAYMENT METHOD: {pay_type}\n")
            f.write("ITEMS:\n")
            for item in items:
                f.write(f"  - {item['qty']}x {item['name']}: ${item['price']:.2f} total\n")
            f.write(f"SUBTOTAL: ${subtotal:.2f}\n")
            if discount > 0:
                f.write(f"PROMO DISCOUNT (Fudge B2G1 Lowest Piece Free): -${discount:.2f}\n")
            f.write(f"SALES TAX ({TAX_RATE*100:.2f}%): ${tax:.2f}\n")
            f.write(f"TOTAL: ${total:.2f}\n")
            if pay_type == "Cash":
                f.write(f"CASH TENDERED: ${cash_tendered:.2f}\n")
                f.write(f"CHANGE DUE: ${change_due:.2f}\n")
            f.write("-" * 60 + "\n")
    except Exception as e:
        print(f"Error tracking order data: {e}")

def view_past_orders():
    clear_screen()
    print("\n" + "="*60)
    print("               PAST TRANSACTION HISTORY               ")
    print("="*60)
    if not os.path.exists(LOG_FILE):
        print("No recorded transactions found.")
    else:
        try:
            with open(LOG_FILE, "r") as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading log file: {e}")
    input("\nPress Enter to return to main menu...")

def run_pos():
    order_counter = 1
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                order_counter = f.read().count("ORDER ID:") + 1
        except Exception:
            order_counter = 1

    while True:
        clear_screen()
        display_menu()
        current_cart = []
        
        while True:
            if current_cart:
                print(f"\n CURRENT TICKET ({len(current_cart)} lines added):")
                for item in current_cart:
                    print(f"   • {item['qty']}x {item['name']} (${item['price'] * item['qty']:.2f})")
            
            choice = input("\nEnter code or Action (C/S/Q): ").strip().upper()
            
            if choice == 'Q':
                print("System closed safely.")
                return
            elif choice == 'S':
                view_past_orders()
                break
            elif choice in ['13', 'M']:
                manage_menu_prices()
                break
            elif choice == 'C':
                if not current_cart:
                    print("Cannot checkout an empty cart.")
                    continue
                break
            
            if choice in MENU:
                weight = 0.0
                if choice == "1":
                    name, price = handle_ice_cream_selection()
                    if name is None:
                        continue
                elif choice == "6":
                    name = handle_kooler_selection()
                    if name is None:
                        continue
                    price = MENU[choice]['price']
                elif choice == "7":
                    name, price = handle_apple_selection()
                    if name is None:
                        continue
                elif choice == "8":
                    name, price, weight = handle_fudge_selection()
                    if name is None:
                        continue
                elif choice == "12":
                    cust_p_in = input("Enter custom price (or 'B' to cancel): $").strip().upper()
                    if cust_p_in == 'B':
                        continue
                    try:
                        price = float(cust_p_in)
                        if price < 0:
                            print("Price cannot be negative.")
                            continue
                    except ValueError:
                        print("Invalid price format. Action ignored.")
                        continue
                    
                    note = input("Enter receipt note for custom item (or Enter for default): ").strip()
                    name = f"Custom Item ({note})" if note else "Custom / Misc Item"
                else:
                    name = MENU[choice]['name']
                    price = MENU[choice]['price']
                
                # Quantity selection step (for non-fudge items)
                if choice == "8":
                    qty = 1  # Fudge quantity is implicit via weight
                else:
                    qty_in = input(f"Quantity of [{name}] (or [B]ack): ").strip().upper()
                    if qty_in == 'B':
                        continue
                    try:
                        qty = int(qty_in)
                        if qty <= 0:
                            raise ValueError
                    except ValueError:
                        qty = 1
                        print("Invalid quantity. Defaulted to 1.")
                
                current_cart.append({"name": name, "price": price, "qty": qty, "weight": weight})
                print(f" Added {name} to current ticket.")
            else:
                print(" Invalid input. Choose a valid menu code, C, S, or Q.")

        if not current_cart or choice in ['S', '13', 'M']:
            continue

        # --- CALCULATIONS ---
        gross_subtotal = sum(item['price'] * item['qty'] for item in current_cart)
        fudge_discount = calculate_fudge_discount(current_cart)
        net_subtotal = gross_subtotal - fudge_discount
        sales_tax = net_subtotal * TAX_RATE
        grand_total = net_subtotal + sales_tax

        # --- PROCESS PAYMENT METHOD ---
        pay_type, cash_tendered, change_due = process_payment(grand_total)
        if pay_type is None:
            continue  # Cashier chose [B]ack during payment, return to main menu with cart intact

        # --- DISPLAY COMPACT RECEIPT ---
        clear_screen()
        print("\n" + "═"*60)
        print("                  SALES RECEIPT                  ")
        print("═"*60)
        print(f"Ticket: #IC-{order_counter:04d}")
        print(f"Time:   {datetime.datetime.now().strftime('%I:%M %p')}")
        print(f"Type:   {pay_type}")
        print("-" * 60)
        
        for item in current_cart:
            item_total = item['price'] * item['qty']
            print(f"{item['qty']}x {item['name'][:35]:<35} ${item_total:>12.2f}")
            if item['qty'] > 1:
                print(f"   (${item['price']:.2f} each)")
                
        print("-" * 60)
        print(f"GROSS SUBTOTAL:{'':<26}${gross_subtotal:>12.2f}")
        if fudge_discount > 0:
            print(f"FUDGE PROMO (CHEAPEST FREE):{'':<14}-${fudge_discount:>12.2f}")
            print(f"NET SUBTOTAL:{'':<28}${net_subtotal:>12.2f}")
        print(f"TAX ({TAX_RATE*100:.2f}%):{'':<28}${sales_tax:>12.2f}")
        print("═" * 60)
        print(f"TOTAL DUE:{'':<31}${grand_total:>12.2f}")
        
        if pay_type == "Cash":
            print(f"CASH TENDERED:{'':<27}${cash_tendered:>12.2f}")
            print(f"CHANGE DUE:{'':<30}${change_due:>12.2f}")
            
        print("═" * 60)

        # --- PROCESS TRANSACTION ---
        confirm = input("\nConfirm and finalize sale? (Y/N): ").strip().upper()
        if confirm == 'Y':
            log_order(f"IC-{order_counter:04d}", current_cart, gross_subtotal, fudge_discount, sales_tax, grand_total, pay_type, cash_tendered, change_due)
            if pay_type == "Cash" and change_due > 0:
                print(f"\n💵 RETURN CHANGE TO CUSTOMER: ${change_due:.2f}")
            print("✔️ Order successfully processed and saved!")
            order_counter += 1
        else:
            print("\nTransaction Voided.")
        
        input("\nPress Enter to reset terminal for next transaction...")

if __name__ == "__main__":
    run_pos()