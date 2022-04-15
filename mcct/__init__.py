import typing as t

import json
import re

from dataclasses import dataclass, field


_V = t.TypeVar("_V")

CARDINALS = t.Literal["north", "east", "south", "west"]



def convert_value(value: _V) -> _V:
    """
        Converts a value to Minecraft's syntax.
    """

    if isinstance(value, dict):
        return {k: convert_value(v) for k, v in value.items()}

    elif isinstance(value, bool):
        return str(value).lower()

    elif isinstance(value, list):
        if len(value) == 0:
            return None

    return value



@dataclass
class TagData:
    """
        Block data properties, not to be confused with the "tag" in certain NBT.

        Example (`bell`): `[attachement=single_wall,facing=south]`
    """

    _dict: t.Dict[str, t.Any] = field(default_factory=dict)


    def parse(self) -> t.List[str]:
        """
            Parses the tag data to a list of `key=value` strings.
        """

        key_value_list = []

        for key, value in self._dict.items():
            c_value = convert_value(value)

            if c_value is None:
                continue

            key_value_list.append(f"{key}={c_value}")

        return key_value_list


    def __str__(self) -> str:
        return f"[{','.join(self.parse())}]"



@dataclass
class NBTData:
    """
        NBT data of anything.

        Example (`chest`):
        ```
            {
                Items: [{
                    Slot: 0b,
                    id: "minecraft:egg",
                    Count: 1b,
                    tag: {
                        HideFlags: 1,
                        Enchantments: [{
                            id: "minecraft:power",
                            lvl: 1s
                        }]
                    }
                ]}
            }
        ```
    """

    _dict: t.Dict[str, t.Any] = field(default_factory=dict)


    @property
    def _nbt(self) -> t.Dict[str, t.Any]:
        return self._dict


    def parse(self) -> t.Dict[str, t.Any]:
        """
            Parses the NBT data to a syntax Minecraft understands.
        """

        converted_dict = {}

        for key, value in self._nbt.items():
            c_value = convert_value(value)

            if c_value is None:
                continue

            elif isinstance(c_value, dict):
                if len(c_value) == 0:
                    continue

            elif isinstance(c_value, list):
                if len(c_value) == 0:
                    continue
            
            converted_dict[key] = convert_value(c_value)

        return converted_dict


    def __str__(self) -> str:
        return re.sub(r'"(.*?)"(?=:)', r'\1', json.dumps(self.parse()))



@dataclass
class Component:
    @dataclass
    class _NBT(NBTData):
        """
            NBT data of a component.
        """

        _dict: t.Dict[str, t.Any] = field(default_factory=dict)


    NBT: _NBT = _NBT()
    """The component's NBT data."""



    def __str__(self) -> str:
        c_id = getattr(self, '_id', None)

        valid_tag_data = TagData(_dict={
            key: value for key, value in self.__dict__.items() if key != 'NBT' and not key.startswith('_')
        }) if len(self.__dict__) > 0 else ''

        valid_nbt_data = str(self.NBT)

        return f"{c_id if c_id is not None else ''}{valid_tag_data}{valid_nbt_data if valid_nbt_data != '{}' else ''}"
