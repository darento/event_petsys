from .filters import (
    filter_total_energy,
    filter_min_ch,
    filter_single_mM,
    filter_max_sm,
    filter_specific_mm,
    filter_channel_list,
    filter_ROI,
)
from .mapping_generator import ChannelType
import numpy as np

det_list = [
    [1033333333333333333, 11.0, 1],
    [1555555555555555555, 33.0, 2],
    [4666666666666666666, 15.0, 3],
    [7444444444444444444, 28.0, 4],
    [1333333333333333333, 21.0, 5],
    [4757575577777777777, 5.0, 6],
    [5555555555555555557, 5.5, 7],
]
chtype_map = {
    1: [ChannelType.TIME, ChannelType.ENERGY],
    2: [ChannelType.TIME, ChannelType.ENERGY],
    3: [ChannelType.TIME, ChannelType.ENERGY],
    4: [ChannelType.TIME, ChannelType.ENERGY],
    5: [ChannelType.TIME, ChannelType.ENERGY],
    6: [ChannelType.TIME, ChannelType.ENERGY],
    7: [ChannelType.TIME, ChannelType.ENERGY],
}


def test_filter_total_energy():
    assert filter_total_energy(50)
    assert filter_total_energy(10.1)
    assert filter_total_energy(99.9)
    assert not filter_total_energy(10)
    assert not filter_total_energy(100)
    assert not filter_total_energy(9)
    assert not filter_total_energy(101)


def test_filter_min_ch():
    assert filter_min_ch(det_list, 6, chtype_map)
    assert not filter_min_ch(det_list, 10, chtype_map)


def test_filter_single_mM():
    det_list = [[0, 0, "sm1"]]
    sm_mM_map = {"sm1": "mM1"}
    assert filter_single_mM(det_list, sm_mM_map)

    det_list = [[0, 0, "sm1"], [0, 0, "sm1"]]
    sm_mM_map = {"sm1": "mM1"}
    assert filter_single_mM(det_list, sm_mM_map)

    det_list = [[0, 0, "sm1"], [0, 0, "sm2"]]
    sm_mM_map = {"sm1": "mM1", "sm2": "mM2"}
    assert not filter_single_mM(det_list, sm_mM_map)


def test_filter_max_sm():
    det1_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    det2_list = [[10, 11, 12], [13, 14, 15], [16, 17, 18]]
    sm_mM_map = {3: 1, 6: 2, 9: 3, 12: 4, 15: 5, 18: 6}

    assert not filter_max_sm(det1_list, det2_list, 3, sm_mM_map)
    assert filter_max_sm(det1_list, det2_list, 6, sm_mM_map)


def test_filter_specific_mm():
    det1_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    det2_list = [[10, 11, 12], [13, 14, 15], [16, 17, 18]]
    sm_mM_map = {3: (1, 1), 6: (2, 2), 9: (3, 3), 12: (4, 4), 15: (5, 5), 18: (6, 6)}

    assert not filter_specific_mm(det1_list, det2_list, 7, 7, sm_mM_map)
    assert filter_specific_mm(det1_list, det2_list, 1, 1, sm_mM_map)


def test_filter_channel_list():
    det1_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    det2_list = [[10, 11, 12], [13, 14, 15], [16, 17, 18]]
    valid_channels = np.array([1, 4, 7, 10, 13, 16])
    invalid_channels = np.array([1, 4, 6])

    assert not filter_channel_list(det1_list, det2_list, invalid_channels)
    assert filter_channel_list(det1_list, det2_list, valid_channels)


def test_filter_ROI():
    assert filter_ROI(5, 5, (0, 10), (0, 10))
    assert not filter_ROI(15, 15, (0, 10), (0, 10))
    assert not filter_ROI(10, 10, (0, 10), (0, 10))
    assert not filter_ROI(0, 0, (0, 10), (0, 10))
