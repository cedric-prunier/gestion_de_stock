""""

Commandes terminal
mysql -u root -p 

CREATE DATABASE boutique;

USE boutique;

CREATE TABLE categorie (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255) NOT NULL
);

CREATE TABLE produit (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255) NOT NULL,
  description TEXT,
  prix FLOAT(10,2) NOT NULL;
  quantite INT NOT NULL,
  id_categorie INT,
  FOREIGN KEY (id_categorie) REFERENCES categorie(id)
);


INSERT INTO categorie (nom) VALUES 
('Électronique'),
('Vêtements'),
('Alimentation'),
('Livres'),
('Jouets');

INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES 
('Téléphone', 'Téléphone portable 5G', 800, 100, 1),
('Ordinateur portable', 'Ordinateur portable 15 pouces', 1200, 50, 1),
('T-shirt', 'T-shirt en coton', 20, 200, 2),
('Pantalon', 'Pantalon en jean', 50, 150, 2);

INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES 
('Pâtes', 'Pâtes alimentaires 500g', 2, 300, 3),
('Riz', 'Riz basmati 1kg', 4, 200, 3);

INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES 
('Roman policier', 'Un roman policier passionnant', 10, 100, 4),
('Livre de cuisine', 'Recettes pour cuisiner à la maison', 15, 50, 4);

INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES 
('Puzzle', 'Puzzle 1000 pièces', 20, 30, 5),
('Peluche', 'Peluche en forme d\'ours', 25, 40, 5);

Modifier type de données requises:
ALTER TABLE produit
MODIFY prix FLOAT(10,2) NOT NULL;


"""

import mysql.connector
import csv


