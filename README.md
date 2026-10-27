# PesaPulse: API Data Analysis Using Python Structures

## Project Overview

This project analyses customer data retrieved from the JSONPlaceholder API. The objective is to practise fetching API data, exploring nested JSON structures, extracting attributes, working with Python dictionaries and sets, counting values and using pandas and Matplotlib to analyse and present results.

**Data source:** https://jsonplaceholder.typicode.com/users

The API provides mock customer records containing personal details, addresses, geographical coordinates, email addresses, websites and company information.

## Project Structure

```text
day1-api-analysis/
├── analysis.py
├── output/
│   ├── customers.csv
│   ├── city_counts.csv
│   └── customer_distribution.png
├── requirements.txt
└── README.md
```

The `.venv` directory contains the local Python virtual environment and is excluded from version control.

## Tools and Libraries

- **Python:** Fetching, processing and analysing data.
- **Requests:** Retrieving data from the API.
- **pandas:** Creating a DataFrame, inspecting data types, validating counts and exporting CSV files.
- **Matplotlib:** Creating and saving the distribution chart.
- **Pathlib:** Managing output file paths.
- **PyArrow:** Columnar data processing support

## Setup and Execution

### 1. Clone the repository

```bash
git clone https://github.com/sndili/day1-api-analysis.git
cd day1-api-analysis
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1 
```

### 4. Install dependencies

```powershell
pip install requests pandas numpy matplotlib pyarrow
pip install -r requirements.txt
```

### 5. Run the analysis

```powershell
python analysis.py
```

The script fetches data from the API, explores the first customer record, calculates city and email domain suffix counts, creates a pandas DataFrame, validates the city counts and saves the output files in the `output` directory.

If the API request fails, the script displays an error message and stops the analysis instead of continuing with an empty dataset.

## Approach

### 1. Fetching the data

The `get_customers()` function retrieves customer records from the live API using `requests.get()` with a 10-second timeout. It checks HTTP responses with `raise_for_status()` and handles request-related failures.

### 2. Exploring nested JSON

The `explore()` function recursively prints each key and its Python data type, using indentation to show the nested structure.

The API contains nested dictionaries under `address`, `address.geo` and `company`. For example, the latitude is accessed through:

```python
customer["address"]["geo"]["lat"]
```

The longitude is accessed through:

```python
customer["address"]["geo"]["lng"]
```

These are the deepest access paths used to extract the geographical coordinates. Both values are converted from strings to floating-point numbers.

### 3. Extracting attributes

The `extract_attributes()` function converts each nested customer record into a flat dictionary containing 12 fields: 

`customer_id`, `name`, `username`, `email`, `email_domain`, `phone`, `city`, `zipcode`, `latitude`, `longitude`, `company` and `website`.

The API's `id` field is renamed to `customer_id`. The `email_domain` field stores the full domain, such as `april.biz`.

### 4. Analysing cities and email domains

The `unique_cities()` function uses a set comprehension to identify distinct cities.

The `city_counts()` and `email_domain_counts()` functions use dictionaries and loops to count occurrences without using `Counter` or pandas for the initial calculations. Email domain suffixes are extracted from the final part of each email domain. For example, the suffix of `april.biz` is `biz`.

The counts are sorted from highest to lowest, with alphabetical ordering used to break ties.

### 5. DataFrame validation and export

The flat records are converted into a pandas DataFrame. The script prints the DataFrame's shape and data types, then compares the manually calculated city counts with pandas' `value_counts()` results.

The customer records and city counts are exported to CSV files `output/city_counts.csv` and `output/customers.csv` without additional index columns.

### 6. Visualisation

The script generates a bar chart showing customer counts by email domain suffix and saves it as `output/customer_distribution.png`.

The city distribution was also examined. Since every city has exactly one customer in this dataset, a city chart would show equal counts across all cities. The email domain suffix chart is more informative because it reveals differences in the frequency of email suffixes.

## Findings

The successful API analysis produced the following results:

1. **10 customer records** were retrieved from the API.
2. **10 unique cities** were identified, with one customer per city.
3. **8 distinct email domain suffixes** were found. The `biz` suffix was the most common, appearing 3 times.
4. The resulting DataFrame had **10 rows and 12 columns**.
5. The manual city counts matched pandas' calculated counts, confirming consistency between the two approaches.

These findings describe the mock dataset returned by the API during the successful run.

## Output Files

| File | Description |
|---|---|
| `output/customers.csv` | Flat customer records containing the 12 required attributes |
| `output/city_counts.csv` | Customer counts for each city, sorted by frequency |
| `output/customer_distribution.png` | Bar chart of customer counts by email domain suffix |

## Assumptions and Limitations

- The API is expected to return a list of customer records with the documented nested fields.
- Email domain suffixes are identified using the text after the final dot in the email domain.
- The findings describe the records returned during the run. API availability and returned data may vary.
- If the API request fails, the script stops rather than substituting hardcoded sample data.
- The city distribution is not varied in this dataset because each city appears once. Email domain suffix counts therefore provide a more useful distribution for visualisation.

## Repository

GitHub: https://github.com/sndili/day1-api-analysis
