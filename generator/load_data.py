import csv
import json

from storage.objects import Game, Weapon


def load_csv(game: Game, filename: str):
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file)
        for weapon in reader:
            w_type = weapon['type'].split(' ')

            if len(w_type) > 1:
                character = w_type[0]
                e_type = w_type[1]
            else:
                character = None
                e_type = weapon['type']

            obj = {
                'name': weapon['name'],
                'stats': map(int, (
                    weapon['strength'],
                    weapon['dexterity'],
                    weapon['intelligence'],
                    weapon['faith']
                )),
                'type': e_type,
                'character': character,
            }
            game.weapons.append(Weapon.from_json(obj, game.characters))


def generate_file(filename: str, input_characters: str, *args):
    print('----')
    print(f'Loading {input_characters}')
    game = Game.from_json_file(input_characters)

    for input_weapons in args:
        print(f'Loading {input_weapons}')
        load_csv(game, input_weapons)

    print(f'Writing {filename}')
    with open(filename, 'w') as f:
        json.dump(game.to_json(), f, sort_keys=True)


if __name__ == '__main__':
    generate_file(
        '../base_game.json',
        'base_game_characters_only.json',
        'base_game_characters_weapons.csv',
        'base_game_weapons.csv',
    )
    generate_file(
        '../characters_game.json',
        'characters_game_characters_only.json',
        'characters_game_characters_weapons.csv',
    )
    generate_file(
        '../dark_root_game.json',
        'empty_game.json',
        'dark_root_game_weapons.csv',
    )
    generate_file(
        '../explorer_game.json',
        'empty_game.json',
        'explorer_game_weapons.csv',
    )
    generate_file(
        '../iron_keep_game.json',
        'empty_game.json',
        'iron_keep_game_weapons.csv',
    )
