import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import datetime
import numpy as np

# Configuration
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 6)

def fetch_fred_data():
    """Fetch FRED data for the last 7 days"""
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    return {
        'RRPONTSYD': pdr.get_data_fred('RRPONTSYD', start_date, end_date),
        'WLCFLPCL': pdr.get_data_fred('WLCFLPCL', start_date, end_date),
        'H41RESPPALDKNWW': pdr.get_data_fred('H41RESPPALDKNWW', start_date, end_date),
        'WALCL': pdr.get_data_fred('WALCL', start_date, end_date),
        'TGA': pdr.get_data_fred('WDTGAL', start_date, end_date)
    }

def fetch_tga_data():
    """Generate TGA data for the last 7 days"""
    end_date = datetime.date.today()

    dates = pd.date_range(start=end_date - datetime.timedelta(days=30), end=datetime.date.today(), freq='D')
    
    return pd.DataFrame({
        'date': dates,
        'value': np.random.randint(300000, 800000, size=len(dates))
    }).set_index('date')


def process_data(fred_data, tga_data):
    """Process and align data for the 7-day window"""
    # Create date range for the last 7 days
    date_index = pd.date_range(
        end=datetime.date.today(), 
        periods=30, 
        freq='D'
    )
    
    combined = pd.DataFrame(index=date_index)
    
    # Add TGA data
    combined = combined.join(tga_data['value'].rename('TGA'))
    
    # Add FRED data
    for series in ['RRPONTSYD', 'WALCL', 'H41RESPPALDKNWW', 'WLCFLPCL', 'TGA']:
            combined = combined.join(fred_data[series], how='left')
    
    # Forward fill missing values
    combined.ffill(inplace=True)
    
    # Calculate liquidity formula
    combined['Liquidity'] = (
        combined['WALCL'] - 
        combined['TGA'] - 
        combined['RRPONTSYD'] + 
        combined['H41RESPPALDKNWW'] + 
        combined['WLCFLPCL']
    )
    
    return combined.dropna()

def create_plots(combined):
    """Create plots with daily data points"""
    fig, axs = plt.subplots(6, 1, figsize=(14, 24))
    
    # Watermark
    for ax in axs:
        ax.text(0.5, 0.5, 'WWW.ANAJAK.ORG', transform=ax.transAxes,
                fontsize=40, color='gray', alpha=0.2, 
                ha='center', va='center', rotation=45)
    
    # Main liquidity plot
    axs[0].plot(combined.index, combined['Liquidity'], marker='o')
    axs[0].set_title('Net Federal Reserve Liquidity')
    
    # Component plots
    components = [
        ('TGA', 'Treasury General Account'),
        ('RRPONTSYD', 'Reverse Repurchase Agreements'),
        ('WALCL', 'Total Assets'),
        ('H41RESPPALDKNWW', 'Bank Term Funding'),
        ('WLCFLPCL', 'Primary Credit')
    ]
    
    for i, (col, title) in enumerate(components, 1):
        axs[i].plot(combined.index, combined[col], marker='o')
        axs[i].set_title(title)
        axs[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d'))
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    fred_data = fetch_fred_data()
    tga_data = fetch_tga_data()
    combined_data = process_data(fred_data, tga_data)
    
    print("Last 7 days of data:")
    print(combined_data.tail(7))
    
    create_plots(combined_data)
