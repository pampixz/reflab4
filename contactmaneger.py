import json
import os
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class Contact:
    def __init__(self, name, phone, email=''):
        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()

    def to_dict(self):
        return {'name': self.name, 'phone': self.phone, 'email': self.email}

    @staticmethod
    def from_dict(data):
        return Contact(data['name'], data['phone'], data.get('email', ''))

    def __str__(self):
        return f"{self.name} | Телефон: {self.phone} | Email: {self.email or 'не указан'}"


class ContactBook:
    def __init__(self, filepath='contacts.json'):
        self.filepath = filepath
        self.contacts = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.contacts = [Contact.from_dict(d) for d in data]
                logging.info("Контакты успешно загружены.")
            except Exception as e:
                logging.error(f"Ошибка загрузки контактов: {e}")

    def save(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([c.to_dict() for c in self.contacts], f, ensure_ascii=False, indent=4)
            logging.info("Контакты сохранены.")
        except Exception as e:
            logging.error(f"Ошибка сохранения контактов: {e}")

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save()

    def remove_contact(self, name):
        before = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        self.save()
        after = len(self.contacts)
        if before == after:
            logging.warning("Контакт не найден для удаления.")
        else:
            logging.info(f"Контакт '{name}' удалён.")

    def find_contact(self, name):
        found = [c for c in self.contacts if name.lower() in c.name.lower()]
        logging.info(f"Найдено {len(found)} совпадений.")
        return found

    def update_contact(self, name, new_contact):
        for i, c in enumerate(self.contacts):
            if c.name.lower() == name.lower():
                self.contacts[i] = new_contact
                self.save()
                logging.info(f"Контакт '{name}' обновлён.")
                return True
        logging.warning(f"Контакт '{name}' не найден.")
        return False

    def list_contacts(self):
        return self.contacts


def show_menu():
    print("\n=== МЕНЮ КОНТАКТНОЙ КНИГИ ===")
    print("1. Добавить контакт")
    print("2. Показать все контакты")
    print("3. Поиск по имени")
    print("4. Редактировать контакт")
    print("5. Удалить контакт")
    print("0. Выход")


def get_input(prompt):
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
        return ''


def input_contact_data():
    name = get_input("Имя: ")
    while not name:
        name = get_input("Имя не может быть пустым. Введите имя: ")
    phone = get_input("Телефон: ")
    while not phone:
        phone = get_input("Телефон не может быть пустым. Введите телефон: ")
    email = get_input("Email (необязательно): ")
    return Contact(name, phone, email)


def main():
    book = ContactBook()
    while True:
        show_menu()
        choice = get_input("Выберите действие: ")
        if choice == '1':
            contact = input_contact_data()
            book.add_contact(contact)
            print("Контакт добавлен.")
        elif choice == '2':
            contacts = book.list_contacts()
            if not contacts:
                print("Список контактов пуст.")
            else:
                print(f"\nВсего контактов: {len(contacts)}")
                for c in contacts:
                    print("-", c)
        elif choice == '3':
            name = get_input("Введите имя для поиска: ")
            found = book.find_contact(name)
            if found:
                for c in found:
                    print("-", c)
            else:
                print("Контакты не найдены.")
        elif choice == '4':
            name = get_input("Имя контакта для редактирования: ")
            found = book.find_contact(name)
            if not found:
                print("Контакт не найден.")
                continue
            print("Введите новые данные:")
            new_contact = input_contact_data()
            if book.update_contact(name, new_contact):
                print("Контакт обновлен.")
        elif choice == '5':
            name = get_input("Введите имя контакта для удаления: ")
            book.remove_contact(name)
        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == '__main__':
    main()