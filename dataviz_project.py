import streamlit as st
import pandas as pd
import altair as alt


selected_fields = ['type_de_reglementation', 'thematique', 'zone', 'reglementations', 'wkt']

data_set = pd.read_csv(r'C:\Users\lebre\Documents\Data_visualisation\Project\Data\Louis_Le_Breton_viz\statistiques-de-controle-des-peches.csv')
data_set['date'] = pd.to_datetime(data_set['control_year'].astype(str) + '-' + data_set['control_month'].astype(str), format='%Y-%m')


selected_facades = ['SA', 'NAMO', 'MEMN', 'MED']
selected_control_type = 'SEA_CONTROL'

filtered_data = data_set[(data_set['facade'].isin(selected_facades)) & (data_set['control_type'] == selected_control_type)]

zone_month_control_data = filtered_data.groupby(['facade', 'control_month'])['number_controls'].sum().reset_index()

st.set_page_config(
    page_title="Statistiques de contrôle des pêches en France métropolitaine",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Les contrôles des pêches maritimes en France métropolitaine')

selected_page = st.sidebar.selectbox(
    'Sélectionner la page',
    ('Accueil', 'Statistiques par façade maritime', 'Statistiques temporels', 'Statistiques par mois et par zone')
)

if selected_page == 'Accueil':
    st.write("""
Voici une collection de graphiques montrant la corrélation négative entre le nombre de contrôles maritimes et le taux d'infraction dans les mers entourant la France métropolitaine.
""")
    st.write("Sélectionnez la page que vous souhaitez afficher dans la barre latérale.")

    chart = alt.Chart(zone_month_control_data).mark_bar().encode(
        x=alt.X('control_month:N', title='Mois de contrôle'),
        y=alt.Y('number_controls:Q', title='Nombre de contrôles'),
        color=alt.Color('facade:N', title='Zone')
    ).properties(
        title='Nombre de contrôles par mois de l\'année pour chaque zone',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

elif selected_page == 'Statistiques temporels':
    st.write("Statistiques en fonction du temps")
    st.write("Nombre de contrôles au fil du temps")
    chart_controls = alt.Chart(filtered_data).mark_bar().encode(
        x='date:T',
        y=alt.Y('number_controls:Q', title='Nombre de contrôles'),
        color='number_controls:Q'
    )
    st.altair_chart(chart_controls, use_container_width=True)
    
    st.write("Taux d'infraction au fil du temps")
    chart_infraction = alt.Chart(filtered_data).mark_bar().encode(
        x='date:T',
        y=alt.Y('infraction_rate:Q', title='Taux d\'infraction'),
        color='infraction_rate:Q'
    )
    st.altair_chart(chart_infraction, use_container_width=True)

elif selected_page == 'Statistiques par façade maritime':
    st.write("Statistiques façade maritime")
    
    st.write("Taux d'infraction en fonction de la zone")
    zone_infraction_data = filtered_data.groupby('facade')['infraction_rate'].mean().reset_index()
    chart_zone_infraction = alt.Chart(zone_infraction_data).mark_bar().encode(
        x='facade:N',
        y=alt.Y('infraction_rate:Q', title='Taux d\'infraction'),
        color='facade:N'
    )
    st.altair_chart(chart_zone_infraction, use_container_width=True)

    st.write("Nombre de contrôles en fonction de la façade maritime")
    facade_control_data = filtered_data.groupby('facade')['number_controls'].sum().reset_index()
    chart_facade_control = alt.Chart(facade_control_data).mark_bar().encode(
        x='facade:N',
        y=alt.Y('number_controls:Q', title='Nombre de contrôles'),
        color='facade:N'
    )
    st.altair_chart(chart_facade_control, use_container_width=True)

elif selected_page == 'Statistiques par mois et par zone':
    st.write("Statistiques par mois et par zone")
    selected_facade = st.selectbox('Façade maritime', selected_facades)
    st.write(f"Statistiques pour la façade : {selected_facade}")
    
    subset = filtered_data[filtered_data['facade'] == selected_facade]

    st.write("Nombre de contrôles par mois")
    chart_controls = alt.Chart(subset).mark_bar().encode(
        x=alt.X('control_month:N', title='Mois'),
        y=alt.Y('number_controls:Q', title='Nombre de contrôles'),
        color='control_month:N'
    )
    st.altair_chart(chart_controls, use_container_width=True)

    st.write("Taux d'infraction par mois")
    chart_infraction = alt.Chart(subset).mark_bar().encode(
        x=alt.X('control_month:N', title='Mois'),
        y=alt.Y('infraction_rate:Q', title='Taux d\'infraction'),
        color='control_month:N'
    )
    st.altair_chart(chart_infraction, use_container_width=True)
    st.write('Test blababa')
