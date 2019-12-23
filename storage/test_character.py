from storage.objects import Game, GameConfig


class TestCharacter:

    def test_herald_souls_per_weapon(self):
        cfg = GameConfig.normal_game()
        game = Game.from_json_file('ex_base_game.json')

        herald = game.get_character('herald')

        weapon_cost = {
            w.name: herald.need_souls(w, cfg)
            for w in game.weapons
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
        game = Game.from_json_file('ex_base_game.json')

        warrior = game.get_character('warrior')

        weapon_cost = {
            w.name: warrior.need_souls(w, cfg)
            for w in game.weapons
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
