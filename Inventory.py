import re


class Item(object):
    """ A virtual class container for all Inventory item types """
    def __init__(self):
        """ level: all items have a level... don't they? """
        self._level = None
        self._shortcode = None

    @property
    def level(self):
        """ Item Level """
        return self._level

    @level.setter
    def level(self, lvl):
        self._level = lvl

    def itemcount(self):
        return 1

    def invcount(self):
        return 1


class Rarity(object):
    """
        Some items have a Rarity value.
        This is a virtual class for all Rarity levels
    """
    def __init__(self):
        self._shortcode = None


class Common(Rarity):
    """ Very Rare level rarity """
    def __init__(self):
        super(Common, self).__init__()
        self._shortcode = "VR"


class Rare(Rarity):
    """ Rare level rarity """
    def __init__(self):
        super(Rare, self).__init__()
        self._shortcode = "VR"


class VeryRare(Rarity):
    """ Very Rare level rarity """
    def __init__(self):
        super(VeryRare, self).__init__()
        self._shortcode = "VR"


class ItemWithRarity(Item):
    def __init__(self):
        super(ItemWithRarity, self).__init__()
        self._rarity = None

    @property
    def rarity(self):
        return self._rarity

    @rarity.setter
    def rarity(self, rarity):
        self._rarity = rarity


class Key(Item):
    """ """
    def __init__(self):
        super(Key, self).__init__()


class Media(Item):
    """ """
    def __init__(self):
        super(Media, self).__init__()


class Powerup(Item):
    """ """
    def __init__(self):
        super(Powerup, self).__init__()


class PowerCube(ItemWithRarity):
    """ """
    def __init__(self):
        super(PowerCube, self).__init__()


class Resonator(ItemWithRarity):
    """ """
    def __init__(self):
        super(Resonator, self).__init__()


class _Pointer(object):
    def __init__(self, data):
        self._data = data
        self._index = 0

    def next(self):
        if self._index == len(self._data):
            raise StopIteration
        element = self._data[self._index]
        self._index += 1
        return element


class Container(ItemWithRarity):
    def __init__(self, guid=None):
        super(Container, self).__init__()
        self._guid = guid or None
        self._contents = []
        # Array of valid items for this container
        self._restricted_items = []

    def __iter__(self):
        return _Pointer(self._contents)

    def __len__(self):
        return len(self.contents)

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, val):
        self._contents = val

    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, val):
        self._guid = val

    def itemcount(self):
        return len(self.contents) + 1

    def invcount(self):
        return self.itemcount()

    def add(self, item):
        assert(any([isinstance(item, x) for x in self._restricted_items]))
        self.contents.append(item)

    def delete(self, item):
        try:
            for elem in self.contents:
                try:
                    # identify item by guid and remove it.
                    if elem.guid == item.guid:
                        self.contents.remove(elem)
                        break
                except AttributeError:
                    if (item.__class__ == elem.__class__ and
                       item.level == elem.level and
                       item.rarity == elem.rarity):
                        self.contents.remove(elem)
                        break
            else:
                raise RuntimeError(
                    "Could not find item with guid {} in inventory".format(
                        item.guid
                    )
                )
        except ValueError:
            pass


class MUFG(Container):
    """ """
    def __init__(self):
        super(Capsule, self).__init__()
        self._restricted_items = [
            Resonator,
            Key,
            Media,
            PowerCube,
            Mod,
            Weapon,
        ]


class Capsule(Container):
    """ """
    def __init__(self):
        super(Capsule, self).__init__()
        self._restricted_items = [
            Resonator,
            Key,
            Media,
            PowerCube,
            Mod,
            Weapon,
        ]


class KeyCapsule(Container):
    def __init__(self):
        super(KeyCapsule, self).__init__()
        self._restricted_items = [
            Key,
        ]

    def invcount(self):
        return 1


class Weapon(ItemWithRarity):
    """ """
    def __init__(self):
        super(Weapon, self).__init__()


class Burster(Weapon):
    """ """
    def __init__(self):
        super(Burster, self).__init__()


class Ultrastrike(Weapon):
    """ """
    def __init__(self):
        super(Ultrastrike, self).__init__()


class Virus(Weapon):
    """ """
    def __init__(self):
        super(Virus, self).__init__()


class Ada(Virus):
    """ """
    def __init__(self):
        super(Ada, self).__init__()


class Jarvis(Virus):
    """ """
    def __init__(self):
        super(Jarvis, self).__init__()


