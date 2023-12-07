import traceback
from django.db import transaction
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from apps.models import Geometry, GeoJsonTypeChoice
from apps.utility import GeometryProcessor


class GeometrySerializer:
    """地圖幾何資料序列化器"""

    class Create(serializers.ModelSerializer):
        class Meta:
            ref_name = "GeometryCreate"
            model = Geometry
            fields = ("title", "type", "points")

        points = serializers.CharField(write_only=True, help_text="座標點，以;分隔或者以|分隔")

        def validate(self, attrs):
            # 根據type的種類，檢查座標點的格式是否正確
            geom_type = attrs.get("type")
            points = attrs.pop("points")
            geometry_processor = GeometryProcessor(points)
            try:
                match geom_type:
                    case GeoJsonTypeChoice.POINT:
                        attrs["geom"] = geometry_processor.point
                    case GeoJsonTypeChoice.LINESTRING:
                        attrs["geom"] = geometry_processor.line_string
                    case GeoJsonTypeChoice.MULTIPOINT:
                        attrs["geom"] = geometry_processor.multi_point
                    case GeoJsonTypeChoice.POLYGON:
                        attrs["geom"] = geometry_processor.polygon
                    case GeoJsonTypeChoice.MULTILINESTRING:
                        attrs["geom"] = geometry_processor.multi_line_string
                    case GeoJsonTypeChoice.MULTIPOLYGON:
                        attrs["geom"] = geometry_processor.multi_polygon
            except ValueError:
                raise serializers.ValidationError({"points": "Invalid points format."})
            except serializers.ValidationError as e:
                raise e
            except:
                print(f"{attrs=}")
                print(traceback.format_exc())
                raise serializers.ValidationError("Unknown error.")
            return attrs

        @transaction.atomic
        def create(self, validated_data):
            geometry = Geometry.objects.create(**validated_data)
            return geometry

    class Retrieve(GeoFeatureModelSerializer):
        class Meta:
            ref_name = "GeometryRetrieve"
            model = Geometry
            geo_field = "geom"  # GeoJSON 資料欄位
            fields = ("title",)

    class Update(serializers.ModelSerializer):
        class Meta:
            ref_name = "GeometryUpdate"
            model = Geometry
            fields = ("title",)
