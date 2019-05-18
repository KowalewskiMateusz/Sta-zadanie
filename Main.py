import pandas as pd
import io
import requests

url = "https://www.dane.gov.pl/media/resources/20190513/Liczba_os%C3%B3b_kt%C3%B3re_przystapi%C5%82y_lub_zda%C5%82y_egzamin_maturalny.csv"
r = requests.get(url).content
data_frame = pd.read_csv(io.StringIO(r.decode('cp1250')),sep = ';')
"""print(data_frame['Przystąpiło/zdało '] == 'przystąpiło')"""

data_frame = data_frame.to_dict()
print(len(data_frame))
a=0
counter = 0
sum = 0
"""
while(a<len(data_frame)):
    if data_frame[a][0] == 'Dolnośląskie' and data_frame[a][1] == 'przystąpiło' and data_frame[a][3] == 2015 :
        sum=sum + data_frame[a][4]
        counter = counter +1
        print("a")
    a = a + 1
print(sum/counter)
"""

