import pandas as pd
import io
import requests
import sys


class Program:
    """main class,responsible for all the functionalities"""

    def __init__(self, url):
        """constructor, download and store data in variable"""
        r = requests.get(url).content  # download data from url
        self.data_frame = pd.read_csv(io.StringIO(r.decode('cp1250')),
                                      sep=';')  # read from csv file, decode from cp1250
        self.data_frame = self.data_frame.to_dict()  # data_frame conversion to dictionary(requirements)
        self.data_frame_length = len(self.data_frame['Terytorium'])  # store the length of dictionary

    def which_province(self):
        """ The user can specify what province he is intrested in"""
        while 1:
            array = []
            j = 0
            print("Dla którego województwa chciałbyś zobaczyć wyniki?")
            province = input("")
            province = province.capitalize()  # first letter of word is capitalized
            for i in range(0, 17):
                array.append(self.data_frame['Terytorium'][j])
                if province == self.data_frame['Terytorium'][j]:  # True if province is one of the possibilities
                    return province
                j = j + 37  # every 37 position is next province in CSV file

            print("Proszę podać poprawną nazwe województwa")  # error handling
            print("Oto lista wszystkich dostępnych możliwości łącznie z całą Polska: ")
            for i in range(len(array)):  # writting all possible provinces
                print(str(i + 1) + "." + array[i])

    @staticmethod
    def men_women(who="Wszyscy"):
        """Method used for specifying which gender the user is intrested in, all people default"""
        while 1:
            print("Czy chciałbyś zobaczyć rozróżnienie na płcie?(Tak/Nie)")
            sex_differentiation = input("")
            sex_differentiation = sex_differentiation.capitalize()  # capitalize first letter for better match
            if sex_differentiation == "Tak":
                while 1:
                    print("Mężczyźni czy Kobiety?(Mężczyźni/Kobiety)")
                    who = input("")
                    who = who.capitalize()  # capitalize first letter for better match
                    if who == "Mężczyźni" or who == "Kobiety":  # true only if user choice matches possibilities
                        return who
                    else:
                        print("Wpisz prawdiłową odpowiedź")
            elif sex_differentiation == 'Nie':
                return who
            else:
                print("Wpisz prawdiłową odpowiedź")

    def average_for_province_in_years(self, who):
        """Method used for finding an average number of people who participated in exam in specified  year"""
        year = input("Podaj do kiedy(posiadam dane od 2010 do 2018 roku): ")
        province = self.which_province()  # specifying province
        loop_counter, if_counter, sums = 0, 0, 0
        while loop_counter < self.data_frame_length:
            "This will be true only if the province,the participants(everyone who took test) nad year are correct"
            if self.data_frame['Terytorium'][loop_counter] == province and self.data_frame['Przystąpiło/zdało '][
               loop_counter] == 'przystąpiło' and self.data_frame['Rok'][loop_counter] <= int(year):
                if who == "Mężczyźni" and loop_counter % 2 == 0:  # sums up number of people(depend on what user chose)
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]  # sums up the number of men
                    if_counter = if_counter + 1
                elif who == "Kobiety" and loop_counter % 2 == 1:
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]  # sums up the number of women
                    if_counter = if_counter + 1
                elif who == "Wszyscy":
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]  # sums up the number of everyone
                    if_counter = if_counter + 1
            loop_counter = loop_counter + 1
        if int(year) > 2018:  # if year is too big program prints all of the years
            print(
                "Wpisałeś date dla, której jeszcze nie mam wyników, "
                "wyświetlam Ci więc dane ze wszystkich zebranych dat: ")
        try:  # try to print data if sums!=0
            print(year, " - ", round(sums / if_counter, 2))
        except ZeroDivisionError:  # if year is too small program says "no data available "
            print("Nie mam danych z tamtych lat!")

    def percent_of_passed_exams(self, province, who):
        """
        Method that returns a nested dictionary of provinces as keys and years as second keys, every years has a
        percent of people who managed to pass it
        """
        participate, passed, percent = [], [], []
        loop_counter = 0
        dictionary = {}

        while loop_counter < self.data_frame_length:
            if self.data_frame['Terytorium'][loop_counter] == province:  # if province is right
                if self.data_frame['Przystąpiło/zdało '][loop_counter] == 'przystąpiło':  # if took part==True
                    participate.append(self.data_frame['Liczba osób'][loop_counter])  # append everyone who took part
                else:
                    passed.append(self.data_frame['Liczba osób'][loop_counter])  # append only those who passed exam
            loop_counter = loop_counter + 1

        # this block of code is responsible of dividing people into men/women/everyone according to user choice

        if who == "Mężczyźni":
            for i in range(len(participate)):
                if i % 2 == 0:
                    percent.append(passed[i] / participate[i] * 100)
        elif who == "Kobiety":
            for i in range(len(participate)):
                if i % 2 == 1:
                    percent.append(passed[i] / participate[i] * 100)
        elif who == "Wszyscy":
            for i in range(len(participate)):
                if i % 2 == 0:
                    percent.append((passed[i] + passed[i + 1]) / (participate[i] + participate[i + 1]) * 100)
        for j in range(len(percent)):  # make a nested dictionary with chosen group of people in all years
            for k in range(len(percent)):
                dictionary[str(k + 2010)] = round(percent[k], 2)
        return dictionary  # return that dictionary

    def all_states(self, who):
        """
        Method that return a nested dictionary of every province percent of those who passed
        an exam in every year. U can specify which group of people u are interested in men/women/everyone.
        Simply loop over every data possible and add the matching data to dictionary.
         """
        dictionary = {}
        province = " "
        for i in range(self.data_frame_length):
            if province != self.data_frame['Terytorium'][i]:
                dictionary[self.data_frame['Terytorium'][i]] = [
                    self.percent_of_passed_exams(self.data_frame['Terytorium'][i], who)]
            province = self.data_frame['Terytorium'][i]
        return dictionary  # return dictionary that just has been made

    def best_state(self, year, who):
        """
        Method that returns the best province in which the percent of people who
        passed exam is the biggest in certain year
        """
        best_province = " "
        best_value = 0
        dictionary = self.all_states(who)  # made dictionary of people who passed in all years
        for key_1, key_2 in dictionary.items():  # loop over dictionary
            for value in key_2:  # loop over list inside dictionary
                if value[year] >= best_value:  # find the best province and percent of people who passed in certain year
                    best_province = key_1
                    best_value = value[year]
        return best_province, best_value  # return it

    def find_regress(self, who):
        """Method that is looking for regress in percent of people who passed an exam in current year and year before"""
        year = 2010
        array = []
        value_year_before = 0
        dictionary = self.all_states(who)  # dictionary of all provinces in all years
        print(dictionary)
        for key_1, key_2 in dictionary.items():  # looping over dictionary
            for value in key_2:  # looping over dictionary inside list inside dictionary
                for inner_key, inner_value in value.items():  # loop over dictionary inside list inside dictionary
                    if value_year_before == 0:
                        pass
                    else:
                        array.append(round(inner_value - value_year_before, 2))  # append the difference beetwen
                    value_year_before = inner_value  # current year and year before
            value_year_before = 0
        counter, next_province = 0, 0
        for i in range(0, 17):  # printing the values in right way with the right provinces
            for j in range(0, 8):  # if the difference is <0 than there is a regress beetwen
                if array[counter] < 0:  # current year and the one before
                    print(self.data_frame['Terytorium'][next_province] + " : " + str(year + j) + " -> " + str(
                        year + j + 1))
                counter = counter + 1
            next_province = next_province + 38  # every 38 position there is next province in csv file
            print(" ")

    def comparision(self, who):
        """Method that compare the percent of people who passed an exam in 2 provinces in through all years"""
        year = 2010
        woj_1 = self.which_province()  # first province
        woj_2 = self.which_province()  # second province
        woj_1_dict = self.percent_of_passed_exams(woj_1, who)  # dictionary of people who passed an exam in province 1
        woj_2_dict = self.percent_of_passed_exams(woj_2, who)  # dictionary of people who passed an exam in province 2
        while year <= 2018:
            if woj_1_dict[str(year)] > woj_2_dict[str(year)]:  # compare every year and choose better province
                print(str(year) + " - " + woj_1)  # printing winner for every year
            else:
                print(str(year) + " - " + woj_2)
            year = year + 1


