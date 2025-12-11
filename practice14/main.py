class Phone:
    def __init__(
        self,
        brand: str,
        model: str,
        price: float,
        color: str,
        storage_gb: int,
        is_in_stock: bool
    ) -> None:
        self.brand = brand
        self.model = model
        self.price = price
        self.color = color
        self.storage_gb = storage_gb
        self.is_in_stock = is_in_stock

    def get_full_name(self) -> str:
        return f"{self.brand} {self.model}"

    def apply_discount(self, discount_percent: float) -> None:
        if 0 <= discount_percent <= 100:
            self.price *= (1 - discount_percent / 100)
        else:
            print("Процент скидки должен быть от 0 до 100")

    def check_availability(self) -> str:
        return "В наличии" if self.is_in_stock else "Нет в наличии"

    def __str__(self) -> str:
        availability = "Да" if self.is_in_stock else "Нет"
        return (
            f"Телефон: {self.get_full_name()}\n"
            f"Цвет: {self.color}\n"
            f"Память: {self.storage_gb} ГБ\n"
            f"Цена: {self.price:.2f} руб.\n"
            f"В наличии: {availability}\n"
            f"{'=' * 30}"
        )


def main():
    print("Демонстрация работы класса Phone:")
    print("=" * 50)

    phone1 = Phone(
        brand="Apple",
        model="iPhone 15 Pro",
        price=129990.0,
        color="Титан",
        storage_gb=256,
        is_in_stock=True
    )

    phone2 = Phone(
        brand="Samsung",
        model="Galaxy S24 Ultra",
        price=119990.0,
        color="Черный",
        storage_gb=512,
        is_in_stock=False
    )

    phone3 = Phone(
        brand="Xiaomi",
        model="14 Pro",
        price=79990.0,
        color="Зеленый",
        storage_gb=256,
        is_in_stock=True
    )

    phone4 = Phone(
        brand="Google",
        model="Pixel 8 Pro",
        price=89990.0,
        color="Белый",
        storage_gb=128,
        is_in_stock=True
    )

    phones = [phone1, phone2, phone3, phone4]

    print("\n1. Полная информация о телефонах:")
    for phone in phones:
        print(phone)

    print("\n2. Использование метода get_full_name():")
    for phone in phones:
        print(f"- {phone.get_full_name()}")

    print("\n3. Применение скидки на телефоны:")
    phone1.apply_discount(10)
    phone3.apply_discount(15)
    phone4.apply_discount(5)
    
    print(f"{phone1.get_full_name()} после 10% скидки: {phone1.price:.2f} руб.")
    print(f"{phone3.get_full_name()} после 15% скидки: {phone3.price:.2f} руб.")
    print(f"{phone4.get_full_name()} после 5% скидки: {phone4.price:.2f} руб.")

    print("\n4. Проверка наличия телефонов:")
    for phone in phones:
        print(f"{phone.get_full_name()}: {phone.check_availability()}")

    print("\n5. Пример с некорректной скидкой:")
    phone_test = Phone("Test", "Model", 1000.0, "Red", 64, True)
    print(f"Цена до скидки: {phone_test.price:.2f}")
    phone_test.apply_discount(150)
    print(f"Цена после некорректной скидки: {phone_test.price:.2f}")

    print("\n6. Детальная информация после изменений:")
    print(f"{phone1.get_full_name()}:")
    print(f"  Цена: {phone1.price:.2f} руб.")
    print(f"  Наличие: {phone1.check_availability()}")


if __name__ == "__main__":
    main()