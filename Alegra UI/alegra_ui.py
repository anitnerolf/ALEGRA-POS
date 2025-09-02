import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

cart = []

def load_products():
    db_path = os.path.join(os.path.dirname(__file__), '../database/alegra_products.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, name, price FROM products')
    products = c.fetchall()
    conn.close()
    return products

def open_product_window():
    product_window = tk.Toplevel(root)
    product_window.title("Select Products")
    product_window.geometry("300x400")

    new_product_button = tk.Button(
        product_window,
        text="Add New Product",
        command=lambda: open_new_product_form(product_window),
        bg="green",
        fg="white"
    )
    new_product_button.pack(pady=(0, 10))

    product_frame = tk.Frame(product_window, bg='white', padx=10, pady=10)
    product_frame.pack(fill='both', expand=True)

    products = load_products()
    for i, product in enumerate(products):
        btn = tk.Button(
            product_frame,
            text=f"{product[1]} - ${product[2]:.2f}",
            command=lambda p=product: [add_to_cart(p)]
        )
        btn.grid(row=i, column=0, sticky="ew", pady=2)

    # Make buttons expand horizontally
    product_frame.columnconfigure(0, weight=1)
    separator = tk.Frame(product_window, height=2, bg="gray")
    separator.pack(fill='x', pady=(10, 5))

    # Add Done/Close button
    close_button = tk.Button(
        product_window,
        text="Done",
        command=product_window.destroy,
        bg="lightgray"
    )
    close_button.pack(pady=(0, 10))


def open_new_product_form(product_window):
    new_product_window = tk.Toplevel(product_window)
    new_product_window.title("Add New Product")
    new_product_window.geometry("300x200")

    tk.Label(new_product_window,text="Product Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(new_product_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(new_product_window, text="Product Price").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    price_entry = tk.Entry(new_product_window)
    price_entry.grid(row=1, column=1, padx=10, pady=5)

    def save_product():
        name = name_entry.get().strip()
        success = False
        try:
            price = float(price_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Price", "Please enter a number")
            return

        if not name:
            messagebox.showerror("Missing Info", "Product name is required.")
            return

        db_path = os.path.join(os.path.dirname(__file__), '../database/alegra_products.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM products WHERE name = ?", (name,))
        count = c.fetchone()[0]
        if count > 0:
            messagebox.showerror("Duplicate Product", f"A product named '{name}' already exists.")
            conn.close()
            return

        try:
            c.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))
            conn.commit()
            success = True  # ✅ Mark success
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save product.\n{str(e)}")
        finally:
            conn.close()

        if success:
            messagebox.showinfo("Success", f"Product '{name}' added.")
            new_product_window.destroy()
            product_window.destroy()
            open_product_window()

    save_btn = tk.Button(new_product_window, text="Save", command=save_product, bg="blue", fg="white")
    save_btn.grid(row=2, column=0, columnspan=2, pady=10)


def add_to_cart(product):
    cart.append(product)
    update_cart()

def update_cart():
    cart_list.delete(0, tk.END)
    total = 0
    for item in cart:
        cart_list.insert(tk.END, f"{item[1]} - ${item[2]:.2f}")
        total += item[2]
    total_label.config(text=f"Total: ${total:.2f}")

def checkout():
    if not cart:
        messagebox.showerror("Error", "No products added to cart")
        return
    total = sum(item[2] for item in cart)
    messagebox.showinfo("Checkout", f"Total: ${total:.2f}\nPayment recorded.")
    cart.clear()
    update_cart()

# --- Main UI ---

root = tk.Tk()
root.title("Alegra POS System")
root.geometry("500x500")

root.columnconfigure(1, weight=2)  # Cart area
root.rowconfigure(1, weight=1)

# Header label
label = tk.Label(root, text="Welcome to Alegra POS", font=("Helvetica", 16), pady=10)
label.grid(row=0, column=0, columnspan=2, sticky="ew")

# Frame for products
frame = tk.Frame(root, bg='light blue', padx=10, pady=10)
frame.grid(row=1, column=0, sticky="nsew")

# Make all buttons expand horizontally
frame.columnconfigure(0, weight=1)

# Frame for cart
cart_frame = tk.Frame(root, bg='light blue', padx=10, pady=10)
cart_frame.grid(row=1, column=1, sticky="nsew")

product_window_button = tk.Button(cart_frame, text="Choose Products", command=open_product_window)
product_window_button.grid(row=0, column=0, padx=1, pady=1)

# Cart listbox
cart_list = tk.Listbox(cart_frame, height=15)
cart_list.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

# Total label
total_label = tk.Label(cart_frame, text="Total: $0.00", font=("Arial", 12, "bold"))
total_label.grid(row=2, column=0, pady=(0, 10))

# Checkout button
checkout_button = tk.Button(cart_frame, text="Checkout", command=checkout, bg="red", fg="white")
checkout_button.grid(row=3, column=0)

# Make cart frame expandable
cart_frame.rowconfigure(0, weight=1)
cart_frame.columnconfigure(0, weight=1)

root.mainloop()
