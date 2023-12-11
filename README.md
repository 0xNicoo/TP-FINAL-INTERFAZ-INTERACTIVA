## Tablero de dibujo con deteccion de manos

Un tablero para dibujar utilizando las manos, mediante una camara se detecta la posicion y movimiento de manos.

Se utilizo:
- Mediapipe para el reconocimiento de manos
- OpenCV para la toma de datos (video de camara)
- Pyglet para armar el tablero y dibujar

### Installation

Instalacion de dependencias y paquetes
```
pip install mediapipe opencv-python numpy
pip install --upgrade --user pyglet      
```

### Run project 
```
python main.py
```