import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import EngFormatter

#on importe nos deux datasets
campaigns = pd.read_csv("campaigns.csv",error_bad_lines=False)
digest_topics = pd.read_csv("Digest topic.csv",error_bad_lines=False)

#là on crée le titre de la page
st.title("Exploration des métriques de la newsletter")

#On selectionne dans notre dataset les données qui nous interessent
digest = campaigns[campaigns['List']== 'Deepnews Digest']
digest = digest[digest['Send Weekday']=='Friday']

#formattage de la colonne 'Send Date' en datetime
digest['Send Date'] = pd.to_datetime(digest["Send Date"],format = "%b %d, %Y %H:%M %p")

#copie du dataset
digest_final = digest.copy()
mylambda= lambda x: x.strip('%')
digest_final['Click Rate']=digest_final['Click Rate'].apply(mylambda)
digest_final['Open Rate']=digest_final['Open Rate'].apply(mylambda)
digest_final['Open Rate']=digest_final['Open Rate'].astype('float64')
digest_final['Click Rate']=digest_final['Click Rate'].astype('float64')
dateDigest = digest_final["Send Date"]


if st.checkbox('voir le dataset des métriques'):
    nombre_lignes_a_visualiser = st.number_input("Nombre de lignes à visualiser")
    st.write(digest_final.head(nombre_lignes_a_visualiser))

#on enlève les données inutiles
digest.drop([186,191,200,210], inplace = True)


#création d'une fonction de plotting
def LinePlotTime(parameter, Parameter_name, dataset, title_name):
    fig, axes = plt.subplots(figsize = (15,8))
    sns.lineplot(x = dateDigest, y = Parameter_name, data = dataset, linewidth=4, c='orangered')
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=18)

    plt.xlabel("Date d'envoi",fontsize=20)
    plt.ylabel(Parameter_name,fontsize=20)
    plt.xticks(rotation=30)
    plt.title(title_name, fontsize=25)
    plt.show()

def LinePlotTimePercent(parameter, Parameter_name, dataset, title_name):
    fig, axes = plt.subplots(figsize = (15,8))
    ax = sns.lineplot(x= dateDigest, y = Parameter_name, data = dataset, linewidth=4, c='orangered')
    plt.ylim(0,100)
    formatter0 = EngFormatter(unit='%')
    ax.yaxis.set_major_formatter(formatter0)
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=18)
    plt.xlabel("Date d'envoi",fontsize=20)
    plt.ylabel(Parameter_name,fontsize=20)
    plt.xticks(rotation=30)
    plt.title(title_name, fontsize=25)



#On crée la selectbox pour les métriques
metrique = st.selectbox('Quelle métrique veux-tu représenter',("Recipients","Open Rates", 'Click Rate', 'Total Bounces'))

if metrique == "Recipients":
    #on représente le nombre de receveurs en fonction du temps
    plot_totalR = LinePlotTime('Total Recipients', 'Total Recipients', digest_final,"Evolution du nombre de destinataires en fonction du temps")
    st.write("Evolution du nombre de destinataires recevant la newsletter")
    st.pyplot(plot_totalR)

elif metrique == 'Open Rates':
    plot_OpenR = LinePlotTimePercent('Open Rate', 'Open Rate', digest_final,"Evolution du taux d'ouverture en fonction du temps" )
    st.write("Evolution du taux d'ouverture")
    st.pyplot(plot_OpenR)

elif metrique == 'Click Rate':
    plot_clicR = LinePlotTimePercent('Click Rate','Click Rate', digest_final,"Evolution du taux de clics en fonction du temps")
    st.write("Evolution du taux de clics en fonction du temps")
    st.pyplot(plot_clicR)
else :
    plot_totalBoun = LinePlotTime('Total Bounces', 'Total Bounces', digest_final, "Evolution du nombre de mail non délivrés au cours du temps")
    st.write("Evolution du nombre de mail non délivrés au cours du temps")
    st.pyplot(plot_totalBoun)



#on intègre les thèmes dans notre jeu de données
topic=pd.read_csv("Digest Topic.csv", encoding = 'UTF-8')
dateDigest = digest_final["Send Date"]
digest_final = digest_final.reset_index(drop = True)
digest_final = digest_final.drop([0,1,2,3])
digest_final = digest_final.reset_index(drop= True)

digest2=pd.concat([digest_final,digest_topics],axis = 1)
digest_theme=digest2
digest_theme.Thème.replace('Economy',"Business", inplace = True )
theme = digest_theme["Thème"]

if st.checkbox("voir les différents thèmes"):
    st.write(pd.DataFrame(digest_theme["Thème"].value_counts()))


def barplots(parameter, Parameter_name, title_name):
    fig, ax = plt.subplots(figsize = (20, 7))
    sns.barplot(x = theme, y = parameter, data =    digest_theme )
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=18)
    plt.xlabel("Thème",fontsize=20)
    plt.ylabel(Parameter_name,fontsize=20)
    plt.xticks(rotation=0)
    plt.title(title_name, fontsize=25)

#st.write(digest_theme)
st.subheader("Représentation des métriques en fonction du thème de la newsletter")
barTheme = st.selectbox("Quelle métrique veux-tu représenter ?", ("Open Rate", "Click Rate", "Unique Clicks","Total Recipients"))
if barTheme == 'Open Rate':
    barplot_openR = barplots('Open Rate', 'Open Rate', "Taux d'ouverture en fonction du thème")
    st.write("Taux d'ouverture en fonction du thème")
    st.pyplot(barplot_openR)
