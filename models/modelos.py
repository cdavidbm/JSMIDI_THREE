import math
import os
import random

import bpy
from mathutils import Vector


def clear_scene():
    """Limpia toda la escena de Blender"""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Limpiar materiales y texturas
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


def create_base_mesh():
    """Crea la malla base con topología común para todos los modelos"""
    # Crear una esfera base con subdivisiones específicas
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1.0,
        enter_editmode=False,
        align="WORLD",
        location=(0, 0, 0),
        segments=16,  # Controla tanto las divisiones horizontales como verticales
    )

    base_obj = bpy.context.active_object
    base_obj.name = "CreatureBase"

    # Entrar en modo edición para refinar la malla
    bpy.context.view_layer.objects.active = base_obj
    bpy.ops.object.mode_set(mode="EDIT")

    # Aplicar subdivisión suave para más geometría
    bpy.ops.mesh.subdivide(number_cuts=1, smoothness=0.5)

    # Salir del modo edición
    bpy.ops.object.mode_set(mode="OBJECT")

    return base_obj


def get_vertex_positions_jellyfish(mesh, time_factor=0):
    """Genera posiciones de vértices para forma de medusa"""
    vertices = []

    for i, vert in enumerate(mesh.vertices):
        pos = vert.co.copy()

        # Forma de campana de medusa
        height_factor = pos.z + 1.0  # Normalizar altura
        if height_factor > 1.0:
            # Parte superior redondeada
            dome_factor = math.sin(height_factor * math.pi * 0.5)
            pos.x *= dome_factor * 1.2
            pos.y *= dome_factor * 1.2
            pos.z *= 0.8
        else:
            # Tentáculos ondulantes
            wave = math.sin(time_factor + i * 0.3) * 0.3
            pos.x *= 0.3 + wave
            pos.y *= 0.3 + wave
            pos.z -= abs(pos.z) * 1.5

        vertices.append(pos)

    return vertices


def get_vertex_positions_coral(mesh, time_factor=0):
    """Genera posiciones de vértices para forma de coral"""
    vertices = []

    for i, vert in enumerate(mesh.vertices):
        pos = vert.co.copy()

        # Estructura ramificada de coral
        branch_factor = math.sin(pos.x * 3) * math.cos(pos.y * 3) * 0.4
        growth_wave = math.sin(time_factor + i * 0.2) * 0.1

        pos.x += branch_factor + growth_wave
        pos.y += branch_factor * 0.7 + growth_wave
        pos.z *= 1.5 + abs(branch_factor)

        vertices.append(pos)

    return vertices


def get_vertex_positions_octopus(mesh, time_factor=0):
    """Genera posiciones de vértices para forma de pulpo"""
    vertices = []

    for i, vert in enumerate(mesh.vertices):
        pos = vert.co.copy()

        # Cuerpo central y tentáculos
        if pos.z > 0:
            # Cabeza del pulpo
            pos *= 1.3
        else:
            # Tentáculos serpenteantes
            tentacle_wave = math.sin(time_factor * 2 + i * 0.5) * 0.4
            spiral = math.cos(i * 0.8) * 0.3

            pos.x += tentacle_wave + spiral
            pos.y += tentacle_wave * 0.8 - spiral
            pos.z *= 2.0

        vertices.append(pos)

    return vertices


def get_vertex_positions_flower(mesh, time_factor=0):
    """Genera posiciones de vértices para forma de flor"""
    vertices = []

    for i, vert in enumerate(mesh.vertices):
        pos = vert.co.copy()

        # Pétalos radiantes
        distance = math.sqrt(pos.x**2 + pos.y**2)
        angle = math.atan2(pos.y, pos.x)

        # Crear forma de pétalos
        petal_factor = math.sin(angle * 6) * 0.5 + 1.0  # 6 pétalos
        bloom_wave = math.sin(time_factor + distance * 2) * 0.2

        pos.x *= petal_factor + bloom_wave
        pos.y *= petal_factor + bloom_wave
        pos.z *= 0.3 + abs(math.sin(angle * 6)) * 0.5

        vertices.append(pos)

    return vertices


def get_vertex_positions_cactus(mesh, time_factor=0):
    """Genera posiciones de vértices para forma de cactus"""
    vertices = []

    for i, vert in enumerate(mesh.vertices):
        pos = vert.co.copy()

        # Estructura espinosa y cilíndrica
        spine_factor = math.sin(pos.z * 8) * math.cos(pos.x * 6) * 0.3
        growth_pulse = math.sin(time_factor * 0.5 + i * 0.1) * 0.1

        # Forma cilíndrica con espinas
        pos.x *= 0.7 + abs(spine_factor)
        pos.y *= 0.7 + abs(spine_factor)
        pos.z *= 1.8 + growth_pulse

        # Añadir protuberancias espinosas
        if random.random() > 0.7:
            spike_dir = Vector((pos.x, pos.y, 0)).normalized() * spine_factor
            pos += spike_dir

        vertices.append(pos)

    return vertices


def get_vertex_positions_fern(mesh, time_factor=0):
    """Genera posiciones de vértices para forma de helecho"""
    vertices = []

    for i, vert in enumerate(mesh.vertices):
        pos = vert.co.copy()

        # Hojas arqueadas y frondosas
        frond_curve = math.sin(pos.z * 2) * 0.8
        leaf_wave = math.sin(time_factor + pos.x * 3) * 0.3

        # Curvatura natural del helecho
        pos.x = pos.x * (1.5 + frond_curve) + leaf_wave
        pos.y = pos.y * (0.8 + abs(frond_curve)) + leaf_wave * 0.5
        pos.z *= 1.2

        # Movimiento suave como en el viento
        wind_sway = math.sin(time_factor * 1.5 + pos.z) * 0.2
        pos.x += wind_sway

        vertices.append(pos)

    return vertices


