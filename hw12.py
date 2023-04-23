from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value.isalpha() or not value.startswith('+380') or len(value) != 13:
            raise ValueError
        self.__value = value

    def __repr__(self) -> str:
        return self.value
    
class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value is None:
            self.__value = value
        else:
            self.__value = self.__set_date(value)

    @staticmethod
    def __set_date(bday: str):
        date_types = ["%d/%m/%Y", "%d/%m"]
        for date_type in date_types:
            try:
                date = datetime.strptime(bday, date_type).date()
                return date
            except ValueError:
                pass
        raise TypeError("Incorrect date format, should be dd/mm/yyyy or dd/mm")
        
    def __str__(self) -> str:
        return str(self.value)


class Record:
    def __init__(self, name: Name, phones: list[Phone] = [], birthday = None) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def days_to_birthday(self):
        self.day = int(self.birthday.split('/')[0])
        self.month = int(self.birthday.split('/')[1])
        today = datetime.today()
        bd_date = datetime(day= self.day, month= self.month, year= today.year)
        count_days = bd_date-today
        return f'{count_days.days} days'

    def add_phone(self, name: Name, phone: Phone):
        if phone not in self.phones:
            self.phones.append(phone)
            return f'I add new number phone {phone.value} to contact {name.value}.'
        else:
            return 'This phone number already exists.'
        
    def dell_phone(self, name:Name, phone: Phone):
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return f'I remove number phone {p.value}.'
        return f"I don't find this number."
    
    def change(self, name: Name ,phone: Phone, new_phone: Phone):
        self.dell_phone(name, phone)
        self.add_phone(name, new_phone)
        return 'Done!'

    def __str__(self) -> str:
        return ', '.join([str(p) for p in self.phones])
    
    def __repr__(self) -> str:
        return str(self)

class AddressBook(UserDict):
    index = 0
    def add_contact(self, record: Record):
        self.data[record.name.value] = record

    def find_phone(self, name: Name):
        for contact in contacts:
            if contact == name.value:
                return contacts[contact]
        return "I don't find this contact"
    def dell_contact(self, name: Name):
        for contact in contacts:
            if contact == name.value:
                contacts.pop(contact)
                return f"I removed contact{name}."
        return 'I dont find contact.'
    
    def save_file (self):
        name_file = 'contacts.bin'
        with open(name_file, "wb") as fh:
            pickle.dump(contacts, fh)

    def read_file(self):
        name_file = 'contacts.bin'
        with open(name_file, "rb") as fh:
            self.data = pickle.load(fh)
    
    def iteranor(self, step):
        lst = [f'{key}: {val.phones}' for key, val in contacts.items()]
        lst_slice = lst[self.index:self.index + int(step)]
        if self.index < len(lst):
            self.index += int(step)
        result = '\n'.join(lst_slice)
        return result
    
    def find(self, value):
        for key, rec in self.data.items():
            if value in key:
                print(f'{key}: {rec.phones}')
            else:
                for phone in rec.phones:
                    if value in phone.value:
                        print(f'{key}: {rec.phones}')

        return ''
    
        
    def __str__(self):
        result = []
        for record in self.data.values():
            result.append(f"{record.name.value}: {', '.join([phone.value for phone in record.phones])} Birthday: {record.birthday}")
        return "\n".join(result)

def input_errors(func):
    def inner(*args):
        try:
            return func(*args)
        except (KeyError, IndexError, ValueError):
            return "Not enough arguments."
        except FileNotFoundError:
            return 'I don`t find file.'
    return inner


@input_errors
def add(*args:tuple):
    tupl = args[0].split()
    name = Name(tupl[1])
    phone = Phone(tupl[2])
    Bp = None
    if len(tupl) == 4:
        Bp = tupl[-1]
    rec = Record(name, [phone], Bp)
    if name.value in contacts:
        for key_contact in contacts:
            if key_contact == name.value and phone.value not in contacts[key_contact].phones:
                return contacts[key_contact].add_phone(name, phone)
    else:
        contacts.add_contact(rec)
        return 'I add new contact'
    
def bdadd(*args):
    tupl = args[0].split()
    name = Name(tupl[1])
    bd = Birthday(tupl[2])
    for key_contact in contacts:
        if key_contact == name.value:
            contacts[key_contact].birthday = tupl[2]

@input_errors
def dell_phone(*args:tuple):
    tupl = args[0].split()
    name = Name(tupl[1])
    phone = Phone(tupl[2])  
    for key_contact in contacts:
        if key_contact == name.value:        
            return contacts[key_contact].dell_phone(name, phone)
    return 'I did not find an entry with the specified name' 

@input_errors
def dell_contact(*args:tuple):
    tupl = args[0].split()
    name = Name(tupl[1])
    return contacts.dell_contact(name)

@input_errors
def change(*args:tuple):
    tupl = args[0].split()
    name = Name(tupl[1])
    old_phone = Phone(tupl[2])
    new_phone = Phone(tupl[3])
    rec = contacts.get(name.value)
    return rec.change(name, old_phone, new_phone)

def delta_days(*args):
    tupl = args[0].split()
    name = Name(tupl[1])
    return contacts[name.value].days_to_birthday()

def iterator(*args):
    tupl = args[0].split()
    step = tupl[1]
    return contacts.iteranor(step)

def phone(*args:tuple):
    tupl = args[0].split()
    name = Name(tupl[1])
    return contacts.find_phone(name)

def find(*args:tuple):
    tupl = args[0].split()
    value = tupl[1]
    return contacts.find(value)


def show_all():
    return contacts

def hello():
    return "How can I help you?"

def comand_enoter():
    return 'Unknow comand. Please, try again.'

@input_errors
def hendler(text:str):
   
    if text == 'hello':
        return hello()
    
    elif text.startswith('add'):
        return add(text)
    
    elif text.startswith('change'):
        return change(text)
    
    
    elif text.startswith('dellcontact'):
        return dell_contact(text)
    
    elif text.startswith('dell'):
        return dell_phone(text)
    
    elif text.startswith('bdadd'):
        return bdadd(text)
    
    elif text.startswith('deltadays'):
        return delta_days(text)
    
    elif text.startswith('iterator'):
        return iterator(text)

    
    elif text.startswith('phone'):
        return phone(text)
    
    elif text.startswith('find'):
        return find(text)
    
    elif text.startswith('show all'):
        return show_all()
    
    elif text == 'readfile':
        contacts.read_file()
    else:
        return comand_enoter()
    
contacts = AddressBook()
def helper():
    comands = {'Hello': "How can I help you?",
              'add': 'add name number_phone 29/09/1996 (Date is not required)',
              'change': 'change name old_number_phone new_number_phone',
              'dellcontact': 'dellcontact name',
              'dell': 'dell name number_phone',
              'bdadd': 'bdadd name 29/09/09',
              'deltadays': 'deltadays name',
              'phone': 'phone name',
              'show all': 'show all (Show all contacts)',
              'iterator': 'iterator 2',
              'readfile': 'read file',
              'find': 'find value'}
    print('Hello. I`m BOT. \nI have this comands.')
    print()
    print(*[f'{key}: {val}' for key, val in comands.items()], sep='\n')

def main():
    helper()

    while True:
        input_comand = input('Pleace, enter comand:').lower()
        if input_comand == 'exit' or input_comand =='close' or input_comand == 'good bye':
            print("Good bye!")
            contacts.save_file()
            break

        comand = hendler(input_comand)
        print(comand)
        
if __name__ == '__main__':
    main()