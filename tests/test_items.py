import numpy as np
import pytest

import pyserialem as pysem


@pytest.fixture
def map_item(drc):
    fn = drc.parent / 'data' / 'nav.nav'
    items = pysem.read_nav_file(fn)
    map_item = items[0]
    assert map_item.kind == 'Map'
    return map_item


def test_coordinate_convert(map_item):
    assert map_item.stagematrix.shape == (2, 2)

    xy = (1, 1)

    new_xy = map_item.pixel_to_stagecoords(xy)

    assert len(new_xy) == 2

    old_xy = map_item.stage_to_pixelcoords(new_xy)

    assert len(new_xy) == 2
    assert np.allclose(xy, old_xy)


def test_load_image(map_item, drc):
    img = map_item.load_image(drc.parent / 'data')

    assert isinstance(img, np.ndarray)
    assert img.shape == tuple(map_item.MapWidthHeight)


def test_add_markers(map_item):
    n = 10

    coords = np.arange(n * 2).reshape(n, 2)
    nav_items = map_item.add_marker_group(coords)

    assert len(nav_items) == n

    pixelcoords = map_item.markers_as_pixel_coordinates()
    assert pixelcoords.shape == (n, 2)
    assert np.allclose(pixelcoords, coords)

    stagecoords = map_item.markers_as_stage_coordinates()
    assert stagecoords.shape == (n, 2)

    nav_item = nav_items[0]
    assert nav_item.kind == 'Marker'

    map_item.update_markers(nav_item)

    assert len(map_item.markers) == n

    map_item.set_markers(nav_item)

    assert len(map_item.markers) == 1


def test_to_from_dict(map_item):
    d = map_item.to_dict()

    new_map_item = pysem.MapItem.from_dict(d)

    e = new_map_item.to_dict()

    assert isinstance(e, dict)

    # cycle twice to get rid of rounding errors
    new_map_item = pysem.MapItem.from_dict(e)

    f = new_map_item.to_dict()

    assert f == e


def test_validate(map_item):
    map_item.validate()

    del map_item.StageXYZ

    with pytest.raises(KeyError):
        map_item.validate()


def test_tag_loading(map_item, drc):
    n = 10

    coords = np.arange(n * 2).reshape(n, 2)
    nav_items = map_item.add_marker_group(coords, acquire=True)

    out = drc.parent / 'data' / 'out2.nav'
    pysem.write_nav_file(out, map_item, *nav_items)

    items = pysem.read_nav_file(out, acquire_only=False)
    assert len(items) == 1 + n

    items = pysem.read_nav_file(out, acquire_only=True)
    assert len(items) == n


def test_nav_item(map_item):
    coords = np.arange(2).reshape(1, 2)
    nav_items = map_item.add_marker_group(coords)
    nav_item = nav_items[0]

    assert isinstance(nav_item.stage_x, float)
    assert isinstance(nav_item.stage_y, float)
    assert isinstance(nav_item.stage_z, float)
    assert len(nav_item.color_rgba) == 4

    assert nav_item.color_str == 'red'

    d = nav_item.to_dict()

    new_nav_item = pysem.NavItem(d, tag='test')
    assert new_nav_item.tag == 'test'
