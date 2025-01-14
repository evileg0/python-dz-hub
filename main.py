from typing import List, Tuple, Optional
from cl1 import *
import datetime

# делаем пока без тестов, они в todo low priority

# пачка итемов
item1 = Item(name="Cookie", amount=1000, cost=99, ddate = datetime.datetime(2025, 1, 19, 15, 44, 32))
item2 = Item(name="Uranium", amount=200, cost=88)
item3 = Item(name="Vodka", amount=10, cost=1900)

# итемы --> hub, удалялка рабочая
hub = Hub()
hub.add_item(item1)
hub.add_item(item2)
#hub.rm_item(item1)
hub.add_item(item3)

# накидаем тэгов (дада, удалять тоже можно) - тут и от класса и от объекта для разнообразия
# можно поменять cost
add_tag = Item.add_tag
add_tag(hub[0], "Bang")
add_tag(hub[0], "Bang")
add_tag(hub[0], "Fragile")
hub[1].add_tag('Fragile')
hub[1].add_tag('Radiactive')
hub[2].add_tag('18+')
hub[1].rm_tag('www')
hub[1].cost = 1

# вывод итемов хаба итератором + длина + repr для итема
print(f"Prints of Hub: {hub}")
print("-------  Iterator output(sorted by total cost):")
for item in hub:
    print(f"Id: {item.id}, Name: {item.name}, {item.amount}pcs x {item.cost}BTC"
          f" Total Cost: {item._amount * item.cost},"
          f" Dispatch time: {item.dispatch_time.strftime('%H:%M:%S %m/%d/%Y')}")
    print(f"*** Tags({len(item)}): '{', '.join(item.tags)}'")
print("------- End of Iterator")
print(f"Item count in Hub: {len(hub)}")
print(f"Prints of Hub[0]: {hub[0]}")

# пример поиска по id (существующий и фэйк)
pos, item = hub.find_by_id(999)
print(f"Element 999: position {pos}, Item: {item}")
pos, item = hub.find_by_id(2)
print(f"Element 2: position {pos}, Item: {item}")

# поиск по вхождению
search_word = "od"
search_res = hub.search(search_word)
print(f"------- Searching for *{search_word}*")
for item in search_res:
    print(item)
print("------- End of Search")

# поиск по тэгу или тэгам
search_tags = ["Fragile", "Radiactive"]
print(f"------- Searching for {search_tags}")
found_items = hub.find_by_tags(search_tags)
print([item for item in found_items])

found_items = hub.find_by_tags(["123"])
print([item for item in found_items])
print("------- End of Search")

# сравнение по цене, а точнее стоимости (цена х количество)
print(f"Цена {hub.find_by_id(3)[1].name} < Цены {hub.find_by_id(2)[1].name}")
print(f"{hub.find_by_id(3)[1] < hub.find_by_id(2)[1]}")

# копирование итема
copied_item = hub[0].copy()
print(f"Copied Item: {copied_item}")
hub.add_item(copied_item)
for item in hub:
    print(f"Id: {item.id}, Name: {item.name}, {item.amount}pcs x {item.cost}BTC"
          f" Total Cost: {item.amount * item.cost},"
          f" Dispatch time: {item.dispatch_time.strftime('%H:%M:%S %m/%d/%Y')}")
    print(f"*** Tags({len(item)}): '{', '.join(item.tags)}'")
print("------- End of Iterator")

# установка даты в хаб
hub.set_date(datetime.datetime(2025, 1, 8))
print(f"Hub date: {hub.get_date()}")

# поиск итемов по дате - до какой-то и в интервале
print(f"Find before: {datetime.datetime(2025, 1, 15)}")
found_items = hub.find_by_date(datetime.datetime(2025, 1, 15))
print([item for item in found_items])
print(f"Find between: {datetime.datetime(2025, 1, 15)} and {datetime.datetime(2025, 1, 30)}")
found_items = hub.find_by_date(datetime.datetime(2025, 1, 15), datetime.datetime(2025, 1, 30))
print([item for item in found_items])

# поиск самых дорогих итемов - тут именно по полю cost
print("Show 2 most valuables")
most_valuable_items = hub.find_most_valuable(2)
print([item for item in most_valuable_items])

# удаление пачки итемов
print("Drop item1 and item2")
items_to_drop = [item1, item2]
hub.drop_items(items_to_drop)
print(hub)

# очистка хаба
print("Clear the Hub")
hub.clear()
print(hub)

# todo звездочные: наполнение рандомом, json - если это последняя строчка на момент проверки, то не успел