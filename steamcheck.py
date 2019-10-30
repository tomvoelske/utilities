import os


class Game:

    game_list = []
    drive_dict = {}

    def __init__(self, game_name, dir_path):
        self.game_name = game_name
        self.dir_path = dir_path
        self.drive_letter = self.dir_path[0]
        if self.drive_letter not in self.drive_dict.keys():
            print('Calculating game directory sizes in drive {0}...'.format(self.drive_letter))
            self.drive_dict[self.drive_letter] = {}
        self.dir_size = self.get_size()
        self.drive_dict[self.drive_letter][self.game_name] = self.dir_size
        Game.game_list.append(self)

    def get_size(self):

        total_size = 0
        for dir_path, _, file_names in os.walk(self.dir_path):
            for file in file_names:
                file_path = os.path.join(dir_path, file)
                total_size += os.path.getsize(file_path)
        total_size /= (1000 * 1000 * 1000)  # GB
        total_size = round(total_size, 2)
        return total_size


def main(number_to_display):

    # add drives and/or disable them as you are interested. I could make this with a proper user GUI, but...

    c_drive = r'C:\SteamLibrary\steamapps\common'
    d_drive = r'D:\Program Files (x86)\Steam\steamapps\common'
    e_drive = r'E:\Program Files (x86)\Steam\steamapps\common'
    g_drive = r'G:\SteamLibrary\steamapps\common'

    steam_dir_lists = []

    # disable as you don't want them checked

    steam_dir_lists.append(c_drive)
    steam_dir_lists.append(d_drive)
    steam_dir_lists.append(e_drive)
    steam_dir_lists.append(g_drive)

    for dir_index, steam_dir in enumerate(steam_dir_lists):
        dir_list = os.listdir(steam_dir)
        for game in dir_list:
            dir_path = os.path.join(steam_dir_lists[dir_index], game)
            _ = Game(game, dir_path)

    print('')

    for drive in Game.drive_dict.keys():
        ordered_sizes = descending_sort_drive(Game.drive_dict[drive])
        print('DRIVE {0}:\n'.format(drive))
        output_list = ordered_sizes[:number_to_display]
        for output_game in output_list:
            game_size = Game.drive_dict[drive][output_game]
            if game_size == 0.0:
                break
            print('{0}: {1} GB'.format(output_game, game_size))
        print('')


def descending_sort_drive(drive_dict):
    return sorted(drive_dict, key=drive_dict.get, reverse=True)


if __name__ == '__main__':
    try:
        number_to_display = int(input('Please type how many to display.\n>'))
        main(number_to_display)
    except TypeError:
        print('Invalid value.')
