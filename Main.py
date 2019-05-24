import pandas as pd
import io
import requests
import sys


class Program:

    def __init__(self, url):
        r = requests.get(url).content
        self.data_frame = pd.read_csv(io.StringIO(r.decode('cp1250')), sep=';')
        self.data_frame = self.data_frame.to_dict()
        self.data_frame_length = len(self.data_frame['Terytorium'])

    def which_province(self):
        while 1:
            array = []
            j = 0
            print("Dla którego województwa chciałbyś zobaczyć wyniki?")
            province = input("")
            province = province.capitalize()
            for i in range(0, 17):
                array.append(self.data_frame['Terytorium'][j])
                if province == self.data_frame['Terytorium'][j]:
                    return province
                j = j + 37

            print("Proszę podać poprawną nazwe województwa")
            print("Oto lista wszystkich dostępnych możliwości łącznie z całą Polska: ")
            for i in range(len(array)):
                print(str(i + 1) + "." + array[i])

    @staticmethod
    def men_women(who="Wszyscy"):
        while 1:
            print("Czy chciałbyś zobaczyć rozróżnienie na płcie?(Tak/Nie)")
            sex_differentiation = input("")
            sex_differentiation = sex_differentiation.capitalize()
            if sex_differentiation == "Tak":
                while 1:
                    print("Mężczyźni czy Kobiety?(Mężczyźni/Kobiety)")
                    who = input("")
                    who = who.capitalize()
                    if who == "Mężczyźni" or who == "Kobiety":
                        return who
                    else:
                        print("Wpisz prawdiłową odpowiedź")
            elif sex_differentiation == 'Nie':
                return who
            else:
                print("Wpisz prawdiłową odpowiedź")

    def average_for_province_in_years(self, who):
        year = input("Podaj do kiedy(posiadam dane od 2010 do 2018 roku): ")
        province = self.which_province()
        loop_counter, if_counter, sums = 0, 0, 0
        while loop_counter < self.data_frame_length:
            if self.data_frame['Terytorium'][loop_counter] == province and self.data_frame['Przystąpiło/zdało '][
                loop_counter] == 'przystąpiło' and self.data_frame['Rok'][loop_counter] <= int(year):
                if who == "Mężczyźni" and loop_counter % 2 == 0:
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]
                    if_counter = if_counter + 1
                elif who == "Kobiety" and loop_counter % 2 == 1:
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]
                    if_counter = if_counter + 1
                elif who == "Wszyscy":
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]
                    if_counter = if_counter + 1
            loop_counter = loop_counter + 1
        if int(year) > 2018:
            print(
                "Wpisałeś data dla, której jeszcze nie mam wyników, wyświetlam Ci więc dane ze wszystkich zebranych dat: ")
        try:
            print(year, " - ", round(sums / if_counter, 2))
        except ZeroDivisionError:
            print("Nie mam danych z tamtych lat!")

    def percent_of_passed_exams(self, province, who):
        participate, passed, percent = [], [], []
        loop_counter = 0
        dictionary = {}

        while loop_counter < self.data_frame_length:
            if self.data_frame['Terytorium'][loop_counter] == province:
                if self.data_frame['Przystąpiło/zdało '][loop_counter] == 'przystąpiło':
                    participate.append(self.data_frame['Liczba osób'][loop_counter])
                else:
                    passed.append(self.data_frame['Liczba osób'][loop_counter])
            loop_counter = loop_counter + 1

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
        for j in range(len(percent)):
            for k in range(len(percent)):
                dictionary[str(k + 2010)] = round(percent[k], 2)
        return dictionary

    def all_states(self, who):
        dictionary = {}
        province = " "
        for i in range(self.data_frame_length):
            if province != self.data_frame['Terytorium'][i]:
                dictionary[self.data_frame['Terytorium'][i]] = [
                    self.percent_of_passed_exams(self.data_frame['Terytorium'][i], who)]
            province = self.data_frame['Terytorium'][i]
        return dictionary

    def best_state(self, year, who):
        best_province = " "
        best_value = 0
        dictionary = self.all_states(who)
        for key_1, key_2 in dictionary.items():
            for value in key_2:
                if value[year] >= best_value:
                    best_province = key_1
                    best_value = value[year]
        return best_province, best_value

    def find_regress(self, who):
        year = 2010
        array = []
        value_year_before = 0
        dictionary = self.all_states(who)
        print(dictionary)
        for key_1, key_2 in dictionary.items():
            for value in key_2:
                for inner_key, inner_value in value.items():
                    if value_year_before == 0:
                        pass
                    else:
                        array.append(round(inner_value - value_year_before, 2))
                    value_year_before = inner_value
            value_year_before = 0
        counter, next_province = 0, 0
        for i in range(0, 17):
            for j in range(0, 8):
                if array[counter] < 0:
                    print(self.data_frame['Terytorium'][next_province] + " : " + str(year + j) + " -> " + str(
                        year + j + 1))
                counter = counter + 1
            next_province = next_province + 38
            print(" ")

    def comparision(self, who):
        year = 2010
        woj_1 = self.which_province()
        woj_2 = self.which_province()
        woj_1_dict = self.percent_of_passed_exams(woj_1, who)
        woj_2_dict = self.percent_of_passed_exams(woj_2, who)
        while year <= 2018:
            if woj_1_dict[str(year)] > woj_2_dict[str(year)]:
                print(str(year) + " - " + woj_1)
            else:
                print(str(year) + " - " + woj_2)
            year = year + 1


class Interface:
    option = " "

    def draw_interface(self):
        print(" ")
        print("Witaj! Co chciałbyś zrobić?")
        print("1) Obliczyć średnią liczbę osób, które przystąpiły do egzaminu dla danego województwa na "
              "przestrzeni lat, do podanego roku włącznie")
        print("2) Obliczyć procentową zdawalność dla danego województwa na przestrzeni lat")
        print("3) Znaleźć województwo o najlepszej zdawalności w konkretnym roku")
        print("4) Znaleźć województwa, które zanotowały regresję zdawalności")
        print("5) Porównać dwa województwa pod względem zdawalności na przestrzeni lat")
        print("6) Zakończyć działanie programu")
        self.option = input()

    def main_loop(self, program):
        if self.option == "1":
            who = program.men_women()
            program.average_for_province_in_years(who)
            self.draw_interface()
        elif self.option == "2":
            who = program.men_women()
            province = self.which_province()
            dictionary = program.percent_of_passed_exams(province, who)
            for key, values in dictionary.items():
                print(str(key) + " - " + str(values) + "%")
            self.draw_interface()
        elif self.option == "3":
            year = input("Jaki rok Cię interesuje?")
            who = program.men_women()
            province, percent = program.best_state(year, who)
            print(str(province) + " - " + str(percent) + "%")
            self.draw_interface()
        elif self.option == "4":
            who = program.men_women()
            program.find_regress(who)
            self.draw_interface()
        elif self.option == "5":
            who = program.men_women()
            program.comparision(who)
            self.draw_interface()
        elif self.option == "6":
            sys.exit(0)


def main():
    url = "https://www.dane.gov.pl/media/resources/20190520/Liczba_os%C3%B3b_kt%C3%B3re_" \
          "przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv"
    program = Program(url)
    """
    interface = Interface()
    interface.draw_interface()
    interface.main_loop(program)"""


if __name__ == '__main__':
    main()
