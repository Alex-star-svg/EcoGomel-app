from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import DropoffPoint, WasteItem


def waste_list(request):
    items = WasteItem.objects.all()

    data = []

    for item in items:
        data.append({
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "code": item.code,
            "recyclable": item.recyclable,
            "hazard_class": item.hazard_class,
            "preparation_steps": item.preparation_steps,
            "what_happens_next": item.what_happens_next,
            "keywords": item.keywords,
            "map_filter_category": item.map_filter_category
        })

    return JsonResponse(data, safe=False)


@require_GET
def points_list(request):
    """Список пунктов приёма для карты Leaflet.

    Координаты отдаются числами (float), а не строками, чтобы их можно
    было сразу передать в L.marker([latitude, longitude]).
    accepted_types — уникальные категории принимаемых отходов
    (map_filter_category, а если она пустая — category); они совпадают
    со значениями фильтров на странице карты.

    Необязательный параметр ?waste_id=<id отхода> оставляет только пункты,
    которые принимают этот отход. Нечисловое значение -> 400.
    """
    points = DropoffPoint.objects.prefetch_related("accepted_types").order_by("id")

    waste_id = request.GET.get("waste_id")
    if waste_id is not None:
        try:
            waste_id = int(waste_id)
        except ValueError:
            return JsonResponse(
                {"error": "waste_id должен быть целым числом"},
                status=400,
            )
        points = points.filter(accepted_types__id=waste_id)

    data = []

    for point in points:
        accepted_types = sorted({
            waste.map_filter_category or waste.category
            for waste in point.accepted_types.all()
        })

        data.append({
            "id": point.id,
            "name": point.name,
            "address": point.address,
            "latitude": float(point.latitude),
            "longitude": float(point.longitude),
            "work_hours": point.working_hours,
            "description": point.description,
            "accepted_types": accepted_types,
        })

    return JsonResponse(data, safe=False)