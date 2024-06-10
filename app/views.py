from django.shortcuts import render
from django.http import HttpRequest
from .models import CSVData
import math
import csv


def upload_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            CSVData.objects.create(data=row)
    return True


# Calculate distance between two geographical
# coordinates using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def get_unique_categories():
    categories = set()
    csv_data = CSVData.objects.values_list('data', flat=True)
    for item in csv_data:
        food_items = item.get('FoodItems', '')
        if isinstance(food_items, str):  # Check if the value is a string
            categories.update(food_items.split(': '))
    return categories


def map_view(request: HttpRequest):
    upload_csv('./data/food-truck-data.csv')
    csv_data = CSVData.objects.all()

    random_lat = None
    random_lon = None
    distances_and_locations = []
    selected_category = request.POST.get('category')

    if request.method == 'POST':
        lat_input = request.POST.get('latitude')
        lon_input = request.POST.get('longitude')
        if lat_input and lon_input:
            random_lat = float(lat_input)
            random_lon = float(lon_input)

    if random_lat is not None and random_lon is not None:
        # Calculate distances if user provided coordinates
        for item in csv_data:
            lat = item.data.get('Latitude')
            lon = item.data.get('Longitude')
            food_items = item.data.get('FoodItems')
            applicant = item.data.get('Applicant')
            address = item.data.get('Address')
            facility_type = item.data.get('FacilityType')
            if lat and lon and (float(lat), float(lon)) != (0.0, 0.0):
                if selected_category and selected_category not in food_items:
                    continue
                distance = haversine(
                    random_lat,
                    random_lon,
                    float(lat),
                    float(lon))
                distances_and_locations.append({
                    'latitude': lat,
                    'longitude': lon,
                    'distance': distance,
                    'applicant': applicant,
                    'food_items': food_items,
                    'address': address,
                    'facility_type': facility_type
                })

        # Sort by distances
        distances_and_locations.sort(key=lambda x: x['distance'])

        # Extract top 5 closest unique locations
        unique_locations = []
        for loc in distances_and_locations:
            if loc not in unique_locations:
                unique_locations.append(loc)
            if len(unique_locations) == 5:
                break
    else:
        # If no user input, show all locations
        for item in csv_data:
            lat = item.data.get('Latitude')
            lon = item.data.get('Longitude')
            food_items = item.data.get('FoodItems')
            applicant = item.data.get('Applicant')
            address = item.data.get('Address')
            facility_type = item.data.get('FacilityType')
            if lat and lon and (float(lat), float(lon)) != (0.0, 0.0):
                if selected_category and selected_category not in food_items:
                    continue
                distances_and_locations.append({
                    'latitude': lat,
                    'longitude': lon,
                    'applicant': applicant,
                    'food_items': food_items,
                    'address': address,
                    'facility_type': facility_type
                })
        unique_locations = distances_and_locations

    # Prepare data for map
    data_with_coords = [
        {
            'latitude': item['latitude'],
            'longitude': item['longitude'],
            'applicant': item['applicant'],
            'food_items': item['food_items'],
            'address': item['address'],
            'facility_type': item['facility_type']
        }
        for item in unique_locations
    ]

    unique_categories = get_unique_categories()

    return render(request, 'app/map.html', {
        'data_with_coords': data_with_coords,
        'random_lat': random_lat,
        'random_lon': random_lon,
        'categories': unique_categories,
        'selected_category': selected_category,
    })
