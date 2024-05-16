import jsonpickle
import numpy as np


def serialize(message: object) -> object:
    """
    Serializes the message to a JSON serializable format.

    ### Parameters
    ----------
    `message`: The message to serialize.

    ### Returns
    ----------
    The serialized message.

    ### Raises
    ----------
    - `TypeError`: If the message cannot be serialized.
    """

    if isinstance(message, list):
        return [serialize(item) for item in message]
    if isinstance(message, np.ndarray):
        return [serialize(item) for item in message.tolist()]
    elif isinstance(message, dict):
        serialized_message = {}
        for key, value in message.items():
            serialized_message[key] = serialize(value)
        return serialized_message
    elif hasattr(message, "toJSON"):
        return message.toJSON()  # type:ignore[reportAttributeAccessIssue]
    elif hasattr(message, "to_json"):
        return message.to_json()  # type:ignore[reportAttributeAccessIssue]
    elif hasattr(message, "to_dict"):
        return message.to_dict()  # type:ignore[reportAttributeAccessIssue]
    elif hasattr(message, "__str__") and callable(getattr(message, "__str__")):
        return str(message)
    else:
        try:
            return dict(message)  # type:ignore[reportCallIssue, reportArgumentType]
        except Exception:
            try:
                return jsonpickle.encode(message)
            except Exception as e:
                raise TypeError(
                    f"Could not serialize the message: {message}. Error: {e}"
                )
