import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.graph_objects as go
import plotly.figure_factory as ff



sns.set_style('whitegrid')


def strip_plot(df, year, county):
    df_year = df[df['year'] == year]
    df_county = df_year[df_year['judet'] == county]

    fig = px.strip(
        df_county,
        x="medie",
        y="liceu",
        color="liceu",
        orientation="h",
        stripmode="overlay",
        color_discrete_sequence=px.colors.qualitative.Prism
    )

    fig.update_layout(
        title='Medii Licee pe Judet',
        xaxis_title='Medii',
        yaxis_title='Licee',
        template='plotly_white',
        xaxis=dict(range=[4.9,10.1]),
    )

    fig.show()


def box_plot(df, year, county):
    df_year = df[df['year'] == year]

    if county:
        df_year = df_year[df_year['judet'] == county]
        x_col = "medie"
        y_col = "liceu"
        title = f"Box & Whisker Plot - Medii pe licee din {county} ({year})"
        category_order = df_year.groupby('liceu')['medie'].median().sort_values(ascending=False).index
    else:
        x_col = "medie"
        y_col = "judet"
        title = f"Box & Whisker Plot - Medii pe județe ({year})"
        category_order = df_year.groupby('judet')['medie'].median().sort_values(ascending=False).index

    fig = px.box(
        df_year,
        x=x_col,
        y=y_col,
        orientation='h',
        category_orders={y_col: category_order},
        color=y_col,
        points="outliers",
        labels={x_col: "Medie", y_col: y_col.capitalize()},
        title=title
    )

    # Format x-axis
    fig.update_xaxes(range=[5, 10.1], tickformat=".2f")

    #fig.write_image(f'figures/{year}-{county}-medii-judete-box.png', scale=2)
    fig.show()


def bar_plot(df, year, county, highschool):
    df_year = df[df['year'] == year]

    title = f'Bar Plot - Rezultate ({year})'
    if county:
        df_year = df_year[df_year['judet'] == county]
        title = f'Bar Plot - Rezultate pe {county} ({year})'

        if highschool:
            df_year = df_year[df_year['liceu'] == highschool]
            title = f'Bar Plot - Rezultate din {highschool} ({year})'


    fig = plt.figure(figsize=(7,5))
    fig.canvas.manager.set_window_title(title)

    rezultate = df_year.groupby('rezultat').size().sort_values(ascending=False).reset_index(name='count')

    colors = sns.color_palette('cool', 1)
    ax = sns.barplot(rezultate, x='rezultat', y='count', color=colors[0], edgecolor='black')

    for i, rezultat in rezultate.iterrows():
        ax.text(i,
                rezultat['count'] + (ax.get_ylim()[1]/100)*2,
                str(rezultat['count']),
                ha='center', va='center',
                fontsize=12)

    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f'))

    plt.title(title)
    plt.xlabel('Rezultat')
    plt.ylabel('Nr. Elevi')
    plt.tight_layout()

    #plt.savefig(f'figures/{year}-rezultate-bar.png', dpi=150)
    plt.show()


def histogram_plot(df, year, county, highschool, score):
    df_year = df[df['year'] == year]
    title = f'Histogram Plot - Medii Romania ({year})'
    label = f'{year}'

    if county:
        df_year = df_year[df_year['judet'] == county]
        title = f'Histogram Plot - Medii pe {county} ({year})'
        label = f'{county}'


        if highschool:
            df_year = df_year[df_year['liceu'] == highschool]
            title = f'Histogram Plot - Medii din {highschool} ({year})'
            label = f'Liceu'


    fig = plt.figure(figsize=(20,10))

    colors = sns.color_palette('cool', 3)


    ax = sns.histplot(data=df_year, x="medie", bins=50,edgecolor='black', fill=True, color=colors[0], alpha=0.5, label=label)

    if highschool:
        #jitter = np.random.uniform(0, 1, size=len(df_year['medie']))
        ax.scatter(df_year['medie'], [0.5] * len(df_year['medie']), color=colors[2], marker='o', s=15, alpha=0.7, label='Note Elevi')
    
    # Display score if provided
    if score:
        plt.axvline(x=score, color=colors[1], linestyle="--", label=f"Nota {score}")

        total_elevi = df_year['medie'].shape[0]
        top_percentile = round(df_year[df_year['medie'] >= score].shape[0] / total_elevi * 100, 3)
        ax.text(score + 0.05, ax.get_ybound()[1] - 100, f'#{round(top_percentile/100*total_elevi)}/{total_elevi} - {top_percentile}%', fontsize=14, ha='left')


    fig.canvas.manager.set_window_title(title)
    plt.title(title)
    plt.xlabel("Final Score")
    plt.ylabel("Number of Students")
    plt.legend()

    #plt.savefig(f'figures/{year}-final-scores-histogram.png', dpi=150)
    plt.show()


def density_plot(df, year, county, score):
    df = df[df['medie'].isna() == False]
    years = df['year'].unique()
    labels = years.astype(str)
    title = f'Density Plot - Medii Romania pe ani'

    data = [df[df['year'] == x]['medie'].tolist() for x in years]


    if year:
        df = df[df['year'] == year]
        counties = df['judet'].unique()
        labels = counties.astype(str)
        title = f'Density Plot - Medii {year} pe judete'

        data = [df[df['judet'] == x]['medie'].tolist() for x in counties]

        if county:
            df = df[df['judet'] == county]
            highschools = df['liceu'].unique()
            title = f'Density Plot - Medii {county} {year}'

            values = [df[df['liceu'] == x]['medie'].tolist() for x in highschools]

            labels = []
            data = []
            for i, value in enumerate(values):
                if len(value) > 1: # To ensure datasets bigger than 1 are used (necessary for KDE)
                    data.append(value)
                    labels.append(str(highschools[i]))


    # Create density plots
    fig = ff.create_distplot(
        data,
        group_labels=labels,
        show_hist=False,
        show_rug=False
    )

    # Add vertical line if nota is provided
    if score:
        fig.add_vline(
            x=score,
            line=dict(color="black", dash="dash"),
            annotation_text=f'Nota {score}',
            annotation_position="top"
        )

    # Update layout for title and axes
    fig.update_layout(
        title=title,
        xaxis_title="Medii",
        yaxis_title="Density",
        template="plotly_white"
    )

    fig.update_xaxes(range=[5, 10], tickformat='.2f')
    fig.update_yaxes(tickformat='.4f')

    fig.show()
    #fig.write_image('figures/yearly_density.png', scale=2)
