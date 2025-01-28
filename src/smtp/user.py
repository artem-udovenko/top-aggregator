class User:
    def __init__(self, **kwargs):
        self.__surname = kwargs.get('surname')
        self.__name = kwargs.get('name')
        self.__patronymic = kwargs.get('patronymic')
        self.__email = kwargs.get('email')

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        self.__surname = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def patronymic(self):
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.__patronymic = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    def __str__(self):
        return '\n'.join([str(i) for i in [self.surname, self.name, self.patronymic, self.email]])