class Gestion_stock:
    def __init__(self):
        self.bd_boutique = mysql.connector.connect(
            host="localhost", user="root", password="Egypte3813", database="boutique"
        )
        self.cursor = self.bd_boutique.cursor()

    def get_total_quantity_by_category(self, category):
        self.cursor.execute(
            "SELECT SUM(quantite) FROM produit WHERE id_categorie = (SELECT id FROM categorie WHERE nom = %s)",
            (category,),
        )

        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def list_categories(self):
        query = "SELECT nom FROM categorie"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def get_produit(self, nom):
        query = "SELECT * FROM produit WHERE nom = %s"
        values = (nom,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result

    def list_produit(self):
        query = "SELECT * FROM produit"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_produit_by_categorie(self, id_categorie):
        query = "SELECT * FROM produit WHERE id_categorie = %s"
        values = (id_categorie,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def list_produit_by_categorie(self, nom_categorie):
        query = "SELECT * FROM produit WHERE id_categorie = (SELECT id FROM categorie WHERE nom = %s)"
        values = (nom_categorie,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def ajouter_produit(self, nom, description, prix, quantite, id_categorie):
        query = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
        values = (nom, description, prix, quantite, id_categorie)
        self.cursor.execute(query, values)
        self.bd_boutique.commit()

    def update_produit(
        self,
        nom,
        new_nom=None,
        new_description=None,
        new_prix=None,
        new_quantite=None,
        new_id_categorie=None,
    ):
        query = "SELECT * FROM produit WHERE nom = %s"
        self.cursor.execute(query, (nom,))
        produit = self.cursor.fetchone()

        if produit:
            if new_nom is None:
                new_nom = nom
            if new_description is None:
                new_description = produit[2]
            if new_prix is None:
                new_prix = produit[3]
            if new_quantite is None:
                new_quantite = produit[4]
            if new_id_categorie is None:
                new_id_categorie = produit[5]

            query = "UPDATE produit SET nom = %s, description = %s, prix = %s, quantite = %s, id_categorie = %s WHERE nom = %s"
            values = (
                new_nom,
                new_description,
                new_prix,
                new_quantite,
                new_id_categorie,
                nom,
            )
            self.cursor.execute(query, values)
            self.bd_boutique.commit()
            return True
        else:
            return False

    def supprimer_produit(self, nom):
        query = "DELETE FROM produit WHERE nom = %s"
        values = (nom,)
        self.cursor.execute(query, values)
        self.bd_boutique.commit()

    export_counter = 0

    def export_csv(self, produits, filename="produits.csv"):
        Gestion_stock.export_counter += 1
        filename = f"produits_{Gestion_stock.export_counter}.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["ID", "Nom", "Description", "Prix", "Quantité", "ID_catégorie"]
            )
            for produit in produits:
                writer.writerow(produit)


def modifier_produit(bd_boutique):
    nom = input("Saisir le nom du produit à modifier: ")
    new_nom_input = input("Saisir le nouveau nom (laisser vide pour ne pas changer): ")
    new_nom = new_nom_input if new_nom_input else None

    new_description_input = input(
        "Saisir la nouvelle description du produit (laisser vide pour ne pas changer): "
    )
    new_description = new_description_input if new_description_input else None

    new_prix_input = input(
        "Saisir le nouveau prix (laisser vide pour ne pas changer): "
    )
    new_prix = float(new_prix_input) if new_prix_input else None

    new_quantite_input = input(
        "Saisir la nouvelle quantité (laisser vide pour ne pas changer): "
    )
    new_quantite = int(new_quantite_input) if new_quantite_input else None

    new_id_categorie_input = input(
        "Saisir le nouvel ID de catégorie (laisser vide pour ne pas changer): "
    )
    new_id_categorie = int(new_id_categorie_input) if new_id_categorie_input else None

    if new_nom or new_description or new_prix or new_quantite or new_id_categorie:
        updated = bd_boutique.update_produit(
            nom,
            new_nom=new_nom,
            new_description=new_description,
            new_prix=new_prix,
            new_quantite=new_quantite,
            new_id_categorie=new_id_categorie,
        )
        if updated:
            print(f"Le produit '{nom}' a été mis à jour.")
        else:
            print(f"Aucun produit trouvé avec le nom '{nom}'.")
    else:
        print("Aucune modification fournie.")


def ajouter_produit(bd_boutique):
    nom = input("Entrez le nom du produit : ")
    description = input("Entrez la description du produit : ")
    prix = float(input("Entrez le prix du produit : "))
    quantite = int(input("Entrez la quantité de stock : "))
    id_categorie = int(input("Entrez l'id de catégorie : "))
    bd_boutique.ajouter_produit(
        nom,
        description,
        prix,
        quantite,
        id_categorie,
    )

    print("Le produit a été ajoutée avec succès.")


def supprimer_produit(bd_boutique):
    nom = input("Entrez le nom du produit : ")

    bd_boutique.supprimer_produit(nom)

    print("Le produit a été supprimé avec succès.")


def show_menu():
    print("Menu:")
    print("1. Afficher la liste des produits")
    print("2. Ajouter un produit")
    print("3. Supprimer un produit")
    print("4. Modifier un produit")
    print("5. Exporter les produits au format CSV")
    print("6. Quitter")


def handle_menu_choice(bd_boutique, choice):
    if choice == 1:
        produits = bd_boutique.list_produit()
        for produit in produits:
            print(produit)
    elif choice == 2:
        ajouter_produit(bd_boutique)
    elif choice == 3:
        supprimer_produit(bd_boutique)
    elif choice == 4:
        modifier_produit(bd_boutique)
    elif choice == 5:
        id_categorie_input = input(
            "Entrez l'ID de catégorie à filtrer (laisser vide pour exporter tous les produits) : "
        )
        if id_categorie_input:
            id_categorie = int(id_categorie_input)
            produits = bd_boutique.get_produit_by_categorie(id_categorie)
        else:
            produits = bd_boutique.list_produit()
        bd_boutique.export_csv(produits)
        print("Les produits ont été exportés avec succès.")
    elif choice == 6:
        quit()


bd_boutique = Gestion_stock()

"""while True:
    show_menu()
    choice = int(input("Veuillez entrer le numéro de votre choix : "))
    handle_menu_choice(bd_boutique, choice)"""
