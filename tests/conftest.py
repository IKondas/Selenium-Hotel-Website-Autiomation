# -------------------------- Imports --------------------------
import __init__
import source.browser_setup as setup

# -------------------------- Room Setup --------------------------
class Room:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
        
room_list = [
    Room("Single", "100", "Aenean porttitor mauris sit amet lacinia molestie. In posuere accumsan aliquet. Maecenas sit amet nisl massa. Interdum et malesuada fames ac ante."),
    Room("Double", "150", "Vestibulum sollicitudin, lectus ac mollis consequat, lorem orci ultrices tellus, eleifend euismod tortor dui egestas erat. Phasellus et ipsum nisl."),
    Room("Suite", "225", "Etiam metus metus, fringilla ac sagittis id, consequat vel neque. Nunc commodo quis nisl nec posuere. Etiam at accumsan ex."),
]

# -------------------------- Client Setup --------------------------
class Client:
    def __init__(self, name, email, phone, subject, description):
        self.name = name
        self.email = email
        self.phone = phone
        self.subject = subject
        self.description = description

class Client2:
    def __init__(self, firstname, lastname, email, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone

# -------------------------- Contact Form Setup --------------------------
class TextFields:
    def __init__(self, name):
        self.name = name

    def blank_msg(self):
        if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
            return "must not be empty"
        else:
            return str(self.name.capitalize() + " may not be blank")
         
    def length_msg(self, min_length, max_length):
        if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
            return "size must be between " + str(min_length) + " and " + str(max_length)
        else:
            return str(self.name.capitalize() + " must be between " + str(min_length) + " and " + str(max_length) + " characters.")

    def check_any_alphanumeric(self, text):    
        for i in text:
            if i.isalnum():
                return True
                break
            else:
                return False

class TextField_Name(TextFields):
    def __init__(self, name, min_length, max_length = 0):
        super().__init__(name)
        self.min_length = min_length
        self.max_length = max_length

    def verify_validity(self, text):
        if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
            if self.max_length == 0:
                return str(self.name).capitalize() + " should not be blank"
            elif len(text) < self.min_length or len(text) > self.max_length:
                return [str(self.name).capitalize() + " should not be blank", TextFields.length_msg(self, self.min_length, self.max_length)]
        elif len(text) == 0 or (len(text) >= self.min_length and TextFields.check_any_alphanumeric(self, text) == False):
                if self.max_length == 0:
                    return TextFields.blank_msg(self)

class TextField_Email(TextFields):
    def __init__(self, name, min_length):
        super().__init__(name)
        self.min_length = min_length

    def find_char(self, s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def check_if_all_spaces(self, text):
        is_all_spaces = True    
        for i in text:
            if i != " ":
                is_all_spaces = False
        return is_all_spaces
    
    def verify_validity(self, text):       
        if len(text) == 0:
            return TextFields.blank_msg(self)
        elif len(text) >= self.min_length and self.check_if_all_spaces(text) == True:
            if setup.driver.current_url.startswith("https://automationintesting.online/reservation/") == False:
                return TextFields.blank_msg(self)
        elif text.find("@") == -1:
            return "must be a well-formed email address"
        else:
            at_sign = text.find("@")
            part1 = text[:at_sign]
            part2 = text[at_sign+1:]
            address = part1 + part2 
            
            special_characters = " !\"#$%&'()*+,-/:;<=>?@[\\]^_`{|}~"

            if any(character in special_characters for character in address) or len(part1) < 1 or len(part2) < 1:
                return "must be a well-formed email address"

            periods = self.find_char(text, ".")
 
            for dot in periods:
                    try:
                        dot_left = text[dot-1]
                        dot_right = text[dot+1]
                    except IndexError:
                        return "must be a well-formed email address"
 
                    if dot_left == "" or dot_left == "." or dot_left == "@" or dot_right == "" or dot_right == "." or dot_right == "@": 
                        return "must be a well-formed email address"
            
class TextField_Phone(TextFields):
    def __init__(self, name, min_length, max_length):
        super().__init__(name)
        self.min_length = min_length
        self.max_length = max_length
    
    def verify_validity(self, text):
        if len(text) == 0:
            return [TextFields.blank_msg(self), TextFields.length_msg(self, self.min_length, self.max_length)]
        elif (len(text) >= self.min_length or len(text) <= self.max_length) and TextFields.check_any_alphanumeric(self, text) == False:
            return TextFields.blank_msg(self)
        elif len(text) < self.min_length or len(text) > self.max_length:
            return TextFields.length_msg(self, self.min_length, self.max_length)

class TextField_Subject(TextFields):
    def __init__(self, name, min_length, max_length):
        super().__init__(name)
        self.min_length = min_length
        self.max_length = max_length

    def verify_validity(self, text):
        if len(text) == 0:
            return [TextFields.blank_msg(self), TextFields.length_msg(self, self.min_length, self.max_length)]
        elif (len(text) >= self.min_length or len(text) <= self.max_length) and TextFields.check_any_alphanumeric(self, text) == False:
            return TextFields.blank_msg(self)
        elif len(text) < self.min_length or len(text) > self.max_length:
            return TextFields.length_msg(self, self.min_length, self.max_length)
        
class TextField_Description(TextFields):
    def __init__(self, name, min_length, max_length):
        super().__init__(name)
        self.min_length = min_length
        self.max_length = max_length

    def verify_validity(self, text):

        replacement = 'Message'
        blank_message = TextFields.blank_msg(self)
        length_message = TextFields.length_msg(self, self.min_length, self.max_length)
        
        blank_message = blank_message.split()
        blank_message[0] = replacement
        blank_message = (' '.join(blank_message))
        
        length_message = length_message.split()
        length_message[0] = replacement
        length_message = (' '.join(length_message))
        
        if len(text) == 0:
            return [blank_message, length_message]
        elif (len(text) >= self.min_length or len(text) <= self.max_length) and TextFields.check_any_alphanumeric(self, text) == False:
            return blank_message
        elif len(text) < self.min_length or len(text) > self.max_length:
            return length_message
