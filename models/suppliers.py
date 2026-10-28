from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Supplier:
    """Поставщик товаров."""

    id: int
    name: str
    contact_person: str
    phone: str
    email: str
    address: str = ""

    def __str__(self) -> str:
        return (
            f"Поставщик №{self.id}: {self.name}, "
            f"контакт: {self.contact_person}"
        )

    def has_contact_email(self) -> bool:
        return bool(self.email.strip())

    @classmethod
    def from_data(cls, data: dict) -> "Supplier":
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            contact_person=str(data["contact_person"]),
            phone=str(data["phone"]),
            email=str(data.get("email", "")),
            address=str(data.get("address", "")),
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
        }


def add_supplier(suppliers: list[Supplier], supplier: Supplier) -> None:
    suppliers.append(supplier)


def find_supplier(suppliers: list[Supplier], supplier_id: int) -> Supplier | None:
    for supplier in suppliers:
        if supplier.id == supplier_id:
            return supplier
    return None


def show_suppliers(suppliers: list[Supplier]) -> None:
    for supplier in suppliers:
        print(supplier)
