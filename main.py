import random
from datetime import datetime, timedelta
from functools import reduce
from typing import Callable, Dict, List, Tuple, Union

Transaction = Dict[str, Union[str, float]]

# ---------------------------------------------------------------
# 1. Звичайні функції
# ---------------------------------------------------------------


def compound_interest(principal: float, rate: float, years: int) -> float:
    """
    Розраховує суму вкладу з урахуванням складних відсотків.

    Args:
        principal (float): Початкова сума вкладу.
        rate (float): Річна відсоткова ставка (у %).
        years (int): Кількість років.

    Returns:
        float: Підсумкова сума.
    """
    return principal * (1 + rate / 100) ** years


def monthly_payment(loan: float, annual_rate: float, months: int) -> float:
    """
    Розраховує щомісячний ануїтетний платіж за кредитом.

    Args:
        loan (float): Сума кредиту.
        annual_rate (float): Річна відсоткова ставка (у %).
        months (int): Строк кредиту в місяцях.

    Returns:
        float: Щомісячний платіж.
    """
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        return loan / months
    factor = (1 + monthly_rate) ** months
    return loan * monthly_rate * factor / (factor - 1)


# ---------------------------------------------------------------
# 2. Функція з параметрами за замовчуванням
# ---------------------------------------------------------------


def net_income(gross: float, tax_rate: float = 18.0, military_fee: float = 5.0) -> float:
    """
    Розраховує дохід після сплати податків.

    Args:
        gross (float): Дохід до оподаткування.
        tax_rate (float, optional): Ставка ПДФО (%). За замовчуванням 18.
        military_fee (float, optional): Військовий збір (%). За замовчуванням 5.

    Returns:
        float: Чистий дохід.
    """
    return gross * (1 - (tax_rate + military_fee) / 100)


# ---------------------------------------------------------------
# 3. Функція зі змінною кількістю аргументів
# ---------------------------------------------------------------


def total_expenses(*expenses: float) -> float:
    """
    Підсумовує довільну кількість витрат.

    Args:
        *expenses (float): Довільна кількість сум витрат.

    Returns:
        float: Загальна сума витрат.
    """
    return sum(expenses)


# ---------------------------------------------------------------
# 4. Лямбда-функції
# ---------------------------------------------------------------

percent_change = lambda old, new: (new - old) / old * 100
uah_to_usd = lambda amount, rate=41.5: round(amount / rate, 2)


# ---------------------------------------------------------------
# 5. Рекурсивна функція
# ---------------------------------------------------------------


def find_amount_range(data: List[Transaction], start: int, end: int) -> Tuple[float, float]:
    """
    Рекурсивно (методом «розділяй і володарюй») знаходить мінімальну
    та максимальну суму транзакції. Глибина рекурсії ~ log2(n).

    Args:
        data (List[Transaction]): Список транзакцій.
        start (int): Початковий індекс.
        end (int): Кінцевий індекс.

    Returns:
        Tuple[float, float]: (мінімум, максимум).
    """
    if start == end:
        value = data[start]["amount"]
        return value, value

    mid = (start + end) // 2
    left_min, left_max = find_amount_range(data, start, mid)
    right_min, right_max = find_amount_range(data, mid + 1, end)
    return min(left_min, right_min), max(left_max, right_max)


# ---------------------------------------------------------------
# 6. Функція вищого порядку
# ---------------------------------------------------------------


def apply_to_transactions(
    data: List[Transaction], func: Callable[[float], float]
) -> List[Transaction]:
    """
    Застосовує задану функцію до суми кожної транзакції.

    Args:
        data (List[Transaction]): Список транзакцій.
        func (Callable[[float], float]): Функція для суми.

    Returns:
        List[Transaction]: Новий список з оновленими сумами.
    """
    return [{**item, "amount": func(item["amount"])} for item in data]


# ---------------------------------------------------------------
# Генерація тестових даних (24 елементи)
# ---------------------------------------------------------------

CATEGORIES = ["Продукти", "Транспорт", "Розваги", "Комунальні", "Одяг", "Здоров'я"]


def generate_transactions(count: int) -> List[Transaction]:
    """Генерує випадкові витрати за вказану кількість днів."""
    base_date = datetime(2026, 1, 1)
    return [
        {
            "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "category": random.choice(CATEGORIES),
            "amount": round(random.uniform(50, 3000), 2),
        }
        for i in range(count)
    ]


