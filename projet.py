########################################## import part ###################################################

import streamlit as st
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from time import time


start_time  = time()




##################### define function for modeling the dataframe #######################################

def count_rows(rows):
    return len(rows)
def get_hour(dt):
    return (dt.hour)
def get_months(dt):
    return dt.month
def get_years(dt):
    return dt.year
def get_minutes(dt):
    return dt.minute
def get_weekday(dt):
    return dt.weekday()

def title_without_saison(title):
    titre = ''
    for i in title:
        if (i == ':'):
            print(titre)
            return titre
        titre = titre + i
    print(titre)
    return titre

######################## define function for diferent plot ############################################


@st.cache(allow_output_mutation = True, suppress_st_warning=True)
def load_df(name):
    df = pd.read_csv(name)
    df["Start Time"] = df["Start Time"].map(pd.to_datetime)
    df["time_watch"] = pd.to_timedelta(df["Duration"])
    df["hour"] = df["Start Time"].map(get_hour)
    df["month"] = df["Start Time"].map(get_months)
    df["year"] = df["Start Time"].map(get_years)
    df["weekday"] = df["Start Time"].map(get_weekday)
    df['Title_without_saison'] = df['Title'].apply(title_without_saison)
    return df

@st.cache(allow_output_mutation = True)
def get_l_profile(df):
    by_profile = df.groupby('Profile Name').apply(count_rows)
    profile = by_profile.to_frame()
    profile = profile.index
    l_profile = []
    for i in profile:
        l_profile.append(i)
    return l_profile






@st.cache(allow_output_mutation = True)
def get_time_wath_by_profile(df):
    time_wath_by_profile = df.groupby('Profile Name')["time_watch"].sum()
    time_wath_by_profile = time_wath_by_profile.to_frame()
    time_wath_by_profile["time_watch"] = time_wath_by_profile["time_watch"].apply(lambda x: x.days)
    return time_wath_by_profile


@st.cache(allow_output_mutation = True)
def get_data_2020_2021_month(df):
    data = df[df["Profile Name"] == "Romain"]
    data_2020 = data[data["year"] == 2020]
    data_2021 = data[data["year"] == 2021]

    data_2020_by_month = data_2020.groupby("month").apply(count_rows)
    data_2021_by_month = data_2021.groupby("month").apply(count_rows)

    data_2020_by_month = data_2020_by_month.to_frame()
    data_2021_by_month = data_2021_by_month.to_frame()


    data_2020_by_month = data_2020_by_month.rename({0:"2020"}, axis='columns')
    data_2021_by_month = data_2021_by_month.rename({0:"2021"}, axis='columns')

    data_2020_2021 = pd.merge(data_2020_by_month,data_2021_by_month, on='month')
    return data_2020_2021

@st.cache(allow_output_mutation = True)
def get_data_2020_2021(df):
    data = df[df["Profile Name"] == "Romain"]
    data_2020 = data[data["year"] == 2020]
    data_2021 = data[data["year"] == 2021]

    data_2020_by_month = data_2020.groupby("hour").apply(count_rows)
    data_2021_by_month = data_2021.groupby("hour").apply(count_rows)

    data_2020_by_month = data_2020_by_month.to_frame()
    data_2021_by_month = data_2021_by_month.to_frame()


    data_2020_by_month = data_2020_by_month.rename({0:"2020"}, axis='columns')
    data_2021_by_month = data_2021_by_month.rename({0:"2021"}, axis='columns')


    data_2020_2021_hour = pd.merge(data_2020_by_month,data_2021_by_month, on='hour')
    return data_2020_2021_hour





@st.cache(allow_output_mutation = True)
def get_number_of_episode_by_hour(df,select_profil):
    number_of_episode_by_hour = df[df["Profile Name"] == select_profil].groupby("hour").apply(count_rows)
    number_of_episode_by_hour = number_of_episode_by_hour.to_frame()
    number_of_episode_by_hour["hour"] = number_of_episode_by_hour.index
    number_of_episode_by_hour = number_of_episode_by_hour.rename({0:"count"}, axis='columns')
    return number_of_episode_by_hour

@st.cache(allow_output_mutation = True)
def get_number_of_episode_by_hour(df,select_profil):
    number_of_episode_by_hour = df[df["Profile Name"] == select_profil].groupby("hour").apply(count_rows)
    number_of_episode_by_hour = number_of_episode_by_hour.to_frame()
    number_of_episode_by_hour["hour"] = number_of_episode_by_hour.index
    number_of_episode_by_hour = number_of_episode_by_hour.rename({0:"count"}, axis='columns')
    return number_of_episode_by_hour



