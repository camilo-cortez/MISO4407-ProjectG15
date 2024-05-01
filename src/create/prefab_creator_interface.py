from enum import Enum

import pygame

import esper
from configurations.shared_config import Color, Position
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator


class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2


def create_text(world: esper.World, txt: str, size: int,
                color: Color, pos: Position, alignment: TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get(
        "assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(
        txt, font, pygame.Color(color.r, color.g, color.b)))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pygame.Vector2(pos.x, pos.y) + origin))
    return text_entity