# MLB Qualifying Offer Calculator

This program calculates the MLB (Major League Baseball) qualifying offer value by fetching salary data from a provided dataset, extracting the top 125 highest salaries, and computing their average.

## What is a Qualifying Offer?

In baseball, a team can provide a departing free agent player with a **qualifying offer**: a one-year contract whose monetary value is the average of the 125 highest salaries from the past season. The player is free to reject it and sign with any other team, but his new team will have to forfeit a draft pick.

## Features

- Fetches live data from the provided URL each time it runs
- Handles corrupted or malformed salary data gracefully
- Calculates the average of the top 125 highest salaries
- Displays comprehensive statistics and visualizations
- Saves results to CSV and creates a visualising PNG file
- Robust error handling

## Prerequisites

- Python 3.7 or higher
- Conda (Anaconda or Miniconda)
- pip (Python package installer)

## Installation

### Step 1: Clone or Download this Repository

```bash
git clone 
```

### Step 2: Create a Conda Environment (Recommended)

Create a conda environment to isolate dependencies:

```bash
conda create -n mlb-qualifying-offer python=3.9
```

Activate the conda environment:

```bash
conda activate mlb-qualifying-offer
```

Alternatively, if you already have a conda environment (e.g., `env1`), you can use that:

```bash
conda activate env1
```

### Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
#or
pip install requests beautifulsoup4 pandas matplotlib lxml
```

This will install:
- `requests` - For fetching data from the web
- `beautifulsoup4` - For parsing HTML
- `pandas` - For data manipulation
- `matplotlib` - For creating visualizations
- `lxml` - HTML parser backend

## Usage

### Running the Script

**Option 1: Using activated conda environment**

Activate your conda environment first, then run:

```bash
conda activate mlb-qualifying-offer

python qualifying_offer_calculator.py

#or
python3 qualifying_offer_calculator.py
```

**Option 2: Using system Python (if packages are installed globally)**

If you have the required packages installed globally:

```bash
python qualifying_offer_calculator.py
# or
python3 qualifying_offer_calculator.py
```

### What the Script Does

1. **Fetches Data**: Retrieves the latest salary data from `https://questionnaire-148920.appspot.com/swe/data.html`
2. **Parses Data**: Extracts player names and salaries from the HTML table, handling corrupted or malformed values
3. **Calculates**: Finds the top 125 highest salaries and computes their average
4. **Displays Results**: Shows the qualifying offer value and relevant statistics in the terminal
5. **Creates Visualizations**: Generates a comprehensive visualization saved as `qualifying_offer_visualization.png`
6. **Saves Data**: Exports the top 125 salaries to `top_125_salaries.csv`

### Output Files

After running the script, you'll find:

- **`qualifying_offer_visualization.png`** - A 4-panel visualization showing:
  - Top 20 highest salaries (bar chart)
  - Salary distribution histogram
  - Top 125 salaries scatter plot
  - Summary statistics panel

- **`top_125_salaries.csv`** - A CSV file containing the top 125 salaries with player names, salaries, years, and levels

### Example Output

```
======================================================================
               MLB QUALIFYING OFFER CALCULATOR
======================================================================

Dataset Statistics:
   • Total players with valid salaries: 1,234
   • Salary range: $507,500.00 - $33,000,000.00

Top 125 Salaries Analysis:
   • Highest salary: $33,000,000.00
   • Lowest salary (in top 125): $15,234,567.00
   • Average of top 125: $18,234,567.89
   • Median of top 125: $17,500,000.00

======================================================================
   QUALIFYING OFFER VALUE: $18,234,567.89
======================================================================

Additional Statistics:
   • Overall mean salary: $4,567,890.12
   • Overall median salary: $1,234,567.00
   • Standard deviation: $5,678,901.23

Note: The qualifying offer is calculated as the average of
   the 125 highest salaries from the dataset.
======================================================================
```

## Data Handling

The script includes robust data cleaning:

- **Removes invalid characters** from salary strings
- **Handles missing values** by skipping corrupted entries
- **Validates salary ranges** (rejects negative or unreasonably large values)
- **Gracefully handles parsing errors** without crashing

## Error Handling

The script handles various error scenarios:

- Network connection failures
- Invalid HTML structure
- Missing or corrupted data
- Parsing errors

If an error occurs, the script will display a clear error message and exit gracefully.

## Technical Details

### Calculation Method
1. Extract all valid salaries from the HTML table
2. Sort salaries in descending order
3. Select the top 125 salaries
4. Calculate the arithmetic mean of these 125 values
5. This mean is the qualifying offer value

### Libraries Used

- **requests**: HTTP library for fetching web data
  - Documentation: https://requests.readthedocs.io/
  
- **beautifulsoup4**: HTML parsing library
  - Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  
- **pandas**: Data manipulation and analysis
  - Documentation: https://pandas.pydata.org/docs/
  
- **matplotlib**: Plotting and visualization
  - Documentation: https://matplotlib.org/stable/contents.html

## References

- MLB Qualifying Offer: https://www.mlb.com/glossary/transactions/qualifying-offer
- BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Matplotlib Documentation: https://matplotlib.org/stable/contents.html

