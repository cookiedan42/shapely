import warnings
from contextlib import contextmanager

import numpy as np
import pytest

import shapely

shapely20_todo = pytest.mark.xfail(
    strict=False, reason="Not yet implemented for Shapely 2.0"
)

point_polygon_testdata = (
    shapely.points(np.arange(6), np.arange(6)),
    shapely.box(2, 2, 4, 4),
)
# XY
point = shapely.Point(2, 3)
line_string = shapely.LineString([(0, 0), (1, 0), (1, 1)])
linear_ring = shapely.LinearRing([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
polygon = shapely.Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
polygon_with_hole = shapely.Polygon(
    [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)],
    holes=[[(2, 2), (2, 4), (4, 4), (4, 2), (2, 2)]],
)
multi_point = shapely.MultiPoint([(0, 0), (1, 2)])
multi_line_string = shapely.MultiLineString([[(0, 0), (1, 2)]])
multi_polygon = shapely.multipolygons(
    [
        [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],
        [(2.1, 2.1), (2.2, 2.1), (2.2, 2.2), (2.1, 2.2), (2.1, 2.1)],
    ]
)
geometry_collection = shapely.GeometryCollection(
    [shapely.Point(51, -1), shapely.LineString([(52, -1), (49, 2)])]
)
empty = shapely.from_wkt("GEOMETRYCOLLECTION EMPTY")
empty_point = shapely.from_wkt("POINT EMPTY")
empty_line_string = shapely.from_wkt("LINESTRING EMPTY")
empty_polygon = shapely.from_wkt("POLYGON EMPTY")
empty_multi_point = shapely.from_wkt("MULTIPOINT EMPTY")
empty_multi_line_string = shapely.from_wkt("MULTILINESTRING EMPTY")
empty_multi_polygon = shapely.from_wkt("MULTIPOLYGON EMPTY")
multi_point_empty = shapely.multipoints([empty_point])
multi_line_stringt_empty = shapely.multilinestrings([empty_line_string])
multi_polygon_empty = shapely.multipolygons([empty_polygon])
geometry_collection_empty = shapely.geometrycollections([empty_line_string])
# XYZ
point_z = shapely.Point(2, 3, 4)
line_string_z = shapely.LineString([(0, 0, 4), (1, 0, 4), (1, 1, 4)])
linear_ring_z = shapely.LinearRing(
    [(0, 0, 8), (1, 0, 7), (1, 1, 6), (0, 1, 9), (0, 0, 8)]
)
polygon_z = shapely.Polygon([(0, 0, 4), (2, 0, 4), (2, 2, 4), (0, 2, 4), (0, 0, 4)])
polygon_with_hole_z = shapely.Polygon(
    [(0, 0, 4), (0, 10, 4), (10, 10, 4), (10, 0, 4), (0, 0, 4)],
    holes=[[(2, 2, 4), (2, 4, 4), (4, 4, 4), (4, 2, 4), (2, 2, 4)]],
)
multi_point_z = shapely.MultiPoint([(0, 0, 4), (1, 2, 4)])
multi_line_string_z = shapely.MultiLineString([[(0, 0, 4), (1, 2, 4)]])
multi_polygon_z = shapely.multipolygons(
    [
        [(0, 0, 4), (1, 0, 4), (1, 1, 4), (0, 1, 4), (0, 0, 4)],
        [(2.1, 2.1, 4), (2.2, 2.1, 4), (2.2, 2.2, 4), (2.1, 2.2, 4), (2.1, 2.1, 4)],
    ]
)
geometry_collection_z = shapely.GeometryCollection([point_z, line_string_z])
empty_geometry_collection_z = shapely.from_wkt("GEOMETRYCOLLECTION Z EMPTY")
empty_point_z = shapely.from_wkt("POINT Z EMPTY")
empty_line_string_z = shapely.from_wkt("LINESTRING Z EMPTY")
empty_polygon_z = shapely.from_wkt("POLYGON Z EMPTY")
empty_multi_point_z = shapely.from_wkt("MULTIPOINT Z EMPTY")
empty_multi_line_string_z = shapely.from_wkt("MULTILINESTRING Z EMPTY")
empty_multi_polygon_z = shapely.from_wkt("MULTIPOLYGON Z EMPTY")
multi_point_empty_z = shapely.multipoints([empty_point_z])
multi_line_stringt_empty_z = shapely.multilinestrings([empty_line_string_z])
multi_polygon_empty_z = shapely.multipolygons([empty_polygon_z])
geometry_collection_empty_z = shapely.geometrycollections([empty_line_string_z])

all_types = (
    point,
    line_string,
    linear_ring,
    polygon,
    polygon_with_hole,
    multi_point,
    multi_line_string,
    multi_polygon,
    geometry_collection,
    empty,
    empty_point,
    empty_line_string,
    empty_polygon,
    empty_multi_point,
    empty_multi_line_string,
    empty_multi_polygon,
    multi_point_empty,
    multi_line_stringt_empty,
    multi_polygon_empty,
    geometry_collection_empty,
)

all_types_z = (
    point_z,
    line_string_z,
    linear_ring_z,
    polygon_z,
    polygon_with_hole_z,
    multi_point_z,
    multi_line_string_z,
    multi_polygon_z,
    geometry_collection_z,
    empty_geometry_collection_z,
    empty_point_z,
    empty_line_string_z,
    empty_polygon_z,
    empty_multi_point_z,
    empty_multi_line_string_z,
    empty_multi_polygon_z,
    multi_point_empty_z,
    multi_line_stringt_empty_z,
    multi_polygon_empty_z,
    geometry_collection_empty_z,
)


@contextmanager
def ignore_invalid(condition=True):
    if condition:
        with np.errstate(invalid="ignore"):
            yield
    else:
        yield


with ignore_invalid():
    line_string_nan = shapely.LineString([(np.nan, np.nan), (np.nan, np.nan)])


@contextmanager
def ignore_warnings(geos_version, category):
    if shapely.geos_version < geos_version:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=category)
            yield
    else:
        yield


def equal_geometries_abnormally_yield_unequal(geom):
    """Older GEOS versions have various issues with "equals"."""
    if geom.is_empty and shapely.get_num_geometries(geom) > 0:
        if shapely.geos_version < (3, 10, 0) and geom.geom_type == "GeometryCollection":
            return True
        if shapely.geos_version < (3, 13, 0) and geom.geom_type.startswith("Multi"):
            return True
    return False
