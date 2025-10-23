# API Endpoints - Agencia de Turismo

## Paquetes Turísticos

### Categorías
- `GET /api/v1/packages/categories/` - Listar todas las categorías
- `GET /api/v1/packages/categories/{id}/` - Obtener categoría específica
- `GET /api/v1/packages/categories/{id}/packages/` - Obtener paquetes de una categoría
- `POST /api/v1/packages/categories/` - Crear nueva categoría
- `PUT /api/v1/packages/categories/{id}/` - Actualizar categoría
- `DELETE /api/v1/packages/categories/{id}/` - Eliminar categoría

### Paquetes
- `GET /api/v1/packages/packages/` - Listar todos los paquetes
- `GET /api/v1/packages/packages/{id}/` - Obtener paquete específico (con itinerarios)
- `GET /api/v1/packages/packages/featured/` - Obtener paquetes destacados
- `GET /api/v1/packages/packages/by_category/?category_id={id}` - Paquetes por categoría
- `GET /api/v1/packages/packages/by_destination/?destination_id={id}` - Paquetes por destino
- `GET /api/v1/packages/packages/{id}/itineraries/` - Itinerarios de un paquete
- `POST /api/v1/packages/packages/` - Crear nuevo paquete
- `PUT /api/v1/packages/packages/{id}/` - Actualizar paquete
- `DELETE /api/v1/packages/packages/{id}/` - Eliminar paquete

## Filtros Disponibles

### Para Paquetes:
- `?category={id}` - Filtrar por categoría
- `?destination={id}` - Filtrar por destino
- `?is_featured=true` - Solo paquetes destacados
- `?min_price={precio}` - Precio mínimo
- `?max_price={precio}` - Precio máximo
- `?min_duration={días}` - Duración mínima
- `?max_duration={días}` - Duración máxima
- `?destination={nombre}` - Buscar por nombre de destino
- `?search={texto}` - Búsqueda general
- `?ordering={campo}` - Ordenar por campo

### Para Categorías:
- `?search={texto}` - Búsqueda por nombre o descripción
- `?ordering={campo}` - Ordenar por campo

## Ejemplos de Uso

### Obtener paquetes destacados:
```
GET /api/v1/packages/packages/featured/
```

### Buscar paquetes por precio:
```
GET /api/v1/packages/packages/?min_price=1000&max_price=2000
```

### Buscar paquetes por destino:
```
GET /api/v1/packages/packages/?destination=París
```

### Obtener paquetes de una categoría específica:
```
GET /api/v1/packages/packages/by_category/?category_id=1
```

### Obtener itinerarios de un paquete:
```
GET /api/v1/packages/packages/1/itineraries/
```

## Respuestas de Ejemplo

### Lista de Paquetes (PackageListSerializer):
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "París Romántico - 3 Días",
      "slug": "paris-romantico-3-dias",
      "category_name": "Romántico",
      "destination_name": "París",
      "destination_city": "París",
      "destination_country": "Francia",
      "short_description": "Escapada romántica de 3 días en París",
      "duration_days": 3,
      "duration_nights": 2,
      "price_adult": "1200.00",
      "price_child": "800.00",
      "max_people": 2,
      "min_people": 2,
      "includes": ["hotel", "meals", "transport", "guide"],
      "image_url": null,
      "is_featured": true,
      "available_from": "2024-01-01",
      "available_until": "2024-12-31",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Detalle de Paquete (PackageDetailSerializer):
```json
{
  "id": 1,
  "name": "París Romántico - 3 Días",
  "slug": "paris-romantico-3-dias",
  "category": {
    "id": 4,
    "name": "Romántico",
    "description": "Escapadas románticas para parejas",
    "icon": "romantic",
    "packages_count": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "destination": {
    "id": 1,
    "name": "París",
    "city": "París",
    "country": "Francia",
    "description": "La ciudad de la luz, famosa por su arte, moda y gastronomía",
    "short_description": "La ciudad más romántica del mundo"
  },
  "description": "Una escapada romántica perfecta en la ciudad de la luz...",
  "short_description": "Escapada romántica de 3 días en París",
  "duration_days": 3,
  "duration_nights": 2,
  "price_adult": "1200.00",
  "price_child": "800.00",
  "max_people": 2,
  "min_people": 2,
  "includes": ["hotel", "meals", "transport", "guide"],
  "image_url": null,
  "is_featured": true,
  "available_from": "2024-01-01",
  "available_until": "2024-12-31",
  "itineraries": [
    {
      "id": 1,
      "day_number": 1,
      "title": "Llegada y Torre Eiffel",
      "description": "Llegada a París, check-in en hotel y visita a la Torre Eiffel al atardecer.",
      "activities": ["Check-in hotel", "Visita Torre Eiffel", "Cena romántica en restaurante"],
      "meals_included": ["desayuno", "cena"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```
