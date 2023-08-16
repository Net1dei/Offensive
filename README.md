# Прочитайте перед использованием
В коде остался наш тестовый логин и пароль с сайта, к которому мы обращаемся, чтобы генерировать картинку. На нём ограниченной кол-во генераций, поэтому если вы хотите продолжить им пользоваться, зарегестрируйтесь и подтвердите код на почте, после это введите свой логин и пароль в файле [parametres.py](src/parameters.py). 



Чтобы загрузить картинку надо: 
1. Нажать кнопку: "Выбрать файлы", справа будет отображаться имя выбранного вами файла.
2. Под кнопкой "Перегенерировать фотографии" есть поле для ввода текста, туда пока можно ввести только английский текст, описывающий фон (модель иногда может не сгенерировать то, что вы хотели, поэтому, чем подробнее описан запрос, тем схоже будет картинка с вашей фантазией).
3. Нажимаете на кнопку "Перегенерировать фотографии" и ожидаете, в это время пока можно будет делать другии функции сайта.
(Кнопка "Загрузить" отображает вашу исходную загруженную фотографию.)


Сама картинка выводится с фиолетовой рамкой сверху и словом "Text" в ней, это функционал шаблона карточки. Пока этот функционал мы полностью не внедрили, но мы просто хотим дать понять, что сгенерированную картинку можно обернуть в шаблон и вписывать текст, что не заставит покупателя открывать описание товара и читать его полностью, чтобы понять нужный ли для него это товар, а только взглянуть на фотокарточку и подчерпнуть полезную для себя информацию. При дальнейшем развитии, на нашем сервисе уже изначально будет несколько таких шаблонов, чтобы предоставить выбор продавцу.


*здесь каждый про своё*



А теперь по коду: для начала по максимуму избавиться от хардкодинга, которым мы не пренебрегали в использовании. 

*здесь каждый про своё*

Код картинки можно упростить, убрав функцию gen_imag(imgB64) и сделав конвертацию на стороне JS, а также в функции downloadurl(prompt) избавиться от метода DRY.
