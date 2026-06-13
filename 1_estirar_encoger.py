import cv2
import os

def mostrar_imagenes_como_video(ruta_carpeta, fps=12):
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

    # Verificar carpeta
    if not os.path.isdir(ruta_carpeta):
        print(f"❌ No existe la carpeta: {ruta_carpeta}")
        return

    # Obtener y ordenar imágenes
    archivos = [f for f in os.listdir(ruta_carpeta)
                if f.lower().endswith(extensiones_validas)]
    
    if not archivos:
        print("❌ No hay imágenes en la carpeta")
        return

    archivos.sort()
    print(f"📸 Cargadas {len(archivos)} imágenes. Velocidad: {fps} FPS")
    print("Presiona cualquier tecla para salir...\n")

    # Tiempo que se muestra cada imagen (en milisegundos)
    tiempo_por_cuadro = int(1000 / fps)

    # Mostrar secuencia
    for nombre in archivos:
        ruta_completa = os.path.join(ruta_carpeta, nombre)
        imagen = cv2.imread(ruta_completa)

        if imagen is None:
            continue

        # Redimensionar para ver mejor si es muy grande
        alto, ancho = imagen.shape[:2]
        max_dim = 800
        if max(alto, ancho) > max_dim:
            escala = max_dim / max(alto, ancho)
            imagen = cv2.resize(imagen, (int(ancho * escala), int(alto * escala)))

        cv2.imshow("Animacion Stop-Motion", imagen)

        # Esperar según la velocidad configurada
        if cv2.waitKey(tiempo_por_cuadro) & 0xFF == 27:  # Tecla ESC para salir
            break

    cv2.destroyAllWindows()
    print("✅ Reproducción finalizada")

# ------------------- CONFIGURACIÓN -------------------
if __name__ == "__main__":
    # Tu ruta exacta
    ruta_imagenes = r"F:\COD_269_PROYECTO_B_12_PRINCIPIOS_ ANIMACION_STOP_MOTION\1_estirar"

    # 👇 AQUÍ CONTROLAS LA VELOCIDAD 👇
    # - 5 a 10 FPS: muy lento
    # - 12 a 15 FPS: ideal para stop-motion
    # - 20+ FPS: muy rápido
    velocidad_fps = 8

    mostrar_imagenes_como_video(ruta_imagenes, fps=velocidad_fps)