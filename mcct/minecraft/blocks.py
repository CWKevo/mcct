import typing as t

from dataclasses import dataclass, field
from mcct import NBTData, Component, CARDINALS



@dataclass
class BellBlock(Component):
    """
        A bell block.
    """

    _id = 'minecraft:bell'

    facing: CARDINALS = None
    """The direction the bell is facing."""
    attachment: t.Literal['single_wall', 'floor', 'ceiling'] = None
    """The attachment type of the bell."""



@dataclass
class ChestBlock(Component):
    """
        A chest block.

        ### Example:

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

    @dataclass
    class _NBT(NBTData):
        """
            The chest's NBT data.
        """

        Lock: str = None
        """When not `None`, prevents the container from being opened unless the opener is holding an item whose name matches this string."""


        @dataclass
        class ChestSlot:
            slot: int
            """ID of the slot where the item is located."""
            count: int
            """The item's count."""
            tag: NBTData
            """The item's NBT data."""


        Items: t.List[ChestSlot] = field(default_factory=list)
        """List of chest items."""



        @property
        def _nbt(self) -> t.Dict[str, t.Any]:
            return {
                "Lock": self.Lock,
                "Items": self.Items
            }


    _id = 'minecraft:chest'
    NBT: _NBT = _NBT()

    facing: CARDINALS = None
    """The direction the chest is facing."""
    type: t.Literal['single', 'left', 'right'] = None
    """The type of the chest."""
    waterlogged: bool = None
    """Whether the chest is waterlogged."""
