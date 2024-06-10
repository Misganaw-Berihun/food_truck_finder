from app.models import CSVData


def get_unique_categories():
    categories = set()
    csv_data = CSVData.objects.values_list('data', flat=True)
    for item in csv_data:
        food_items = item.get('FoodItems', '')
        if isinstance(food_items, str):
            categories.update(food_items.split(': '))
    return categories
