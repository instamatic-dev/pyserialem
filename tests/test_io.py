import numpy as np
import pytest

import pyserialem as pysem


def test_reader_writer(drc):
    fn = drc.parent / 'data' / 'nav.nav'

    items = pysem.read_nav_file(fn)

    assert isinstance(items, list)
    assert len(items) == 1

    out = drc.parent / 'data' / 'out.nav'

    pysem.write_nav_file(out, *items)

    assert out.exists()

    pysem.read_nav_file(out)

    assert isinstance(items, list)
    assert len(items) == 1


def test_mdoc_reader(drc):
    fn = drc.parent / 'data' / 'gm.mrc.mdoc'

    items = pysem.read_mdoc_file(fn)

    assert len(items) == 26
    assert isinstance(items[0], dict)

    kind = 'ZValue'
    items = pysem.read_mdoc_file(fn, only_kind=kind)
    assert len(items) == 25
    assert items[0]['kind'] == kind

    kind = 'MontSection'
    items = pysem.read_mdoc_file(fn, only_kind=kind)
    assert len(items) == 1
    assert items[0]['kind'] == kind
