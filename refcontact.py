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


class ContactBook:
    def __init__(self, filepath='contacts.json'):
        self.filepath = filepath
        self.contacts = []
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.contacts = [Contact.from_dict(d) for d in data]

    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in self.contacts], f, ensure_ascii=False, indent=4)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save()

    def remove_contact(self, name):
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        self.save()

    def find_contact(self, name):
        return [c for c in self.contacts if name.lower() in c.name.lower()]

    def update_contact(self, name, new_contact):
        for i, c in enumerate(self.contacts):
            if c.name.lower() == name.lower():
                self.contacts[i] = new_contact
                self.save()
                return True
        return False

    def list_contacts(self):
        return self.contacts


# --- Интерфейс взаимодействия с пользователем ---

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


def add_contact_flow(book):
    name = get_input("Имя: ")
    phone = get_input("Телефон: ")
    email = get_input("Email (необязательно): ")
    book.add_contact(Contact(name, phone, email))
    print("Контакт добавлен.")


def show_all_contacts(book):
    contacts = book.list_contacts()
    if not contacts:
        print("Список контактов пуст.")
    else:
        for c in contacts:
            print("-", c)


def search_contact_flow(book):
    name = get_input("Введите имя для поиска: ")
    found = book.find_contact(name)
    if found:
        for c in found:
            print("-", c)
    else:
        print("Контакты не найдены.")


def edit_contact_flow(book):
    name = get_input("Имя контакта для редактирования: ")
    found = book.find_contact(name)
    if not found:
        print("Контакт не найден.")
        return
    print("Введите новые данные:")
    new_name = get_input("Новое имя: ")
    new_phone = get_input("Новый телефон: ")
    new_email = get_input("Новый email: ")
    updated = book.update_contact(name, Contact(new_name, new_phone, new_email))
    if updated:
        print("Контакт обновлен.")
    else:
        print("Ошибка при обновлении.")


def delete_contact_flow(book):
    name = get_input("Введите имя контакта для удаления: ")
    book.remove_contact(name)
    print("Контакт удален, если он существовал.")


def main():
    contact_book = ContactBook()
    actions = {
        '1': add_contact_flow,
        '2': show_all_contacts,
        '3': search_contact_flow,
        '4': edit_contact_flow,
        '5': delete_contact_flow
    }

    while True:
        show_menu()
        user_choice = get_input("Выберите действие: ")
        if user_choice == '0':
            print("До свидания!")
            break
        action = actions.get(user_choice)
        if action:
            action(contact_book)
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == '__main__':
    main()