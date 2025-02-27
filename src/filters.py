from itertools import chain
from typing import Tuple

import numpy as np

from src.mapping_generator import ChannelType
from src.utils import get_max_en_channel, get_num_eng_channels


def filter_total_energy(
    en_total: float, en_min: float = 10, en_max: float = 100
) -> list:
    """
    Filters the event based on the total energy of the event.

    The function checks if the total energy of the event is within a specified range (en_min, en_max).

    Parameters:
        - en_total (float): The total energy of the event.
        - en_min (float, optional): The minimum energy threshold. Defaults to 10.
        - en_max (float, optional): The maximum energy threshold. Defaults to 100.

    Returns:
    bool: True if the total energy is within the range (en_min, en_max), False otherwise.
    """
    if (en_total > en_min) & (en_total < en_max):
        return True
    else:
        return False


def filter_min_ch(
    det_list: list[list], min_ch: int, chtype_map: dict, sum_rows_cols: bool
) -> bool:
    """
    Filters the event based on the minimum number of channels.

    The function checks if the number of channels in the detector is greater than a specified threshold (min_ch).

    Parameters:
        - det_list (list): The event data.
        - min_ch (int): The minimum number of channels.
        - chtype_map (dict): A dictionary mapping the channel type to the channel number.
        - sum_rows_cols (bool): A flag to indicate whether to sum the rows and columns.

    Returns:
    bool: True if the number of channels is greater than min_ch, False otherwise.
    """
    num_eng_ch = get_num_eng_channels(det_list, chtype_map)
    if not sum_rows_cols:
        return num_eng_ch >= min_ch
    else:
        if min_ch <= num_eng_ch < len(det_list):
            return True
        else:
            return False


def filter_single_mM(det_list: list[list], sm_mM_map: dict) -> bool:
    """
    This function filters out super modules that have more than one mini module hit.

    Parameters:
        - det_list (list[list]): A nested list where each sublist represents a hit. Each sublist contains information about the hit.
        - sm_mM_map (dict): A dictionary mapping the super module (sm) to the mini module (mM).

    Returns:
    bool: True if the super module has exactly one mini module hit, False otherwise.
    """
    n_mm = len(set(sm_mM_map[x[2]] for x in det_list))
    return n_mm == 1


def filter_max_sm(
    det1_list: list[list], det2_list: list[list], max_sm: int, sm_mM_map: dict
) -> bool:
    """
    Filters events based on the number of supermodules present.

    Parameters:
        - det1_list (list[list]): The first list of detections.
        - det2_list (list[list]): The second list of detections.
        - max_sm (int): The maximum number of supermodules allowed.
        - sm_mM_map (dict): A mapping from module to supermodule.

    Returns:
    bool: True if the number of unique supermodules in the event does not exceed max_sm, False otherwise.

    Note: This function is only valid for coinc mode.
    """
    sm_set = set()
    for hit in chain(det1_list, det2_list):
        sm_set.add(sm_mM_map[hit[2]])
        if len(sm_set) > max_sm:
            return False
    return True


def filter_specific_mm(
    det1_list: list[list],
    det2_list: list[list],
    sm_num: int,
    mm_num: int,
    sm_mM_map: dict,
) -> bool:
    """
    Selects events in a specific mini module.

    Parameters:
        - det1_list (list[list]): The first list of detections.
        - det2_list (list[list]): The second list of detections.
        - sm_num (int): The supermodule number to filter for.
        - mm_num (int): The mini module number to filter for.
        - sm_mM_map (dict): A mapping from module to supermodule and mini module.

    Returns:
    bool: True if the specified supermodule and mini module is present in the event, False otherwise.
    """
    for hit in chain(det1_list, det2_list):
        if sm_mM_map[hit[2]] == (sm_num, mm_num):
            return True
    return False


def filter_channel_list(
    det1_list: list[list], det2_list: list[list], valid_channels: np.ndarray
) -> bool:
    """
    Filters events based on whether all impacts in either list are in the valid channels list.

    Parameters:
        - det1_list (list[list]): The first list of detections.
        - det2_list (list[list]): The second list of detections.
        - valid_channels (np.ndarray): An array of valid channels.

    Returns:
    bool: True if all impacts in either det1_list or det2_list are in valid_channels, False otherwise.
    """
    return all(imp[0] in valid_channels for imp in det1_list) or all(
        imp[0] in valid_channels for imp in det2_list
    )


def filter_ROI(
    x_pos: float, y_pos: float, x_ROI: Tuple[float, float], y_ROI: Tuple[float, float]
) -> bool:
    """
    Filters events based on the position of the event.

    Parameters:
        - x_pos (float): The x position of the event.
        - y_pos (float): The y position of the event.
        - x_ROI (Tuple[float, float]): The x position of the region of interest.
        - y_ROI (Tuple[float, float]): The y position of the region of interest.

    Returns:
    bool: True if the event is within the region of interest, False otherwise.
    """
    return (
        (x_pos > x_ROI[0])
        & (x_pos < x_ROI[1])
        & (y_pos > y_ROI[0])
        & (y_pos < y_ROI[1])
    )


def filter_coincidence(
    det1_list: list[list],
    det2_list: list[list],
    chtype_map: dict,
    time_window: float,
) -> list[bool, float, float]:
    """
    Filters events based on the time difference between two detectors.

    Parameters:
        - det1_list (list[list]): The first list of detections.
        - det2_list (list[list]): The second list of detections.
        - chtype_map (dict): A dictionary mapping the channel type to the channel number.
        - time_window (float): The time window for the coincidence.

    Returns:
    list[bool, float, float]: A list containing a boolean value indicating whether the event is within the time window, t1 and t2.
    """
    tch_det1 = get_max_en_channel(det1_list, chtype_map, ChannelType.TIME)
    tch_det2 = get_max_en_channel(det2_list, chtype_map, ChannelType.TIME)
    time_diff = abs(tch_det1[0] - tch_det2[0])
    return time_diff < time_window, tch_det1, tch_det2
