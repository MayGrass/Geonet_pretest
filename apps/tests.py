from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.gis.geos import Point
from apps.models import Geometry


class GeometryTestCase(APITestCase):
    def setUp(self):
        # 建立測試資料
        self.new_geometry = Geometry.objects.create(title="Point test", type="Point", geom=Point(1, 1))

    def test_create(self):
        url = reverse("interview_api:geometry-list")
        base_test_data = {"title": "test"}
        # 測試Point
        point_test_data = base_test_data | {"type": "Point", "points": "1,1"}
        response = self.client.post(url, point_test_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 測試LineString
        line_string_test_data = base_test_data | {"type": "LineString", "points": "1,1;2,2"}
        response = self.client.post(url, line_string_test_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 測試Polygon
        polygon_test_data = base_test_data | {"type": "Polygon", "points": "0,0;0,1;1,1;0,0"}
        response = self.client.post(url, polygon_test_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 測試MultiPoint
        multi_point_test_data = base_test_data | {"type": "MultiPoint", "points": "1,1|2,2"}
        response = self.client.post(url, multi_point_test_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 測試MultiLineString
        multi_line_string_test_data = base_test_data | {"type": "MultiLineString", "points": "1,1;2,2|3,3;4,4"}
        response = self.client.post(url, multi_line_string_test_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 測試MultiPolygon
        multi_polygon_test_data = base_test_data | {
            "type": "MultiPolygon",
            "points": "0,0;0,1;1,1;0,0|0,0;0,1;1,1;0,0",
        }
        response = self.client.post(url, multi_polygon_test_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        url = reverse("interview_api:geometry-detail", kwargs={"pk": self.new_geometry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_answer = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1.0, 1.0]},
                    "properties": {"title": "Point test"},
                }
            ],
        }
        self.assertEqual(response.data, response_answer)

    def test_update(self):
        url = reverse("interview_api:geometry-detail", kwargs={"pk": self.new_geometry.id})
        update_test_data = {"title": "update test"}
        response = self.client.put(url, update_test_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Geometry.objects.get(pk=self.new_geometry.id).title, update_test_data["title"])

    def test_destroy(self):
        url = reverse("interview_api:geometry-detail", kwargs={"pk": self.new_geometry.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Geometry.objects.filter(pk=self.new_geometry.id).exists(), False)
