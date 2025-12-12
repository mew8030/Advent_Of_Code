
class Homework:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__hw = []
        self.__results = []
        from logger import Logger
        self.l = Logger(True)

    def analyze_hw(self):
        tmp = []
        zipped = []
        operators = {'+', '-', '*', '/'}
        try:
            with open(self.__file_path) as f:
                for data_set in f.read().splitlines():
                    self.l.log_debug(1, f"reading data_set {data_set}")
                    
                    self.__hw.append(data_set)

                self.l.log_event(f"zipping the list")
                zipped = list(zip(*self.__hw[:-1]))
                self.l.log_event(f"extracting the operators")
                ops = list("".join(self.__hw[-1:]))
                self.l.log_event(f"clearing the homework analysis to make room for cephlapod method")
                for i in range(0, len(self.__hw)):
                    self.__hw[i] = []
                self.l.log_event(f"clearing unneeded spaces on list for operators")
                while ' ' in ops:
                    ops.remove(' ')
                self.l.log_debug(0, f"getting the list of operators {ops}")
                self.l.log_debug(0, f"the homework analysis should be cleared self.__hw {self.__hw}")
                self.l.log_event(f"setting up values for analysis after being zipped")
                i = 0
                for z in zipped:
                    z = "".join(z).replace(' ', '')
                    self.l.log_debug(0, f"getting data from zipped list {z}")
                    if z != '':
                        self.__hw[i].append(int(z))
                        i += 1
                    elif z == '':
                        i = self.insert_empty(i)
                while i != 0:
                    i = self.insert_empty(i)
                self.__hw[len(self.__hw) - 1] = ops

            self.l.log_debug(1, f"Setup complete, displaying analysis")
            for line in self.__hw:
                self.l.log_debug(1, f"{line}")
            self.l.log_event(f"homework analyzation complete")
        except FileNotFoundError as e:
            self.l.log_event(f"File was not found during analyzation of homework {e}")
        except ValueError as e:
            self.l.log_event(f"ERROR: {e}")


    def insert_empty(self, i):
        while i < len(self.__hw) - 1:
            self.__hw[i].append([])
            i += 1
        return 0


    def setup_questions_and_answers(self):
        answer = 0
        for i in range(0, len(self.__hw[0])):
            operator = self.__hw[len(self.__hw) - 1][i]
            self.l.log_debug(0, f"the operator is {operator}")
            for j in range(0, len(self.__hw) - 1):
                if self.__hw[j][i] == []:
                    continue
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