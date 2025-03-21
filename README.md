# TODO
* [ ] Trabajar en el software de reconocimiento de piezas
    * [X] Hacer que las cámaras funcionen síncronamente
    * [ ] Reconocer el punto medio que sería el robot y su alcance máximo
    * [X] Ver si se puede hacer con convolución, evitar IA
* [ ] Empezar a planear el tipo de controlador a usarse
    * Probablemente sea un controlador adaptable, José me vendió la idea
* [ ] Trabajar en el API que interconectará todo
    * Python o C++

# Lo que he hecho
* Asegurar la conexión entre la computadora y la cámara RealSense 435i
* Establecer los parámetros necesarios para que la cámara funcione correctamente
* Hacer la montura de la cámara para montarla en el robot
* Definir los objetivos central y particulares de la tesis

# Notas
## UFACTORY
The robot has callbacks, this should allow me to play with the servo motors like with the haptic touch, implementing my own controller at the end. The project shall be called from the active directory, I'll see if I can do something to include a path dependency to further simplify the project and not have that serious of a `.gitignore`

## RealSense
Only works properly with 10Gb+ USB speeds and cables, finding that out was a pain in the ass. Still need to figure out how to run different threaded models so that I can have one thread for each camera and one for the realsense.
