#!/usr/bin/env python3
"""
MLB Qualifying Offer Calculator

This script calculates the MLB qualifying offer value by:
1. Fetching salary data from the provided URL
2. Extracting and cleaning salary values
3. Finding the top 125 highest salaries
4. Calculating the average of those salaries
5. Displaying the result with visualizations

The qualifying offer is a one-year contract whose monetary value is the 
average of the 125 highest salaries from the past season.

Resources and Libraries Used:
- requests: https://requests.readthedocs.io/ - HTTP library for fetching web data
- BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ - HTML parsing
- pandas: https://pandas.pydata.org/docs/ - Data manipulation and analysis
- matplotlib: https://matplotlib.org/stable/contents.html - Data visualization
- lxml: HTML parser backend for BeautifulSoup

Implementation Notes:
- HTML parsing uses BeautifulSoup with lxml parser for robust table extraction
- Salary parsing handles various formats and corrupted data using regex
- Data validation includes sanity checks for reasonable salary ranges
- Error handling ensures graceful failure with informative messages
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import re
from typing import List, Tuple
import sys


def fetch_html_data(url: str) -> str:
    """
    Fetches HTML data from the provided URL.
    
    Args:
        url: The URL to fetch data from
        
    Returns:
        HTML content as a string
        
    Raises:
        requests.RequestException: If the request fails
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        raise


def parse_salary(salary_str: str) -> float:
    """
    Parses a salary string and converts it to a float.
    Handles various formats and corrupted data.
    
    Args:
        salary_str: Salary string (e.g., "$11,666,667" or "$507,500")
        
    Returns:
        Salary as a float, or None if parsing fails
    """
    if not salary_str or not isinstance(salary_str, str):
        return None
    
    # Remove dollar signs, commas, and whitespace
    cleaned = salary_str.replace('$', '').replace(',', '').strip()
    
    # Remove any non-numeric characters except decimal point
    cleaned = re.sub(r'[^\d.]', '', cleaned)
    
    if not cleaned:
        return None
    
    try:
        salary = float(cleaned)
        # Sanity check: salaries should be positive and reasonable
        # Reject negative values or extremely large values (likely corrupted)
        if salary < 0 or salary > 1e10:  # $10 billion cap
            return None
        return salary
    except (ValueError, TypeError):
        return None


