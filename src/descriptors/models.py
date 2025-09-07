from typing import Any, TypeAlias, List
from functools import reduce, cached_property

JSON: TypeAlias = dict[str, Any]


class Field:
    def __init__(self, path: str):
        self.__path = path

    @property
    def path(self) -> str:
        return self.__path

    @cached_property
    def keys(self) -> List[str]:
        return self.path.split('.')

    def __get__(self, instance):
        if instance is None:
            return self
        return self._get_value(instance.payload)

    def __set__(self, instance, value):
        if instance is None:
            return
        self._set_value(instance.payload, value)

    def _get_value(self, payload: JSON) -> Any:
        try:
            return reduce(lambda d, k: d[k], self.keys, payload)
        except (KeyError, TypeError):
            return None

    def _set_value(self, payload: JSON, value: Any) -> None:
        keys = self.keys[:-1]
        last_key = self.keys[-1]

        parent = reduce(
            lambda d, k: d.setdefault(k, {}),
            keys,
            payload
        )

        parent[last_key] = value

class Model:
    def __init__(self, payload: JSON):
        self.payload = payload