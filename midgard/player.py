from abc import abstractmethod
from enum import Enum

import pygame
from pygame.sprite import Sprite

from midgard.animation import Animation
from midgard.constants import HeroConstants, MAX_HERO_SPEED, HERO_HEIGHT_CORRECTION
from midgard.sprite import SpriteSheet
from midgard.vector2d import Vector2D


class Direction(Enum):
    LEFT = 1
    RIGHT = 2


# TODO implement state
class PlayerState:
    def __init__(self, player):
        self.player = player
        pass

    @abstractmethod
    def update(self):
        pass

    def _update_x(self, direction):
        if direction == 'right':
            old_pos = self.player.vector.x
            self.player.vector.x += MAX_HERO_SPEED

            if self.player.game.level.collide_with_wall(self.player):
                self.player.vector.x = old_pos

        elif direction == 'left':
            old_pos = self.player.vector.x
            self.player.vector.x -= MAX_HERO_SPEED

            if self.player.game.level.collide_with_wall(self.player):
                self.player.vector.x = old_pos

        self.player.game.level.check_player_enemy_collisions(self.player)


class WalkState(PlayerState):

    def __init__(self, player):
        super().__init__(player)
        pass

    def update(self):
        if self.player.direction_facing == Direction.RIGHT:
            self.player.animation.set_frames('right_walking')
            self._update_x( 'right')

        else:
            self.player.animation.set_frames('left_walking')
            self._update_x( 'left')

        if not self.player.game.level.is_on_platform(self.player):
            self.player.state = MoveDownState(self.player)


class MoveUpState(PlayerState):

    def __init__(self, player):
        super().__init__(player)
        self.player.calculate_jump_height()
        pass

    def update(self):
        if self.player.direction_facing == Direction.RIGHT:
            self.player.animation.set_frames('right_jump')
        else:
            self.player.animation.set_frames('left_jump')

        if self.player.vector.y <= self.player.jump_height:
            self.player.state = MoveDownState(self.player)
        else:
            self.player.vector.y -= self.player.player_constants.jump_speed


class MoveDownState(PlayerState):

    def __init__(self, player):
        super().__init__(player)

    def update(self):
        if self.player.direction_facing == Direction.RIGHT:
            self.player.animation.set_frames('right_jump')
        else:
            self.player.animation.set_frames('left_jump')

        if self.player.game.level.collide_with_platform(self.player):
            self.player.state = IdleState(self.player)

        else:
            self.player.vector.y += self.player.player_constants.jump_speed


class IdleState(PlayerState):

    def __init__(self, player):
        super().__init__(player)
        pass

    def update(self):
        if self.player.direction_facing == Direction.RIGHT:
            self.player.animation.set_frames('right_idle')
        else:
            self.player.animation.set_frames('left_idle')


class AttackState(PlayerState):

    def __init__(self, player):
        super().__init__(player)
        pass

    def update(self):
        if self.player.direction_facing == Direction.RIGHT:
            if self.player.animation.set_frames('right_attack'):
                self.player.state = IdleState(self.player)
        else:
            if self.player.animation.set_frames('left_attack'):
                self.player.state = IdleState(self.player)


class JumpDownWalkState(PlayerState):
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        if self.player.direction_facing == Direction.RIGHT:
            self.player.animation.set_frames('right_jump')
            self._update_x( 'right')
        else:
            self.player.animation.set_frames('left_jump')
            self._update_x( 'left')

        if self.player.game.level.collide_with_platform(self.player):
            self.player.state = WalkState(self.player)
        else:
            self.player.vector.y += self.player.player_constants.jump_speed


class JumpUpWalkState(PlayerState):

    def __init__(self, player):
        super().__init__(player)
        self.player.calculate_jump_height()

    def update(self):
        if self.player.direction_facing == Direction.RIGHT:
            self.player.animation.set_frames('right_jump')
            self._update_x( 'right')
        else:
            self.player.animation.set_frames('left_jump')
            self._update_x( 'left')

        if self.player.vector.y <= self.player.jump_height:
            self.player.state = JumpDownWalkState(self.player)
        else:
            self.player.vector.y -= self.player.player_constants.jump_speed


class MovingAttackState(PlayerState):

    def __init__(self, player):
        super().__init__(player)

    def update(self):

        if self.player.direction_facing == Direction.RIGHT:
            if self.player.animation.set_frames('right_attack'):
                self.player.state = WalkState(self.player)
                return
            self._update_x('right')
        else:
            if self.player.animation.set_frames('left_attack'):
                self.player.state = WalkState(self.player)
                return
            self._update_x('left')

        if not self.player.game.level.is_on_platform(self.player):
            self.player.state = MoveDownState(self.player)


