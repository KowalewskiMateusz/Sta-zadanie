import Interface
import Program


def main():
    """The main function"""

    url = "https://www.dane.gov.pl/media/resources/20190520/Liczba_os%C3%B3b_kt%C3%B3re_" \
          "przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv"  # url with csv file
    program = Program.Program(url)  # make an instance of Program class
    interface = Interface.Interface()  # make an instance of Interface class
    interface.draw_interface()  # drawing an interface
    interface.main_loop(program)  # main loop of the program


if __name__ == '__main__':  # with this line we can use that program as a script
    main()
