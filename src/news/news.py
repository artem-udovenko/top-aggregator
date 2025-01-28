class News:
    def __init__(self, **kwargs):
        self.__header = kwargs.get('header')
        self.__text = kwargs.get('text')
        self.__author = kwargs.get('author')
        self.__date = kwargs.get('date')
        self.__time = kwargs.get('time')

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, value):
        self.__header = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    def __str__(self):
        return '\n'.join([str(i) for i in [self.header, self.text, self.author, self.date, self.time]])