# ---------------------------------------------------------------
# Допоміжні функції введення з валідацією
# ---------------------------------------------------------------


def input_float(prompt: str, min_value: float = 0.0) -> float:
    """Запитує число, поки користувач не введе коректне значення."""
    while True:
        try:
            value = float(input(prompt).replace(",", "."))
            if value < min_value:
                print(f"Значення має бути не менше {min_value}.")
                continue
            return value
        except ValueError:
            print("Будь ласка, введіть число.")


def show_menu() -> None:
    print("\nОберіть операцію:")
    print("1. Показати транзакції")
    print("2. Конвертувати витрати в USD (map)")
    print("3. Знайти великі витрати (filter)")
    print("4. Загальна сума витрат (reduce)")
    print("5. Найменша і найбільша витрата (рекурсія)")
    print("6. Розрахувати складні відсотки")
    print("7. Розрахувати щомісячний платіж за кредитом")
    print("8. Підсумувати власні витрати")
    print("9. Розрахувати чистий дохід")
    print("10. Зміна у відсотках")
    print("0. Вийти")


# ---------------------------------------------------------------
# Основна програма
# ---------------------------------------------------------------


def main() -> None:
    print("Вітаємо в програмі «Особисті фінанси»!")
    transactions = generate_transactions(24)

    while True:
        show_menu()
        try:
            choice = int(input("Ваш вибір: "))

            if choice == 1:
                for t in transactions:
                    print(f"{t['date']} | {t['category']:<11} | {t['amount']:>8.2f} грн")

            elif choice == 2:
                converted = apply_to_transactions(transactions, uah_to_usd)
                usd_list = list(map(lambda t: t["amount"], converted))
                for t in converted[:5]:
                    print(f"{t['date']} | {t['category']:<11} | {t['amount']:>7.2f} USD")
                print(f"... усього {len(usd_list)} записів")

            elif choice == 3:
                limit = input_float("Мінімальна сума витрати (грн): ")
                big = list(filter(lambda t: t["amount"] >= limit, transactions))
                if big:
                    for t in big:
                        print(f"{t['date']} | {t['category']:<11} | {t['amount']:>8.2f} грн")
                    print(f"Знайдено: {len(big)}")
                else:
                    print("Витрат за таким критерієм не знайдено.")

            elif choice == 4:
                total = reduce(lambda acc, t: acc + t["amount"], transactions, 0)
                print(f"Загальна сума витрат: {total:.2f} грн")

            elif choice == 5:
                min_a, max_a = find_amount_range(transactions, 0, len(transactions) - 1)
                print(f"Найменша витрата: {min_a:.2f} грн")
                print(f"Найбільша витрата: {max_a:.2f} грн")

            elif choice == 6:
                principal = input_float("Початкова сума (грн): ")
                rate = input_float("Річна ставка (%): ")
                years = int(input_float("Кількість років: "))
                result = compound_interest(principal, rate, years)
                print(f"Підсумкова сума: {result:.2f} грн (прибуток {result - principal:.2f} грн)")

            elif choice == 7:
                loan = input_float("Сума кредиту (грн): ", 1)
                rate = input_float("Річна ставка (%): ")
                months = int(input_float("Строк (місяців): ", 1))
                pay = monthly_payment(loan, rate, months)
                print(f"Щомісячний платіж: {pay:.2f} грн")
                print(f"Переплата: {pay * months - loan:.2f} грн")

            elif choice == 8:
                raw = input("Введіть суми через пробіл: ").replace(",", ".").split()
                amounts = [float(x) for x in raw]
                if not amounts:
                    print("Ви нічого не ввели.")
                else:
                    print(f"Разом: {total_expenses(*amounts):.2f} грн")

            elif choice == 9:
                gross = input_float("Дохід до оподаткування (грн): ")
                print(f"Чистий дохід: {net_income(gross):.2f} грн")

            elif choice == 10:
                old = input_float("Старе значення: ", 0.01)
                new = input_float("Нове значення: ")
                print(f"Зміна: {percent_change(old, new):+.1f}%")

            elif choice == 0:
                print("Дякуємо за використання програми!")
                break

            else:
                print("Невірний вибір. Спробуйте ще раз.")

        except ValueError:
            print("Будь ласка, введіть коректне число.")


if __name__ == "__main__":
    main()
