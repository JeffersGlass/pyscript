import js

import asyncio
from faker import Faker
from uuid import uuid4

plugin = Plugin("ppp")

class ListView(list):
    def __init__(self, /, page_element, *args, **kwargs):
        self.page_element = page_element
        super().__init__(*args, **kwargs)

    def append(self, item):
        #js.console.log("Running method append on ListView")
        result = super().append(item)
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def clear(self):
        #js.console.log("Running method clear on ListView")
        result = super().clear()
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def copy(self):
        #js.console.log("Running method copy on ListView")
        result = super().copy()
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def count(self, item):
        #js.console.log("Running method count on ListView")
        result = super().count(item)
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def extend(self, item):
        #js.console.log("Running method extend on ListView")
        result = super().extend(item)
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def index(self,item):
        #js.console.log("Running method index on ListView")
        result = super().index(item)
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def insert(self, index, item):
        #js.console.log("Running method insert on ListView")
        result = super().insert(index, item)
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def pop(self):
        #js.console.log("Running method pop on ListView")
        result = super().pop()
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def remove(self,index):
        #js.console.log("Running method remove on ListView")
        result = super().remove(index)
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def reverse(self):
        #js.console.log("Running method reverse on ListView")
        result = super().reverse()
        asyncio.ensure_future(self.page_element.rerender())
        return result

    def sort(self):
        #js.console.log("Running method sort on ListView")
        result = super().sort()
        asyncio.ensure_future(self.page_element.rerender())
        return result


@plugin.register_custom_element("py-listview")
class PyListViewElement:
    def __init__(self, element):
        self.element = element

    def connect(self):
        #Create proxy for list
        self._listname = self.element.getAttribute("list")
        if self._listname is None:
            raise AttributeError("py-listview tag must have a 'list' attribute")
        print(f"{self._listname}")

        if self._listname not in globals():
            print(f"Creating new list {self._listname}")
            globals()[self._listname] = ListView(page_element = self)
        else:
            print(f"Using existing list {self._listname}")
            raise NotImplementedError("Cannot use existing list for ListView")
            #if not isinstance(globals()[self._listname], ListView)

        self._list = globals()[self._listname]


        self.set_default_style()
    
    def set_default_style(self):
        self.element.style.display = "flex"
        self.element.style.flexWrap = "wrap"
        self.element.style.borderStyle = "solid"
        self.element.style.borderWidth = "2px"
        self.element.style.borderColor = "rgb(100 116 130)"

        self.box_size = 10

    async def rerender(self):
        self.clear()

        for item in self._list:
            box = js.document.createElement("div")
            box.style.flexBasis = "4rem"
            box.style.flex = "1 1 auto"
            box.style.backgroundColor = "AliceBlue"
            #box.style.height = "4rem"
            box.style.borderStyle = "solid"
            box.style.borderWidth = "2px"
            box.style.borderColor = "rgb(100 116 130)"

            box.style.display = "flex"
            box.style.justifyContent = "center"
            box.style.alignItems = "center"

            content = js.document.createElement("div")
            content.id = "lv" + str(uuid4())
            content.style.textAlign = "center"
            content.style.wordWrap = "break-word"
            content.style.maxWidth = "24rem"

            box.appendChild(content)
            self.element.appendChild(box)
            display(item, target=content.id)

    def clear(self):
        while self.element.firstChild:
            self.element.removeChild(self.element.firstChild)

async def test_listview(lv_name):
    sleep_time = .5
    lv = globals()[lv_name]
    lv.append(1)
    assert lv == [1]
    await asyncio.sleep(sleep_time)
    
    lv.clear()
    assert lv == []
    await asyncio.sleep(sleep_time)
    
    lv.extend([1,2,3,4,4])
    assert lv == [1,2,3,4,4]
    await asyncio.sleep(sleep_time)
    
    x = lv.copy()
    assert x == [1,2,3,4,4]
    await asyncio.sleep(sleep_time)
    
    assert lv.count(4) == 2
    await asyncio.sleep(sleep_time)
    
    assert lv.index(2) == 1
    await asyncio.sleep(sleep_time)
    
    lv.insert(0, 5)
    assert lv == [5,1,2,3,4,4]
    await asyncio.sleep(sleep_time)
    
    y = lv.pop()
    assert y == 4
    await asyncio.sleep(sleep_time)
    
    assert lv == [5,1,2,3,4]
    await asyncio.sleep(sleep_time)
    
    lv.remove(2)
    assert lv == [5,1,3,4]
    await asyncio.sleep(sleep_time)
    
    lv.reverse()
    assert lv == [4,3,1,5]
    await asyncio.sleep(sleep_time)
    
    lv.sort()
    assert lv == [1,3,4,5]
    await asyncio.sleep(sleep_time)
    
    print("tests pass")

#asyncio.ensure_future(test_listview("mylist"))

async def biglist(lv_name):
    sleep_time = .1
    lv = globals()[lv_name]
    for i in range(100):
        lv.append(i)
        await asyncio.sleep(sleep_time)

#asyncio.ensure_future(biglist("mylist"))

from dataclasses import dataclass
from random import randint

@dataclass
class classroom():
    teacher: str
    room_num: str
    floor: int

async def objlist(lv_name):
    lv = globals()[lv_name]
    f = Faker()
    for _ in range(5):
        c = classroom(teacher = f.name(), room_num = "A" + str(randint(101,499)), floor = randint(1,4))
        lv.append(c)
        await asyncio.sleep(1)

asyncio.ensure_future(objlist("mylist"))
