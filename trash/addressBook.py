
class Contact:
    def __init__(self, name, phone_num, email, address):
        self.name = name
        self.phone_num = phone_num
        self.email = email
        self.address = address

    def print_info(self):
        print("Name: ", self.name)
        print("Phone Number: ", self.phone_num)
        print("E-mail: ", self.email)
        print("Address: ", self.address)

def set_contact():
    name = input('Name : ')
    phone_num = input('phone_num : ')
    email = input('email : ')
    address = input('address : ')
    contact = Contact(name, phone_num, email, address)
    return contact

def print_contact(contact_list):
    for contact in contact_list:
        contact.print_info()

def delete_contact(contact_list, name):
    for key, contact in enumerate(contact_list):
        if contact.name == name:
            del contact_list[key]

def store_contact(contact_list):
    with open('contact_db.txt', 'wt') as f:
        for contact in contact_list:
            f.write(contact.name +'\n')
            f.write(contact.phone_num +'\n')
            f.write(contact.email +'\n')
            f.write(contact.address +'\n')

def load_contact(contact_list):
    with open('contact_db.txt', 'rt') as f:
        lines = f.readlines()
        num = len(lines) / 4
        num = int(num)

        for i in range(num):
            name = lines[4*i].rstrip('\n')
            phone_num = lines[4*i+1].rstrip('\n')
            email = lines[4*i+2].rstrip('\n')
            address = lines[4*i+3].rstrip('\n')

            contact = Contact(name, phone_num, email, address)
            contact_list.append(contact)



def print_menu():
    print('1. addressBook insert')
    print('2. adressBook print')
    print('3. addressBook delete')
    print('4. quit')
    menu = int(input('select Menu : '))
    return menu


def run():
    contact_list = []
    load_contact(contact_list)
    while 1:
        menu = print_menu()
        if menu == 1:
            insertion = set_contact()
            contact_list.append(insertion)
        elif menu == 2:
            print_contact(contact_list)
        elif menu == 3:
            name = input('delete Name :')
            delete_contact(contact_list, name)
        elif menu == 4:
            store_contact(contact_list)
            break

if __name__ == '__main__':
    run()
