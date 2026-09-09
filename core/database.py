"""
core/database.py - Capa de Persistencia y SQLite DAO para "El Abismo Acecha"
"""

import sqlite3
import os
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Crea las tablas iniciales si no existen y siembra datos iniciales."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Tabla Partida
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS partida (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_partida TEXT NOT NULL,
                pos_x REAL NOT NULL DEFAULT 600.0,
                pos_y REAL NOT NULL DEFAULT 600.0,
                salud_actual INTEGER NOT NULL DEFAULT 100,
                salud_maxima INTEGER NOT NULL DEFAULT 100,
                stamina_actual REAL NOT NULL DEFAULT 100.0,
                dia_actual INTEGER NOT NULL DEFAULT 1,
                tiempo_dia REAL NOT NULL DEFAULT 0.0,
                fecha_guardado DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 2. Tabla Inventario
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                partida_id INTEGER NOT NULL,
                slot_index INTEGER NOT NULL,
                item_id TEXT NOT NULL,
                cantidad INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (partida_id) REFERENCES partida(id) ON DELETE CASCADE
            );
            """)

            # 3. Tabla Recetas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS recetas (
                recipe_id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                item_resultado TEXT NOT NULL,
                cantidad_resultado INTEGER NOT NULL DEFAULT 1,
                ingrediente_1 TEXT NOT NULL,
                cant_ingrediente_1 INTEGER NOT NULL,
                ingrediente_2 TEXT,
                cant_ingrediente_2 INTEGER DEFAULT 0
            );
            """)

            # 4. Tabla Notas (Lore)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                nota_id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                pos_x REAL NOT NULL,
                pos_y REAL NOT NULL,
                encontrada INTEGER NOT NULL DEFAULT 0
            );
            """)

            conn.commit()

        self._seed_default_data()

    def _seed_default_data(self):
        """Siembra recetas iniciales y notas en la base de datos."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Insertar Recetas por defecto
            cursor.execute("SELECT COUNT(*) FROM recetas")
            if cursor.fetchone()[0] == 0:
                recetas_iniciales = [
                    ('rec_hacha', 'Hacha de Madera', 'herramienta', 'hacha', 1, 'madera', 5, 'piedra', 2),
                    ('rec_pico', 'Pico de Piedra', 'herramienta', 'pico', 1, 'madera', 3, 'piedra', 5),
                    ('rec_antorcha', 'Antorcha', 'herramienta', 'antorcha', 1, 'madera', 2, 'hierro', 1),
                    ('rec_espada', 'Espada de Hierro', 'arma', 'espada', 1, 'madera', 2, 'hierro', 4),
                    ('rec_muro', 'Muro de Madera', 'estructura', 'muro_madera', 1, 'madera', 4, None, 0),
                    ('rec_fogata', 'Fogata de Campo', 'estructura', 'fogata', 1, 'madera', 6, 'piedra', 4)
                ]
                cursor.executemany("""
                INSERT INTO recetas (recipe_id, nombre, categoria, item_resultado, cantidad_resultado, 
                                     ingrediente_1, cant_ingrediente_1, ingrediente_2, cant_ingrediente_2)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, recetas_iniciales)

            # Insertar Notas por defecto
            cursor.execute("SELECT COUNT(*) FROM notas")
            if cursor.fetchone()[0] == 0:
                notas_iniciales = [
                    ("Diario de la Expedición - Día 1", 
                     "Desperté rodeado de niebla. Los árboles parecen susurrar nombres que no reconozco. El refugio debe ser construido antes del anochecer.", 
                     500.0, 500.0, 0),
                    ("Nota Ensangrentada", 
                     "La luz las ahuyenta... No dejes que la fogata se apague cuando caiga la negrura de medianoche.", 
                     1200.0, 800.0, 0),
                    ("Fragmento del Investigador", 
                     "Las sombras no son monstruos ordinarios. Emergen del núcleo del abismo. No hay mapa que muestre este lugar.", 
                     1800.0, 1400.0, 0)
                ]
                cursor.executemany("""
                INSERT INTO notas (titulo, contenido, pos_x, pos_y, encontrada)
                VALUES (?, ?, ?, ?, ?)
                """, notas_iniciales)

            conn.commit()

    def crear_nueva_partida(self, nombre="Superviviente"):
        """Crea un nuevo registro de partida e inicializa su inventario básico."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO partida (nombre_partida, pos_x, pos_y, salud_actual, salud_maxima, stamina_actual, dia_actual, tiempo_dia)
            VALUES (?, 600.0, 600.0, 100, 100, 100.0, 1, 0.0)
            """, (nombre,))
            partida_id = cursor.lastrowid

            # Inventario inicial: 5 Madera, 2 Piedras
            cursor.execute("INSERT INTO inventario (partida_id, slot_index, item_id, cantidad) VALUES (?, 0, 'madera', 5)", (partida_id,))
            cursor.execute("INSERT INTO inventario (partida_id, slot_index, item_id, cantidad) VALUES (?, 1, 'piedra', 2)", (partida_id,))
            conn.commit()
            return partida_id

    def cargar_partida(self, partida_id):
        """Devuelve los datos de la partida especificada."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM partida WHERE id = ?", (partida_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def obtener_partidas(self):
        """Devuelve la lista de partidas guardadas."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM partida ORDER BY fecha_guardado DESC")
            return [dict(row) for row in cursor.fetchall()]

    def obtener_recetas(self):
        """Devuelve todas las recetas de crafteo."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recetas")
            return [dict(row) for row in cursor.fetchall()]

    def obtener_notas(self):
        """Devuelve todas las notas narrativas."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notas")
            return [dict(row) for row in cursor.fetchall()]
