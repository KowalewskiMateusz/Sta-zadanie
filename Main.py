import pandas as pd
import io
import requests


class Program:
    data_frame = 0
    data_frame_dlugosc = 0

    def __init__(self, url):
        r = requests.get(url).content
        self.data_frame = pd.read_csv(io.StringIO(r.decode('cp1250')), sep=';')
        self.data_frame = self.data_frame.to_dict()
        self.data_frame_dlugosc = len(self.data_frame['Terytorium'])

    def mezczynza_kobieta(self, kto="wszyscy"):
        czy_rozróżniać = input("Czy chciałbyś zobaczyć rozróżnienie na płcie?(Tak/Nie) ")
        if (czy_rozróżniać == "Tak"):
            kto = input("mężczyźni czy kobiety?")
            return (kto)
        else:
            return (kto)

    def average_for_state_in_years(self, kto):
        rok = input("Podaj do kiedy: ")
        wojewodztwo = input("Podaj województwo: ")
        loop_counter, if_counter, sums = 0, 0, 0
        while loop_counter < self.data_frame_dlugosc:
            if self.data_frame['Terytorium'][loop_counter] == wojewodztwo and self.data_frame['Przystąpiło/zdało '][
                loop_counter] == 'przystąpiło' and self.data_frame['Rok'][loop_counter] <= int(rok):
                if kto == "mężczyźni" and loop_counter % 2 == 0:
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]
                    if_counter = if_counter + 1
                elif kto == "kobiety" and loop_counter % 2 == 1:
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]
                    if_counter = if_counter + 1
                elif kto == "wszyscy":
                    sums = sums + self.data_frame['Liczba osób'][loop_counter]
                    if_counter = if_counter + 1
            loop_counter = loop_counter + 1
        print(rok, " - ", sums / if_counter)

    def percent_of_passed_exams(self, wojewodztwo, kto):
        przystopilo, zdalo, percent = [], [], []
        zdalo = []
        loop_counter = 0
        dict = {}

        while loop_counter < self.data_frame_dlugosc:
            if self.data_frame['Terytorium'][loop_counter] == wojewodztwo:
                if self.data_frame['Przystąpiło/zdało '][loop_counter] == 'przystąpiło':
                    przystopilo.append(self.data_frame['Liczba osób'][loop_counter])
                else:
                    zdalo.append(self.data_frame['Liczba osób'][loop_counter])
            loop_counter = loop_counter + 1

        if kto == "mężczyźni":
            for i in range(len(przystopilo)):
                if i % 2 == 0:
                    percent.append(zdalo[i] / przystopilo[i] * 100)
        elif kto == "kobiety":
            for i in range(len(przystopilo)):
                if i % 2 == 1:
                    percent.append(zdalo[i] / przystopilo[i] * 100)
        elif kto == "wszyscy":
            for i in range(len(przystopilo)):
                if i % 2 == 0:
                    percent.append((zdalo[i] + zdalo[i + 1]) / (przystopilo[i] + przystopilo[i + 1]) * 100)
        for j in range(len(percent)):
            for k in range(len(percent)):
                dict[str(k + 2010)] = round(percent[k], 2)
        return dict

    def all_states(self, kto):
        dict = {}
        list_of_states = [""]
        terytorium = " "
        for i in range(self.data_frame_dlugosc):
            if terytorium != self.data_frame['Terytorium'][i]:
                dict[self.data_frame['Terytorium'][i]] = [
                    Program.percent_of_passed_exams(self.data_frame['Terytorium'][i], kto)]
            terytorium = self.data_frame['Terytorium'][i]
        return dict

    def best_state(self, rok):
        kto = "kobiety"
        najlepsze_wojewodztwo = " "
        najlepsza_wartosc = 0
        dict = self.all_states(kto)
        for key_1, key_2 in dict.items():
            for value in key_2:
                if value[rok] >= najlepsza_wartosc:
                    najlepsze_wojewodztwo = key_1
                    najlepsza_wartosc = value[rok]
        return najlepsze_wojewodztwo, najlepsza_wartosc

    def find_regres(self):
        rok = 2010
        list = []
        value_year_before = 0
        dict = self.all_states("wszyscy")
        for key_1, key_2 in dict.items():
            for value in key_2:
                for inner_key, inner_value in value.items():
                    if (value_year_before == 0):
                        pass
                    else:
                        list.append(round(inner_value - value_year_before, 2))
                    value_year_before = inner_value
            value_year_before = 0
        k,l = 0,0
        for i in range(0, 17):
            for j in range(0, 8):
                if list[k] < 0:
                    print(self.data_frame['Terytorium'][l] + " : " + str(rok + j) + " -> " + str(rok + j + 1))
                k = k + 1
            l = l+38



url = "https://www.dane.gov.pl/media/resources/20190520/Liczba_os%C3%B3b_kt%C3%B3re_przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv"
Program = Program(url)
Program.find_regres()
