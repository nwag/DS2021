class ForgottenList:
    def __init__(self, pers_list):
        self.pers_list = pers_list
        self.speech_output = ""

    def generate_speech_output_forgotten_list(self):
        if self.pers_list:
            speech_output = "Vergesse heute nicht "
            c = 0
            if len(self.pers_list) == 1:
                speech_output += self.pers_list[0] + "."
            else:
                for element in self.pers_list:
                    c += 1
                    if c < len(self.pers_list):
                        speech_output += element + ", "
                    else:
                        speech_output = speech_output[:-2] + " und " + element + "."
            self.speech_output = speech_output
        else:
            self.speech_output = "Deine Liste ist leer."

    def add_element(self, element):
        self.pers_list.append(str(element))

    def remove_element(self, element):
        try:
            self.pers_list.remove(str(element))
        except ValueError:
            pass