elif barTheme == 'Click Rate':
    barplot_ClickR = barplots('Click Rate', 'Click Rate', 'Taux de cliks en fonction du thème')
    st.write("Taux de cliks en fonction du thème")
    st.pyplot(barplot_ClickR)
elif barTheme == "Unique Clicks":
    barplot_UClick = barplots("Unique Clicks", "Unique Clicks", 'Taux de cliks uniques en fonction du thème')
    st.write("Taux de cliks en fonction du thème")
    st.pyplot(barplot_UClick)
else :
    barplot_totalR = barplots('Total Recipients', 'Total Recipients', 'Destinaires en fonction du thème')
    st.write("Destinataires en fonction du thème")
    st.pyplot(barplot_totalR)


st.subheader("Représentation des désinscriptions en fonction du thème et de la newsletter")

def scatterthing(x, y, hue,xlabel,ylabel, title):
    fig, ax = plt.subplots(figsize=(20,10))
    sns.scatterplot(digest_theme["Unsubscribes"].sort_values(),digest_theme['Title'], hue = digest_theme['Thème'], s = 300 )

    # plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=18)
    # formatter0 = EngFormatter(unit='%')
    # ax.yaxis.set_major_formatter(formatter0)
    plt.xlabel(xlabel,fontsize=20)
    plt.ylabel(ylabel,fontsize=20)
    plt.xticks(fontsize = 17)
    plt.title(title, fontsize=27)
    plt.legend(fontsize = 15)
    plt.tight_layout()


scat_Uns = scatterthing(digest_theme["Unsubscribes"],digest_theme['Title'],digest_theme['Thème'],"Unsubscribers",'Digest issue',"Unsubscribers by digest by thème" )

if st.checkbox("voir le scatterplot"):
    st.pyplot(scat_Uns)


st.subheader("Visualisations des subscribers")
digest_theme['New Subscribers'] = 0
for i in digest_theme.index:
  if i == 0:
    digest_theme.loc[i,'New Subscribers'] = 0
  else :
    digest_theme.loc[i, 'New Subscribers'] = digest_theme.loc[i, 'Total Recipients'] - digest_theme.loc[i - 1, 'Total Recipients']

#Date = digest_theme_complete['Send Date']
#New_Subscribers = digest_theme_complete['New Subscribers']
#Unsuscribers = digest_theme_complete['Unsubscribes']
#Theme = digest_theme_complete['Thème']

def doubleLinePlot():
    fig, axes = plt.subplots(2,1, figsize = (20, 10),)

    New_sub = sns.lineplot(x = digest_theme['Send Date'], y = digest_theme['New Subscribers'],  ax = axes[0])
    Unsub = sns.lineplot(x = digest_theme   ['Send Date'], y = digest_theme['Unsubscribes'] , ax = axes[1])

    New_sub.set_xlabel("Send Date",fontsize=18)
    Unsub.set_xlabel("Send Date",fontsize=18)

    New_sub.set_ylabel("New subscribers",fontsize=20)
    Unsub.set_ylabel("Unsubscribers",fontsize=20)

    New_sub.tick_params(labelsize=15)
    Unsub.tick_params(labelsize=15)

    plt.tight_layout()



doubleplot = doubleLinePlot()
if st.checkbox("voir le double plot"):
    st.pyplot(doubleplot)

st.subheader("Clics par éditeurs")
pub_df = pd.read_csv("reports_data.csv")
pub_grp_sr = pub_df.groupby(["publisher"])

pub_grp_df = pd.DataFrame(pub_grp_sr['unique_clicks'].sum().sort_values(ascending=False))
pub_grp_sum_df = pub_grp_df
pub_grp_sum_df.columns = ['uniq_tt']

pub_grp_mean_df = pd.DataFrame(pub_grp_sr['unique_clicks'].mean().sort_values(ascending=False))
pub_grp_mean_df.columns = ['uniq_moy']


pub_grp_merge_df = pub_grp_sum_df.join(pub_grp_mean_df)
pub_grp_merge_df.uniq_moy = pub_grp_merge_df.uniq_moy.round(2)

pub_grp_merge_df_small50 = pub_grp_merge_df.loc[pub_grp_merge_df['uniq_tt'] >= 50]


def clics_editeurs():
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(10, 11))

    # Plot the total clicks
    sns.set_color_codes("pastel")
    sns.barplot(x="uniq_tt", y=pub_grp_merge_df_small50.index, data=pub_grp_merge_df_small50,
                label="Total", color="g")

    # Plot the mean clicks
    sns.set_color_codes("colorblind")
    sns.barplot(x="uniq_moy", y=pub_grp_merge_df_small50.index, data=pub_grp_merge_df_small50,label="Moyen", color="g")

    # Add a legend and informative axis label
    ax.legend(ncol=1, loc="center right", frameon=True, fontsize=16, shadow=2)
    ax.set_xlabel("Nombre de clics")
    sns.despine(left=True, bottom=True)
    plt.title("Nombre de clics (moyen, total) >= 50 par publisher", fontdict={'fontsize': 18})

    plt.tight_layout()

    plt.savefig("nb_clics_publishers.png", dpi=200)


if st.checkbox('Voir le nombre de clics pour les 50 éditeurs les plus cliqués'):
    st.pyplot(clicsEdi = clics_editeurs())
    if st.checkbox("clique"):
        st.write("on peut voir ici que le newyorktimes est plus cliqué que les autres, mais simplement parce qu'il est plus présent")
        st.write("manchester evening a été très cliqué ")
