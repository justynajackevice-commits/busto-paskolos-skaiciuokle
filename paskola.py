import streamlit as st
import pandas as pd #paskolos likučio duomenis atvaizduoti reikalinga Pandas. Kiekvieniems paskolos metams sukursiu lentelę

st.title('Būsto paskolos grąžinimo skaičiuoklė')
st.header('Įvedami duomenys')

namo_verte=st.number_input(
    'Namo vertė',
    min_value=0.0,
    value=100000.0,
    step =1500.0
)
pradinis_inasas=st.number_input(
    'Pradinis įnašas',
    min_value=0.0,
    value=30000.0,
    step=1000.0
)

palukanu_norma=st.number_input(
    'Palūkanų norma(proc.)',
    min_value=0.0,
    value=3.5,
    step=0.1
)

paskolos_terminas=st.number_input(
   'Paskolos terminas (metai)',
   min_value=15,
   max_value=50,
   value=30,
   step=1 
)

paskolos_suma = namo_verte - pradinis_inasas
menesine_palukanu_norma = palukanu_norma / 100 / 12
menesiu_skaicius = paskolos_terminas * 12


if menesine_palukanu_norma > 0:
    menesine_imoka = (
        paskolos_suma
        * menesine_palukanu_norma
        * (1 + menesine_palukanu_norma) ** menesiu_skaicius
        / ((1 + menesine_palukanu_norma) ** menesiu_skaicius - 1)
    )
else:
    menesine_imoka = paskolos_suma / menesiu_skaicius

#st.write('Mėnesinė įmoka:', round(menesine_imoka,2),'Eur')


bendra_grazinama_suma=menesine_imoka*menesiu_skaicius
bendros_palukanos=bendra_grazinama_suma-paskolos_suma

st.header('Įmokos')
st.metric('Mėnesinė įmoka',f'{menesine_imoka:.2f} Eur')
st.metric("Bendra grąžinama suma", f"{bendra_grazinama_suma:.2f} Eur")
st.metric("Bendros palūkanos", f"{bendros_palukanos:.2f} Eur")

likutis = paskolos_suma
metai = [0]
likuciai = [paskolos_suma]

for menuo in range(1, menesiu_skaicius + 1):
    menesio_palukanos = likutis * menesine_palukanu_norma
    grazinama_paskolos_dalis = menesine_imoka - menesio_palukanos
    likutis = likutis - grazinama_paskolos_dalis

    if menuo % 12 == 0:
        metai.append(menuo // 12)
        likuciai.append(max(likutis, 0))


#Pandas sukuria lentelę, o po to naudosiu linechart
grafiko_duomenys = pd.DataFrame({
    "Metai": metai,
    "Paskolos likutis": likuciai
})

st.header("Mokėjimų grafikas")
st.line_chart(
    grafiko_duomenys,
    x='Metai',
    y='Paskolos likutis'
)