class Mod(ItemWithRarity):
    """ """
    def __init__(self):
        super(Mod, self).__init__()


class MultiHack(Mod):
    """ """
    def __init__(self):
        super(MultiHack, self).__init__()


class ForceAmp(Mod):
    """ """
    def __init__(self):
        super(ForceAmp, self).__init__()


class Turret(Mod):
    """ """
    def __init__(self):
        super(Turret, self).__init__()


class Shield(Mod):
    """ """
    def __init__(self):
        super(Shield, self).__init__()


class AxaShield(Shield):
    def __init__(self):
        super(AxaShield, self).__init__()
        self.rarity = VeryRare()


class LinkAmp(Mod):
    """ """
    def __init__(self):
        super(LinkAmp, self).__init__()


class SoftBankUltraLink(LinkAmp):
    def __init__(self):
        super(SoftBankUltraLink, self).__init__()
        self.rarity = VeryRare()


class HeatSink(Mod):
    """ """
    def __init__(self):
        super(HeatSink, self).__init__()


class Inventory(object):
    def __init__(self):
        self._inventory = []
        self._shortcodes = {
            'X': Burster,
            'P': PowerCube,
            'MH': MultiHack,
            'HS': HeatSink,
            'S': Shield,
            'FA': ForceAmp,
            'LA': LinkAmp,
            'T': Turret,
            'R': Resonator,
            'US': Ultrastrike
        }
        self._raritycodes = {
            'C': Common,
            'R': Rare,
            'VR': VeryRare
        }

    @property
    def inventory(self):
        return self._inventory

    @property
    def resonators(self):
        return [x for x in self._inventory if isinstance(x, Resonator)]

    @property
    def weapons(self):
        return [x for x in self._inventory if isinstance(x, Weapon)]

    @property
    def bursters(self):
        return [x for x in self.weapons if isinstance(x, Burster)]

    @property
    def mods(self):
        return [x for x in self._inventory if isinstance(x, Mod)]

    @property
    def powercubes(self):
        return [x for x in self._inventory if isinstance(x, PowerCube)]

    @property
    def capsules(self):
        return {x.guid: x for x in self._inventory if isinstance(x, Capsule)}

    def itemcount(self):
        return reduce(lambda a, b: a+b.itemcount(), self.inventory, 0)

    def invcount(self):
        return reduce(lambda a, b: a+b.invcount(), self.inventory, 0)

    def add(self, item):
        self.inventory.append(item)

    def delete(self, item):
        try:
            for elem in self.inventory:
                try:
                    # identify item by guid and remove it.
                    if elem.guid == item.guid:
                        self.inventory.remove(elem)
                        break
                except AttributeError:
                    if (item.__class__ == elem.__class__ and
                       item.level == elem.level and
                       item.rarity == elem.rarity):
                        self.inventory.remove(elem)
                        break
            else:
                raise RuntimeError(
                    "Could not find item with guid {} in inventory".format(
                        item.guid
                    )
                )
        except ValueError:
            pass

    def find_item(self, guid=None):
        for item in self.inventory:
            try:
                if item.guid == guid:
                    return item
            except AttributeError:
                pass
        return None

    def apply_transaction(self, transaction):
        tx_re = re.compile(
            (
             r'(?P<crdr>CR|DR)\s+(?P<target>\w+)\s+'
             r'(?P<transaction>(?:\d+\s+(?:{})\d\s*)+)'
            ).format('|'.join(x for x in self._shortcodes))
        )
        operations = {
            "CR": "add",
            "DR": "delete"
        }
        for match in tx_re.finditer(transaction):
            target = self
            if match.group("target") != "INV":
                target = self.find_item(guid=match.group("target"))
            self._apply_individual_transaction(
                operations[match.group("crdr")],
                target,
                match.group("transaction")
            )

    def _apply_individual_transaction(self, operation, target, transaction):
        tx_re = re.compile(
            r'(?P<amount>\d+)\s+(?P<shortcode>(?:{}))(?P<level>\d)\s*'.format(
                '|'.join(x for x in self._shortcodes)
            )
        )

        for match in tx_re.finditer(transaction):
            for _ in range(0, int(match.group("amount"))):
                klass = self._shortcodes[match.group("shortcode")]
                item = klass()
                item.level = int(match.group("level"))
                try:
                    item.rarity = self._raritycodes[match.group("rarity")]
                except IndexError:
                    pass
                getattr(target, operation)(item)