def extract_salary_data(html: str) -> pd.DataFrame:
    """
    Extracts salary data from HTML table.
    
    Args:
        html: HTML content containing the salary table
        
    Returns:
        DataFrame with columns: Player, Salary, Year, Level
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the table
    table = soup.find('table', {'id': 'salaries-table'})
    if not table:
        raise ValueError("Could not find salary table in HTML")
    
    data = []
    rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')[1:]
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 2:
            continue
        
        try:
            player = cols[0].get_text(strip=True) if len(cols) > 0 else ""
            salary_str = cols[1].get_text(strip=True) if len(cols) > 1 else ""
            year = cols[2].get_text(strip=True) if len(cols) > 2 else ""
            level = cols[3].get_text(strip=True) if len(cols) > 3 else ""
            
            salary = parse_salary(salary_str)
            
            # Only include rows with valid salaries
            if salary is not None:
                data.append({
                    'Player': player,
                    'Salary': salary,
                    'Year': year,
                    'Level': level
                })
        except Exception as e:
            # Skip rows that cause errors
            continue
    
    if not data:
        raise ValueError("No valid salary data found in HTML")
    
    return pd.DataFrame(data)


def calculate_qualifying_offer(df: pd.DataFrame) -> Tuple[float, pd.DataFrame]:
    """
    Calculates the qualifying offer value based on the top 125 salaries.
    
    Args:
        df: DataFrame containing salary data
        
    Returns:
        Tuple of (qualifying_offer_value, top_125_df)
    """
    # Sort by salary in descending order
    sorted_df = df.sort_values('Salary', ascending=False).reset_index(drop=True)
    
    # Get top 125 salaries
    top_125 = sorted_df.head(125).copy()
    
    # Calculate average
    qualifying_offer = top_125['Salary'].mean()
    
    return qualifying_offer, top_125


def format_currency(amount: float) -> str:
    """
    Formats a number as currency.
    
    Args:
        amount: The amount to format
        
    Returns:
        Formatted currency string (e.g., "$15,234,567")
    """
    return f"${amount:,.2f}"


def create_visualizations(df: pd.DataFrame, top_125: pd.DataFrame, qualifying_offer: float):
    """
    Creates visualizations of the salary data.
    
    Args:
        df: Full DataFrame with all salaries
        top_125: DataFrame with top 125 salaries
        qualifying_offer: The calculated qualifying offer value
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('MLB Qualifying Offer Analysis', fontsize=16, fontweight='bold')
    
    # 1. Top 125 salaries bar chart
    ax1 = axes[0, 0]
    top_20 = top_125.head(20)
    ax1.barh(range(len(top_20)), top_20['Salary'].values / 1e6, color='steelblue')
    ax1.set_yticks(range(len(top_20)))
    ax1.set_yticklabels(top_20['Player'].values, fontsize=8)
    ax1.set_xlabel('Salary (Millions USD)', fontsize=10)
    ax1.set_title('Top 20 Highest Salaries (from Top 125)', fontsize=12, fontweight='bold')
    ax1.axvline(x=qualifying_offer / 1e6, color='red', linestyle='--', 
                label=f'Qualifying Offer: ${qualifying_offer/1e6:.2f}M')
    ax1.legend()
    ax1.invert_yaxis()
    
    # 2. Salary distribution histogram
    ax2 = axes[0, 1]
    ax2.hist(df['Salary'].values / 1e6, bins=50, color='lightblue', edgecolor='black', alpha=0.7)
    ax2.axvline(x=qualifying_offer / 1e6, color='red', linestyle='--', linewidth=2,
                label=f'Qualifying Offer: ${qualifying_offer/1e6:.2f}M')
    ax2.set_xlabel('Salary (Millions USD)', fontsize=10)
    ax2.set_ylabel('Frequency', fontsize=10)
    ax2.set_title('Salary Distribution (All Players)', fontsize=12, fontweight='bold')
    ax2.legend()
    
    # 3. Top 125 salary range
    ax3 = axes[1, 0]
    top_125_sorted = top_125.sort_values('Salary', ascending=True)
    ax3.scatter(range(len(top_125_sorted)), top_125_sorted['Salary'].values / 1e6, 
                color='green', alpha=0.6, s=20)
    ax3.axhline(y=qualifying_offer / 1e6, color='red', linestyle='--', linewidth=2,
                label=f'Qualifying Offer: ${qualifying_offer/1e6:.2f}M')
    ax3.set_xlabel('Rank (1-125)', fontsize=10)
    ax3.set_ylabel('Salary (Millions USD)', fontsize=10)
    ax3.set_title('Top 125 Salaries (Sorted)', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Summary statistics
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    stats_text = f"""
    QUALIFYING OFFER CALCULATION
    
    Total Players in Dataset: {len(df):,}
    Valid Salaries Found: {len(df):,}
    
    Top 125 Salaries:
    • Highest: {format_currency(top_125['Salary'].max())}
    • Lowest (in top 125): {format_currency(top_125['Salary'].min())}
    • Average: {format_currency(top_125['Salary'].mean())}
    • Median: {format_currency(top_125['Salary'].median())}
    
    ════════════════════════════════════
    QUALIFYING OFFER VALUE:
    {format_currency(qualifying_offer)}
    ════════════════════════════════════
    
    Overall Statistics:
    • All Salaries Mean: {format_currency(df['Salary'].mean())}
    • All Salaries Median: {format_currency(df['Salary'].median())}
    • All Salaries Std Dev: {format_currency(df['Salary'].std())}
    """
    
    ax4.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', 
             facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('qualifying_offer_visualization.png', dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: qualifying_offer_visualization.png")
    plt.close()


def display_results(qualifying_offer: float, top_125: pd.DataFrame, df: pd.DataFrame):
    """
    Displays the results in a formatted way.
    
    Args:
        qualifying_offer: The calculated qualifying offer value
        top_125: DataFrame with top 125 salaries
        df: Full DataFrame with all salaries
    """
    print("\n" + "="*70)
    print(" " * 15 + "MLB QUALIFYING OFFER CALCULATOR")
    print("="*70)
    print(f"\nDataset Statistics:")
    print(f"   • Total players with valid salaries: {len(df):,}")
    print(f"   • Salary range: {format_currency(df['Salary'].min())} - {format_currency(df['Salary'].max())}")
    
    print(f"\nTop 125 Salaries Analysis:")
    print(f"   • Highest salary: {format_currency(top_125['Salary'].max())}")
    print(f"   • Lowest salary (in top 125): {format_currency(top_125['Salary'].min())}")
    print(f"   • Average of top 125: {format_currency(top_125['Salary'].mean())}")
    print(f"   • Median of top 125: {format_currency(top_125['Salary'].median())}")
    
    print(f"\n" + "="*70)
    print(f"   QUALIFYING OFFER VALUE: {format_currency(qualifying_offer)}")
    print("="*70)
    
    print(f"\nAdditional Statistics:")
    print(f"   • Overall mean salary: {format_currency(df['Salary'].mean())}")
    print(f"   • Overall median salary: {format_currency(df['Salary'].median())}")
    print(f"   • Standard deviation: {format_currency(df['Salary'].std())}")
    
    print(f"\nNote: The qualifying offer is calculated as the average of")
    print(f"   the 125 highest salaries from the dataset.")
    print("="*70 + "\n")


def main():
    """
    Main function to run the qualifying offer calculator.
    """
    url = 'https://questionnaire-148920.appspot.com/swe/data.html'
    
    print("Fetching salary data...")
    try:
        html = fetch_html_data(url)
        print("Data fetched successfully")
        
        print("Parsing salary data...")
        df = extract_salary_data(html)
        print(f"Parsed {len(df):,} valid salary records")
        
        print("Calculating qualifying offer...")
        qualifying_offer, top_125 = calculate_qualifying_offer(df)
        print("Calculation complete")
        
        print("Creating visualizations...")
        create_visualizations(df, top_125, qualifying_offer)
        print("Visualizations created")
        
        display_results(qualifying_offer, top_125, df)
        
        # Save top 125 to CSV for reference
        top_125.to_csv('top_125_salaries.csv', index=False)
        print(f"Top 125 salaries saved to: top_125_salaries.csv")
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

