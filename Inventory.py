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

    @property
    def resonators(self):
        return [x for x in self._contents if isinstance(x, Resonator)]

    @property
    def weapons(self):
        return [x for x in self._contents if isinstance(x, Weapon)]

    @property
    def bursters(self):
        return [x for x in self.weapons if isinstance(x, Burster)]

    @property
    def mods(self):
        return [x for x in self._inventory if isinstance(x, Mod)]

    @property
    def powercubes(self):
        return [x for x in self._inventory if isinstance(x, PowerCube)]

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


class Transaction(object):
    def __init__(self):
        self._transaction = None

    def __call__(self, target):
        pass


class Inventory(object):
    def __init__(self):
        self._inventory = []
        self._staged_transactions = []
        self._shortcodes = {
            "level_items": {
                'X': Burster,
                'P': PowerCube,
                'R': Resonator,
                'US': Ultrastrike
            },
            "nolevel_items": {
                'MH': MultiHack,
                'HS': HeatSink,
                'S': Shield,
                'FA': ForceAmp,
                'LA': LinkAmp,
                'T': Turret,
            }
        }
        self._raritycodes = {
            'C': Common,
            'R': Rare,
            'VR': VeryRare
        }

    def __setattr__(self, name, val):
        if name in ("_staged_transactions",
                    "_inventory",
                    "_shortcodes",
                    "_raritycodes"):
            self.__dict__[name] = val
        if name in ("staged_transactions", "inventory"):
            realname = "_{}".format(name)
            self.__dict__[realname] = val

    def __getattr__(self, name):
        property_map_lists = {
            "resonators": Resonator,
            "weapons": Weapon,
            "bursters": Burster,
            "mods": Mod,
            "powercubes": PowerCube,
            "shields": Shield,
        }
        property_map_dicts = {
            "capsules": Capsule
        }
        if name in self.__dict__:
            return self.__dict__[name]
        if name in ("staged_transactions", "inventory"):
            try:
                realname = "_{}".format(name)
                return self.__dict__[realname]
            except KeyError:
                raise AttributeError(
                    "Could not find attribute {} ({}) on {}".format(
                        name,
                        realname,
                        type(self).__name__
                    )
                )
        if name in property_map_lists:
            return [
                x for x in self.inventory
                if isinstance(x, property_map_lists[name])
            ]
        if name in property_map_dicts:
            return {
                x.guid: x for x in self.inventory
                if isinstance(x, property_map_dicts[name])
            }
        raise AttributeError(
            "No attribute {} on {}".format(name, type(self).__name__)
        )

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

    def stage_transaction(self, transaction):
        self.staged_transactions.append(transaction)

    def apply_staged_transactions(self):
        for transaction in self.staged_transactions:
            self.apply_transaction(transaction)

    def apply_transaction(self, transaction):
        tx_re = re.compile(
            (
             r'(?P<crdr>CR|DR)\s+(?P<target>\w+)\s+'
             r'(?P<transaction>(?:\d+\s+\w+\d?\s*)+)'
            )
        )
        operations = {
            "CR": "add",
            "DR": "delete"
        }
        print "Applying transactions from {}".format(transaction)
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
            (
                r'(?P<amount>\d+)\s+'
                r'(?:'
                r'(?P<lshortcode>(?:{}))(?P<level>\d)|'
                r'(?P<rarity>{})(?P<nlshortcode>(?:{}))'
                r')\s*'
            ).format(
                '|'.join(x for x in self._shortcodes["level_items"]),
                '|'.join(x for x in self._raritycodes),
                '|'.join(x for x in self._shortcodes["nolevel_items"])
            )
        )

        print "Searching for matches in {}".format(transaction)
        for match in tx_re.finditer(transaction):
            for _ in range(0, int(match.group("amount"))):
                if match.group("nlshortcode"):
                    shortcode = match.group("nlshortcode")
                    klass = self._shortcodes["nolevel_items"][shortcode]
                    item = klass()

                if match.group("lshortcode"):
                    shortcode = match.group("lshortcode")
                    klass = self._shortcodes["level_items"][shortcode]
                    item = klass()
                    item.level = int(match.group("level"))

                print klass
                try:
                    item.rarity = self._raritycodes[match.group("rarity")]
                except KeyError:
                    pass
                getattr(target, operation)(item)