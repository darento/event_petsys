from .filters import (
    filter_total_energy,
    filter_min_ch,
    filter_single_mM,
    filter_max_sm,
    filter_specific_mm,
    filter_channel_list,
)

import numpy as np


def test_filter_total_energy():
    assert not filter_total_energy(10)
    assert not filter_total_energy(100)
    assert filter_total_energy(10.01)
    assert filter_total_energy(99.99)
    assert filter_total_energy(50)
    assert not filter_total_energy(5)
    assert not filter_total_energy(105)


def test_filter_min_ch():
    assert filter_min_ch([1, 2, 3], 3)
    assert filter_min_ch([1, 2, 3, 4], 3)
    assert not filter_min_ch([1, 2], 3)
    assert not filter_min_ch([], 1)


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
    assert filter_max_sm(det1_list, det2_list, 5, sm_mM_map)


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