class Player(Sprite):

    def __init__(self, game):
        super().__init__()
        self.jump_height = None
        self.player_constants = HeroConstants()
        self.screen = game.screen
        self.camera = game.camera
        self.screen_rect = self.screen.get_rect()
        self.game = game

        hero_spritesheet = SpriteSheet(self.player_constants.PLAYER_SPRITE_SHEET_LOCATION)
        self.hero_spritesheet_dictionary = {}

        self._load_player_spritesheet(self.hero_spritesheet_dictionary, hero_spritesheet)
        self.hero_image = hero_spritesheet.get_image(130, 8, 30, 30)
        self.rect = self.hero_image.get_rect()

        self.hero_image = pygame.transform.scale(self.hero_image,
                                                 (int(self.rect.width * self.player_constants.HERO_SCALE_SIZE),
                                                  int(self.rect.height * self.player_constants.HERO_SCALE_SIZE)))
        self.rect = self.hero_image.get_rect()

        self.vector = Vector2D()

        self.animation = Animation(self.hero_spritesheet_dictionary, 100)
        self.animation.set_frames('right_idle')

        self.rect.x = self.screen_rect.midleft[0]
        self.rect.y = self.screen_rect.midleft[1]
        self.rect.bottom = self.rect.bottom - 10 * self.player_constants.HERO_SCALE_SIZE
        self.rect.height = self.rect.height - HERO_HEIGHT_CORRECTION

        #self.rect.x = self.rect.x + 10


        print(self.rect.width)


        self.vector.y = float(self.rect.bottom)

        # TODO use state pattern for state of player
        self.state = MoveDownState(self)
        self.direction_facing = Direction.RIGHT

        #TODO move around
        self.damage = 10

        # player inits and sets the stage for with his vect that vect whereever he starts is 0

    def blitme(self):

        self.screen.blit(self.animation.current_animation_with_scale(self.player_constants.HERO_SCALE_SIZE), self.rect)

        # pygame.draw.rect(self.screen, pygame.Color('red'), self.rect)

        # pygame.draw.line(self.screen, pygame.Color('red'), (0, self.rect.bottom),
        #               (100, self.rect.bottom))

    def _load_player_spritesheet(self, hero_spritesheet_dictionary, hero_spritesheet):
        # TODO add second spritesheet jump
        hero_spritesheet_dictionary['left_idle'] = hero_spritesheet.get_images(self.player_constants.right_idle_list,
                                                                               True)
        hero_spritesheet_dictionary['left_jump'] = hero_spritesheet.get_images(self.player_constants.right_jump_list,
                                                                               True)
        hero_spritesheet_dictionary['left_walking'] = hero_spritesheet.get_images(
            self.player_constants.right_walking_list, True)

        hero_spritesheet_dictionary['left_attack'] = hero_spritesheet.get_images(
            self.player_constants.right_attack_list,
            True)

        hero_spritesheet_dictionary['right_idle'] = hero_spritesheet.get_images(self.player_constants.right_idle_list,
                                                                                False)
        hero_spritesheet_dictionary['right_walking'] = hero_spritesheet.get_images(
            self.player_constants.right_walking_list, False)
        hero_spritesheet_dictionary['right_jump'] = hero_spritesheet.get_images(self.player_constants.right_jump_list,
                                                                                False)
        hero_spritesheet_dictionary['right_attack'] = hero_spritesheet.get_images(
            self.player_constants.right_attack_list,
            False)

    def update(self):
        self.state.update()
        self.camera.vector.x = self.vector.x
        self.rect.bottom = self.vector.y
        # print(self.camera.vector.x)

    def calculate_jump_height(self):
        self.jump_height = self.vector.y - self.player_constants.MAX_JUMP_HEIGHT

    def take_damage(self, damage):
        pass

    def change_state(self, key, down):
        print(type(self.state))
        if type(self.state) is IdleState and down:
            if key == pygame.K_LEFT:
                self.direction_facing = Direction.LEFT
                self.state = WalkState(self)

            elif key == pygame.K_RIGHT:
                self.direction_facing = Direction.RIGHT
                self.state = WalkState(self)

            elif key == pygame.K_SPACE:
                self.state = MoveUpState(self)
            elif key == pygame.K_a:
                self.state = AttackState(self)

        elif type(self.state) is WalkState:
            if key == pygame.K_SPACE and down:
                self.state = JumpUpWalkState(self)
            elif key == pygame.K_a and down:
                self.state = MovingAttackState(self)
            elif key == pygame.K_RIGHT and not down:
                self.state = IdleState(self)
            elif key == pygame.K_LEFT and not down:
                self.state = IdleState(self)

        elif type(self.state) is JumpDownWalkState and not down:
            if key == pygame.K_LEFT:
                self.state = MoveDownState(self)
            elif key == pygame.K_RIGHT:
                self.state = MoveDownState(self)

        elif type(self.state) is JumpUpWalkState and not down:
            if key == pygame.K_LEFT:
                self.state = MoveUpState(self)
            elif key == pygame.K_RIGHT:
                self.state = MoveUpState(self)
        elif type(self.state) is MovingAttackState and not down:
            if key == pygame.K_LEFT:
                self.state = AttackState(self)
            elif key == pygame.K_RIGHT:
                self.state = AttackState(self)

