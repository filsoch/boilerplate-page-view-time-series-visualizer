import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', header=0, parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], label='Data', color='red')
    step = len(df.index) // 7
    selected_ticks = df.index[::step]
    selected_tick_labels = pd.to_datetime(selected_ticks).strftime('%Y-%m')
    ax.set_xticks(selected_ticks)
    ax.set_xticklabels(selected_tick_labels)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.tight_layout()
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month_name()
    df_bar = df_bar .groupby(['year', 'month'])['value'].mean().reset_index()
    df_bar = df_bar.pivot(index='year', columns='month', values='value')
    df_bar = df_bar.reindex(
    ['January', 'February', 'March', 'April', 'May', 'June', 
     'July', 'August', 'September', 'October', 'November', 'December'], 
    axis=1
)
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 8))
    df_bar.plot(kind='bar', width=0.5, ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months') 

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    sns.boxplot(data=df_box, hue='year',x='year', y='value', ax=axes[0],legend=False, palette="Set1", flierprops=dict(marker='D',markersize=1))
    axes[0].grid(False)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    sns.boxplot(data=df_box, hue='month',x='month', y='value', ax=axes[1], legend=False, palette="Set1", flierprops=dict(marker='D',markersize=1))
    axes[1].grid(False)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

