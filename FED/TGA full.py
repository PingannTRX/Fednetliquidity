import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import datetime
import numpy as np

# Configuration
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 6)

# Fetch economic data from FRED
def fetch_fred_data():
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime.now()
    
    return {
        'RRPONTSYD': pdr.get_data_fred('RRPONTSYD', start_date, end_date),
        'WLCFLPCL': pdr.get_data_fred('WLCFLPCL', start_date, end_date),
        'H41RESPPALDKNWW': pdr.get_data_fred('H41RESPPALDKNWW', start_date, end_date),
        'WALCL': pdr.get_data_fred('WALCL', start_date, end_date)
    }

# Simulate TGA data (replace with actual API calls if available)
def fetch_tga_data():
    dates = pd.date_range(start='2020-01-01', end=datetime.datetime.now(), freq='D')
    return pd.DataFrame({
        'date': dates,
        'value': np.random.randint(300000, 800000, size=len(dates))
    }).set_index('date')

# Process and combine datasets
def process_data(fred_data, tga_data):
    dfs = {
        'TGA': tga_data['value'],
        'RRP': fred_data['RRPONTSYD']['RRPONTSYD'],
        'WAL': fred_data['WALCL']['WALCL'],
        'H4': fred_data['H41RESPPALDKNWW']['H41RESPPALDKNWW'],
        'WLC': fred_data['WLCFLPCL']['WLCFLPCL']
    }
    
    # Create combined dataframe
    combined = pd.DataFrame()
    for name, df in dfs.items():
        combined[name] = df.resample('D').ffill()
        
    # Forward fill missing values
    combined.ffill(inplace=True)
    
    # Calculate liquidity formula
    combined['Liquidity'] = (
        combined['WAL'] - 
        combined['TGA'] - 
        combined['RRP'] + 
        combined['H4'] + 
        combined['WLC']
    )
    
    return combined

# Create plots with watermark
def create_plots(combined):
    fig, axs = plt.subplots(6, 1, figsize=(14, 24))
    
    # Add watermark to all plots
    for ax in axs:
        ax.text(0.5, 0.5, 'WWW.ANAJAK.ORG', transform=ax.transAxes,
                fontsize=40, color='gray', alpha=0.2, 
                ha='center', va='center', rotation=45)
    
    # Main liquidity plot
    axs[0].plot(combined.index, combined['Liquidity'], label='Net Liquidity')
    axs[0].set_title('Net Federal Reserve Liquidity\n(WALCL - TGA - RRPONTSYD + H41RESPPALDKNWW + WLCFLPCL)')
    
    # Component plots
    components = ['TGA', 'RRP', 'WAL', 'H4', 'WLC']
    titles = [
        'Treasury General Account (TGA)',
        'Reverse Repurchase Agreements (RRPONTSYD)',
        'Total Assets (WALCL)',
        'Bank Term Funding Program (H41RESPPALDKNWW)',
        'Primary Credit (WLCFLPCL)'
    ]
    
    for i, (col, title) in enumerate(zip(components, titles), 1):
        axs[i].plot(combined.index, combined[col])
        axs[i].set_title(title)
    
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == '__main__':
    fred_data = fetch_fred_data()
    tga_data = fetch_tga_data()
    combined_data = process_data(fred_data, tga_data)
    create_plots(combined_data)