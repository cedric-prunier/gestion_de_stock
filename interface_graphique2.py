import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gestion_de_stock import Gestion_stock
import matplotlib.pyplot as plt


class Application(tk.Tk):
    def __init__(self, bd_boutique):
        super().__init__()
        self.bd_boutique = bd_boutique
        self.title("Gestion de stock")
        self.geometry("800x600")
        self.products_visible = False
        self.create_widgets()
        self.refresh_product_list()

    def show_histogram(self):
        # Récupérez les données pour l'histogramme
        categories = self.bd_boutique.list_categories()
        quantities = [
            self.bd_boutique.get_total_quantity_by_category(cat) for cat in categories
        ]

        # Créez l'histogramme en barres
        plt.bar(categories, quantities)

        # Ajoutez des titres et des étiquettes d'axe
        plt.title("Quantité de produits par catégorie")
        plt.xlabel("Catégories")
        plt.ylabel("Quantité")

        # Affichez l'histogramme
        plt.show()

    def create_widgets(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Fichier", menu=self.file_menu)
        self.file_menu.add_command(
            label="Exporter au format CSV", command=self.export_csv
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.quit)

        self.product_actions_var = tk.StringVar(self)
        self.product_actions_var.set("Actions sur les produits")
        self.product_actions_menu = tk.OptionMenu(
            self,
            self.product_actions_var,
            "Ajouter un produit",
            "Supprimer un produit",
            "Modifier un produit",
            command=self.execute_product_action,
        )
        self.product_actions_menu.pack(pady=10)
        self.product_list = ttk.Treeview(self)
        self.product_list["columns"] = (
            "ID",
            "Nom",
            "Description",
            "Prix",
            "Quantité",
            "ID_catégorie",
        )
        self.product_list.column("#0", width=0, stretch=tk.NO)
        self.product_list.heading("#0", text="", anchor=tk.W)

        for col in self.product_list["columns"]:
            self.product_list.column(col, anchor=tk.W, width=100)
            self.product_list.heading(col, text=col, anchor=tk.W)

        self.product_list.pack(fill=tk.BOTH, expand=True)

        self.category_var = tk.StringVar(self)
        self.category_var.set("Toutes les catégories")
        self.categories = ["Toutes les catégories"] + self.bd_boutique.list_categories()
        self.category_menu = tk.OptionMenu(
            self,
            self.category_var,
            *self.categories,
            command=self.refresh_on_category_change
        )
        self.category_menu.pack(pady=10)

        # Ajoutez le bouton "Exporter en CSV"
        self.export_csv_button = tk.Button(
            self, text="Exporter en CSV", command=self.export_csv
        )
        self.export_csv_button.pack(pady=10)

        self.histogram_button = tk.Button(
            self, text="Afficher l'histogramme", command=self.show_histogram
        )

        self.histogram_button.pack(pady=10)

    def execute_product_action(self, selected_action):
        if selected_action == "Ajouter un produit":
            self.add_product()
        elif selected_action == "Supprimer un produit":
            self.delete_selected_product()
        elif selected_action == "Modifier un produit":
            self.edit_selected_product()

    def refresh_on_category_change(self, event):
        self.refresh_product_list()

    def toggle_product_list(self):
        if self.products_visible:
            self.hide_product_list()
        else:
            self.refresh_product_list()
        self.products_visible = not self.products_visible

    def refresh_product_list(self):
        selected_category = self.category_var.get()
        self.product_list.delete(*self.product_list.get_children())

        if selected_category == "Toutes les catégories":
            products = self.bd_boutique.list_produit()
        else:
            products = self.bd_boutique.list_produit_by_categorie(selected_category)

        for product in products:
            self.product_list.insert(
                "",
                tk.END,
                values=(
                    product[0],
                    product[1],
                    product[2],
                    product[3],
                    product[4],
                    product[5],
                ),
            )

    def export_csv(self):
        selected_category = self.category_var.get()
        if selected_category == "Toutes les catégories":
            products = self.bd_boutique.list_produit()
        else:
            products = self.bd_boutique.list_produit_by_categorie(selected_category)
        self.bd_boutique.export_csv(products)
        messagebox.showinfo("Succès", "Les produits ont été exportés avec succès.")

    def add_product(self):
        # Créer un formulaire pour ajouter un produit
        add_product_window = tk.Toplevel(self)
        add_product_window.title("Ajouter produit")

        # Créer des champs pour saisir les informations du produit
        tk.Label(add_product_window, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        nom_entry = tk.Entry(add_product_window)
        nom_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_product_window, text="Description:").grid(
            row=1, column=0, padx=5, pady=5
        )
        description_entry = tk.Entry(add_product_window)
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_product_window, text="Prix:").grid(row=2, column=0, padx=5, pady=5)
        prix_entry = tk.Entry(add_product_window)
        prix_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_product_window, text="Quantité:").grid(
            row=3, column=0, padx=5, pady=5
        )
        quantite_entry = tk.Entry(add_product_window)
        quantite_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_product_window, text="ID de catégorie:").grid(
            row=4, column=0, padx=5, pady=5
        )
        id_categorie_entry = tk.Entry(add_product_window)
        id_categorie_entry.grid(row=4, column=1, padx=5, pady=5)

        add_product_window.transient(self)
        add_product_window.grab_set()

        add_button = tk.Button(
            add_product_window,
            text="Ajouter",
            command=lambda: self.add_and_refresh(
                nom_entry.get(),
                description_entry.get(),
                float(prix_entry.get()),
                int(quantite_entry.get()),
                int(id_categorie_entry.get()),
            ),
        )
        add_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def add_and_refresh(self, nom, description, prix, quantité, id_categorie):
        self.bd_boutique.ajouter_produit(nom, description, prix, quantité, id_categorie)
        self.refresh_product_list()
        messagebox.showinfo("Succès", "Le produit a été ajouté avec succès.")

    def delete_selected_product(self):
        selected_item = self.product_list.focus()
        if selected_item:
            values = self.product_list.item(selected_item, "values")
            nom_produit = values[1]
            self.bd_boutique.supprimer_produit(nom_produit)
            self.refresh_product_list()

    def edit_selected_product(self):
        selected_item = self.product_list.focus()
        if selected_item:
            values = self.product_list.item(selected_item, "values")
            self.open_edit_product_window(*values)

    def open_edit_product_window(
        self, id, nom, description, prix, quantite, id_categorie
    ):
        edit_product_window = tk.Toplevel(self)
        edit_product_window.title("Modifier produit")

        # Créer des champs pour saisir les informations du produit
        tk.Label(edit_product_window, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        nom_entry = tk.Entry(edit_product_window)
        nom_entry.insert(tk.END, nom)
        nom_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edit_product_window, text="Description:").grid(
            row=1, column=0, padx=5, pady=5
        )
        description_entry = tk.Entry(edit_product_window)
        description_entry.insert(tk.END, description)
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(edit_product_window, text="Prix:").grid(
            row=2, column=0, padx=5, pady=5
        )
        prix_entry = tk.Entry(edit_product_window)
        prix_entry.insert(tk.END, prix)
        prix_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(edit_product_window, text="Quantité:").grid(
            row=3, column=0, padx=5, pady=5
        )
        quantite_entry = tk.Entry(edit_product_window)
        quantite_entry.insert(tk.END, quantite)
        quantite_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(edit_product_window, text="ID de catégorie:").grid(
            row=4, column=0, padx=5, pady=5
        )
        id_categorie_entry = tk.Entry(edit_product_window)
        id_categorie_entry.insert(tk.END, id_categorie)
        id_categorie_entry.grid(row=4, column=1, padx=5, pady=5)

        edit_product_window.transient(self)
        edit_product_window.grab_set()

        # Créez un bouton pour enregistrer les modifications
        save_button = tk.Button(
            edit_product_window,
            text="Enregistrer",
            command=lambda: self.save_and_refresh(
                id,
                nom_entry.get(),
                description_entry.get(),
                float(prix_entry.get()),
                int(quantite_entry.get()),
                int(id_categorie_entry.get()),
            ),
        )
        save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def save_and_refresh(self, id, nom, description, prix, quantite, id_categorie):
        self.bd_boutique.update_produit(
            id, nom, description, prix, quantite, id_categorie
        )
        self.refresh_product_list()
        messagebox.showinfo("Succès", "Le produit a été modifié avec succès.")


if __name__ == "__main__":
    bd_boutique = Gestion_stock()
    app = Application(bd_boutique)
    app.mainloop()
