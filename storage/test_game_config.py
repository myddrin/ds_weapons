from storage.objects import GameConfig


class TestGameConfig:

    def test_normal_game(self):
        cfg = GameConfig.normal_game()

        assert cfg.cost(0) == 0
        assert cfg.cost(1) == 2
        assert cfg.cost(2) == 2 + 4
        assert cfg.cost(3) == 2 + 4 + 8
        assert cfg.cost(4) is None

    def test_campaign_game(self):
        cfg = GameConfig.campaign_game()

        assert cfg.cost(0) == 0
        assert cfg.cost(1) == 4
        assert cfg.cost(2) == 4 + 8
        assert cfg.cost(3) == 4 + 8 + 16
        assert cfg.cost(4) == 4 + 8 + 16 + 20
        assert cfg.cost(5) is None
