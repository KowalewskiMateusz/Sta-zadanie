import Interface
import Main
import Program

def who(): #test example testing best_province function
    a,b = program.best_state("2010", "Wszyscy")
    assert a == "Kujawsko-pomorskie"
    assert b == 82.87


url = "https://www.dane.gov.pl/media/resources/20190520/Liczba_os%C3%B3b_kt%C3%B3re_" \
          "przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv"
program = Main.Program(url)


who()