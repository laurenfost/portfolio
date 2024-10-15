"""
wine_dashboard.py
authors: Lily Hartley, Lauren Foster
DS 3500 homework 3
"""
import panel as pn
from api_wine_analysis import load_wine_data, create_widgets, label_bins_with_ranges, update_sankey

#load data
wine_df = load_wine_data('winequality-red.csv', 'winequality-white.csv')

#put quality column into bins for sankey diagram
wine_df['quality_bins'] = label_bins_with_ranges(wine_df, 'quality', bin_count=5)

choose_color, quality_slider, alcohol_slider, ph_slider, volatile_acidity_slider = create_widgets(wine_df)

#binding the update_sankey function to the widgets using pn.bind()
interactive_sankey = pn.bind(
    update_sankey,
    df=wine_df,
    color=choose_color.param.value,
    quality_range=quality_slider.param.value,
    alcohol_range=alcohol_slider.param.value,
    ph_range=ph_slider.param.value,
    volatile_acidity_range=volatile_acidity_slider.param.value)

#create dashboard
dashboard = pn.Column(
    pn.pane.Markdown("## Wine Data Dashboard"),
    choose_color,
    quality_slider,
    alcohol_slider,
    ph_slider,
    volatile_acidity_slider,
    pn.pane.Plotly(interactive_sankey))
#display dashboard
dashboard.show()


