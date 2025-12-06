
class Invalid_ids:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__id_ranges = []
        self.__sum_invalid_ids = 0
        self.tmpstr = ""
        from logger import Logger
        self.log = Logger(False)
        self.get_ids()

    
    def get_ids(self):
        self.log.log_event("getting ids from file")
        with open(self.__file_path) as f:
            self.log.log_event("organizing ids into a managable container")
            self.organize_ids(f.read().strip())

    def list_id_ranges(self):
        pass

    def organize_ids(self, ranges):
        for id_range in ranges.split(','):
            id_range = id_range.strip()
            self.log.log_event(f"extracting {id_range}")
            low, high = id_range.split('-')
            self.__id_ranges.append((low, high))
        self.log.log_event(f"EXTRACTION COMPLETE")

    def find_invalid_ids(self):
        self.log.log_event("searching for invalid ids")
        for l, h in self.__id_ranges:
            for i in range (int(l), int(h) + 1):
                str_conversion = str(i)
                self.log.log_event(f"checking number {str_conversion}")
                self.tmpstr = ""

                for num_char in str_conversion:
                    self.tmpstr += num_char
                    if len(str_conversion) > 1 and len(str_conversion) % len(self.tmpstr) == 0 and not len(self.tmpstr) > len(str_conversion)/2:
                        index = 0
                        same_flag = True
                        while index + len(self.tmpstr) <= len(str_conversion) and same_flag == True:
                            self.log.log_event(f"checking if {self.tmpstr} matches {str_conversion[index: index + len(self.tmpstr)]}")
                            if self.tmpstr == str_conversion[index: index + len(self.tmpstr)]:
                                self.log.log_event(f"{self.tmpstr} == {str_conversion[index: index + len(self.tmpstr)]} so far so good")
                                index += len(self.tmpstr)
                                continue
                            else:
                                self.log.log_event(f"{self.tmpstr} doesn't match {str_conversion[index: index + len(self.tmpstr)]}")
                                same_flag = False
                                break

                        if same_flag == True:
                            self.__sum_invalid_ids += i
                            self.log.log_event(f"invalid id {i} found, sum total is {self.__sum_invalid_ids}")
                            break
        self.log.log_event(f"Found number of invalid ids to be: {self.__sum_invalid_ids}")
    """
    if len(str_conversion) % 2 == 0:
        cut_here = len(str_conversion) // 2
        if str_conversion[:cut_here] == str_conversion[cut_here:]:
            self.__sum_invalid_ids += i
            self.log.log_event(f"invalid id {i} found, sum total is {self.__sum_invalid_ids}")
    """
