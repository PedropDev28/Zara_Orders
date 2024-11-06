from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework.views import APIView  # Cambia a APIView
from .utils import get_db_handle
from bson import ObjectId


# GET colors
# GET brands
# GET availability
# GET conditions
# GET attributes (Todos los atributos que ya se hayan insertado)
# GET documents (Primeros 10) (Si nos calentamos lo hacemos con paginación)
# GET documents by (filtro/s) (Sencillos, sin condicionales)

# DELETE documento by id
# UPDATE documento by id
# POST documento/s

#   {
#     "_id": "6723b4b90c80c85647647b94",
#     "url": "https://www.zara.com/us/en/satin-effect-corset-bodysuit-p00219805.html",
#     "language": "en-US",
#     "name": "SATIN EFFECT CORSET BODYSUIT",
#     "sku": "128666521-966-2",
#     "mpn": "128666521-966-2",
#     "brand": "ZARA",
#     "description": "Bodysuit with sweetheart neckline and adjustable spaghetti straps. Bottom snap button closure.",
#     "price": 30,
#     "currency": "USD",
#     "availability": "InStock",
#     "condition": "NewCondition",
#     "images": "https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png~https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png~https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png~https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png~https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png~https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png~https://static.zara.net/stdstatic/1.234.0-b.45/images/transparent-background.png",
#     "color": "Color Pale pink | 0219/805",
#     "size_list": "S/M/L",
#     "scraped_at": "2021-10-13 01:21:25"
#   },

# Leer todos los colores disponibles que hay en todas las ordenes teniendo en cuenta la orden arriba comentada
class ReadColorsView(APIView):
    @swagger_auto_schema(
        operation_description="Leer todos los colores disponibles",
        responses={200: "Successful Operation"}
    )
    def get(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Extrae colores únicos de la colección de órdenes
        colors = orders_collection.distinct("color")
        client.close()

        return JsonResponse(colors, safe=False)


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
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Precio mínimo", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Precio máximo", type=openapi.TYPE_NUMBER),
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

        # Filtro por precio mínimo y máximo
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price and max_price:
            filter_conditions['price'] = {"$gte": float(min_price), "$lte": float(max_price)}
        elif min_price:
            filter_conditions['price'] = {"$gte": float(min_price)}
        elif max_price:
            filter_conditions['price'] = {"$lte": float(max_price)}

        # Obtén documentos según las condiciones de filtro dinámicas
        documents = list(orders_collection.find(filter_conditions).limit(10))
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

        result = orders_collection.delete_one({"_id": ObjectId(document_id)})
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

        # Actualiza el documento con los campos proporcionados
        result = orders_collection.update_one({"_id": ObjectId(document_id)}, {"$set": update_fields})
        client.close()

        if result.modified_count > 0:
            return JsonResponse({'status': 'Document updated successfully'})
        else:
            return JsonResponse({'error': 'Document not found or no changes made'}, status=404)

        
        
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
                'images': openapi.Schema(type=openapi.TYPE_STRING, description="URLs de las imágenes"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="Color"),
                'size_list': openapi.Schema(type=openapi.TYPE_STRING, description="Tamaño disponible"),
                'scraped_at': openapi.Schema(type=openapi.TYPE_STRING, description="Fecha y hora de scraping"),
            },
            required=['url', 'language', 'name', 'sku', 'mpn', 'brand', 'description', 'price', 'currency',
                      'availability', 'condition', 'images', 'color', 'size_list', 'scraped_at']
        ),
        responses={200: "Document created successfully"}
    )
    def post(self, request):
        db_handle, client = get_db_handle()
        orders_collection = db_handle['orders']

        # Recoge el JSON con los atributos desde el frontend
        document = request.data

        # Crea el documento en MongoDB
        result = orders_collection.insert_one(document)
        client.close()

        if result.inserted_id:
            return JsonResponse({'status': 'Document created successfully'})
        else:
            return JsonResponse({'error': 'Document creation failed'}, status=500)

        
        
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

        # Lee un documento por ID
        document = orders_collection.find_one({"_id": ObjectId(document_id)})
        client.close()

        if document:
            document['_id'] = str(document['_id'])
            return JsonResponse(document, safe=False)
        else:
            return JsonResponse({'error': 'Document not found'}, status=404)
