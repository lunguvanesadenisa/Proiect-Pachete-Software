import pandas as pd
import matplotlib.pyplot as plt

#6. importul unei fișier csv sau json în pachetul pandas;
#12.prelucrări statistice, gruparea și agregarea datalor în pachetul pandas;
#13.prelucrarea seturilor de date cu merge / join;

df = pd.read_csv('SET_DE_DATE_WALMART_PS.csv')
df1 = pd.read_csv('SET_DE_DATE_WALMART_PS_2.csv')

jonctiune = pd.merge(df,
                  df1[['Store','Fuel_Price']],
                  on='Store')

print(jonctiune)

print('------'*20)

print(jonctiune.groupby("Store").agg({
    "Fuel_Price": "mean",
    "Weekly_Sales": "max",
    "Temperature": ["min","max"]
}))

#9. utilizarea funcțiilor de grup;
#7. accesarea datelor cu loc și iloc;
#14.reprezentare grafică a datelor cu pachetul matplotlib;
#1. utilizarea listelor și a dicționarelor, incluzând metode specifice acestora;
print('------'*20)
print(jonctiune.loc[jonctiune['Store'].isin([5, 2]),['Store','Unemployment']])

plot=jonctiune.groupby('Store')['Weekly_Sales'].sum()
plot.sort_values().plot(kind='bar')
plt.title("Magazinele in functie de totalul vanzarilor saptamanale")
plt.show()

print('------'*20)
print(jonctiune.iloc[:20])

#3. definirea și apelarea unor funcții;
def pret_mediu_combustibil(store_id):
    store_data = jonctiune[jonctiune["Store"] == store_id]
    return round(store_data["Fuel_Price"].mean(), 2)

print('------'*20)
print("Media pretului pentru magazinul 8:", pret_mediu_combustibil(8))

#10.tratarea valorilor lipsă;
print('------'*20)
if jonctiune["Fuel_Price"].isnull().any():
    jonctiune["Fuel_Price"].fillna(jonctiune["Fuel_Price"].mean(), inplace=True)
    print("Valorile lipsa au fost inlocuite cu media.")
else:
    print("Nu exista valori lipsa.")

#5. utilizarea structurilor repetitive;
print('------'*20)
total_vanzari = 0
for vanzari in jonctiune['Weekly_Sales']:
    total_vanzari += vanzari
print(f"Totalul vanzarilor: {total_vanzari}")

#4. utilizarea structurilor condiționale;
print('------'*20)
jonctiune2=jonctiune.loc[(jonctiune['Store']==10)]
print (jonctiune2)
print('------'*20)

for pret in jonctiune2['Fuel_Price']:
    if pret >3 :
        print("Pretul combustibilului este ridicat.")
    elif pret <2.5:
        print("Pretul combustibilului este scazut.")
    else:
        print(f"Pretul combustibilului este standard.")

#8. modificarea datelor în pachetul pandas;
#11.ștergerea de coloane și înregistrări;

print('------'*20)
jonctiune['Weekly_Sales_2'] = jonctiune['Weekly_Sales'] / 1000
print(jonctiune.loc[(jonctiune['Store']==5)])
jonctiune.loc[(jonctiune['Store']==5),'Weekly_Sales']=jonctiune.loc[(jonctiune['Store']==5),'Weekly_Sales']*1.1
jonctiune.loc[(jonctiune['Store']==5),'Weekly_Sales_2']=jonctiune.loc[(jonctiune['Store']==5),'Weekly_Sales_2']*1.1
print(jonctiune.loc[(jonctiune['Store']==5)])
print('------'*20)
jonctiune.drop(columns=['Holiday_Flag'], inplace=True)
jonctiune = jonctiune[jonctiune['Weekly_Sales'] >= 1000]
print(jonctiune)

#2.utilizarea seturilor și a tuplurilor, incluzând metode specifice acestora;
print('------'*20)
set_temperaturi = set(zip(jonctiune['Date'], jonctiune['Temperature']))
print("Temperaturile în zilele respective:", set_temperaturi)

print('------'*20)
tuplu = (int(jonctiune.loc[1, 'Store']),jonctiune.loc[1, 'Date'], float(jonctiune.loc[1, 'Weekly_Sales']))
print("Magazinul a inregistrat vanzari saptamanale pana in ziua respectiva in valoare de:", tuplu)

#15.utilizarea pachetului scikit-learn (clusterizare, regresie logistică)
#16.utilizarea pachetului statmodels (regresie multiplă).

from sklearn.cluster import KMeans
print('------'*20)
clusterizare = jonctiune[['Weekly_Sales', 'Unemployment']].dropna()

kmeans = KMeans(n_clusters=3, random_state=0)
jonctiune.loc[clusterizare.index, 'Cluster'] = kmeans.fit_predict(clusterizare)
print(jonctiune[['Weekly_Sales', 'Unemployment', 'Cluster']])


import statsmodels.api as sm
print('------'*20)

X = df[['Unemployment', 'Temperature']].dropna()
y = df['Weekly_Sales'].loc[X.index]

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

print(model.summary())