import math

from storage.objects import Game, GameConfig

if __name__ == '__main__':
    import argparse

    possible_games = [
        'characters',
        'dark_root',
        'explorer',
        'iron_keep',
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--campaign-mode', action='store_true',
        help='Use the campaign upgrade cost'
    )
    parser.add_argument(
        '--players', '-p', type=int, choices=range(1, 5), default=4,
        help='Number of players (from 1 to 4)'
    )
    parser.add_argument(
        '--game', '-g', nargs='+', metavar='GAME', choices=possible_games,
        default=[],
        help=f'Choose the games to load: {", ".join(possible_games)}',
    )
    args = parser.parse_args()

    if args.campaign_mode:
        cfg = GameConfig.campaign_game()
    else:
        cfg = GameConfig.normal_game()

    game = Game.from_json_file('base_game.json')
    for g in args.game:
        game.extend_from_file(f'{g}_game.json')

    print(f'Loaded {len(game.characters)} characters and {len(game.weapons)} weapons')

    souls_per_room = cfg.souls_per_room(args.players)
    for weapon in game.weapons:
        souls_cost = {}
        for character in game.characters:
            v = character.need_souls(weapon, cfg)
            if v:
                souls_cost[character.name] = math.ceil(v / souls_per_room)
            else:
                souls_cost[character.name] = v

        print(f'{weapon}')
        print(f'  => {", ".join((f"{k}: {v} rooms" for k, v in souls_cost.items()))}')
