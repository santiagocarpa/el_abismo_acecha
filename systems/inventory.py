"""
systems/inventory.py - Sistema de Gestión de Inventario para "El Abismo Acecha"
"""

ITEM_DEFINITIONS = {
    "madera": {"nombre": "Madera", "categoria": "recurso", "color": (139, 90, 43), "max_stack": 99},
    "piedra": {"nombre": "Piedra", "categoria": "recurso", "color": (120, 120, 120), "max_stack": 99},
    "hierro": {"nombre": "Hierro", "categoria": "recurso", "color": (210, 140, 60), "max_stack": 99},
    "fogata": {"nombre": "Fogata de Campo", "categoria": "estructura", "color": (255, 140, 30), "max_stack": 20},
    "espada": {"nombre": "Espada de Hierro", "categoria": "arma", "color": (200, 210, 225), "max_stack": 1},
    "muro_madera": {"nombre": "Muro de Madera", "categoria": "estructura", "color": (110, 70, 35), "max_stack": 20},
    "hacha": {"nombre": "Hacha de Madera", "categoria": "herramienta", "color": (160, 110, 60), "max_stack": 1},
    "pico": {"nombre": "Pico de Piedra", "categoria": "herramienta", "color": (100, 130, 140), "max_stack": 1},
    "antorcha": {"nombre": "Antorcha", "categoria": "herramienta", "color": (240, 180, 50), "max_stack": 10},
}

class Inventory:
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        # Cada slot es None o {"item_id": str, "cantidad": int}
        self.slots = [None] * capacity

    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """Añade una cantidad de un ítem buscando primero slots existentes o libres."""
        if item_id not in ITEM_DEFINITIONS:
            return False

        max_stack = ITEM_DEFINITIONS[item_id]["max_stack"]
        rem = quantity

        # 1. Intentar apilar en slots existentes
        for slot in self.slots:
            if slot and slot["item_id"] == item_id:
                space = max_stack - slot["cantidad"]
                if space > 0:
                    to_add = min(rem, space)
                    slot["cantidad"] += to_add
                    rem -= to_add
                    if rem == 0:
                        return True

        # 2. Usar slots vacíos si aún queda remanente
        for i in range(self.capacity):
            if self.slots[i] is None:
                to_add = min(rem, max_stack)
                self.slots[i] = {"item_id": item_id, "cantidad": to_add}
                rem -= to_add
                if rem == 0:
                    return True

        return rem < quantity  # Retorna True si al menos parte fue añadida

    def get_item_count(self, item_id: str) -> int:
        """Retorna la cantidad total de un ítem en todo el inventario."""
        total = 0
        for slot in self.slots:
            if slot and slot["item_id"] == item_id:
                total += slot["cantidad"]
        return total

    def has_materials(self, req_dict: dict) -> bool:
        """Verifica si el inventario posee las cantidades indicadas en el diccionario."""
        for item_id, qty_req in req_dict.items():
            if qty_req > 0 and self.get_item_count(item_id) < qty_req:
                return False
        return True

    def consume_materials(self, req_dict: dict) -> bool:
        """Resta del inventario los materiales requeridos. Retorna True si se consumieron."""
        if not self.has_materials(req_dict):
            return False

        for item_id, qty_req in req_dict.items():
            if qty_req <= 0:
                continue
            rem_to_remove = qty_req
            for i in range(self.capacity):
                slot = self.slots[i]
                if slot and slot["item_id"] == item_id:
                    if slot["cantidad"] > rem_to_remove:
                        slot["cantidad"] -= rem_to_remove
                        rem_to_remove = 0
                        break
                    else:
                        rem_to_remove -= slot["cantidad"]
                        self.slots[i] = None
                        if rem_to_remove == 0:
                            break
        return True

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remueve una cantidad específica de un ítem."""
        return self.consume_materials({item_id: quantity})