def create_shape_keys(obj):
    """Crea los Shape Keys para todos los modelos"""
    # Asegurar que el objeto esté activo
    bpy.context.view_layer.objects.active = obj

    # Crear la clave base
    obj.shape_key_add(name="Basis")

    mesh = obj.data

    # Definir los modelos y sus funciones
    models = [
        ("Jellyfish", get_vertex_positions_jellyfish),
        ("Coral", get_vertex_positions_coral),
        ("Octopus", get_vertex_positions_octopus),
        ("Flower", get_vertex_positions_flower),
        ("Cactus", get_vertex_positions_cactus),
        ("Fern", get_vertex_positions_fern),
    ]

    # Crear Shape Keys para cada modelo
    for name, position_func in models:
        shape_key = obj.shape_key_add(name=name)
        new_positions = position_func(mesh)

        # Aplicar las nuevas posiciones
        for i, pos in enumerate(new_positions):
            if i < len(shape_key.data):
                shape_key.data[i].co = pos


def create_animations(obj):
    """Crea animaciones para cada Shape Key"""
    # Limpiar animaciones existentes
    obj.animation_data_clear()

    # Crear nueva acción
    action = bpy.data.actions.new(name="ShapeKeyAnimations")
    obj.animation_data_create()
    obj.animation_data.action = action

    # Configurar el rango de frames
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 120  # 4 segundos a 30fps

    # Animar cada Shape Key
    shape_keys = obj.data.shape_keys.key_blocks[1:]  # Saltar 'Basis'

    for i, shape_key in enumerate(shape_keys):
        frame_offset = i * 20  # Desfase para cada animación

        # Keyframes para animación en bucle
        frames = [
            1 + frame_offset,
            30 + frame_offset,
            60 + frame_offset,
            90 + frame_offset,
            120,
        ]
        values = [0.0, 1.0, 0.5, 1.0, 0.0]

        for frame, value in zip(frames, values):
            shape_key.value = value
            shape_key.keyframe_insert(data_path="value", frame=frame)

    # Configurar interpolación suave
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = "BEZIER"
                keyframe.handle_left_type = "AUTO"
                keyframe.handle_right_type = "AUTO"


def create_materials():
    """Crea materiales para visualización"""
    materials = []

    # Colores para cada tipo de criatura
    colors = [
        (0.2, 0.6, 0.9, 1.0),  # Azul medusa
        (0.9, 0.4, 0.2, 1.0),  # Naranja coral
        (0.6, 0.2, 0.8, 1.0),  # Púrpura pulpo
        (0.9, 0.7, 0.3, 1.0),  # Amarillo flor
        (0.3, 0.7, 0.2, 1.0),  # Verde cactus
        (0.2, 0.8, 0.4, 1.0),  # Verde helecho
    ]

    names = ["Jellyfish", "Coral", "Octopus", "Flower", "Cactus", "Fern"]

    for i, (color, name) in enumerate(zip(colors, names)):
        mat = bpy.data.materials.new(name=f"Material_{name}")
        mat.use_nodes = True

        # Configurar nodo principled
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if principled:
            principled.inputs[0].default_value = color  # Base Color
            principled.inputs[7].default_value = 0.3  # Roughness
            principled.inputs[15].default_value = (
                0.8  # Transmission (para transparencia)
            )

        materials.append(mat)

    return materials[0]  # Retornar el primer material


def setup_scene():
    """Configura la escena con iluminación y cámara"""
    # Añadir luz
    bpy.ops.object.light_add(type="SUN", location=(2, 2, 5))
    sun = bpy.context.active_object
    sun.data.energy = 3.0

    # Configurar cámara
    bpy.ops.object.camera_add(location=(4, -4, 3))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)  # Apuntar hacia el origen


def main():
    """Función principal que ejecuta todo el proceso"""
    print("Iniciando generación de modelos con Shape Keys...")

    # Limpiar escena
    clear_scene()

    # Crear malla base
    base_obj = create_base_mesh()

    # Crear Shape Keys
    create_shape_keys(base_obj)

    # Crear animaciones
    create_animations(base_obj)

    # Aplicar material
    material = create_materials()
    base_obj.data.materials.append(material)

    # Configurar escena
    setup_scene()

    # Configurar viewport para mejor visualización
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"
                    break

    print("¡Generación completada!")
    print("Shape Keys creados:")
    if base_obj.data.shape_keys:
        for key in base_obj.data.shape_keys.key_blocks:
            print(f"  - {key.name}")

    # Guardar archivo
    try:
        documents_path = os.path.expanduser("~/Documents")
        blend_file_path = os.path.join(documents_path, "morphing_creatures.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
        print(f"Archivo guardado como: {blend_file_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        # Intentar guardar en la carpeta del script
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            blend_file_path = os.path.join(script_dir, "morphing_creatures.blend")
            bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
            print(f"Archivo guardado como: {blend_file_path}")
        except Exception as e:
            print(f"No se pudo guardar el archivo: {e}")


# Ejecutar el script
if __name__ == "__main__":
    main()
