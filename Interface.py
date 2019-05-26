import sys

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
                print("Jaki rok Cię interesuje?")
                year = input("")

                while 1:
                    if year.isdigit():
                        pass
                    else:
                        print("Wpisz liczbę nie wyraz")
                        year = input("")
                        continue
                    if int(year) > 2018 or int(year) < 2010:
                        print("Mam dane z lat 2010-2018. Wpisz jedną z tych dat.")
                        print("Jaki rok Cię interesuje?")
                        year = input("")
                    else:
                        break
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
            else:
                print("Prosze podać poprawno komende")