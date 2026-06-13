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
    total_imagenes = len(archivos)
    tiempo_por_cuadro = int(1000 / fps)  # Tiempo en milisegundos por imagen

    # Estados de control
    pausado = False
    indice_actual = 0

    # Dimensiones de la ventana y botones
    ancho_ventana = 800
    alto_ventana = 600
    alto_barra_botones = 80

    # Coordenadas de los botones
    boton_pausa_play = (50, alto_ventana + 10, 200, alto_ventana + 60)   # x1,y1,x2,y2
    boton_repetir = (280, alto_ventana + 10, 430, alto_ventana + 60)
    boton_salir = (510, alto_ventana + 10, 660, alto_ventana + 60)

    # Función para detectar clic en botones
    def detectar_clic(event, x, y, flags, param):
        nonlocal pausado, indice_actual
        if event == cv2.EVENT_LBUTTONDOWN:
            # Botón Pausa / Play
            if boton_pausa_play[0] <= x <= boton_pausa_play[2] and boton_pausa_play[1] <= y <= boton_pausa_play[3]:
                pausado = not pausado
            # Botón Repetir
            elif boton_repetir[0] <= x <= boton_repetir[2] and boton_repetir[1] <= y <= boton_repetir[3]:
                indice_actual = 0
                pausado = False
            # Botón Salir
            elif boton_salir[0] <= x <= boton_salir[2] and boton_salir[1] <= y <= boton_salir[3]:
                cv2.destroyAllWindows()
                os._exit(0)

    # Crear ventana y asignar función de clic
    cv2.namedWindow("Animacion Stop-Motion", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Animacion Stop-Motion", ancho_ventana, alto_ventana + alto_barra_botones)
    cv2.setMouseCallback("Animacion Stop-Motion", detectar_clic)

    print("✅ Controles listos: Play/Pausa, Repetir, Salir")
    print(f"Velocidad: {fps} FPS | Presiona ESC para salir rápido\n")

    while True:
        if not pausado:
            if indice_actual >= total_imagenes:
                indice_actual = total_imagenes - 1  # Se queda en la última imagen al terminar
            # Cargar imagen actual
            ruta_completa = os.path.join(ruta_carpeta, archivos[indice_actual])
            imagen = cv2.imread(ruta_completa)

            if imagen is None:
                indice_actual += 1
                continue

            # Redimensionar imagen para que entre en la ventana
            alto_img, ancho_img = imagen.shape[:2]
            escala = min((ancho_ventana - 40) / ancho_img, (alto_ventana - 40) / alto_img)
            nuevo_ancho = int(ancho_img * escala)
            nuevo_alto = int(alto_img * escala)
            imagen_redim = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))

            # Crear fondo completo
            fondo = 255 * np.ones((alto_ventana + alto_barra_botones, ancho_ventana, 3), dtype=np.uint8)
            # Centrar imagen
            y_offset = (alto_ventana - nuevo_alto) // 2
            x_offset = (ancho_ventana - nuevo_ancho) // 2
            fondo[y_offset:y_offset+nuevo_alto, x_offset:x_offset+nuevo_ancho] = imagen_redim

            # Dibujar botones
            cv2.rectangle(fondo, (boton_pausa_play[0], boton_pausa_play[1]),
                          (boton_pausa_play[2], boton_pausa_play[3]), (0, 150, 0), -1)
            cv2.putText(fondo, "Play/Pausa", (boton_pausa_play[0]+20, boton_pausa_play[1]+35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            cv2.rectangle(fondo, (boton_repetir[0], boton_repetir[1]),
                          (boton_repetir[2], boton_repetir[3]), (0, 100, 200), -1)
            cv2.putText(fondo, "Repetir", (boton_repetir[0]+30, boton_repetir[1]+35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            cv2.rectangle(fondo, (boton_salir[0], boton_salir[1]),
                          (boton_salir[2], boton_salir[3]), (200, 0, 0), -1)
            cv2.putText(fondo, "Salir", (boton_salir[0]+40, boton_salir[1]+35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            # Mostrar todo
            cv2.imshow("Animacion Stop-Motion", fondo)

            if indice_actual < total_imagenes - 1:
                indice_actual += 1

        # Esperar según velocidad
        tecla = cv2.waitKey(tiempo_por_cuadro) & 0xFF
        if tecla == 27:  # Tecla ESC para salir rápido
            break

    cv2.destroyAllWindows()
    print("✅ Reproducción finalizada")

# ------------------- CONFIGURACIÓN -------------------
if __name__ == "__main__":
    import numpy as np  # Importamos numpy para manejar el fondo

    # Tu ruta exacta
    ruta_imagenes = r"F:\COD_269_PROYECTO_B_12_PRINCIPIOS_ ANIMACION_STOP_MOTION\4.posetopose"

   
    velocidad_fps = 12  # Menor = más lento, Mayor = más rápido

    mostrar_imagenes_como_video(ruta_imagenes, fps=velocidad_fps)