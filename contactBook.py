import json
import inspect

class ContactModel:
    def __init__(self, json_file):
        self.json_file = json_file
        self.contacts = self.get_contacts()

    def _jsonLoad(self):
        with open(self.json_file) as json_data:
            return json.load(json_data)

    def _jsonDump(self, json_new):
        with open(self.json_file, 'w') as json_out:
            json.dump(json_new, json_out,indent = 3)


    def new_contact(self, name, phone = None):
        contact_new = {"name":name, "phone": phone}
        self.contacts.append(contact_new)
        self.save_contacts()

    def get_contacts(self):
        return self._jsonLoad()['persons']

    def save_contacts(self):
        self._jsonDump({'persons': self.contacts})

    def search_contact(self, name):
        id_contact = 0
        for x in self.contacts:
            if x['name'] == name:
                return x, id_contact
            id_contact += 1
        else:
            return False

    def verify_contact(self, name):
        x = self.search_contact(name)
        if x != False:
            return True
        return x

    def delete_contact(self, name):
        id_contact = self.search_contact(name)[1]
        self.contacts.pop(id_contact)
        self.save_contacts()

    def update_contact(self, name, new_phone):
        id_contact = self.search_contact(name)[1]

        self.contacts[id_contact]['phone'] = new_phone
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

        print('\nMENU' , end='\n\n')

        num_entry = 1
        for entry in menu:
            print ('{}. {}'.format(num_entry, entry))
            num_entry += 1

    def contact_notFound(self):
        print('The contact that you are looking for is not in the contact book')

    def contactList(self, contacts):
        print('List of contacts: \n')
        for contact in contacts:
            self.contactView(contact)

    def contactView(self, contact):
        print('- Name: {} -- Phone: {}'.format(contact['name'], contact['phone']))

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


class ContactController:

    def __init__(self, json):
        self.model = ContactModel(json)
        self.view = ContactView()

    def show_presentation(self):
        self.view.presentation()

    def start(self):
    	status = True
    	
    	while True:
            self.view.menu()
            option = int(input('Select an option: ')) - 1
            
            if option == 0:
            	print ('You selected Add a new contact', end='\n\n')
            	self.add()
            elif option == 1:
            	print ('You selected Display all contacts', end='\n\n')
            	self.display()
            elif option == 2:
            	print ('You selected Delete an existing contact', end='\n\n')
            	self.delete()
            elif option == 3:
            	print ('You selected Update an existing contact', end='\n\n')
            	self.update()
            elif option == 4:
            	print ('You selected Search an existing contact', end='\n\n')
            	self.search()
            elif option == 5:
            	break

            else:
            	print('I did not understand what you selected, could you please try again?')

    def add(self):
        self.view.ask_contactInfo()
        new_name = input('Name: ')
        new_phone = input('Phone number: ')

        try:
            self.model.new_contact(new_name, new_phone)
            self.view.contact_added()
        except:
            self.view.error()

    def delete(self):
        self.view.ask_contactname()
        name_delete = input('Name: ')

        try:
            self.model.delete_contact(name_delete)
            self.view.contact_deleted(name_delete)

        except:
            self.view.error()

    def display(self):
        contacts = self.model.get_contacts()
        self.view.contactList(contacts)

    def update(self):
        self.view.ask_contactname()
        contact_name = input('Name: ')

        if self.model.verify_contact(contact_name):
            print('Insert the new contact informations')
            new_phone = input('New phone: ')
            self.model.update_contact(contact_name, new_phone)
        else:
            print('The contact is not in your contactbook')
	
    def search(self):
        self.view.ask_contactname()
        contact_name = input('Name: ')
        
        if self.model.verify_contact(contact_name):
            contact = self.model.search_contact(contact_name)[0]
            self.view.contactView(contact)

        else:
        	print('The contact is not in your contactbook')

        