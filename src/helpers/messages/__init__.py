import copy
from fastapi_babel.core import make_gettext as _

from src.helpers.messages.message_source import messages_dict


def get_message(key, **kwargs):

    msg = copy.deepcopy(messages_dict.get(key, "===== msg error ====="))

    if isinstance(msg, dict):
        if "a_sync" in kwargs.keys():
            if kwargs["a_sync"]:
                msg = msg.pop("a_sync", "----- msg error -----")
            else:
                msg = msg.pop("sync", "+++++ msg error +++++")
            kwargs.pop("a_sync")
        else:
            msg = msg.pop("sync", "+++++ msg error +++++")
    return _(msg).format(**kwargs)
