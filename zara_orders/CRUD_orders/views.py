import re
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from pymongo import ReturnDocument
from rest_framework.views import APIView 
from .utils import get_db_handle
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class ReadColorsView(APIView):
    def get(self, request):
        logger.info("Connecting to database")
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        try:
            # Extrae todos los valores únicos de "color" en MongoDB
            raw_colors = orders_collection.distinct("color")
            logger.info(f"Fetched colors: {raw_colors}")

            # Filtra solo el nombre del color, eliminando duplicados y valores no válidos
            unique_colors = set()
            for color in raw_colors:
                # Toma solo la parte antes de "|", y elimina espacios adicionales
                base_color = color.split('|')[0].strip()
                
                # Filtra valores que parecen nombres de colores, descartando números
                if re.match(r'^[A-Za-z\s]+$', base_color):  # Solo letras y espacios
                    unique_colors.add(base_color)

            colors_list = list(unique_colors)
            logger.info(f"Processed colors: {colors_list}")
        except Exception as e:
            logger.error(f"Error fetching colors: {e}")
            return JsonResponse({"error": "Error fetching colors"}, status=500)
        finally:
            client.close()

        return JsonResponse(colors_list, safe=False)


class ReadBrandsView(APIView):
    @swagger_auto_schema(
        operation_description="Leer todas las marcas disponibles",
        responses={200: "Successful Operation"}
    )
    def get(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Extrae marcas únicas de la colección de órdenes
        brands = orders_collection.distinct("brand")
        client.close()

        return JsonResponse(brands, safe=False)


class ReadAvailabilityView(APIView):
    @swagger_auto_schema(
        operation_description="Leer todas las disponibilidades disponibles",
        responses={200: "Successful Operation"}
    )
    def get(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Extrae disponibilidades únicas de la colección de órdenes
        availability = orders_collection.distinct("availability")
        client.close()

        return JsonResponse(availability, safe=False)


class ReadConditionsView(APIView):
    @swagger_auto_schema(
        operation_description="Leer todas las condiciones disponibles",
        responses={200: "Successful Operation"}
    )
    def get(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Extrae condiciones únicas de la colección de órdenes
        conditions = orders_collection.distinct("condition")
        client.close()

        return JsonResponse(conditions, safe=False)


class ReadAttributesView(APIView):
    @swagger_auto_schema(
        operation_description="Leer todos los atributos de una orden",
        responses={200: "Successful Operation"}
    )
    def get(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Lee un documento para obtener la estructura de los atributos
        attribute_sample = orders_collection.find_one()
        client.close()

        if attribute_sample:
            attributes = list(attribute_sample.keys())
            return JsonResponse(attributes, safe=False)
        else:
            return JsonResponse([], safe=False)


class ReadDocumentsView(APIView):
    @swagger_auto_schema(
        operation_description="Leer los primeros 10 documentos",
        responses={200: "Successful Operation"}
    )
    def get(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        documents = list(orders_collection.find({}).limit(10))
        client.close()

        for document in documents:
            document['_id'] = str(document['_id'])

        return JsonResponse(documents, safe=False)


class ReadDocumentsByFilterView(APIView):
    @swagger_auto_schema(
        operation_description="Leer documentos por filtro",
        responses={200: "Successful Operation"},
        manual_parameters=[
            openapi.Parameter('color', openapi.IN_QUERY, description="Color del producto", type=openapi.TYPE_STRING),
            openapi.Parameter('brand', openapi.IN_QUERY, description="Marca del producto", type=openapi.TYPE_STRING),
            openapi.Parameter('availability', openapi.IN_QUERY, description="Disponibilidad del producto", type=openapi.TYPE_STRING),
            openapi.Parameter('price', openapi.IN_QUERY, description="Precio mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('condition', openapi.IN_QUERY, description="Condición", type=openapi.TYPE_NUMBER),
            # Añade otros parámetros según los campos que quieras filtrar
        ]
    )
    def get(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Construye el diccionario de filtros en base a los parámetros recibidos
        filter_conditions = {}

        # Ejemplo de filtro por color
        color = request.query_params.get('color')
        if color:
            filter_conditions['color'] = color

        # Filtro por marca
        brand = request.query_params.get('brand')
        if brand:
            filter_conditions['brand'] = brand.upper()

        # Filtro por disponibilidad
        availability = request.query_params.get('availability')
        if availability:
            filter_conditions['availability'] = availability
        
        condition = request.query_params.get('condition')
        if condition:
            filter_conditions['condition'] = condition
            
        min_price = request.query_params.get('price')
        if min_price:
            filter_conditions['price'] = {"$lte": float(min_price)}
        

        # Obtén documentos según las condiciones de filtro dinámicas
        documents = list(orders_collection.find(filter_conditions))
        client.close()

        for document in documents:
            document['_id'] = str(document['_id'])

        return JsonResponse(documents, safe=False)

class DeleteDocumentView(APIView):
    @swagger_auto_schema(
        operation_description="Eliminar un documento por ID",
        responses={200: "Document deleted successfully", 404: "Document not found"},
        manual_parameters=[ 
            openapi.Parameter('document_id', openapi.IN_PATH, description="ID del documento", type=openapi.TYPE_STRING)
        ]
    )
    def delete(self, request, document_id):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Eliminar el documento utilizando el campo 'id' personalizado
        result = orders_collection.delete_one({"id": int(document_id)})  

        client.close()

        if result.deleted_count > 0:
            return JsonResponse({'status': 'Document deleted successfully'})
        else:
            return JsonResponse({'error': 'Document not found'}, status=404)

class TestDatabaseConnectionView(APIView):
    @swagger_auto_schema(
        operation_description="Probar la conexión a la base de datos",
        responses={200: "Connection successful", 500: "Connection failed"}
    )
    def get(self, request):
        try:
            db_handle, client = get_db_handle()
            orders_collection = db_handle['orders']

            document_count = orders_collection.count_documents({})
            client.close()

            return JsonResponse({
                "status": "success",
                "message": "Conexión a MongoDB exitosa.",
                "document_count": document_count
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
            
            
class UpdateDocumentView(APIView):
    @swagger_auto_schema(
        operation_description="Actualizar un documento por ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING, description="URL del producto"),
                'language': openapi.Schema(type=openapi.TYPE_STRING, description="Idioma"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del producto"),
                'sku': openapi.Schema(type=openapi.TYPE_STRING, description="SKU del producto"),
                'mpn': openapi.Schema(type=openapi.TYPE_STRING, description="Número de parte del fabricante"),
                'brand': openapi.Schema(type=openapi.TYPE_STRING, description="Marca"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="Descripción"),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description="Precio"),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description="Moneda"),
                'availability': openapi.Schema(type=openapi.TYPE_STRING, description="Disponibilidad"),
                'condition': openapi.Schema(type=openapi.TYPE_STRING, description="Condición"),
                'images': openapi.Schema(type=openapi.TYPE_STRING, description="URLs de las imágenes"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="Color"),
                'size_list': openapi.Schema(type=openapi.TYPE_STRING, description="Tamaño disponible"),
                'scraped_at': openapi.Schema(type=openapi.TYPE_STRING, description="Fecha y hora de scraping"),
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="ID del documento")
            },
            description="Campos a actualizar en el documento"
        ),
        responses={200: "Document updated successfully", 404: "Document not found"},
        manual_parameters=[ 
            openapi.Parameter('document_id', openapi.IN_PATH, description="ID del documento", type=openapi.TYPE_STRING)
        ]
    )
    def put(self, request, document_id):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Recoge el JSON con los datos de actualización desde el frontend
        update_fields = request.data

        # Actualiza el documento usando el campo 'id' en lugar de '_id'
        result = orders_collection.update_one({"id": int(document_id)}, {"$set": update_fields})  # Usamos 'id' personalizado

        client.close()

        if result.modified_count > 0:
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'error': False}, status=404)

class CreateDocumentView(APIView):
    @swagger_auto_schema(
        operation_description="Crear un documento",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING, description="URL del producto"),
                'language': openapi.Schema(type=openapi.TYPE_STRING, description="Idioma"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del producto"),
                'sku': openapi.Schema(type=openapi.TYPE_STRING, description="SKU del producto"),
                'mpn': openapi.Schema(type=openapi.TYPE_STRING, description="Número de parte del fabricante"),
                'brand': openapi.Schema(type=openapi.TYPE_STRING, description="Marca"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="Descripción"),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, description="Precio"),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description="Moneda"),
                'availability': openapi.Schema(type=openapi.TYPE_STRING, description="Disponibilidad"),
                'condition': openapi.Schema(type=openapi.TYPE_STRING, description="Condición"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="Color"),
                'size_list': openapi.Schema(type=openapi.TYPE_STRING, description="Tamaño disponible"),
                'scraped_at': openapi.Schema(type=openapi.TYPE_STRING, description="Fecha y hora de scraping"),
            },
            required=['url', 'language', 'name', 'sku', 'mpn', 'brand', 'description', 'price', 'currency',
                      'availability', 'condition', 'images', 'color', 'size_list', 'scraped_at'],
        ),
        responses={200: "true", 500: "False"}
    )
    def post(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']
        counters_collection = db_handle['counters']  # La colección para manejar el contador de IDs

        # Obtén el siguiente ID disponible (para manejar las inserciones en serie)
        counter = counters_collection.find_one_and_update(
            {"_id": "orders_id"},  # Identificador único para la secuencia
            {"$inc": {"sequence_value": 1}},  # Incrementa el valor del contador
            return_document=ReturnDocument.AFTER  # Devuelve el documento actualizado
        )

        if not counter:
            # Si no existe un documento con _id "orders_id", creamos uno
            counters_collection.insert_one({"_id": "orders_id", "sequence_value": 1})
            counter = {"sequence_value": 1}

        # Verifica si request.data es una lista o un solo objeto
        orders = request.data if isinstance(request.data, list) else [request.data]
        inserted_ids = []  # Para almacenar los IDs de las órdenes insertadas

        for order in orders:
            order['id'] = counter['sequence_value']  # Asigna el siguiente ID disponible

            # Inserta la orden en la colección de órdenes
            result = orders_collection.insert_one(order)
            
            if result.inserted_id:
                inserted_ids.append(str(result.inserted_id))  # Convertir ObjectId a string
                counter['sequence_value'] += 1  # Incrementa el ID para la siguiente orden

        # Actualiza el contador en la colección de counters
        counters_collection.update_one(
            {"_id": "orders_id"},
            {"$set": {"sequence_value": counter['sequence_value']}}
        )

        client.close()

        if inserted_ids:
            return JsonResponse({'status': True, 'inserted_ids': inserted_ids})
        else:
            return JsonResponse({'error': False}, status=500)  
        
class ReadDocumentView(APIView):
    @swagger_auto_schema(
        operation_description="Leer un documento por ID",
        responses={200: "Successful Operation", 404: "Document not found"},
        manual_parameters=[ 
            openapi.Parameter('document_id', openapi.IN_PATH, description="ID del documento", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, document_id):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Lee un documento usando el campo 'id' en lugar de ObjectId
        document = orders_collection.find_one({"id": int(document_id)})

        client.close()

        if document:
            # Convierte todos los ObjectId a str
            document = {key: str(value) if isinstance(value, ObjectId) else value for key, value in document.items()}

            return JsonResponse(document, safe=False)
        else:
            return JsonResponse({'error': 'Document not found'}, status=404)