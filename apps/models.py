from django.db import models
from django.contrib.gis.db import models as gis_models


class TimeBaseModel(models.Model):
    """時間基礎模型"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GeoJsonTypeChoice(models.TextChoices):
    # 參考: https://zh.wikipedia.org/wiki/GeoJSON

    # 基本幾何類型
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"
    # 複合幾何類型
    MULTIPOINT = "MultiPoint"
    MULTILINESTRING = "MultiLineString"
    MULTIPOLYGON = "MultiPolygon"


class Geometry(TimeBaseModel):
    """地圖幾何資料"""

    type = models.CharField(choices=GeoJsonTypeChoice.choices, max_length=50)
    title = models.CharField(max_length=100)
    geom = gis_models.GeometryField(help_text="地圖幾何資料")

    def __str__(self):
        return self.title
