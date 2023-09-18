import sys
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from services import DataModelService


bgpfgl_style = dict(
    background="#a0d2eb"
)

class TkCallWrapper(tk.CallWrapper):
    def __call__(self, *args):
        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except (SystemExit, KeyboardInterrupt) as e:
            sys.exit()
        except Exception as e:
            if not isinstance(e, tk.TclError):
                print(e)
                messagebox.showerror(
                    title=f"{e.__class__.__name__}",
                    message=str(e)
                )

class Application():
    def __init__(self) -> None:
        tk.CallWrapper = TkCallWrapper
        self.root = root = tk.Tk()
        root.title("P.E Tuckshop")
        root.minsize(800, 600)
        root.maxsize(800, 600)
        self.user: dict = None
        self.dms = DataModelService()
        self.container = container = tk.Frame(root, **bgpfgl_style)
        container.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.render_login()
    
    def get_container_frame(self):
        self.clear_widget(self.container)
        frame = tk.Frame(self.container, **bgpfgl_style)
        frame.place(relheight=0.89, relwidth=0.98, relx=0.01, rely=0.1)
        tk.Button(self.container, text="H O M E", command=self.render_home, foreground="#000000", background="#a0d2eb",
                  relief=tk.FLAT
        ).place(relheight=0.1, relwidth=1, relx=0, rely=0.0)
        return frame
    
    @classmethod
    def clear_widget(cls, widget: tk.Widget):
        inner_widgets = list(widget.children.values())
        for w in inner_widgets:
            w.destroy()

    def render_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        actions_menu = tk.Menu(menu)
        menu.add_cascade(label="Actions", menu=actions_menu)
        actions_menu.add_command(label="Home", command=self.render_home)
        actions_menu.add_command(label="Logout", command=self.logout)
        actions_menu.add_command(label="Exit", command=self.exit)
    
    def render_login(self):
        self.clear_widget(self.container)
        tk.Label(self.container, text="P.E Tuckshop Login", **bgpfgl_style).place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)
        form_frame = tk.Frame(self.container, **bgpfgl_style)
        form_frame.place(relx=0.2, rely=0.4, relheight=0.5, relwidth=0.6)
        username_var, password_var = tk.StringVar(form_frame, ""), tk.StringVar(form_frame, "")
        def submit_login_form(*args, **kwargs):
            password = password_var.get()
            username = username_var.get()
            u = self.dms.login(username, password)
            if u:
                self.user = u
                self.render_menu()
                self.render_home()
            else:
                messagebox.showerror("Invalid", "User with the given name/pasword was not found!")
        tk.Label(form_frame, text="Username").pack(side=tk.TOP, fill=tk.X)
        tk.Entry(form_frame, textvariable=username_var).pack(side=tk.TOP, fill=tk.X)
        tk.Label(form_frame, text="Password").pack(side=tk.TOP, fill=tk.X)
        tk.Entry(form_frame, textvariable=password_var, show="*").pack(side=tk.TOP, fill=tk.X)
        tk.Button(form_frame, text="Login", command=submit_login_form).pack(side=tk.TOP, fill=tk.X)
    
    def render_home(self):
        frame = self.get_container_frame()
        tk.Button(frame, text="POS", command=self.render_pos).place(relx=0.01, rely=0.0, relheight=0.32, relwidth=0.48)
        tk.Button(frame, text="Sales", command=self.render_sales_list).place(relx=0.51, rely=0.0, relheight=0.32, relwidth=0.48)
        tk.Button(frame, text="Purchases", command=self.render_purchases_list).place(relx=0.01, rely=0.33, relheight=0.32, relwidth=0.48)
        tk.Button(frame, text="Products", command=self.render_products_list).place(relx=0.51, rely=0.33, relheight=0.32, relwidth=0.48)
        tk.Button(frame, text="Users", command=self.render_users_list).place(relx=0.01, rely=0.68, relheight=0.32, relwidth=0.48)
        tk.Button(frame, text="Logout", command=self.logout).place(relx=0.51, rely=0.68, relheight=0.32, relwidth=0.48)
    
    def render_products_list(self):
        frame = self.get_container_frame()
        tk.Button(frame, text="Add New", command=self.render_products_form).place(relheight=0.15, relwidth=1, relx=0, rely=0)
        products = self.dms.fetch("SELECT * FROM products")
        columns = ("id", "name", "price", "qty")
        table = ttk.Treeview(frame, columns=columns, show="headings")
        [table.heading(i, text=i) for i in columns]
        table.place(relheight=0.85, relwidth=1, relx=0, rely=0.15)
        for product in products:
            table.insert("", tk.END, values=list(product.values()))
    
    def render_products_form(self, product: dict={}):
        frame = self.get_container_frame()
        name_var, price_var, qty_var = tk.StringVar(frame, product.get("name")), tk.DoubleVar(frame, product.get("price")), tk.IntVar(frame, product.get("qty"))
        def save():
            name, price, qty = name_var.get(), price_var.get(), qty_var.get()
            if product.get("id"):
                self.dms.c.execute(f'UPDATE products SET (name="{name}", price={price}, qty={qty}) WHERE id={product.get("id")}')
            else:
                self.dms.c.execute(f'INSERT INTO products ("name", "price", "qty") VALUES ("{name}", {price}, {0})')
            self.render_products_list()
        tk.Label(frame, text="Name").grid(row=0, column=0)
        tk.Entry(frame, textvariable=name_var).grid(row=0, column=1)
        tk.Label(frame, text="Price").grid(row=1, column=0)
        tk.Entry(frame, textvariable=price_var).grid(row=1, column=1)
        # tk.Label(frame, text="Qty").grid(row=2, column=0)
        # tk.Entry(frame, textvariable=qty_var).grid(row=2, column=1)
        tk.Button(frame, text="Save", command=save).grid(row=3, column=1)
        tk.Button(frame, text="Back", command=self.render_products_list).grid(row=3, column=0)
    
    def render_users_list(self):
        frame = self.get_container_frame()
        tk.Button(frame, text="Add New", command=self.render_users_form).place(relheight=0.15, relwidth=1, relx=0, rely=0)
        users = self.dms.fetch("SELECT id, username FROM users")
        columns = ("id", "username")
        table = ttk.Treeview(frame, columns=columns, show="headings")
        [table.heading(i, text=i) for i in columns]
        table.place(relheight=0.85, relwidth=1, relx=0, rely=0.15)
        for user in users:
            table.insert("", tk.END, values=(user["id"], user["username"]))
    
    def render_users_form(self, user: dict={}):
        frame = self.get_container_frame()
        username_var, password_var = tk.StringVar(frame, user.get("username")), tk.StringVar(frame, user.get("password"))
        def save():
            username, password = username_var.get(), password_var.get()
            if user.get("id"):
                self.dms.c.execute(f'UPDATE users SET (username="{username}", password="{password}") WHERE id={user.get("id")}')
            else:
                self.dms.c.execute(f'INSERT INTO users ("username", "password") VALUES ("{username}", "{password}")')
            self.render_users_list()
        tk.Label(frame, text="Username").grid(row=0, column=0)
        tk.Entry(frame, textvariable=username_var).grid(row=0, column=1)
        tk.Label(frame, text="password").grid(row=1, column=0)
        tk.Entry(frame, textvariable=password_var).grid(row=1, column=1)
        tk.Button(frame, text="Save", command=save).grid(row=3, column=1)
        tk.Button(frame, text="Back", command=self.render_users_list).grid(row=3, column=0)
    
    def render_sales_items_list(self):
        frame = self.get_container_frame()
        tk.Button(frame, text="Add New", command=self.render_pos).place(relheight=0.15, relwidth=1, relx=0, rely=0)
        purchases = self.dms.fetch('SELECT "id", "product_id", "sale_id", "unit_price", "qty", "total" FROM sale_items')
        columns = ("id", "product_id", "sale_id", "unit_price", "qty", "total")
        table = ttk.Treeview(frame, columns=columns, show="headings")
        [table.heading(i, text=i) for i in columns]
        table.place(relheight=0.85, relwidth=1, relx=0, rely=0.15)
        for item in purchases:
            table.insert("", tk.END, values=[item.get(i) for i in columns])

    def render_sales_list(self):
        frame = self.get_container_frame()
        tk.Button(frame, text="Sales items", command=self.render_sales_items_list).place(relheight=0.15, relwidth=0.5, relx=0, rely=0)
        tk.Button(frame, text="Add New", command=self.render_pos).place(relheight=0.15, relwidth=0.5, relx=0.5, rely=0)
        purchases = self.dms.fetch('SELECT "id", "customer", "cashier", "timestamp", "total" FROM sales')
        columns = ("id", "customer", "cashier", "timestamp", "total")
        table = ttk.Treeview(frame, columns=columns, show="headings")
        [table.heading(i, text=i) for i in columns]
        table.place(relheight=0.85, relwidth=1, relx=0, rely=0.15)
        for item in purchases:
            table.insert("", tk.END, values=[item.get(i) for i in columns])
        
    def render_purchases_list(self):
        frame = self.get_container_frame()
        tk.Button(frame, text="Add New", command=self.render_purchases_form).place(relheight=0.15, relwidth=1, relx=0, rely=0)
        purchases = self.dms.fetch('SELECT "id", "product_id", "unit_price", "qty", "total" FROM purchases')
        columns = ("id", "product_id", "unit_price", "qty", "total")
        table = ttk.Treeview(frame, columns=columns, show="headings")
        [table.heading(i, text=i) for i in columns]
        table.place(relheight=0.85, relwidth=1, relx=0, rely=0.15)
        for item in purchases:
            table.insert("", tk.END, values=[item.get(i) for i in columns])
    
    def render_purchases_form(self, purchase: dict={}):
        frame = self.get_container_frame()
        product_id_var, qty_var, total_var = tk.IntVar(frame, purchase.get("product_id")), tk.IntVar(frame, purchase.get("qty")), tk.DoubleVar(frame, purchase.get("total"))
        def save():
            product_id, qty, total = product_id_var.get(), qty_var.get(), total_var.get()
            unit_price = round(total / qty, 2)
            if purchase.get("id"):
                self.dms.c.execute(f'UPDATE purchases SET (product_id={product_id}, unit_price={unit_price}, qty={qty}, total={total}) WHERE id={purchase.get("id")}')
            else:
                self.dms.c.execute(f'INSERT INTO purchases ("product_id", "unit_price", "qty", "total") VALUES ({product_id}, {unit_price}, {qty}, {total})')
                product = self.dms.fetch_by_id("products", product_id)
                self.dms.c.execute(f'UPDATE products SET qty={product["qty"] + qty} WHERE id={product_id}')
            self.render_purchases_list()
        tk.Label(frame, text="product id").grid(row=0, column=0)
        tk.Entry(frame, textvariable=product_id_var).grid(row=0, column=1)
        tk.Label(frame, text="qty").grid(row=2, column=0)
        tk.Entry(frame, textvariable=qty_var).grid(row=2, column=1)
        tk.Label(frame, text="total").grid(row=3, column=0)
        tk.Entry(frame, textvariable=total_var).grid(row=3, column=1)
        tk.Button(frame, text="Save", command=save).grid(row=4, column=1)
        tk.Button(frame, text="Back", command=self.render_purchases_list).grid(row=4, column=0)

    def render_pos(self):
        frame = self.get_container_frame()
        invoice_items = []
        total = 0
        timestamp = datetime.datetime.now()
        tk.Label(frame, text="P.E Point of Sale", **bgpfgl_style).place(relx=0, rely=0, relwidth=1, relheight=0.1)
        inv_form_frame = tk.Frame(frame, **bgpfgl_style)
        inv_form_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
        customer_var = tk.StringVar(inv_form_frame, )
        tk.Label(inv_form_frame, text="Customer Name", **bgpfgl_style).pack(side=tk.TOP, fill=tk.X, expand=True)
        tk.Entry(inv_form_frame, textvariable=customer_var).pack(side=tk.TOP, fill=tk.X, expand=True)
        item_form_frame = tk.Frame(frame, **bgpfgl_style)
        item_form_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.1)
        product_id_var, qty_var= tk.IntVar(item_form_frame, ), tk.IntVar(item_form_frame, 1)
        inv_list_text = tk.Text(frame, )
        inv_list_text.place(relx=0, rely=0.3, relwidth=1, relheight=0.6)
        inv_list_text.config(state=tk.DISABLED)
        def add_item():
            product_id, qty = product_id_var.get(), qty_var.get()
            product = self.dms.fetch_by_id("products", product_id)
            if not (product and qty):
                messagebox.showerror("incorrect_data", f"Product {product_id} or qty {qty} not found!")
                return
            invoice_items.append({
                "name": product['name'],
                "product_id": product['id'],
                "qty": qty,
                "unit_price": product['price'],
                "total": round(product['price'] * qty, 2)
            })
            product_invoice_qty = sum([i['qty'] for i in invoice_items if i['product_id'] == product['id']])
            if product_invoice_qty > product['qty']:
                messagebox.showerror("Insufficient Qty", f"Product {product['name']}: Qty left in stock {product['qty']}")
                invoice_items.pop()
                return
            render_invoice_items()
            product_id_var.set(0)
            qty_var.set(1)
        tk.Label(item_form_frame, text="Product ID").place(relx=0.0, rely=0, relwidth=0.2)
        tk.Entry(item_form_frame, textvariable=product_id_var).place(relx=0.2, rely=0, relwidth=0.2)
        tk.Label(item_form_frame, text="QTY").place(relx=0.4, rely=0, relwidth=0.2)
        tk.Entry(item_form_frame, textvariable=qty_var).place(relx=0.6, rely=0, relwidth=0.2)
        tk.Button(item_form_frame, text="Add Item", command=add_item).place(relx=0.8, rely=0, relwidth=0.2)
        def render_invoice_items():
            inv_list_text.config(state=tk.NORMAL)
            inv_list_text.delete(1.0, tk.END)
            header = f"{'#':9}| {'Product':30} | {'Unit Price':10} | {'Quantity':10} | {'Total':10}\n"
            body = "\n".join([
                f"{str(index):9}| {i['name']:30} | {str(i['unit_price']):10} | {str(i['qty']):10} | {str(i['total']):10}" 
                for (index, i) in enumerate(invoice_items)
            ])
            total = round(sum([i['total'] for i in  invoice_items], 0.00), 2)
            footer = f"\n\n{'Items':69}{str(len(invoice_items))}\n{'Total':69}{str(total)}"
            inv_list_text.insert(tk.END, header+body+footer)
            inv_list_text.config(state=tk.DISABLED)
        render_invoice_items()

        def save():
            customer = customer_var.get()
            total = round(sum([i['total'] for i in  invoice_items], 0.00), 2)
            if not (total and customer):
                messagebox.showerror("Invalid Invoice", f"Customer {customer} or total {total} not found!")
                return
            sales_id = self.dms.c.execute(f'INSERT INTO sales ("timestamp", "customer", "total", "cashier") VALUES ("{timestamp}", "{customer}", {total}, "{self.user["username"]}")').lastrowid
            self.dms.c.executemany('INSERT INTO sale_items ("unit_price", "qty", "total", "product_id", "sale_id") VALUES (?, ?, ?, ?, ?)', [
                (i["unit_price"], i["qty"], i["total"], i["product_id"], sales_id) for i in invoice_items
            ])
            for i in invoice_items:
                self.dms.c.execute(f'UPDATE products SET qty=qty-{i["qty"]} WHERE id={i["product_id"]}')
            messagebox.showinfo("Done", f"Invoice for {customer} was created successfully!")
            self.render_pos()

        tk.Button(frame, text="Submit Invoice", command=save).place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

    def run(self):
        self.root.mainloop()

    def logout(self):
        self.exit()

    def exit(self):
        self.dms.cnxn.commit()
        self.root.destroy()
        sys.exit(0)


if __name__ == "__main__":
    app = Application()
    app.run()
