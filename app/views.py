from django.shortcuts import render
from django.http import HttpRequest
from .utils.data_processing import (
    fetch_csv_data, process_location_data, filter_by_category,
    calculate_distances, get_top_unique_locations
)
from .utils.categories import get_unique_categories


def map_view(request: HttpRequest):
    csv_data = fetch_csv_data()

    random_lat = None
    random_lon = None
    selected_category = request.POST.get('category')
    if request.method == 'POST':
        lat_input = request.POST.get('latitude')
        lon_input = request.POST.get('longitude')
        if lat_input and lon_input:
            random_lat = float(lat_input)
            random_lon = float(lon_input)

    processed_data = [process_location_data(item) for item in csv_data]
    filtered_data = filter_by_category(processed_data, selected_category)
    filtered_data = [d for d in filtered_data if (float(d['latitude']),
                     float(d['longitude'])) != (0.0, 0.0)]

    if (random_lat is not None and random_lon is not None):
        locations_with_distances = calculate_distances(
            filtered_data, random_lat, random_lon)
        
        unique_locations = get_top_unique_locations(locations_with_distances)
    else:
        unique_locations = filtered_data

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
