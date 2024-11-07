from typing import Any, Optional
from datetime import time

from appdaemon.adapi import ADAPI
from appdaemon.utils import sync_wrapper

import appdaemon.plugins.hass.hassapi as hass
from appdaemon import utils

bool_true = {"y", "yes", "true", "on"}
bool_false = {"n", "no", "false", "off"}


@sync_wrapper
async def get_state_float(
    self: ADAPI, entity: str, **kwargs: Optional[Any]
) -> Optional[float]:
    value = await self.get_state(entity, **kwargs)
    try:
        return float(value)
    except:
        self.log("Failed to get float value for entity %s. Received: %s", entity, value)
        return None


@sync_wrapper
async def get_state_bool(
    api: ADAPI, entity: str, **kwargs: Optional[Any]
) -> Optional[bool]:
    value = await api.get_state(entity, **kwargs)
    if value is None:
        return None
    try:
        return to_bool(value.lower())
    except:
        api.log("Failed to get bool value for entity %s. Received: %s", entity, value)
        return None


def to_bool(value: str) -> Optional[bool]:
    if value in bool_true:
        return True
    elif value in bool_false:
        return False
    else:
        return None


def time_in_range(
    cur_time: time, from_time: Optional[time], to_time: Optional[time]
) -> bool:
    if from_time is None or to_time is None:
        return False
    if from_time == to_time:
        return cur_time == from_time
    if from_time > to_time:  # This is an overnight range
        return cur_time > from_time or cur_time < to_time
    else:  # This is an intraday range
        return from_time < cur_time < to_time
