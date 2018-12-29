# Система распознавания лиц

## Введение

В последнее время системы распознавания лиц используются все шире, область применения этой технологии поистине огромна: от обычных селфи-дронов до дронов-полицейских. Ее интеграция в различные устройства проводится повсеместно. Сам процесс распознавания реально завораживает, и это сподвигло меня сделать проект связанный именно с этим.  Целью моего стажерского проекта является создание простой open source-ной системы распознавания лиц с квадрокоптера Клевер.

## Разработка

Первой задачей было найти алгоритм самого распознавания. В качестве пути решения проблемы было выбрано использовать [готовое API для Python](https://github.com/ageitgey/face_recognition). Данное API сочетает в себе ряд преимуществ: скорость и точность распознавания, а также простота использования.

## Установка

Для начала нужно установить все необходимые библиотеки:

```
pip install face_recognition
pip install opencv-python
```
Затем достаточно скачать сам скрипт из репозитория:

```
git clone https://github.com/mmkuznecov/face_recognition_from_clever.git
```
## Объяснение кода
Подключаем библиотеки:

```python
import face_recognition
import cv2
import os
import urllib.request
import numpy as np
```
Создаем список кодировок изображений и список имен:

```python
faces_images=[]
for i in os.listdir('faces/'):
    faces_images.append(face_recognition.load_image_file('faces/'+i))
known_face_encodings=[]
for i in faces_images:
    known_face_encodings.append(face_recognition.face_encodings(i)[0])
known_face_names=[]
for i in os.listdir('faces/'):
    i=i.split('.')[0]
    known_face_names.append(i)
```
***Дополнение: все изображения хранятся в папке faces в формате name.jpg***

<img src="https://github.com/mmkuznecov/face_recognition_from_clever/blob/master/files/screen.jpg" width="50%">
<img src="https://github.com/mmkuznecov/face_recognition_from_clever/blob/master/faces/Mikhail.jpg" width="30%">
<img src="https://github.com/mmkuznecov/face_recognition_from_clever/blob/master/faces/Timofey.jpg" width="30%">

Инициализируем некоторые переменные:

```python
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
```
Берем изображение с сервера и преобразуем его в cv2 формат:

```python
req = urllib.request.urlopen('http://192.168.11.1:8080/snapshot?topic=/main_camera/image_raw')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
frame = cv2.imdecode(arr, -1)
```
Объяснение дальнейшего кода можно найти на github’е используемого API в комментариях к [следующему скрипту](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py)

TODO: Иллюстрации
