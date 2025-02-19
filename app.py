from tkinter import *
from pymongo import MongoClient
import pymongo

def create_order():
    try:
        uri: str = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        
        database = client["zara"]
        collection = database["orders"]
        
        order = {
            "order_id": 1,
            "price": 7.9
        }
        
        collection.insert_one(order)
        
        client.close()
        
        print("Orden creada")
        
    except pymongo.errors.ConnectionFailure as error:
        print(f"Error de conexión: {error}")
        
def read_orders():
    try:
        uri: str = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        
        database = client["zara"]
        collection = database["orders"]
        
        orders = collection.find()
        order = collection.find_one({ "order_id" : 1 })
        
        for order in orders:
            print(order)
            
        print("La orden es:", order)
        
        client.close()
        
        print("Ordenes leídas")
        
    except pymongo.errors.ConnectionFailure as error:
        print(f"Error de conexión: {error}")
        
def update_order():
    try:
        uri: str = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        
        database = client["zara"]
        collection = database["orders"]
        
        query = {"order_id": 1}
        new_values = {"$set": {"price": "7.9"}}
        
        collection.update_one(query, new_values)
        
        client.close()
        
        print("Orden actualizada")
        
    except pymongo.errors.ConnectionFailure as error:
        print(f"Error de conexión: {error}")
        
def delete_order(id):
    try:
        uri: str = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        
        database = client["zara"]
        collection = database["orders"]
        
        query = {"order_id": id}
        
        collection.delete_one(query)
        
        client.close()
        
        print("Orden eliminada")
        
    except pymongo.errors.ConnectionFailure as error:
        print(f"Error de conexión: {error}")
        
        
def create_order_gui():
    window = Tk()
    window.title("Crear Orden")
    
    label = Label(window, text="Crear Orden")
    label.pack()
    
    button = Button(window, text="Crear Orden", command=create_order)
    button.pack()
    
    window.mainloop()
    
def read_orders_gui():
    window = Tk()
    window.title("Leer Ordenes")
    
    label = Label(window, text="Leer Ordenes")
    label.pack()
    
    button = Button(window, text="Leer Ordenes", command=read_orders)
    button.pack()
    
    window.mainloop()
    
def update_order_gui():
    window = Tk()
    window.title("Actualizar Orden")
    
    label = Label(window, text="Actualizar Orden")
    label.pack()
    
    button = Button(window, text="Actualizar Orden", command=update_order)
    button.pack()
    
    window.mainloop()
    
def delete_order_gui():
    window = Tk()
    window.title("Eliminar Orden")
    
    label = Label(window, text="Eliminar Orden")
    label.pack()
    
    button = Button(window, text="Eliminar Orden", command=lambda: delete_order(1))
    button.pack()
    
    window.mainloop()
    
def main():
    create_order_gui()
    read_orders_gui()
    update_order_gui()
    delete_order_gui()
    
if __name__ == "__main__":
    main()