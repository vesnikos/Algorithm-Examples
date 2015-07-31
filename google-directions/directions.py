# coding=utf-8
__author__ = 'vesnikos'

import os
import shapefile
from googlemaps import Client


from googlemaps import directions
from googlemaps import geocoding

cwd = os.path.dirname(__file__)


class geocoder(object):
    def __init__(self, client):
        self.client = client

    def coords(self, address):
        return [(y['lat'], y['lng']) for y in
                [x['geometry']['location'] for x in geocoding.geocode(self.client, address=address, language="el")]]


def decode(point_str):
    #  https://gist.github.com/signed0/2031157


    '''Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html

    This is a generic method that returns a list of (latitude, longitude)
    tuples.

    :param point_str: Encoded polyline string.
    :type point_str: string
    :returns: List of 2-tuples where each tuple is (latitude, longitude)
    :rtype: list

    '''

    # sone coordinate offset is represented by 4 to 5 binary chunks
    coord_chunks = [[]]
    for char in point_str:

        # convert each character to decimal from ascii
        value = ord(char) - 63

        # values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)
        value &= 0x1F

        coord_chunks[-1].append(value)

        if split_after:
            coord_chunks.append([])

    del coord_chunks[-1]

    coords = []

    for coord_chunk in coord_chunks:
        coord = 0

        for i, chunk in enumerate(coord_chunk):
            coord |= chunk << (i * 5)

        # there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord  # invert
        coord >>= 1
        coord /= 100000.0

        coords.append(coord)

    # convert the 1 dimensional list to a 2 dimensional list and offsets to
    # actual values
    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue

        prev_x += coords[i + 1]
        prev_y += coords[i]
        # a round to 6 digits ensures that the floats are the same as when
        # they were encoded
        points.append((round(prev_x, 6), round(prev_y, 6)))

    return points


def GetGoogleKey(file=None):
    with open(file, "r") as f:
        for line in f:
            if line.startswith(('#', '\n')):
                continue
            return line


client = Client(key=GetGoogleKey(
                        os.path.join(cwd,'google-key.txt')
                        )
                    )

loc = geocoder(client)
latlong = loc.coords("Triantafyllopoy 35 thessaloniki")

wp = directions.directions(client, "Γεωργίου Γεννηματά καλαμαριά", "Triantafyllopouloy 35 Pylaia", language="el")

wr = shapefile.Writer(shapefile.POLYLINE)
wr.autoBalance = 1
wr.field("Route")

w_critical_points = shapefile.Writer(shapefile.POINT)
w_critical_points.autoBalance = 1
w_critical_points.field("Directions", "C", 254)

for route in wp:
    points = decode(route['overview_polyline']['points'])
    wr.poly(shapeType=3, parts=[points])
    wr.record(route['summary'].encode("cp1253"))
    for leg in route['legs']:
        for step in leg['steps']:
            w_critical_points.point(float(step['start_location']['lng']), float(step['start_location']['lat']))
            w_critical_points.record(step['html_instructions'].encode("UTF8"))
    w_critical_points.save(target=os.path.join("critical_points"))
    wr.save(target=os.path.join("route"))
