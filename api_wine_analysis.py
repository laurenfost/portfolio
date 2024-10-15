"""
api_wine_analysis.py
authors: Lily Hartley, Lauren Foster
DS 3500 homework 3
"""

import pandas as pd
import panel as pn
from sankey import _code_mapping, make_sankey

pn.extension()

def load_wine_data(file1, file2):
    """combine 2 csv files into one dataframe"""
    df_red = pd.read_csv(file1, delimiter=';')
    df_white = pd.read_csv(file2, delimiter=';')
    df_red['color'] = 'red'
    df_white['color'] = 'white'
    wine_df = pd.concat([df_red, df_white], ignore_index=True)
    return wine_df


def create_widgets(df):
    """create the interactive widgets for the dashboard, selectors and sliders"""
    choose_color = pn.widgets.Select(name='Color', options=['red', 'white', 'both'], value='both')
    quality_slider = pn.widgets.IntRangeSlider(name='Wine Quality', start=df['quality'].min(),
                                               end=df['quality'].max(),
                                               value=(5, 8))
    alcohol_slider = pn.widgets.RangeSlider(name='Alcohol Content', start=df['alcohol'].min(),
                                            end=df['alcohol'].max(),
                                            step=0.1, value=(10.0, 12.0))
    ph_slider = pn.widgets.RangeSlider(name='pH', start=df['pH'].min(), end=df['pH'].max(), step=0.1,
                                       value=(2.00, 3.50))
    volatile_acidity_slider = pn.widgets.RangeSlider(name='Volatile Acidity', start=df['volatile acidity'].min(),
                                                     end=df['volatile acidity'].max(), step=0.1, value=(1.30, 1.80))
    return choose_color, quality_slider, alcohol_slider, ph_slider, volatile_acidity_slider


def label_bins_with_ranges(df, column_name, bin_count):
    """categorize a column into bins and label the bins with ranges, returns a new column with the binned data labeled
    with ranges"""
    binned_column, bin_edges = pd.cut(df[column_name], bins=bin_count, include_lowest=True, right=False, retbins=True)
    labels = [f"{bin_edges[i]:.1f}-{bin_edges[i + 1]:.1f}" for i in range(len(bin_edges) - 1)]
    binned_column = pd.cut(df[column_name], bins=bin_edges, labels=labels, include_lowest=True, right=False)
    return binned_column

def update_sankey(df, color, quality_range, alcohol_range, ph_range, volatile_acidity_range):
    """ call sankey function and update the sankey graph when widgets are interacted with"""
    filtered_df = df[
        (df['quality'] >= quality_range[0]) &
        (df['quality'] <= quality_range[1]) &
        (df['alcohol'] >= alcohol_range[0]) &
        (df['alcohol'] <= alcohol_range[1]) &
        (df['pH'] >= ph_range[0]) &
        (df['pH'] <= ph_range[1]) &
        (df['volatile acidity'] >= volatile_acidity_range[0]) &
        (df['volatile acidity'] <= volatile_acidity_range[1])
        ]

    if color != 'both':
        filtered_df = filtered_df[filtered_df['color'] == color]
    sankey_fig = make_sankey(filtered_df, src='quality_bins', targ='color')
    return sankey_fig