class Interface:
    """
    Interface that control all of the user actions and high logic of the program
    """

    option = " "

    def draw_interface(self):
        """Method that print menu"""

        print(" ")
        print("Witaj! Co chciałbyś zrobić?")
        print("1) Obliczyć średnią liczbę osób, które przystąpiły do egzaminu dla danego województwa na "
              "przestrzeni lat, do podanego roku włącznie")
        print("2) Obliczyć procentową zdawalność dla danego województwa na przestrzeni lat")
        print("3) Znaleźć województwo o najlepszej zdawalności w konkretnym roku")
        print("4) Znaleźć województwa, które zanotowały regresję zdawalności")
        print("5) Porównać dwa województwa pod względem zdawalności na przestrzeni lat")
        print("6) Zakończyć działanie programu")
        self.option = input()  # user choice of action

    def main_loop(self, program):
        """
        That is a main loop of the program, every action is started here, it calls out all of the program features
        """
        while 1:
            if self.option == "1":  # Option for finding an average number of
                who = program.men_women()  # people who participated in exam in specified  year
                program.average_for_province_in_years(who)
                self.draw_interface()
            elif self.option == "2":  # Option for finding a percent of those who passed in specified province
                who = program.men_women()  # through all the years
                province = program.which_province()
                dictionary = program.percent_of_passed_exams(province, who)
                for key, values in dictionary.items():
                    print(str(key) + " - " + str(values) + "%")
                self.draw_interface()
            elif self.option == "3":  # Option for finding the best province in certain year
                year = input("Jaki rok Cię interesuje?")
                who = program.men_women()
                province, percent = program.best_state(year, who)
                print(str(province) + " - " + str(percent) + "%")
                self.draw_interface()
            elif self.option == "4":  # Option for finding regress in exam result in certain province
                who = program.men_women()
                program.find_regress(who)
                self.draw_interface()
            elif self.option == "5":  # Option for comparing two province(in exam passing content)
                who = program.men_women()
                program.comparision(who)
                self.draw_interface()
            elif self.option == "6":  # Exit the program
                sys.exit(0)


def main():
    """The main function"""

    url = "https://www.dane.gov.pl/media/resources/20190520/Liczba_os%C3%B3b_kt%C3%B3re_" \
          "przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv"  # url with csv file
    program = Program(url)  # make an instance of Program class
    interface = Interface()  # make an instance of Interface class
    interface.draw_interface()  # drawing an interface
    interface.main_loop(program)  # main loop of the program


if __name__ == '__main__':  # with this line we can use that program as a script
    main()
