from storage.objects import Deck, GameConfig


class TestCharacter:

    def test_herald_souls_per_weapon(self):
        cfg = GameConfig.normal_game()
        game = Deck.from_json_file('../test_data/ex_base_game.json')

        herald = game.characters.get('herald')

        weapon_cost = {
            n: herald.need_souls(w, cfg)
            for n, w in game.weapons.items()
        }
        assert weapon_cost == {
            'cathedral knight armour': 8,
            "tiny being's ring": 2,
            'replenishment': 6,
            'golden wing crest shield': 12,
            'bountiful light': 14,
            'antiquated robes': 8,
            'avelyn': 28,
            'black armour': 12,
            'blessed gem': 6,
        }

    def test_warrior_souls_per_weapon(self):
        cfg = GameConfig.normal_game()
        game = Deck.from_json_file('../test_data/ex_base_game.json')

        warrior = game.characters.get('warrior')

        weapon_cost = {
            n: warrior.need_souls(w, cfg)
            for n, w in game.weapons.items()
        }
        assert weapon_cost == {
            'cathedral knight armour': None,
            "tiny being's ring": None,
            'replenishment': None,
            'golden wing crest shield': None,
            'bountiful light': None,
            'antiquated robes': 8,
            'avelyn': 20,
            'black armour': 12,
            'blessed gem': 6,
        }
