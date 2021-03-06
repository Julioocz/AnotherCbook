import json


class ContactModel:

    def __init__(self, json_file):
        self.json_file = json_file
        self.contacts = self.get_contacts()
        self.contacts_names = self.get_contacts_names()

    def _jsonLoad(self):
        with open(self.json_file) as json_data:
            return json.load(json_data)

    def _jsonDump(self, json_new):
        with open(self.json_file, 'w') as json_out:
            json.dump(json_new, json_out, indent=3)

    def new_contact(self, name, phone=None):
        contact_new = {"name": name, "phone": phone}
        self.contacts.append(contact_new)
        self.save_contacts()

    def get_contacts(self):
        return self._jsonLoad()['persons']

    def save_contacts(self):
        self._jsonDump({'persons': self.contacts})

    def get_contacts_names(self):
        contacts_names = []
        for contact in self.contacts:
            contacts_names.append(contact['name'])
        return contacts_names

    def search_contact(self, name):
        index_contact = self.contacts_names.index(name)
        return self.contacts[index_contact]

    def verify_contact(self, name):
        return name in self.contacts_names

    def delete_contact(self, name):
        index_contact = self.contacts_names.index(name)
        self.contacts.pop(index_contact)
        self.save_contacts()

    def update_contact(self, name, new_phone):
        index_contact = self.contacts_names.index(name)
        self.contacts[index_contact]['phone'] = new_phone
        self.save_contacts()


class ContactView:

    def presentation(self):
        print("Welcome to AnotHer CBook \n")

    def menu(self):
        menu = []
        menu.append("Add a new contact")
        menu.append("Display all existing contacts")
        menu.append("Delete an existing contact")
        menu.append("Update an existing contact")
        menu.append("Search an existing contact by name")
        menu.append("Exit")

        print('\nMENU', end='\n\n')

        num_entry = 1
        for entry in menu:
            print('{}. {}'.format(num_entry, entry))
            num_entry += 1

    def menu_interaction(self, option):

        if option == 0:
            print('You selected Add a new contact', end='\n\n')

        elif option == 1:
            print('You selected Display all contacts', end='\n\n')

        elif option == 2:
            print('You selected Delete an existing contact', end='\n\n')

        elif option == 3:
            print('You selected Update an existing contact', end='\n\n')

        elif option == 4:
            print('You selected Search an existing contact', end='\n\n')

    def menu_out_of_bound(self):
        print('I did not understand what you selected, try again!')

    def contact_notFound(self):
        print('The contact that you are looking or is not in the contact book')

    def contactList(self, contacts):
        print('List of contacts: \n')
        for contact in contacts:
            self.contactView(contact)

    def contactView(self, contact):
        name = contact['name']
        phone = contact['phone']
        print('- Name: {} -- Phone: {}'.format(name, phone))

    def contact_deleted(self, name):
        print('The contact named {} has been deleted'.format(name.title()))

    def contact_added(self):
        print('The contact has been added')

    def contact_found(self, contact):
        print('The contact that you where looking for has been found: ')
        self.contactView(contact)

    def contact_updated(self, new_contact):
        print('The contact has been updated\nNew contact:')
        self.contactView(new_contact)

    def ask_contactInfo(self):
        print('Insert the contact info.')

    def ask_contactname(self):
        print('Insert the contact name')

    def error(self):
        print('UPS.. something went bad')

    def input_info(self, message):
        return input(message)

    def contact_not_found(self):
        print('The contact that you are looking has not been found')


class ContactController:

    def __init__(self, json):
        self.model = ContactModel(json)
        self.view = ContactView()

    def show_presentation(self):
        self.view.presentation()

    def start(self):
        options = [self.add, self.display, self.delete,
                   self.update, self.search, self.exit]

        while True:
            self.view.menu()
            option = int(self.view.input_info('Select an option: ')) - 1

            if 0 <= option <= 5:
                self.view.menu_interaction(option)
                options[option]()

            else:
                self.view.menu_out_of_bound()

    def add(self):
        self.view.ask_contactInfo()
        new_name = self.view.input_info('Name: ')
        new_phone = self.view.input_info('Phone number: ')
        self.model.new_contact(new_name, new_phone)
        self.view.contact_added()

    def delete(self):
        self.view.ask_contactname()
        name_delete = self.view.input_info('Name: ')

        if self.model.verify_contact(name_delete):
            self.model.delete_contact(name_delete)
            self.view.contact_deleted(name_delete)

        else:
            self.view.contact_not_found

    def display(self):
        contacts = self.model.get_contacts()
        self.view.contactList(contacts)

    def update(self):
        self.view.ask_contactname()
        contact_name = self.view.input_info('Name: ')

        if self.model.verify_contact(contact_name):
            print('Insert the new contact informations')
            new_phone = self.view.input_info('New phone: ')
            self.model.update_contact(contact_name, new_phone)
        else:
            self.view.contact_not_found

    def search(self):
        self.view.ask_contactname()
        contact_name = self.view.input_info('Name: ')

        if self.model.verify_contact(contact_name):
            contact = self.model.search_contact(contact_name)
            self.view.contactView(contact)

        else:
            self.view.contact_not_found

    def exit(self):
        return quit()
