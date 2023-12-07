from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from apps.models import Geometry
from apps.serializers import GeometrySerializer
from apps.utility import swagger_success_response


class CustomResponse(Response):
    def __init__(
        self, status_code: int = 200, data: dict | None = None, status: bool = True, message=None, *args, **kwargs
    ):
        response_data = {
            "status": str(status).lower() if isinstance(status, bool) else status,
            "message": message if message else "success",
        }

        if data is not None:
            response_data = response_data | data

        super().__init__(data=response_data, status=status_code, *args, **kwargs)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="建立地圖資訊",
        request_body=GeometrySerializer.Create,
        responses={
            200: swagger_success_response({"status": "true", "message": "success", "id": 1}),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="取得地圖詳細資訊",
        responses={
            200: swagger_success_response(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {"type": "Point", "coordinates": [120.23621657974621, 22.976396975365063]},
                            "properties": {"title": "鉅網資訊股份有限公司"},
                        }
                    ],
                }
            ),
        },
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_summary="更新地名",
        request_body=GeometrySerializer.Update,
        responses={
            200: swagger_success_response(),
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="刪除地標",
        responses={
            200: swagger_success_response(),
        },
    ),
)
class GeoMetryViewSet(ViewSet):
    def create(self, request):
        serializer = GeometrySerializer.Create(data=request.data)
        if serializer.is_valid():
            new_geom = serializer.save()
            return CustomResponse(data={"id": new_geom.id})
        return CustomResponse(status=False, message=serializer.errors, status_code=400)

    def retrieve(self, request, pk=None):
        try:
            geometry = Geometry.objects.filter(pk=pk)
        except:
            return CustomResponse(status=False, message="Bad Request", status_code=400)
        if not geometry.exists():
            return CustomResponse(status=False, message="Not Found", status_code=404)
        else:
            serializer = GeometrySerializer.Retrieve(geometry, many=True)
            return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            geometry = Geometry.objects.get(pk=pk)
        except Geometry.DoesNotExist:
            return CustomResponse(status=False, message="Not Found", status_code=404)
        else:
            serializer = GeometrySerializer.Update(instance=geometry, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse()
            return CustomResponse(status=False, message=serializer.errors, status_code=400)

    def destroy(self, request, pk=None):
        try:
            geometry = Geometry.objects.get(pk=pk)
        except Geometry.DoesNotExist:
            return CustomResponse(status=False, message="Not Found", status_code=404)
        else:
            geometry.delete()
            return CustomResponse()
