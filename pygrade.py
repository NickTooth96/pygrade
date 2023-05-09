import datetime
import os
import sys
import getopt
import time
import toml


__VERSION__ = "1.3.0"
__AUTHOR__ = "Nicholas Toothaker"

no_arg = "ERROR: No arguments given"
versionMSG = "Version " + __VERSION__ + " by " + __AUTHOR__

class Course_Grade:

    course_grade_catagories = {}
    total_grade = 0
    course_name = ""

    def __init__(self, data):
        for element in data:
            if element == "course_name":
                self.course_name = data[element]
            else: 
                self.course_grade_catagories[element] = data[element]
        attempted = 0
        for element in self.course_grade_catagories:
            grade = 0
            self.course_grade_catagories[element]["catagory_name"] = element             
            if (self.course_grade_catagories[element]["possible_score"] == 0):
                grade = 0
            else:
                grade = self.course_grade_catagories[element]["current_score"] / self.course_grade_catagories[element]["possible_score"] 
                self.course_grade_catagories[element]["catagory_score"] = grade * 100
                grade = grade * self.course_grade_catagories[element]["percentage"]
                attempted += self.course_grade_catagories[element]["percentage"]
            self.total_grade += grade
            
        self.total_grade = round((self.total_grade / attempted) * 100,2)
    
    def get_greatest_length(self):
        great_length = 0
        for x in self.course_grade_catagories:
            if len(x) > great_length:
                great_length = len(x) + 4
        if great_length < 16:
            great_length = 16
        return great_length

    def grade_to_string(self):
        output = ""
        i = 0
        num = self.get_greatest_length()
        barrier = ""
        while i < (num + 6): 
            barrier += "-"
            i += 1
        num_as_str = str(num + 4)
        output += self.course_name + "\n"
        output += barrier + "\n"
        for element in self.course_grade_catagories:
            out = ""
            if self.course_grade_catagories[element]["possible_score"] != 0:
                out += self.course_grade_catagories[element]["catagory_name"] + format(": ",num_as_str) 
                out = out[:num]
                if len(str(round(self.course_grade_catagories[element]["catagory_score"], 2))) < 5 and str(round(self.course_grade_catagories[element]["catagory_score"], 2))[-1] == "0":
                    out += str(round(self.course_grade_catagories[element]["catagory_score"], 2)) + "0%\n"
                else:
                    out += str(round(self.course_grade_catagories[element]["catagory_score"], 2)) + "%\n"

            else:
                out += self.course_grade_catagories[element]["catagory_name"] + format(": ",num_as_str) 
                out = out[:num]
                out += "N/A\n"
            output += out
        output += barrier + ("\nTotal"  + format(": ",num_as_str))[:num + 1] + str(self.total_grade) + "%"
        return output

    def generate_textfile(self):
        time = {0:"h",1:"m",2:"s"}
        input = str(datetime.datetime.now())
        i = 0
        text_output_filename = ""
        for element in input:
            if element != " ":
                if element != ":":
                    if element != ".":
                        text_output_filename += element
                    else: 
                        text_output_filename += str(time[i])
                        break
                else:
                    text_output_filename += str(time[i])
                    i += 1 
            else:   
                text_output_filename += "_" 
        path = "output/" + text_output_filename + ".txt"
        f = open(path, "x")
        contents = self.grade_to_string()
        f.write(contents)


def config_file(filepath=None):
        if filepath:
            data = toml.load(filepath,_dict=dict)
        else:
            data = toml.load("config.toml", _dict=dict)
        newCG = Course_Grade(data)
        return newCG

def command_line():
    sum = 0
    course_grade_catagories = {}
    while sum < 100 :    
        user_input_catagory = input("Please Enter a catagory: ")
        user_input_percentage = int(input("Please Enter Final Grade Percentage: "))
        if user_input_percentage + sum > 100:
            print("ERROR: Course Grade Greater than 100")
            answer = input("Disregard and continue? [Y/N] ")
            if answer in "yY":
                course_grade_catagories[user_input_catagory] = user_input_percentage
                break
            elif answer in "Nn":
                print("Enter Valid Input")
        course_grade_catagories[user_input_catagory] = user_input_percentage
        sum += user_input_percentage
        print(sum)
    print(course_grade_catagories)
    newCG = Course_Grade(course_grade_catagories)
    return newCG


arglist = sys.argv[1:]
options = "hcfp:v"
long_options = ["Help", "File", "Commandline"]
start_time = time.time()

if len(arglist) < 1:
    print(no_arg)
    raise SystemExit

try: 
    arguments, values = getopt.getopt(arglist, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-f", "--File"):
            cg = config_file()
            cg.generate_textfile()
            print(cg.grade_to_string())
            end_time = time.time()
            print(f"Runtime:    {end_time - start_time:.2f} seconds")
        elif currentArgument in ("-p", "--filepath"):
            cg = config_file(arglist[1])
            cg.generate_textfile()
            print(cg.grade_to_string())
            end_time = time.time()
            print(f"Runtime:    {end_time - start_time:.2f} seconds")
        elif currentArgument in ("-c", "--Commandline"):
            cg = command_line()
            cg.generate_textfile()
            print(cg.grade_to_string())
            end_time = time.time()
            print(f"Runtime:    {end_time - start_time:.2f} seconds")
        elif currentArgument in ("-h", "--Help"):
            path = os.path.join(os.path.dirname(__file__), ".help.txt")
            f = open(path,"r")
            for line in f:
                print(line, end="")
        elif currentArgument in ("-v","--version"):
                print(versionMSG)
except getopt.error as err:
    print(str(err))

# print(cg.course_grade_catagories)
# print(cg.total_grade)
# print(cg.course_grade_catagories["HWs"]["catagory_score"])
# print()
# print(type(cg.get_greatest_length()))
# print(cg.get_greatest_length())
# print()
