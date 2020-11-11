import cv2
import numpy as np
from time import sleep

l_min = 80
# минимальная ширина прямоугольника
a_min = 80
# минимальная высота прямоугольника

offset = 6
# допустимая ошибка между пикселями

pos_l = 650
# доложение линии счета

delay = 60
# видео FPS(Количество кадров в секунду)

detec = []
car = 0


def p_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


# указывает на середину


cap = cv2.VideoCapture('video.mp4')
subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()
# cоздать фоновый вычитатель

while True:
    # если данные верны, выполнить цикл
    ret, frame1 = cap.read()
    # прочитать видео
    t = float(1 / delay)
    # kоличество кадров в секунду (приравнять к переменной)
    sleep(t)
    # время сна
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    # преобразования цветового пространства
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    # размытие изображений
    img_sub = subtracao.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
    contor, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame1, (25, pos_l), (1200, pos_l), (255, 127, 0), 3)
    for (i, c) in enumerate(contor):
        (x, y, w, h) = cv2.boundingRect(c)
        validate = (w >= l_min) and (h >= a_min)
        if not validate:
            continue
        #     подтверждать линии

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        centro = p_centro(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame1, centro, 4, (0, 0, 255), -1)
        # построить круги в списке координат центра

        for (x, y) in detec:
            if y < (pos_l + offset) and y > (pos_l - offset):
                car += 1
                cv2.line(frame1, (25, pos_l), (1200, pos_l), (0, 127, 255), 3)
                detec.remove((x, y))
                print("car_detected : " + str(car))
    #             этот цикл вычисляет количество машин, которые пересекают введенную нами линию, т.е. удаляет ошибки

    cv2.putText(frame1, "AUTO COUNT : " + str(car), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    # печатать количество car
    cv2.imshow("Video Original", frame1)

    if cv2.waitKey(1) == 7:
        break
#         if 7 окно закрывается

cv2.destroyAllWindows()
cap.release()
# функции
