from typing import List, Tuple, Optional
import datetime

class Item:
    """Информация о товаре"""
    _amount: int
    cost: int
    id: int
    description: str
    dispatch_time: datetime
    _tags: set

    def __init__(self, name: str, ddate: datetime = datetime.datetime.now(), amount: int = 0, cost: int = 0, description: str = ''):
        self.name = name
        self._amount = amount
        self._cost = cost
        self._tags  = set()
        self.id = 0
        self.dispatch_time = ddate

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def tags(self) -> set:
        return self._tags

    def set_cost(self, cost: int):
        """Устанавливает стоимость элемента"""
        self._cost = cost

    def get_cost(self) -> int:
        """Возвращает стоимость элемента"""
        return self._cost

    def add_tag(self, tag: str) -> None:
        """Добвляет тег"""
        self._tags.add(tag)

    def rm_tag(self, tag: str) -> None:
        """Удаляет тег"""
        if tag in self._tags:
            self._tags.remove(tag)

    def is_tagged(self, tag: str) -> bool:
        """Проверяет, содержит ли элемент тег"""
        return tag in self._tags

    def copy(self):
        """Возвращает новый объект Item с таким же описанием, ценой и именем, но с другим id"""
        new_item = Item(self.name, self.dispatch_time, self._amount, self._cost)
        new_item._tags = self._tags.copy()  # Копируем теги
        return new_item

    def __lt__(self, other: "Item") -> bool:
        """Сравнивает товары по количесnву * цена"""
        return self._amount * self._cost < other._amount * other._cost

    def __len__(self):
        """Количество тегов"""
        return len(self._tags)

    def __repr__ (self):
        return f"[{self.id}] {self.name} {*self._tags,} dispatch by {self.dispatch_time.strftime('%H:%M:%S %m/%d/%Y')}"

    cost = property(get_cost, set_cost)

class Hub:
    _hub_instance: "Hub" = None
    """
    Создаётся один раз
    """

    def __new__(cls):
        if cls._hub_instance is None:
            cls._hub_instance = super(Hub, cls).__new__(cls)
            cls._hub_instance._items = []
            cls._hub_instance._max_id = 1
        return cls._hub_instance

    def __init__(self):
        """Инициализировать пустой магазин"""
        if not hasattr(self, '_items'):
            self._items = []
            self._date = None

    def search(self, item_name: str) -> List[Item]:
        """Возвращает лист товаров, похожих по названию на запрос"""
        return [item for item in self._items if item_name.lower() in item.name.lower()]

    def __len__(self):
        """Количетво разных итемов"""
        return len(self._items)

    def add_item(self, item: Item):
        """Добавляет итем c id = _max_id (поле hub)"""
        item.id = self._max_id
        self._items.append(item)
        self._max_id += 1

    def max_id(self):
        """Возвращает максимальный id в списке _items - устарело, потом можно удалить"""
        if not self._items:
            return 0
        return max(item.id for item in self._items)

    def rm_item(self, item_or_id):
        """Удаляет элемент по id или если объект совпадает"""
        if isinstance(item_or_id, int):
            # Удаление по id
            self._items = [item for item in self._items if item.id != item_or_id]
        else:
            # Удаление по совпадению объекта
            self._items = [item for item in self._items if item != item_or_id]

    def drop_items(self, items: List[Item]):
        """Удаляет все товары из Hub, которые содержатся в items"""
        self._items = [item for item in self._items if item not in items]

    def clear(self):
        """Удаляет все товары из Hub"""
        self._items = []

    def find_by_id(self, id: int) -> Tuple[int, Optional[Item]]:
        """Возвращает (pos, item) предмета с id, если он есть в Hub, и (-1, None) если его нет"""
        for pos, item in enumerate(self._items):
            if item.id == id:
                return pos, item
        return -1, None

    def find_by_tags(self, tags: List[str]) -> List[Item]:
        """Возвращает контейнер, содержащий все предметы из items, у которых есть все теги из tags"""
        return [item for item in self._items if all(item.is_tagged(tag) for tag in tags)]

    def find_by_date(self, *args) -> List[Item]:
        """Возвращает лист всех Item, подходящих по дате"""
        if len(args) == 1:
            date = args[0]
            return [item for item in self._items if item.dispatch_time and item.dispatch_time <= date]
        elif len(args) == 2:
            start_date, end_date = args
            return [item for item in self._items if item.dispatch_time and start_date <= item.dispatch_time <= end_date]
        else:
            raise ValueError("Неверное количество аргументов. Ожидается 1 или 2 аргумента.")

    def find_most_valuable(self, amount: int = 1) -> List[Item]:
        """Возвращает первые amount самых дорогих предметов на складе"""
        sorted_items = sorted(self._items, key=lambda item: item._cost, reverse=True)
        return sorted_items[:amount]

    def __iter__(self):
        """Итерация по объекту по стоимости = amount x cost"""
        return iter(sorted(self._items, key=lambda item: item._amount * item._cost , reverse = True))

    def __getitem__(self, index) -> Item:
        """Получение элемента по индексу"""
        return self._items[index]

    def __repr__ (self):
        retnum = min(3, len(self._items))
        item_names = [item.name for item in self._items[:retnum]]
        return f"Top Items by cost(max 3): {', '.join(item_names)}"

    def set_date(self, date: datetime):
        """Устанавливает дату в hub"""
        self._date = date

    def get_date(self) -> Optional[datetime]:
        """Возвращает дату hub"""
        return self._date

