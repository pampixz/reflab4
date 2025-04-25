import json
import os


class Contact:
    def __init__(self, name, phone, email=''):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {'name': self.name, 'phone': self.phone, 'email': self.email}

    @staticmethod
    def from_dict(data):
        return Contact(data['name'], data['phone'], data.get('email', ''))

    def __str__(self):
        return f"{self.name} | Телефон: {self.phone} | Email: {self.email or 'не указан'}"


class DataManager:
    def __init__(self, filepath='contacts.json'):
        self.filepath = filepath

    def load_contacts(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Contact.from_dict(d) for d in data]
        return []

    def save_contacts(self, contacts):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in contacts], f, ensure_ascii=False, indent=4)


class ContactBook:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.contacts = self.data_manager.load_contacts()

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.data_manager.save_contacts(self.contacts)

    def remove_contact(self, name):
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        self.data_manager.save_contacts(self.contacts)

    def find_contact(self, name):
        return [c for c in self.contacts if name.lower() in c.name.lower()]

    def update_contact(self, name, new_contact):
        for i, c in enumerate(self.contacts):
            if c.name.lower() == name.lower():
                self.contacts[i] = new_contact
                self.data_manager.save_contacts(self.contacts)
                return True
        return False

    def list_contacts(self):
        return self.contacts


class UserInterface:
    def __init__(self, book):
        self.book = book

    def show_menu(self):
        print("\n=== МЕНЮ КОНТАКТНОЙ КНИГИ ===")
        print("1. Добавить контакт")
        print("2. Показать все контакты")
        print("3. Поиск по имени")
        print("4. Редактировать контакт")
        print("5. Удалить контакт")
        print("0. Выход")

    def get_input(self, prompt):
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\nПрервано пользователем.")
            return ''

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_input("Выберите действие: ")
            if choice == '1':
                name = self.get_input("Имя: ")
                phone = self.get_input("Телефон: ")
                email = self.get_input("Email (необязательно): ")
                self.book.add_contact(Contact(name, phone, email))
                print("Контакт добавлен.")
            elif choice == '2':
                contacts = self.book.list_contacts()
                if not contacts:
                    print("Список контактов пуст.")
                else:
                    for c in contacts:
                        print("-", c)
            elif choice == '3':
                name = self.get_input("Введите имя для поиска: ")
                found = self.book.find_contact(name)
                if found:
                    for c in found:
                        print("-", c)
                else:
                    print("Контакты не найдены.")
            elif choice == '4':
                name = self.get_input("Имя контакта для редактирования: ")
                found = self.book.find_contact(name)
                if not found:
                    print("Контакт не найден.")
                    continue
                print("Введите новые данные:")
                new_name = self.get_input("Новое имя: ")
                new_phone = self.get_input("Новый телефон: ")
                new_email = self.get_input("Новый email: ")
                updated = self.book.update_contact(name, Contact(new_name, new_phone, new_email))
                print("Контакт обновлен." if updated else "Ошибка при обновлении.")
            elif choice == '5':
                name = self.get_input("Введите имя контакта для удаления: ")
                self.book.remove_contact(name)
                print("Контакт удален, если он существовал.")
            elif choice == '0':
                print("До свидания!")
                break
            else:
                print("Неверный ввод. Попробуйте снова.")


if __name__ == '__main__':
    data_manager = DataManager()
    book = ContactBook(data_manager)
    ui = UserInterface(book)
    ui.run()
