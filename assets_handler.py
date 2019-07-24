import os
import pygame
from typing import Tuple
import constants


class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(source=self.sprite_sheet,
                   dest=(0, 0), area=(x, y, width, height))
        image.set_colorkey(constants.VIOLET) # Violet as the transparent color
        return image


class Image(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data: Tuple, assets_path: str) -> None:
        super().__init__()
        sprite_sheet = SpriteSheet(assets_path)
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3],)
        self.rect = self.image.get_rect()


class Numbers:
    nums_path = os.path.join("assets", "nums.png")

    # Large numbers needed for a live score, added to a list
    num_0 = (4, 61, 24, 33)
    num_1 = (7, 122, 24, 33)
    num_2 = (7, 178, 24, 33)
    num_3 = (7, 233, 24, 33)
    num_4 = (0, 312, 24, 33)
    num_5 = (0, 353, 24, 33)
    num_6 = (2, 0, 24, 33)
    num_7 = (36, 0, 24, 33)
    num_8 = (71, 0, 24, 33)
    num_9 = (105, 0, 24, 33)
    num_list = [num_0, num_1, num_2, num_3, num_4,
                num_5, num_6, num_7, num_8, num_9]

    # Small numbers needed for a score in the summary. added to a list
    s_num_0 = (356, 0, 22, 25)
    s_num_1 = (2, 273, 22, 24)
    s_num_2 = (137, 0, 22, 25)
    s_num_3 = (164, 0, 22, 25)
    s_num_4 = (191, 0, 22, 25)
    s_num_5 = (219, 0, 22, 25)
    s_num_6 = (247, 0, 22, 25)
    s_num_7 = (274, 0, 22, 25)
    s_num_8 = (302, 0, 22, 25)
    s_num_9 = (329, 0, 22, 25)
    small_num_list = [s_num_0, s_num_1, s_num_2, s_num_3, s_num_4,
                      s_num_5, s_num_6, s_num_7, s_num_8, s_num_9]

    def __init__(self, large):
        """ Constructor with a boolean value expected to determine
        if large or small numbers are to be used. """

        self.score = {}
        self.copy_score = {}
        self.large = large

        if self.large:
            for i in range(len(self.num_list)):
                self.score[str(i)] = Image(self.num_list[i], self.nums_path)
                self.copy_score[str(i)] = Image(self.num_list[i], self.nums_path)
        else:
            for i in range(len(self.small_num_list)):
                self.score[str(i)] = Image(self.small_num_list[i], self.nums_path)
                self.copy_score[str(i)] = Image(self.small_num_list[i], self.nums_path)

    def number(self, num):
        return self.score[num]

    # Create a new asset, so a number with the same digits could be displayed
    def new_number(self, num):
        return self.copy_score[num]

    def generate_score(self, score_sprites, score):

        score_sprites.empty()  # Clear a score sprite

        str_score = str(score)
        s = self.number(str_score[0])

        # Set a score's position depending on its size
        if self.large:
            pos_x = constants.SCREEN_WIDTH / 2 - 10
            pos_y = 10
        else:
            pos_x = 553
            pos_y = 205

        s.rect.x = pos_x
        s.rect.y = pos_y

        score_sprites.add(s)

        # If a score has more digits than one, add the second
        # and further digits to the right
        if len(str_score) > 1:
            # If a number contains same digits, create new assets
            for i in range(1, len(str_score)):
                if str_score[i] == str_score[0] or str_score[i] == str_score[i - 1]:
                    s = self.new_number(str_score[i])
                else:
                    s = self.number(str_score[i])
                pos_x += s.rect.width + 2
                s.rect.x = pos_x
                s.rect.y = pos_y
                score_sprites.add(s)

        return score_sprites
