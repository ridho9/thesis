from perwalian_api.model import Model
from typing import Any, List, Optional, Type, TypeVar


class Store:
    def __init__(self):
        self.items: List[Model] = []

    def clear(self):
        self.items = []

    def create(self, item: Model):
        if item in self.items:
            raise Exception(f"Duplicate {item}")

        self.items.append(item)

    def get(self, model: Type[Model], id: str) -> Optional[Model]:
        for item in self.items:
            if isinstance(item, model) and item.id == id:
                return item
        return None

    def delete(self, model: Type[Model], id: str):
        item = self.get(model, id)
        if item:
            self.items.remove(item)
            return item
        else:
            raise Exception(f"Not found {model} {id}")


store = Store()