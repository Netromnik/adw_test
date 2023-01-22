# пользовательская история
- Есть тизер(рекламное объявление)
- У тизера есть заголовок (ограничен 64 символами), описание, категория
- Тизер принадлежит автору
- Автор заходит в личный кабинет и создает тизеры
- Администратор заходит в этот же кабинет и тоже видит список тизеров
- Администратор может выбрать список тизеров и пометить их статусом "оплачено" или "октаз"
- Авторы не могут менять статус тизерам
- Если тизеру проставлен статус "оплачено или "октаз", то изменить этот статус уже нельзя
- За каждый оплаченный тизер автор получает фиксированное количество денег, но предполагается, что в будущем стоимость за оплаченный тизер может меняться, допустим сейчас авторы получают 50р за каждый оплаченный тизер, а через год будут получать по 100р
- У пользователя есть кошелек, который пополняется за каждый оплаченный тизер (т.е в момент, когда администратор оплачивает тизер)

# задача
- спроектировать бд (в качестве автора и администратора можем использовать стандартную модель User) 
- спроектировать апи для простановки статуса "оплачено" или "октаз" для списка тизеров
- написать тесты для апи
- предполагается, что код пишется в рамках крупного проекта, с долгосрочной поддержкой и развитием
- во время проерки задания будет обращаться внимание на организацию кода, декомпозицию, именование переменных, правильность бизнес логики
- в качестве фреймворка использовать django
- предполагается, что взаимодействие фронтэнда и бекэнда осуществляется по rest api