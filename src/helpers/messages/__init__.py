import copy
from fastapi_babel.core import make_gettext as _

from src.helpers.messages.message_source import messages_dict


def get_message(key, **kwargs):
    """
    Get a localized message based on a message key and optional keyword arguments.

    This function retrieves a message from the message dictionary based on the provided key and replaces placeholders
    in the message with values from the keyword arguments.

    Args:
        key (str): The message key to look up in the message dictionary.
        **kwargs: Optional keyword arguments containing values to replace placeholders in the message.

    Returns:
        str: The localized message with placeholders replaced by values.

    Example usage:

    ```python
    message_key = "greeting_message"
    user_name = "John"
    message = get_message(message_key, name=user_name)
    ```

    In this example, if the "greeting_message" key corresponds to the message "{name}, welcome!", the `get_message`
    function will return "John, welcome!" after replacing the "{name}" placeholder with the provided user name.

    """
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
