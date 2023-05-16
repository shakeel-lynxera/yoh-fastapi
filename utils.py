from geopy.distance import geodesic


def calculate_distance(user_lat, user_lng, resource_lat, resource_lng, distance_unit):
    try:
        distance_instance = geodesic((float(user_lat), float(user_lng)), (resource_lat, resource_lng))
        if distance_unit == "miles":
            distance_instance = round(distance_instance.miles, 2)
        if distance_unit == "km":
            distance_instance = round(distance_instance.kilometers, 2)
        if distance_unit == "meters":
            distance_instance = round(distance_instance.meters, 2)
        return distance_instance
    except Exception as e:
        print(e)
