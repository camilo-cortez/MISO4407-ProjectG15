from configurations.explosion_config import ExplosionConfig
import esper
from src.create.prefab_creator_game import create_explosion
from src.ecs.components.c_hitbox import CHitbox
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_hitbox import CHitbox, get_rect_relative


def system_collision_bullet_enemy(world: esper.World, explosion_cfg: ExplosionConfig, score_entity: int):
    enemy_components = world.get_components(CHitbox, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)
    score_comp = world.component_for_entity(score_entity, CScore)
    c_s: CSurface
    c_he: CHitbox
    c_t: CTransform
    c_te: CTransform
    c_tag_e: CTagEnemy

    for bullet_entity, (c_s, c_t, _) in bullet_components:
        bullet_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for enemy_entity, (c_he, c_te, c_tag_e) in enemy_components:
            enemy_rect = get_rect_relative(c_he.collider, c_te.pos)
            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)
                create_explosion(world, c_te.pos, explosion_cfg)
                score_comp.score += c_tag_e.score_value
