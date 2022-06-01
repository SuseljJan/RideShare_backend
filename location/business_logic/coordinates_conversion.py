
def latlng_to_coordinates(lat, lng):
    return 'SRID=4326;POINT({} {})'.format(lng, lat)


def coordinates_to_latlng(point_object):
    return [point_object.x, point_object.y]
