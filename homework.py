
class Homework:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__hw = []
        self.__results = []
        from logger import Logger
        self.l = Logger(True)

    def analyze_hw(self):
        tmp = []
        operators = {'+', '-', '*', '/'}
        try:
            with open(self.__file_path) as f:
                for data_set in f.read().splitlines():
                    self.l.log_debug(1, f"reading data_set {data_set}")
                    for data in data_set.split(' '):
                        if data.isnumeric():
                            tmp.append(int(data))
                        elif data in operators:
                            tmp.append(data)
                        else:
                            continue
                    self.__hw.append(tmp)
                    tmp = []
            for line in self.__hw:
                self.l.log_debug(1, f"{line}")
            self.l.log_event(f"homework analyzation complete")
        except FileNotFoundError as e:
            self.l.log_event(f"File was not found during analyzation of homework {e}")
        except ValueError as e:
            self.l.log_event(f"ERROR: {e}")

    def setup_questions_and_answers(self):
        answer = 0
        for i in range(0, len(self.__hw[0])):
            operator = self.__hw[len(self.__hw) - 1][i]
            self.l.log_debug(0, f"the operator is {operator}")
            for j in range(0, len(self.__hw) - 1):
                if operator == '+':
                    self.l.log_debug(0, f"adding {self.__hw[j][i]} to {answer}")
                    answer += self.__hw[j][i]
                if operator == '*':
                    if answer == 0:
                        self.l.log_debug(0, f"answer is currently 0, initializing answer to {self.__hw[j][i]}")
                        answer = self.__hw[j][i]
                    else:    
                        self.l.log_debug(0, f"multiplying {self.__hw[j][i]} to {answer}")
                        answer *= self.__hw[j][i]
            self.l.log_debug(1, f"the answer for section {i} is {answer}")
            self.__results.append(answer)
            answer = 0

    def get_grand_total(self):
        grand_total = 0
        for number in self.__results:
            grand_total += number
        return grand_total