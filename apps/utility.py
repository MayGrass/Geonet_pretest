from django.contrib.gis.geos import Point, Polygon, MultiPolygon, LineString, MultiLineString, MultiPoint
from rest_framework import serializers
from drf_yasg import openapi


def swagger_success_response(data=True):
    return openapi.Response(
        description="success",
        examples={"application/json": {"status": "true", "message": "success"} | {} if data is True else data},
    )


class GeometryProcessor:
    """地圖幾何資料處理器"""

    def __init__(self, points: list[list]):
        self.points = points

    def _validate_number(self, coords: list) -> list:
        """檢查數字"""

        try:
            return [tuple(map(float, coord.split(","))) for coord in coords]
        except ValueError:
            raise serializers.ValidationError({"points": "Invalid points format."})

    def validate_point(self) -> list:
        # 只能有一個點
        point = self.points.split(",")
        if len(point) > 2:
            raise serializers.ValidationError({"points": "Point type expects only 1 point."})
        # 檢查數字
        try:
            return [float(coord) for coord in point]
        except ValueError:
            raise serializers.ValidationError({"points": "Invalid points format."})

    def validate_linestring(self) -> list:
        # 至少需要2個點
        points = self.points.split(";")
        if len(points) < 2:
            raise serializers.ValidationError({"points": "LineString type expects at least 2 points."})
        return self._validate_number(points)

    def validate_polygon(self) -> list:
        # 多邊形至少需要4個點，且第一個點和最後一個點必須相同
        polygon = self.points.split(";")
        if len(polygon) < 4 or polygon[0] != polygon[-1]:
            raise serializers.ValidationError(
                {"points": "Polygon type expects at least 4 points and the first and last points must be the same."}
            )
        return self._validate_number(polygon)

    def validate_multipoint(self) -> list:
        points = self.points.split("|")
        if len(points) < 2:
            raise serializers.ValidationError({"points": "MultiPoint type expects at least 2 points."})
        single_points = []
        for point in points:
            geom_processor = GeometryProcessor(point)
            single_points.append(Point(geom_processor.validate_point()))
        return single_points

    def validate_multilinestring(self) -> list:
        # 至少需要兩條線
        multilinestring = self.points.split("|")
        if len(multilinestring) < 2:
            raise serializers.ValidationError({"points": "MultiLineString type expects at least 2 lines."})
        lines = []
        for line in multilinestring:
            geom_processor = GeometryProcessor(line)
            lines.append(LineString(geom_processor.validate_linestring()))
        return lines

    def validate_multipolygon(self) -> list:
        # 至少需要兩個多邊形
        multipolygon = self.points.split("|")
        if len(multipolygon) < 2:
            raise serializers.ValidationError({"points": "MultiPolygon type expects at least 2 polygons."})
        polygons = []
        for polygon in multipolygon:
            geom_processor = GeometryProcessor(polygon)
            polygons.append(Polygon(geom_processor.validate_polygon()))
        return polygons

    @property
    def point(self):
        point = self.validate_point()
        return Point(point[0], point[1])

    @property
    def line_string(self):
        line_string = self.validate_linestring()
        return LineString(line_string)

    @property
    def polygon(self):
        polygon = self.validate_polygon()
        return Polygon(polygon)

    @property
    def multi_point(self):
        multi_point = self.validate_multipoint()
        return MultiPoint(multi_point)

    @property
    def multi_line_string(self):
        multi_line_string = self.validate_multilinestring()
        return MultiLineString(multi_line_string)

    @property
    def multi_polygon(self):
        multi_polygon = self.validate_multipolygon()
        return MultiPolygon(multi_polygon)
