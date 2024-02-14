Project for detecting blood cells in CBC images.

The solution consists of:

1. Code for building a blood cell detection model based on neural networks with YOLO v.8 architecture.
2. Server-side code that launches the trained model and implements image processing, providing results in file format.
Using deep learning model.

For model training, an archive of images with annotations is used (archive.zip file). The archive contains data divided into three sets (train, val, test). 
The model is trained on the train set with validation on val. The annotation file provides a line-by-line description of objects with class and bounding box information. 
Additionally, information about model training is provided in the data.yaml file (list of classes and datasets for training and validation). 
After model training is complete, a folder \runs\detect\train_i is generated.

Using the file server for detection calls.

The Python code for the file server is located in the CBC_Interface.py file. Upon execution, the code accesses the model.ini file containing paths to:

- Model file
- Folder with source images
- Working directory
- Folder with detection results

The file loads the detection model and starts scanning the folder with source images. 
Upon detecting an image for detection, the program moves it to the working directory and inputs it to the model. 
Based on the results, the model generates a file with the image and bounding boxes, as well as a text file with detection results. 
This text file contains information that the LIS can use to calculate the CBC study result. 
After processing is complete, all files are moved to the results folder, and both the working and source folders are cleared.




Проект для детекции тел крови на изображениях ОАК.

Решение состоит из: 
1. Кода для построения модели детекции тел крови на основе нейронных сетей с архитектурой YOLO v.8
2. Кода файл сервера, который запускает готовую модель и реализует обработку изображений с выдачей результатов в виде файлов.

Использование модели глубокого обучения.

Для обучения модели используется архив изображений с аннтотациями (файл archive.zip). В архиве данные разбиты на три выборки (train, val, test).
Модель обучается на train с валидацией на val. В файле аннотаций приведено построчное описание объектов с указанием класса и bounding box.
Также информация об обучении модели приведена в файле data.yaml (перечень классов и выборки для обучения и валидации).
После завершения обучения сети формируется папка \runs\detect\train_i

Использвание файл сервера для вызова детектирования

Python код для файл сервера находится в файле CBC_Interface.py
После запуска кода на исполнение происходит обращение к ini-файлу model.ini, содержащему пути к:
- файлу модели 
- папке с исходными изображениями
- рабочей папке
- папке с результатами детектирования
Файл загружает модель детектирования и приступает к сканированию папки с исходными изображениями.
После обнаружения изображения для детектирования, программа переносит его в рабочую папку и подает на вход модели.
Модель по результатам работы формирует файл с изображением и bounding boxes, а также текстовый файл с результатами детекции.
Данный текстовый файл содержит информацию, которую ЛИС может использовать для расчета результата ОАК исследования.
После завершения обработки, все файлы переносятся в папку с результатами. При этом рабочая и исходная папки очищаются.

