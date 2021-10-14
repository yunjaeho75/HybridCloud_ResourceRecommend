from . import spamfilter
from . import psoazure
from . import AbstractHelper

def get(ws) -> AbstractHelper:
    if ws.data_helper == "spamfilter":
        return spamfilter.helper()

    if ws.data_helper == "azure-vm":
        return psoazure.helper()

    if ws.data_helper == "time-series-base":
        return spamfilter.base_helper()

    return None

