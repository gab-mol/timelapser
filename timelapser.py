import cv2
import time
from datetime import datetime as dt
import threading
import os
import logging

DIR = os.getcwd()
START_DATE = dt.date((dt.now()))

START_H = str(dt.time(dt.now()))
START_H = "".join(START_H.split(".")[:1]).replace(":", ".")

# Guardar log de ejecución
try:
    LOG_DIR = os.path.join(DIR, "timelapser_logs")
    os.mkdir(LOG_DIR)
except:
    print("LOG_DIR ya existe.")

LNAME = f"log_{START_DATE}_{START_H}.log"
PATH_LOG = os.path.join(LOG_DIR,LNAME)
logging.basicConfig(filename=PATH_LOG,
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger("timelapser_log")
logger.info(f"################  -  {START_DATE}  -  ################")

# Directorios de almacenamiento
try:
    REC_DIR = os.path.join(DIR, "timelapser_records")
    os.mkdir(REC_DIR)
    logger.info(f"Creado dir.: {REC_DIR}")
except:
    msg = f"dir. {REC_DIR} ya existe."
    logger.warning(msg)
    print(msg)

try:
    OUTP_DIR_D = os.path.join(REC_DIR, f"start_{START_DATE}")
    os.mkdir(OUTP_DIR_D)
    logger.info(f"Creado dir. {OUTP_DIR_D}")
except:
    msg = "dir. del dia de hoy ya existe"
    logger.warning(msg)
    print(msg)

try:
    OUTP_DIR_H = os.path.join(OUTP_DIR_D, f"start_{START_H}")
    os.mkdir(OUTP_DIR_H)
    logger.info(f"Creado dir. {OUTP_DIR_H}")
except:
    msg = "dir. para hora de inicio ya existe."
    logger.warning(msg)
    print(msg)


class TimeLapse:
    def __init__(self, interval:float, cam=0):
        '''
        Si está conectada NOBLEX en modo webcam, funciona con `cam=0`.
        de lo contrario, `cam=0` implica que se usará la cámara de la laptop.

        :interval: Intervalo en segundos entre capturas.

        :cam: Número de la cámara que conectará `cv2`. A qué camara se \
        refiere cada número depende de los dispositivos disponibles. \
        Arg. defoult = 0, (la cámara USB pasa a ser 0).
        '''
        # Intervalo en segundos entre fotos
        self.interval = interval
        logger.info(f"intervalo: {interval}s")        

        # thread
        self.running = False
        self.thread = None
        self.stop_event = threading.Event()

        # Inicializa la cámara
        self.cap = cv2.VideoCapture(cam)
        if not self.cap.isOpened():
            msg = "No se puede acceder a la camara"
            logger.critical(msg)
            raise Exception(msg)
        
        # Contador de capturas
        self.counter = 0

    def start(self):
        """Inicia el thread para tomar fotos."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(
                target=self.run, 
                args=(self.stop_event,),
                daemon=True
                )
            self.thread.start()
            msg = "------ Timelapse iniciado... ------"
            logger.info(msg)
            print(msg)
    
    def stop(self):
        """Detiene el thread."""
        if self.running:
            self.running = False
            self.stop_event.set()
            logger.info("------ Timelapse detenido ------")
            self.cap.release()

    def take_photo(self):
        """Toma una foto y la guarda."""
        ret, frame = self.cap.read()
        if ret:
            filename = os.path.join(OUTP_DIR_H,f"{self.counter}.jpg")
            cv2.imwrite(filename, frame)
            logger.info(f"Foto guardada: {filename}")
            self.counter += 1
        else:
            logger.error("Error al capturar la imagen.")

    def run(self,stop_event:threading.Event):
        """Función que corre en segundo plano en el thread."""

        while not stop_event.is_set():
            self.take_photo()
            time.sleep(self.interval)
            if self.stop_event.is_set():
                break

if __name__  == "__main__":
    # Parámetros del timelapse
    photo_interval = 120 # segundos
    camara = 1

    # Hilo principal
    timelapse = TimeLapse(photo_interval, cam=camara)
    print("Intervalo de captura seteado en: ", photo_interval)
    timelapse.start()
    ## ¡¡¡¡
    input("Presionar |Enter| para detener la captura...\n")
    ## !!!!
    logger.warning("# El Usuario solicita detener el programa.")
    print("PEDIDO DETENER:",dt.time(dt.now()))
    timelapse.stop() 
    time.sleep(1)
    print("DETENIDO:",dt.time(dt.now()))