@st.cache(allow_output_mutation = True)
def get_most_view_serie_movie(df):
    most_view_serie_movie_romain = df[df["Profile Name"] == "Romain"].groupby("Title_without_saison").apply(count_rows)
    most_view_serie_movie_romain.sort_values(ascending=False, inplace =True)
    most_view_serie_movie_romain = most_view_serie_movie_romain.to_frame()
    most_view_serie_movie_romain = most_view_serie_movie_romain.rename({0:"count"}, axis='columns')
    most_view_serie_movie_romain['title'] = most_view_serie_movie_romain.index



    most_view_serie_movie_justine = df[df["Profile Name"] == "Justine"].groupby("Title_without_saison").apply(count_rows)
    most_view_serie_movie_justine.sort_values(ascending=False, inplace =True)
    most_view_serie_movie_justine = most_view_serie_movie_justine.to_frame()
    most_view_serie_movie_justine = most_view_serie_movie_justine.rename({0:"count"}, axis='columns')
    most_view_serie_movie_justine['title'] = most_view_serie_movie_justine.index


    most_view_serie_movie_maman = df[df["Profile Name"] == "Maman"].groupby("Title_without_saison").apply(count_rows)
    most_view_serie_movie_maman.sort_values(ascending=False, inplace =True)
    most_view_serie_movie_maman = most_view_serie_movie_maman.to_frame()
    most_view_serie_movie_maman = most_view_serie_movie_maman.rename({0:"count"}, axis='columns')
    most_view_serie_movie_maman['title'] = most_view_serie_movie_maman.index


    most_view_serie_movie_mapa = df[df["Profile Name"] == "Mamie Et Papy"].groupby("Title_without_saison").apply(count_rows)
    most_view_serie_movie_mapa.sort_values(ascending=False, inplace =True)
    most_view_serie_movie_mapa = most_view_serie_movie_mapa.to_frame()
    most_view_serie_movie_mapa = most_view_serie_movie_mapa.rename({0:"count"}, axis='columns')
    most_view_serie_movie_mapa['title'] = most_view_serie_movie_mapa.index
    return most_view_serie_movie_romain,most_view_serie_movie_justine,most_view_serie_movie_maman,most_view_serie_movie_mapa

@st.cache(allow_output_mutation = True)
def get_most_view_m(df):
    most_view_m = df.groupby("Title").apply(count_rows)
    most_view_m.sort_values(ascending=False, inplace=True)
    most_view_m = most_view_m.to_frame()
    return most_view_m


@st.cache(allow_output_mutation = True)
def get_most_view_m1(df):
    most_view_m = df[df["Profile Name"] == "Romain"].groupby("Title").apply(count_rows)
    most_view_m.sort_values(ascending=False, inplace=True)
    most_view_m1 = most_view_m.to_frame()
    most_view_m1 = most_view_m1.rename({0:"count"}, axis='columns')
    most_view_m1["Title"] = most_view_m1.index
    return most_view_m1


############################  Decorators #############################


def my_decorator(func):
    def wrapper(*args, **kwargs):
        t = time()
        func(*args, **kwargs)
        return time() - t
    return wrapper


################# define plot function ################################################
@my_decorator
def plot_time_wath_by_profile(df):
    time_wath_by_profile = get_time_wath_by_profile(df)

    st.bar_chart(time_wath_by_profile)

@my_decorator
def plot_nb_serie_by_profile(df):
    nb_serie_by_profile = df.groupby('Profile Name').apply(count_rows)

    st.bar_chart(nb_serie_by_profile)

@my_decorator
def plot_data_2020_2021_month(df):
    data_2020_2021_month = get_data_2020_2021_month(df)

    st.line_chart(data_2020_2021_month)

@my_decorator
def plot_data_2020_2021_hour(df):
    data_2020_2021_hour = get_data_2020_2021(df)

    st.line_chart(data_2020_2021_hour)

@my_decorator
def plot_nb_episodes_month_year(df):
    tab1, tab2, tab3, tab4 = st.tabs(["2019", "2020", "2021","2022"])

    with tab1:
        mask = df["year"] == 2019
        valeur = df[mask].groupby('month').apply(count_rows)
        fig, ax = plt.subplots()
        sns.histplot(x='month',data=df[mask],hue='Profile Name', multiple="stack")
        ax.set_xlim(1,12)
        ax.set_xticks(range(1,13))
        st.pyplot(fig)

        
    with tab2:
        mask = df["year"] == 2020
        valeur = df[mask].groupby('month').apply(count_rows)
        fig, ax = plt.subplots()
        sns.histplot(x='month',data=df[mask],hue='Profile Name', multiple="stack")
        ax.set_xlim(1,12)
        ax.set_xticks(range(1,13))
        st.pyplot(fig)

        
    with tab3:
        mask = df["year"] == 2021
        valeur = df[mask].groupby('month').apply(count_rows)
        fig, ax = plt.subplots()
        sns.histplot(x='month',data=df[mask],hue='Profile Name', multiple="stack")
        ax.set_xlim(1,12)
        ax.set_xticks(range(1,13))
        st.pyplot(fig)

        
    with tab4:
        mask = df["year"] == 2022
        valeur = df[mask].groupby('month').apply(count_rows)
        fig, ax = plt.subplots()
        sns.histplot(x='month',data=df[mask],hue='Profile Name', multiple="stack")
        ax.set_xlim(1,12)
        ax.set_xticks(range(1,13))
        st.pyplot(fig)

