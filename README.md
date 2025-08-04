# TODO
* [ ] Añadir un set de objetos revisados, para si ya se encontró el objeto no estar constantemente checándolo
* [ ] Trabajar en el API que interconectará todo
* [ ] Análisis de manipulabilidad
* [ ] Análisis del funcionamiento de la cámara

# Lo que he hecho
* Asegurar la conexión entre la computadora y la cámara RealSense 435i
* Establecer los parámetros necesarios para que la cámara funcione correctamente
* Hacer la montura de la cámara para montarla en el robot
* Definir los objetivos central y particulares de la tesis
* Definir el controlador a usar
* Crear el modelo de segmentación de imágenes y unirlo con la medición de distancias
* Crear la conexión computadora-robot, todo desde un mismo proyecto de Python
* Empezar a definir la conexión entre los dos sistemas


# Notas
## UFACTORY
The robot has callbacks, this should allow me to play with the servo motors like with the haptic touch, implementing my own controller at the end. The project shall be called from the active directory, I'll see if I can do something to include a path dependency to further simplify the project and not have that serious of a `.gitignore`

## RealSense
Only works properly with 10Gb+ USB speeds and cables, finding that out was a pain in the ass. Still need to figure out how to run different threaded models so that I can have one thread for each camera and one for the realsense.

## gRPC API
The thing works wonder, but I'm thinking I could go really far and make this into a fully distributed system if I can just get a hold of some static IP's from the DSTI to open specific ports for communication, it would definitely be interesting and it would allow me to run the 'n' model instead of the 'x' model of YOLO11.

