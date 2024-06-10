from django.test import TestCase, Client
from django.urls import reverse
from app.models import CSVData
from app.utils.calculations import haversine
from app.utils.categories import get_unique_categories
from app.utils.data_processing import (
    fetch_csv_data, process_location_data, filter_by_category,
    calculate_distances, get_top_unique_locations
)


class MapViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('map_view')

        CSVData.objects.create(data={
            'Latitude': 37.7749,
            'Longitude': -122.4194,
            'FoodItems': 'Hot Dogs: Snacks',
            'Applicant': 'Test Vendor 1',
            'Address': 'Test Address 1',
            'FacilityType': 'Truck'
        })
        CSVData.objects.create(data={
            'Latitude': 0.0,
            'Longitude': 0.0,
            'FoodItems': 'Ice Cream',
            'Applicant': 'Test Vendor 2',
            'Address': 'Test Address 2',
            'FacilityType': 'Cart'
        })
        CSVData.objects.create(data={
            'Latitude': 34.0522,
            'Longitude': -118.2437,
            'FoodItems': 'Burgers',
            'Applicant': 'Test Vendor 3',
            'Address': 'Test Address 3',
            'FacilityType': 'Truck'
        })

    def test_map_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/map.html')
        self.assertIn('data_with_coords', response.context)
        self.assertIn('categories', response.context)

        data_with_coords = response.context['data_with_coords']
        for item in data_with_coords:
            self.assertNotEqual(
                (float(item['latitude']), float(item['longitude'])), (0.0, 0.0)
                )

    def test_map_view_post_with_coordinates(self):
        response = self.client.post(self.url, {
            'latitude': '37.7749',
            'longitude': '-122.4194'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/map.html')
        self.assertIn('data_with_coords', response.context)
        self.assertIn('categories', response.context)

        data_with_coords = response.context['data_with_coords']
        for item in data_with_coords:
            self.assertNotEqual(
                (float(item['latitude']), float(item['longitude'])), (0.0, 0.0)
                )

    def test_map_view_post_with_category(self):
        response = self.client.post(self.url, {
            'latitude': '37.7749',
            'longitude': '-122.4194',
            'category': 'Burgers'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/map.html')
        self.assertIn('data_with_coords', response.context)
        self.assertIn('categories', response.context)

        data_with_coords = response.context['data_with_coords']
        for item in data_with_coords:
            self.assertIn('Burgers', item['food_items'])

    def test_map_view_no_post_data(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/map.html')
        self.assertIn('data_with_coords', response.context)
        self.assertIn('categories', response.context)

        data_with_coords = response.context['data_with_coords']
        for item in data_with_coords:
            self.assertNotEqual(
                (float(item['latitude']), float(item['longitude'])), (0.0, 0.0)
                )


class UtilsTests(TestCase):

    def setUp(self):
        CSVData.objects.create(data={
            'Latitude': 37.7749,
            'Longitude': -122.4194,
            'FoodItems': 'Hot Dogs: Snacks',
            'Applicant': 'Test Vendor 1',
            'Address': 'Test Address 1',
            'FacilityType': 'Truck'
        })
        CSVData.objects.create(data={
            'Latitude': 0.0,
            'Longitude': 0.0,
            'FoodItems': 'Ice Cream',
            'Applicant': 'Test Vendor 2',
            'Address': 'Test Address 2',
            'FacilityType': 'Cart'
        })
        CSVData.objects.create(data={
            'Latitude': 34.0522,
            'Longitude': -118.2437,
            'FoodItems': 'Burgers',
            'Applicant': 'Test Vendor 3',
            'Address': 'Test Address 3',
            'FacilityType': 'Truck'
        })

    def test_haversine(self):
        distance = haversine(37.7749, -122.4194, 34.0522, -118.2437)
        self.assertAlmostEqual(distance, 559, delta=1)

    def test_get_unique_categories(self):
        unique_categories = get_unique_categories()
        self.assertIn('Hot Dogs', unique_categories)
        self.assertIn('Snacks', unique_categories)
        self.assertIn('Ice Cream', unique_categories)
        self.assertIn('Burgers', unique_categories)

    def test_fetch_csv_data(self):
        data = fetch_csv_data()
        self.assertEqual(len(data), 3)

    def test_process_location_data(self):
        item = CSVData.objects.first()
        processed_data = process_location_data(item)
        self.assertEqual(processed_data['latitude'], 37.7749)
        self.assertEqual(processed_data['longitude'], -122.4194)
        self.assertEqual(processed_data['food_items'], 'Hot Dogs: Snacks')
        self.assertEqual(processed_data['applicant'], 'Test Vendor 1')
        self.assertEqual(processed_data['address'], 'Test Address 1')
        self.assertEqual(processed_data['facility_type'], 'Truck')

    def test_filter_by_category(self):
        items = fetch_csv_data()
        processed_data = [process_location_data(item) for item in items]
        filtered_data = filter_by_category(processed_data, 'Burgers')
        self.assertEqual(len(filtered_data), 1)
        self.assertEqual(filtered_data[0]['food_items'], 'Burgers')

    def test_calculate_distances(self):
        items = fetch_csv_data()
        processed_data = [process_location_data(item) for item in items]
        distances = calculate_distances(processed_data, 37.7749, -122.4194)
        self.assertEqual(len(distances), 2)
        self.assertAlmostEqual(distances[0]['distance'], 0, delta=1)

    def test_get_top_unique_locations(self):
        items = fetch_csv_data()
        processed_data = [process_location_data(item) for item in items]
        top_locations = get_top_unique_locations(processed_data, top_n=2)
        self.assertEqual(len(top_locations), 2)
        self.assertNotIn(
            (0.0, 0.0),
            [(loc['latitude'], loc['longitude']) for loc in top_locations]
        )
