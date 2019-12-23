import json
from enum import Enum
from typing import List, Optional, Dict

import attr


@attr.s
class GameConfig:
    level_cost: List[int] = attr.ib()
    souls_per_player: int = attr.ib(default=2)

    @classmethod
    def normal_game(cls):
        return cls([0, 2, 4, 8])

    @classmethod
    def campaign_game(cls):
        return cls([0, 4, 8, 16, 20])

    def cost(self, level: int) -> int:
        if level < len(self.level_cost):
            return sum((c for c in self.level_cost[:level + 1]))

    def souls_per_room(self, players: int) -> int:
        return players * self.souls_per_player

    def souls_per_boss(self, spark: int) -> int:
        return spark * self.souls_per_player


class JsonObject:

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_json(cls, obj: Dict, **kwargs) -> 'JsonObject':
        return cls(**obj)

    def to_json(self) -> Dict:
        raise NotImplementedError


@attr.s
class Stats(JsonObject):
    strength: int = attr.ib()
    dexterity: int = attr.ib()
    intelligence: int = attr.ib()
    faith: int = attr.ib()

    def __str__(self):
        return f'(str={self.strength}, dex={self.dexterity}, int={self.intelligence}, fai={self.faith})'

    def __getitem__(self, item: int):
        if item == 0:
            return self.strength
        elif item == 1:
            return self.dexterity
        elif item == 2:
            return self.intelligence
        elif item == 3:
            return self.faith
        raise IndexError(f'No stat for {item}')

    def __next__(self):
        for i in range(0, 4):
            yield self[i]

    @classmethod
    def from_json(cls, obj: List, **kwargs) -> 'Stats':
        return cls(*obj)

    def to_json(self) -> List:
        return [
            self.strength,
            self.dexterity,
            self.intelligence,
            self.faith,
        ]


@attr.s
class Weapon(JsonObject):

    class Type(Enum):
        Weapon = 'weapon'
        Shield = 'shield'
        Armour = 'armour'
        Ring = 'ring'
        Spell = 'spell'
        Upgrade = 'upgrade'

    name: str = attr.ib()
    stats: Stats = attr.ib()
    type: Type = attr.ib()
    level: int = attr.ib()
    character: Optional["Character"] = attr.ib(default=None)

    def __str__(self):
        if self.character:
            character = ' - ' + self.character.name
        else:
            character = ''
        return f'{self.name} - {self.type.value}{character}: {self.stats}'

    @classmethod
    def from_json(cls, obj: Dict, characters: List["Character"] = None) -> 'Weapon':
        w_type = obj.pop('type')
        if w_type[-1] == '+':
            # TODO(tr) count number of + to get the level
            w_type = w_type.replace('+', '')
            level = 1
        else:
            level = 0
        e_type = cls.Type(w_type)
        stats = Stats.from_json(obj.pop('stats'))
        character_name = obj.pop('character', None)
        character = None
        if character_name:
            for c in characters:
                if c.name == character_name:
                    character = c
                    break
            else:
                raise RuntimeError(f'Did not find character {character_name} when loading {obj}')

        return cls(type=e_type, stats=stats, level=level, character=character, **obj)

    def to_json(self) -> Dict:
        def _filter(field: attr.Attribute, _value) -> bool:
            return field.name not in ('type', 'level', 'stats', 'character')

        d = attr.asdict(self, filter=_filter)
        d['stats'] = self.stats.to_json()
        d['type'] = self.type.value
        if self.level > 0:
            d['type'] += '+' * self.level
        if self.character:
            d['character'] = self.character.name
        return d


@attr.s
class Character(JsonObject):
    name: str = attr.ib()
    stats: List[Stats] = attr.ib(default=attr.Factory(list))

    @classmethod
    def from_json(cls, obj: Dict, **kwargs) -> 'Character':
        stats = [
            Stats.from_json(s)
            for s in obj.pop('stats')
        ]
        return cls(stats=stats, **obj)

    def to_json(self) -> Dict:
        d = attr.asdict(self)
        d['stats'] = [
            s.to_json()
            for s in self.stats
        ]
        return d

    def need_souls(self, weapon: Weapon, cfg: GameConfig) -> Optional[int]:
        if weapon.character is not None and weapon.character != self:
            return

        souls = 0
        for i, stat in enumerate(weapon.stats):
            try:
                level = 0
                while self.stats[level][i] < stat:
                    level += 1
            except IndexError:
                return  # Cannot equip that weapon

            s = cfg.cost(level)
            if s is None:
                return  # Cannot equip that weapon
            souls += s

        return souls


@attr.s
class Game(JsonObject):
    characters: List[Character] = attr.ib(default=attr.Factory(list))
    weapons: List[Weapon] = attr.ib(default=attr.Factory(list))

    def get_character(self, name: str) -> Character:
        for c in self.characters:
            if c.name == name:
                return c

    def extend_from_file(self, filename: str):
        with open(filename) as f:
            obj = json.load(f)
            self.characters.extend([
                Character.from_json(c)
                for c in obj['characters']
            ])
            self.weapons.extend([
                Weapon.from_json(w, self.characters)
                for w in obj['weapons']
            ])

    @classmethod
    def from_json(cls, obj: Dict, **kwargs) -> 'Game':
        characters = [
            Character.from_json(c)
            for c in obj.pop('characters')
        ]
        weapons = [
            Weapon.from_json(w, characters)
            for w in obj.pop('weapons')
        ]
        return cls(characters=characters, weapons=weapons)

    @classmethod
    def from_json_file(cls, filename: str) -> 'Game':
        obj = cls()
        obj.extend_from_file(filename)
        return obj

    def to_json(self) -> Dict:
        return {
            'characters': [
                c.to_json()
                for c in self.characters
            ],
            'weapons': [
                w.to_json()
                for w in self.weapons
            ]
        }