@my_decorator
def plot_time_watch(df):
    select_profil = st.selectbox('Select the profile',
    ('Romain', 'Justine', 'Maman'))
    st.line_chart(data=get_number_of_episode_by_hour(df,select_profil), x="hour", y="count")

@my_decorator
def plot_weekday_comsuption(df,l_profile):
    weekday = st.select_slider(
        'Select a weekday',
        options=['Mon','Tue','Wed', 'Thu', 'Fri', 'Sat', 'Sun'])



    if weekday == "Mon":
        data = df[df["weekday"] == 0]
    elif weekday == "Tue":
        data = df[df["weekday"] == 1]
    elif weekday == "Wed":
        data = df[df["weekday"] == 2]
    elif weekday == "Thu":
        data = df[df["weekday"] == 3]
    elif weekday == "Fri":
        data = df[df["weekday"] == 4]
    elif weekday == "Sat":
        data = df[df["weekday"] == 5]
    else :
        data = df[df["weekday"] == 6]



    by_profile_count = data.groupby("Profile Name").apply(count_rows)
    by_profile_count = by_profile_count.to_frame()
    by_profile_count = by_profile_count.rename({0:"count"}, axis='columns')

    sizes = np.array(by_profile_count["count"])

    def absolute_value(val):
        a  = np.round(val/100.*sizes.sum(), 0)
        return a



    fig, ax = plt.subplots()
    ax.pie(by_profile_count["count"] , labels = l_profile,autopct=absolute_value)
    st.pyplot(fig)

@my_decorator
def plot_favorite_show_by_account(df):
    
    most_view_serie_movie_romain,most_view_serie_movie_justine,most_view_serie_movie_maman,most_view_serie_movie_mapa = get_most_view_serie_movie(df)

    plt.rcParams.update({'font.size': 11})
    fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(4, 1,figsize=(10, 10))
    fig.suptitle('Favorite show by account')
    ax1.bar(most_view_serie_movie_romain['title'][0:5], most_view_serie_movie_romain['count'][0:5], width=0.8)
    ax1.set_title("Romain")
    ax2.bar(most_view_serie_movie_justine['title'][0:5], most_view_serie_movie_justine['count'][0:5], width=0.8)
    ax2.set_title("Justine")
    ax3.bar(most_view_serie_movie_maman['title'][0:5], most_view_serie_movie_maman['count'][0:5], width=0.8)
    ax3.set_title("Maman")
    ax4.bar(most_view_serie_movie_mapa['title'][0:5], most_view_serie_movie_mapa['count'][0:5], width=0.8)
    ax4.set_title("Mamie et Papy")
    fig.tight_layout()
    st.pyplot(fig)

@my_decorator
def plot_most_view_all(df):
    plt.rcParams.update({'font.size': 15})
    most_view_m = get_most_view_m(df)
    fig, ax = plt.subplots(figsize=(20,10))
    ax.bar(most_view_m.index[0:3],most_view_m[0][0:3], width=0.8)

    st.pyplot(fig)

@my_decorator
def plot_most_rewatch(df):
    plt.rcParams.update({'font.size': 15})
    most_view_m1  =get_most_view_m1(df)
    fig = plt.figure(figsize=(20,10))
    sns.barplot(data=most_view_m1[0:3], x="Title", y="count")
    st.pyplot(fig)



####################################################### main ###################################################
if __name__ == '__main__':

    liste_time_decorator = []
    st.title("Project - My Netflix Data between 2019-2022")

    name_data = "ViewingActivity.csv"
    df = load_df(name_data)

    l_profile = get_l_profile(df)

    st.title("1 - How much time do we spend on Netflix ?")

    liste_time_decorator.append(plot_time_wath_by_profile(df))

    st.title("2 - How many movie/series have we seen ?")
    liste_time_decorator.append(plot_nb_serie_by_profile(df))

    st.title("3 - Has the covid impacted my consumption of series ?")
    liste_time_decorator.append(plot_data_2020_2021_month(df))

    st.title("4 - Do I always watch my episodes at the same time ?")
    liste_time_decorator.append(plot_data_2020_2021_hour(df))

    st.title("5 - Who has watched the most episodes per month and per year ?")
    liste_time_decorator.append(plot_nb_episodes_month_year(df))

    st.title("6 - At what time do we watch more Netflix ?")
    liste_time_decorator.append(plot_time_watch(df) )

    st.title("7 - Who watches the most episodes based on the days of the week ?")
    liste_time_decorator.append(plot_weekday_comsuption(df,l_profile))

    st.title("8 - What are the different shows that account watch ")
    liste_time_decorator.append(plot_favorite_show_by_account(df))

    st.title("9 - Episode most view on all the account")
    liste_time_decorator.append(plot_most_view_all(df))

    st.title("10 - What are the episode I look several time ?")
    liste_time_decorator.append(plot_most_rewatch(df))


    st.write("End of analyze - Jouanel Romain - linkedin : https://www.linkedin.com/in/romain-jouanel-b94205195/  - github : https://github.com/JouanelR/")

    st.write(time() -start_time )


    st.write("time execution for each plot")

    for i in range(len(liste_time_decorator)):
        st.write(i+1,liste_time_decorator[i])
