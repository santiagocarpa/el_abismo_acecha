"""
systems/crafting.py - Sistema de Validación y Crafteo de Recetas
"""

from systems.inventory import ITEM_DEFINITIONS

RECIPES = [
    {
        "recipe_id": "rec_fogata",
        "nombre": "Fogata de Campo",
        "categoria": "estructura",
        "resultado": "fogata",
        "cantidad_resultado": 1,
        "ingredientes": {"madera": 4, "piedra": 2},
        "descripcion": "Emite un halo de luz que ahuyenta a las sombras nocturnas."
    },
    {
        "recipe_id": "rec_espada",
        "nombre": "Espada de Hierro",
        "categoria": "arma",
        "resultado": "espada",
        "cantidad_resultado": 1,
        "ingredientes": {"madera": 3, "hierro": 4},
        "descripcion": "Arma filosa. Aumenta el daño de ataque contra las sombras a 35 HP."
    },
    {
        "recipe_id": "rec_muro",
        "nombre": "Muro de Madera",
        "categoria": "estructura",
        "resultado": "muro_madera",
        "cantidad_resultado": 1,
        "ingredientes": {"madera": 5},
        "descripcion": "Barrera física resistente para frenar a las criaturas oscuras."
    },
    {
        "recipe_id": "rec_hacha",
        "nombre": "Hacha de Madera",
        "categoria": "herramienta",
        "resultado": "hacha",
        "cantidad_resultado": 1,
        "ingredientes": {"madera": 4, "piedra": 2},
        "descripcion": "Herramienta básica para talar árboles con mayor rapidez."
    },
    {
        "recipe_id": "rec_pico",
        "nombre": "Pico de Piedra",
        "categoria": "herramienta",
        "resultado": "pico",
        "cantidad_resultado": 1,
        "ingredientes": {"madera": 3, "piedra": 5},
        "descripcion": "Permite picar rocas y vetas de hierro de manera eficiente."
    },
    {
        "recipe_id": "rec_antorcha",
        "nombre": "Antorcha",
        "categoria": "herramienta",
        "resultado": "antorcha",
        "cantidad_resultado": 1,
        "ingredientes": {"madera": 2, "hierro": 1},
        "descripcion": "Proporciona luz móvil para llevar en la oscuridad."
    },
]

class CraftingSystem:
    @staticmethod
    def get_recipes():
        return RECIPES

    @staticmethod
    def can_craft(recipe: dict, inventory) -> bool:
        """Verifica si el inventario posee los materiales requeridos para la receta."""
        return inventory.has_materials(recipe["ingredientes"])

    @staticmethod
    def craft(recipe: dict, inventory) -> bool:
        """
        Ejecuta el crafteo:
        1. Verifica que existan materiales suficientes.
        2. Resta los materiales requeridos del inventario.
        3. Añade el ítem resultante al inventario.
        """
        if not CraftingSystem.can_craft(recipe, inventory):
            return False

        # Consumir materiales requeridos
        consumed = inventory.consume_materials(recipe["ingredientes"])
        if consumed:
            # Añadir resultado
            inventory.add_item(recipe["resultado"], recipe["cantidad_resultado"])
            return True
        return False
