from app.models import CSVData
from app.utils.calculations import haversine


def fetch_csv_data():
    return CSVData.objects.all()


def process_location_data(item):
    return {
        'latitude': item.data.get('Latitude'),
        'longitude': item.data.get('Longitude'),
        'food_items': item.data.get('FoodItems'),
        'applicant': item.data.get('Applicant'),
        'address': item.data.get('Address'),
        'facility_type': item.data.get('FacilityType')
    }


def filter_by_category(locations, selected_category):
    if not selected_category:
        return locations
    return [loc for loc in locations if selected_category in loc['food_items']]


def calculate_distances(locations, lat, lon):
    distances = []
    for loc in locations:
        if (loc['latitude'] and loc['longitude'] and
           (float(loc['latitude']), float(loc['longitude'])) != (0.0, 0.0)):
            distance = haversine(
                lat, lon, float(loc['latitude']),
                float(loc['longitude']))
            loc['distance'] = distance
            distances.append(loc)
    return sorted(distances, key=lambda x: x['distance'])


def get_top_unique_locations(locations, top_n=5):
    unique_locations = []
    seen = set()
    for loc in locations:
        coord = (loc['latitude'], loc['longitude'])
        if coord not in seen and coord != (0.0, 0.0):
            seen.add(coord)
            unique_locations.append(loc)
        if len(unique_locations) == top_n:
            break
    return unique_locations
