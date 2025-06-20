import tkinter as tk
from tkinter import messagebox
import datetime

# --- Product, CartItem, ShoppingCart, and Shop logic classes ---

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total_price(self):
        return self.product.price * self.quantity

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_to_cart(self, product, quantity):
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def view_cart(self):
        return [(item.product.name, item.quantity, item.get_total_price()) for item in self.items]

    def get_total_amount(self):
        return sum(item.get_total_price() for item in self.items)

    def clear_cart(self):
        self.items = []

    def remove_from_cart(self, product_id):
        for item in self.items:
            if item.product.product_id == product_id:
                item.quantity -= 1
                if item.quantity <= 0:
                    self.items.remove(item)
                return

class Shop:
    def __init__(self):
        self.products = [
            Product(1, "Notebook", 50),
            Product(2, "Stationery Kit", 200),
            Product(3, "Sticky Notes", 60),
            Product(4, "Scientific Calculator", 1100),
            Product(5, "Noise-cancelling Headphones", 2500),
            Product(6, "Study Lamp", 1000),
            Product(7, "Study Chair", 3700),
            Product(8, "Backpack", 1500),
            Product(9, "Whiteboard", 700),
            Product(10, "Highlighter Pens", 25)
        ]

        self.users = {}  # username: password
        self.logged_in_user = None
        self.cart = ShoppingCart()

# --- GUI Application Class ---

class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Online Shopping App")
        self.shop = Shop()
        self.build_login_screen()

    def build_login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to Online Shop", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Signup", command=self.signup).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.shop.users and self.shop.users[username] == password:
            self.shop.logged_in_user = username
            self.build_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.shop.users:
            messagebox.showerror("Signup Failed", "User already exists")
        else:
            self.shop.users[username] = password
            messagebox.showinfo("Signup Success", "Account created. You can now log in.")

    def build_main_screen(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome {self.shop.logged_in_user}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Available Products", font=("Arial", 14)).pack()

        for product in self.shop.products:
            frame = tk.Frame(self.root)
            frame.pack(pady=2)
            tk.Label(frame, text=f"{product.name} - ₹{product.price}", width=30, anchor="w").pack(side="left")
            qty_var = tk.IntVar()
            qty_var.set(1)
            qty_entry = tk.Entry(frame, textvariable=qty_var, width=5)
            qty_entry.pack(side="left")
            tk.Button(frame, text="Add to Cart",
                      command=lambda p=product, q=qty_var: self.add_to_cart(p, q)).pack(side="left")

        tk.Button(self.root, text="🛍 View Cart", command=self.view_cart).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.build_login_screen).pack()

    def add_to_cart(self, product, qty_var):
        quantity = qty_var.get()
        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0")
            return
        self.shop.cart.add_to_cart(product, quantity)
        messagebox.showinfo("Added", f"{product.name} added to cart.")

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("🛒 Your Cart")

        cart = self.shop.cart.items
        if not cart:
            tk.Label(cart_window, text="Your cart is empty.").pack(padx=20, pady=20)
            return

        for item in cart:
            frame = tk.Frame(cart_window)
            frame.pack(pady=2, anchor='w')

            name = item.product.name
            qty = item.quantity
            total = item.get_total_price()

            tk.Label(frame, text=f"{name} x {qty} = ₹{total}", width=30, anchor="w").pack(side="left")
            tk.Button(frame, text="➕", command=lambda p=item.product: self.add_to_cart(p, tk.IntVar(value=1))).pack(side="left")
            tk.Button(frame, text="❌", command=lambda pid=item.product.product_id, win=cart_window: self.remove_from_cart(pid, win)).pack(side="left")

        total = self.shop.cart.get_total_amount()
        tk.Label(cart_window, text=f"Total: ₹{total}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(cart_window, text="✅ Checkout", command=lambda: self.checkout(cart_window)).pack()

    def remove_from_cart(self, product_id, window):
        self.shop.cart.remove_from_cart(product_id)
        window.destroy()
        self.view_cart()

    def checkout(self, window):
        if not self.shop.cart.items:
            messagebox.showwarning("Empty Cart", "Your cart is empty!")
            return

        bill_window = tk.Toplevel(self.root)
        bill_window.title("🧾 Detailed Checkout")

        tk.Label(bill_window, text="🧾 Invoice", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(bill_window, text=f"Customer: {self.shop.logged_in_user}").pack()
        tk.Label(bill_window, text=f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}").pack()

        header = tk.Frame(bill_window)
        header.pack(pady=5)
        tk.Label(header, text="Product", width=20, anchor='w').grid(row=0, column=0)
        tk.Label(header, text="Qty", width=5).grid(row=0, column=1)
        tk.Label(header, text="Price", width=10).grid(row=0, column=2)
        tk.Label(header, text="Total", width=10).grid(row=0, column=3)

        subtotal = 0
        for i, item in enumerate(self.shop.cart.items):
            row = tk.Frame(bill_window)
            row.pack()
            name = item.product.name
            qty = item.quantity
            price = item.product.price
            total = item.get_total_price()
            subtotal += total

            tk.Label(row, text=name, width=20, anchor='w').grid(row=0, column=0)
            tk.Label(row, text=str(qty), width=5).grid(row=0, column=1)
            tk.Label(row, text=f"₹{price}", width=10).grid(row=0, column=2)
            tk.Label(row, text=f"₹{total}", width=10).grid(row=0, column=3)

        tax = round(subtotal * 0.18, 2)
        final_total = round(subtotal + tax, 2)

        tk.Label(bill_window, text=f"\nSubtotal: ₹{subtotal}").pack()
        tk.Label(bill_window, text=f"Tax (18%): ₹{tax}").pack()
        tk.Label(bill_window, text=f"Total to Pay: ₹{final_total}", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(bill_window, text="✅ Confirm Payment", command=lambda: self.finalize_checkout(bill_window)).pack(pady=10)

    def finalize_checkout(self, bill_window):
        self.shop.cart.clear_cart()
        bill_window.destroy()
        messagebox.showinfo("Success", "Payment successful! Thank you for shopping.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x600")
    app = ShoppingApp(root)
    root.mainloop()
