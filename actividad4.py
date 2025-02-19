import pymongo
from pymongo import MongoClient

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")

db = client["nombre_base_datos"]
collection = db["nombre_coleccion"]

# Leer todos los documentos
for doc in collection.find():
    print(doc)
    
# Leer un solo documento
document = collection.find_one({"nombre": "Juan"})


# Actualizar un solo documento
collection.update_one({"nombre": "Juan"}, {"$set": {"edad": 31}})

# Actualizar múltiples documentos
collection.update_many({"edad": {"$gt": 30}}, {"$set": {"activo": True}})

# Eliminar un solo documento
collection.delete_one({"nombre": "Luis"})

# Eliminar múltiples documentos
collection.delete_many({"edad": {"$lt": 25}})


# Create
try:
    uri: str = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    
    database = client["zara"]
    collection = database["orders"]
    
    order = {
        "url": "https://www.zara.com/us/en/classic-fish-knife-p47401307.html",
        "language": "en-US", 
        "order-id": 1,
        "name": "Classic fish knife",
        "sku": "115616554-999-99",
        "mpn": "115616554-999-99",
        "brand": "ZARAHOME",
        "description": "18/10 smooth stainless steel with a shiny finish.",
        "price": "6.9",
        "currency": "USD",
        "availability": "InStock",	
        "condition": "UsedCondition",
        "images": "https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png~https://static.zara.net/stdstatic",
        "color": "Color Colored leather | 7401/307",
        "size_list": "0.2 x 21 x 2.5 cm",
        "scraped_at": "2021-10-13 01:21:51"
    }
    
    collection.insert_one(order)
    
    client.close()
    
    print("Orden creada")
    
except pymongo.errors.ConnectionFailure as error:
    print(f"Error de conexión: {error}")
    
# Read
try:
    uri: str = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    
    database = client["zara"]
    collection = database["orders"]
    
    orders = collection.find()
    order = collection.find_one({ "order-id" : 1 })
    
    # for order in orders:
    #     print(order)
        
    print("La orden es:", order)
    
    client.close()
    
    print("Ordenes leídas")
    
except pymongo.errors.ConnectionFailure as error:
    print(f"Error de conexión: {error}")
    
# Update
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
    
    
# Delete
try:
    uri: str = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    
    database = client["zara"]
    collection = database["orders"]
    
    query = {"order_id": 1}
    
    collection.delete_one(query)
    
    client.close()
    
    print("Orden eliminada")
    
except pymongo.errors.ConnectionFailure as error:
    print(f"Error de conexión: {error}")