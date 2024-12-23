class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.total_earnings = 0
        self.price = price

    def buy(self, quantity):
        if quantity > self.quantity:
            print(f"Нема доволно количина за {self.name}.")
            return False
        self.quantity -= quantity
        self.total_earnings += self.price * quantity
        return True

    def __str__(self):
        return f"{self.name} - Цена: {self.price}, Количина: {self.quantity}, Заработка: {self.total_earnings}"


class DigitalProduct(Product):
    def __init__(self, name, quantity, price, size):
        super().__init__(name, quantity, price)
        self.size = size

    def buy(self, quantity):
        discounted_price = self.price * 0.9
        if quantity > self.quantity:
            print(f"Нема доволно количина за {self.name}.")
            return False
        self.quantity -= quantity
        self.total_earnings += discounted_price * quantity
        return True

    def get_size_in_GB(self):
        return self.size * 0.001

    def __str__(self):
        return super().__str__() + f", Големина: {self.size} MB"


class FoodProduct(Product):
    def __init__(self, name, quantity, price, calories):
        super().__init__(name, quantity, price)
        self.calories = calories

    def buy(self, quantity):
        adjusted_price = self.price * 1.045
        if quantity > self.quantity:
            print(f"Нема доволно количина за {self.name}.")
            return False
        self.quantity -= quantity
        self.total_earnings += adjusted_price * quantity
        return True

    def __str__(self):
        return super().__str__() + f", Калории: {self.calories}"


class Store:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.total_food_products_earnings = 0
        self.total_digital_products_earnings = 0

    def add_product(self, product):
        self.products.append(product)

    def list_all_products(self):
        return self.products

    def list_all_digital_products(self):
        return [product for product in self.products if isinstance(product, DigitalProduct)]

    def list_all_food_products(self):
        return [product for product in self.products if isinstance(product, FoodProduct)]

    def get_products_less_than_price(self, price):
        return [product for product in self.products if product.price < price]

    def get_products_in_MB_range(self, start_mb, end_mb):
        return [product for product in self.products if isinstance(product, DigitalProduct) and start_mb <= product.size <= end_mb]

    def get_products_in_calorie_range(self, start_cal, end_cal):
        return [product for product in self.products if isinstance(product, FoodProduct) and start_cal <= product.calories <= end_cal]


class Buyer:
    def __init__(self, name, available_funds):
        self.name = name
        self.available_funds = available_funds

    def buy_product(self, store, product_name, quantity):
        product = next((p for p in store.products if p.name == product_name), None)
        if not product:
            print(f"Продуктот {product_name} не е достапен.")
            return


        if isinstance(product, DigitalProduct):
            total_price = product.price * 0.9 * quantity
        elif isinstance(product, FoodProduct):
            total_price = product.price * 1.045 * quantity
        else:
            total_price = product.price * quantity

        if total_price > self.available_funds:
            print(f"Немате доволно средства за {product_name}.")
            return

        if product.buy(quantity):
            self.available_funds -= total_price
            if isinstance(product, FoodProduct):
                store.total_food_products_earnings += total_price
            elif isinstance(product, DigitalProduct):
                store.total_digital_products_earnings += total_price
            print(f"Успешно купивте {quantity} од {product_name}.")
        else:
            print(f"Не е можно да купите {product_name}, нема доволно количина.")

    def __str__(self):
        return f"Купувач: {self.name}, Средства: {self.available_funds}"



store = Store("Продавница")
store.add_product(FoodProduct("Леб", 10, 50, 200))
store.add_product(DigitalProduct("Телефон", 5, 10000, 500))
store.add_product(Product("Тетратка", 20, 80))


buyer = Buyer("Иван", 2000)

print("Добредојдовте во продавницата!")
while True:
    print("\nДостапни продукти:")
    for product in store.list_all_products():
        print(product)

    choice = input("\nШто сакате да купите? (Име на продукт или 'излез' за да завршите): ")
    if choice.lower() == "излез":
        print("Ви благодариме за посетата!")
        break

    quantity = int(input("Колку сакате да купите? "))

    buyer.buy_product(store, choice, quantity)

    print("\nВашите преостанати средства:", buyer.available_funds)
    print("\nСостојбата на продавницата:")
    for product in store.list_all_products():
        print(product)
