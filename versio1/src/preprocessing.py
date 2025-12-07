from rich.table import Table
import pandas as pd
import re

from data.data import load_data
from config.log_config import console



# Utils
def print_table(df: pd.DataFrame):
    table = Table(title="", show_lines=True)

    for col in df.columns:
        table.add_column(col, style="cyan")

    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row.values])

    console.print(table)




def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae min_salary y max_salary de la columna 'Salary Estimate' 
    y las agrega como nuevas columnas en el DataFrame.
    """
    df = df.copy()

    def extract_numbers(text):
        numbers = re.findall(r"(\d+)", text)
        if len(numbers) >= 2:
            return int(numbers[0]) * 1000, int(numbers[1]) * 1000
        else:
            return None, None

    df["min_salary"], df["max_salary"] = zip(*df["Salary Estimate"].apply(extract_numbers))
    return df


def clean_founded(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte 'Founded' a 'Company Age'. Si Founded == -1, e sun valor null"""
    df = df.copy()
    df['Company Age'] = df['Founded'].apply(lambda x: 2025 - x if (pd.notna(x) and x != -1) else None)
    return df


def clean_size(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte 'Size' (ej. '201 to 500 employees', '10000+ employees')
    en 'Size mean' numérico.
    """
    df = df.copy()

    def parse_size(size):
        if size in [None, '-1', 'Unknown / Non-Applicable']:
            return None
        if '+' in size:
            return float(size.replace('+ employees', '').strip())
        if 'to' in size:
            low, high = size.replace('employees', '').split('to')
            return int((float(low) + float(high)) / 2)
        return None

    df['Size mean'] = df['Size'].apply(parse_size)
    return df


def clean_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte 'Revenue' (rangos tipo '$100 to $500 million (USD)')
    en 'Revenue mean'.
    """
    df = df.copy()

    def parse_revenue(rev):
        if rev in ['Unknown / Non-Applicable', '-1', None]:
            return None
        
        rev = rev.replace('(USD)', '').replace('$', '').strip()

        # Caso "X to Y million" o "billion"
        if 'to' in rev:
            low, high = rev.split('to')
            low = low.strip()
            high = high.strip()

            # Identificar unidad
            if 'million' in high:
                mul = 1_000_000
            elif 'billion' in high:
                mul = 1_000_000_000
            else:
                return None

            low_val = float(low.replace('million', '').replace('billion', '').strip()) * mul
            high_val = float(high.replace('million', '').replace('billion', '').strip()) * mul

            return (low_val + high_val) / 2
        
        return None

    df['Revenue mean'] = df['Revenue'].apply(parse_revenue)
    return df


def group_type_of_ownership(df):
    df = df.copy()

    mapping = {
        # Private
        "Company - Private": "Private",
        "Private Practice / Firm": "Private",
        "Franchise": "Private",
        "Self-employed": "Private",
        "Subsidiary or Business Segment": "Private",

        # Public and Government
        "Company - Public": "Public",
        "Nonprofit Organization": "Public",
        "Government": "Public",

        # Education and Health
        "College / University": "Education/Health",
        "School / School District": "Education/Health",
        "Hospital": "Education/Health",

        # Unknown or miscellaneous
        "-1": "Other/Unknown",
        "Unknown": "Other/Unknown",
        "Other Organization": "Other/Unknown",
        "Contract": "Other/Unknown"
    }

    df["Type of ownership grouped"] = df["Type of ownership"].map(mapping)

    return df


def clean_type_of_ownership(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Mapeig 
    mapping = {
        # Private
        "Company - Private": "Private",
        "Private Practice / Firm": "Private",
        "Franchise": "Private",
        "Self-employed": "Private",
        "Subsidiary or Business Segment": "Private",

        # Public and Government
        "Company - Public": "Public",
        "Nonprofit Organization": "Public",
        "Government": "Public",

        # Education and Health
        "College / University": "Education/Health",
        "School / School District": "Education/Health",
        "Hospital": "Education/Health",

        # Unknown or miscellaneous
        "-1": None,
        "Unknown": None,
        "Other Organization": None,
        "Contract": None
    }

    df["Ownership"] = df["Type of ownership"].map(mapping)

    dummies = pd.get_dummies(df["Ownership"], prefix="Ownership")
    df = pd.concat([df, dummies], axis=1)
    return df



def clean_sector(df: pd.DataFrame) -> pd.DataFrame:
    
    mapping = {
        # 1. Tech & Digital
        "Information Technology": "Tech & Digital",
        "Telecommunications": "Tech & Digital",
        "Media": "Tech & Digital",
        "Real Estate": "Tech & Digital",

        # 2. Business & Professional Services
        "Business Services": "Business & Professional Services",
        "Accounting & Legal": "Business & Professional Services",
        "Insurance": "Business & Professional Services",
        "Finance": "Business & Professional Services",  # o "Finance" por separado si quieres
        "Manufacturing": "Business & Professional Services",

        # 3. Healthcare & Biotech
        "Health Care": "Healthcare & Biotech",
        "Biotech & Pharmaceuticals": "Healthcare & Biotech",

        # 4. Education & Non-Profit
        "Education": "Education & Non-Profit",
        "Non-Profit": "Education & Non-Profit",

        # 5. Public Sector
        "Government": "Public Sector",
        "Aerospace & Defense": "Public Sector",  

        # 6. Industrial & Energy
        "Construction, Repair & Maintenance": "Industrial & Energy",
        "Oil, Gas, Energy & Utilities": "Industrial & Energy",
        "Mining & Metals": "Industrial & Energy",
        "Transportation & Logistics": "Industrial & Energy",

        # 7. Consumer & Retail
        "Retail": "Consumer & Retail",
        "Consumer Services": "Consumer & Retail",
        "Restaurants, Bars & Food Services": "Consumer & Retail",
        "Travel & Tourism": "Consumer & Retail",
        "Arts, Entertainment & Recreation": "Consumer & Retail",

        # 8. Unknown / Other
        "-1": None,
    }


    df["Sector grouped"] = df["Sector"].map(mapping).fillna("Other")
    dummies = pd.get_dummies(df["Sector grouped"], prefix="Sector")
    df = pd.concat([df, dummies], axis=1)
    return df


def clean_location(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    metro_map = {
        # --- NYC METRO ---
        "New York, NY": "NYC Metro",
        "Brooklyn, NY": "NYC Metro",
        "Bronx, NY": "NYC Metro",
        "Queens Village, NY": "NYC Metro",
        "Far Rockaway, NY": "NYC Metro",
        "Staten Island, NY": "NYC Metro",
        "Mount Vernon, NY": "NYC Metro",
        "Great Neck, NY": "NYC Metro",
        "Manhasset, NY": "NYC Metro",
        "Harrison, NY": "NYC Metro",
        "Lake Success, NY": "NYC Metro",
        "Valley Stream, NY": "NYC Metro",
        "West Orange, NJ": "NYC Metro",
        "Parsippany, NJ": "NYC Metro",
        "Whippany, NJ": "NYC Metro",
        "Woodbridge, NJ": "NYC Metro",
        "Iselin, NJ": "NYC Metro",
        "Jersey City, NJ": "NYC Metro",
        "Hoboken, NJ": "NYC Metro",
        "Secaucus, NJ": "NYC Metro",
        "Fairfield, NJ": "NYC Metro",
        "Weehawken, NJ": "NYC Metro",
        "Florham Park, NJ": "NYC Metro",
        "Newark, NJ": "NYC Metro",
        "Berkeley Heights, NJ": "NYC Metro",
        "Montvale, NJ": "NYC Metro",
        "Woodcliff Lake, NJ": "NYC Metro",
        "Little Ferry, NJ": "NYC Metro",
        "Essex Fells, NJ": "NYC Metro",
        "Franklin Lakes, NJ": "NYC Metro",
        "Camden, NJ": "NYC Metro",
        "Marlton, NJ": "NYC Metro",
        "Moorestown, NJ": "NYC Metro",

        # --- SF BAY AREA ---
        "San Francisco, CA": "SF Bay Area",
        "Oakland, CA": "SF Bay Area",
        "Berkeley, CA": "SF Bay Area",
        "San Mateo, CA": "SF Bay Area",
        "Redwood City, CA": "SF Bay Area",
        "Foster City, CA": "SF Bay Area",
        "Palo Alto, CA": "SF Bay Area",
        "East Palo Alto, CA": "SF Bay Area",
        "Cupertino, CA": "SF Bay Area",
        "Santa Clara, CA": "SF Bay Area",
        "San Jose, CA": "SF Bay Area",
        "Sunnyvale, CA": "SF Bay Area",
        "Mountain View, CA": "SF Bay Area",
        "Menlo Park, CA": "SF Bay Area",
        "Los Gatos, CA": "SF Bay Area",
        "Milpitas, CA": "SF Bay Area",
        "Pleasanton, CA": "SF Bay Area",
        "Union City, CA": "SF Bay Area",
        "Newark, CA": "SF Bay Area",
        "Campbell, CA": "SF Bay Area",
        "San Ramon, CA": "SF Bay Area",
        "Walnut Creek, CA": "SF Bay Area",
        "Emeryville, CA": "SF Bay Area",

        # --- LOS ANGELES METRO ---
        "Los Angeles, CA": "Los Angeles Metro",
        "Santa Monica, CA": "Los Angeles Metro",
        "Burbank, CA": "Los Angeles Metro",
        "Pasadena, CA": "Los Angeles Metro",
        "Beverly Hills, CA": "Los Angeles Metro",
        "Long Beach, CA": "Los Angeles Metro",
        "Carson, CA": "Los Angeles Metro",
        "Torrance, CA": "Los Angeles Metro",
        "Glendale, CA": "Los Angeles Metro",
        "Inglewood, CA": "Los Angeles Metro",
        "Monterey Park, CA": "Los Angeles Metro",
        "Venice, CA": "Los Angeles Metro",
        "Anaheim, CA": "Los Angeles Metro",
        "Signal Hill, CA": "Los Angeles Metro",
        "Northridge, CA": "Los Angeles Metro",
        "Whittier, CA": "Los Angeles Metro",
        "Pico Rivera, CA": "Los Angeles Metro",
        "Culver City, CA": "Los Angeles Metro",
        "Gardena, CA": "Los Angeles Metro",
        "Marina del Rey, CA": "Los Angeles Metro",
        "Hawthorne, CA": "Los Angeles Metro",
        "City of Industry, CA": "Los Angeles Metro",
        "Alhambra, CA": "Los Angeles Metro",
        "Arcadia, CA": "Los Angeles Metro",
        "Irwindale, CA": "Los Angeles Metro",

        # --- SAN DIEGO METRO ---
        "San Diego, CA": "San Diego Metro",
        "El Cajon, CA": "San Diego Metro",
        "National City, CA": "San Diego Metro",

        # --- CHICAGO METRO ---
        "Chicago, IL": "Chicago Metro",
        "Evanston, IL": "Chicago Metro",
        "Naperville, IL": "Chicago Metro",
        "Arlington Heights, IL": "Chicago Metro",
        "Oak Brook, IL": "Chicago Metro",
        "Northbrook, IL": "Chicago Metro",
        "Deerfield, IL": "Chicago Metro",
        "Downers Grove, IL": "Chicago Metro",
        "Rolling Meadows, IL": "Chicago Metro",
        "Northlake, IL": "Chicago Metro",
        "Broadview, IL": "Chicago Metro",
        "Bridgeview, IL": "Chicago Metro",
        "Itasca, IL": "Chicago Metro",
        "Maywood, IL": "Chicago Metro",
        "Glenview, IL": "Chicago Metro",
        "Elk Grove Village, IL": "Chicago Metro",
        "Burr Ridge, IL": "Chicago Metro",

        # --- HOUSTON METRO ---
        "Houston, TX": "Houston Metro",
        "Sugar Land, TX": "Houston Metro",
        "Pearland, TX": "Houston Metro",
        "Pasadena, TX": "Houston Metro",
        "Spring, TX": "Houston Metro",

        # --- DALLAS–FORT WORTH ---
        "Dallas, TX": "DFW Metro",
        "Fort Worth, TX": "DFW Metro",
        "Arlington, TX": "DFW Metro",
        "Plano, TX": "DFW Metro",
        "Richardson, TX": "DFW Metro",
        "Irving, TX": "DFW Metro",
        "Grapevine, TX": "DFW Metro",
        "Lewisville, TX": "DFW Metro",
        "Addison, TX": "DFW Metro",
        "Carrollton, TX": "DFW Metro",
        "Coppell, TX": "DFW Metro",
        "Farmers Branch, TX": "DFW Metro",
        "Southlake, TX": "DFW Metro",
        "Roanoke, TX": "DFW Metro",

        # --- AUSTIN METRO ---
        "Austin, TX": "Austin Metro",
        "Round Rock, TX": "Austin Metro",
        "Cedar Park, TX": "Austin Metro",
        "West Lake Hills, TX": "Austin Metro",

        # --- SAN ANTONIO METRO ---
        "San Antonio, TX": "San Antonio Metro",
        "Fort Sam Houston, TX": "San Antonio Metro",
        "Lackland AFB, TX": "San Antonio Metro",

        # --- PHOENIX METRO ---
        "Phoenix, AZ": "Phoenix Metro",
        "Scottsdale, AZ": "Phoenix Metro",
        "Tempe, AZ": "Phoenix Metro",
        "Mesa, AZ": "Phoenix Metro",
        "Chandler, AZ": "Phoenix Metro",
        "Glendale, AZ": "Phoenix Metro",

        # --- SALT LAKE CITY METRO ---
        "Salt Lake City, UT": "Salt Lake City Metro",
        "West Jordan, UT": "Salt Lake City Metro",
        "Sandy, UT": "Salt Lake City Metro",
        "Draper, UT": "Salt Lake City Metro",
        "Lehi, UT": "Salt Lake City Metro",
        "American Fork, UT": "Salt Lake City Metro",

        # --- PHILADELPHIA METRO ---
        "Philadelphia, PA": "Philadelphia Metro",
        "King of Prussia, PA": "Philadelphia Metro",
        "Radnor, PA": "Philadelphia Metro",
        "Malvern, PA": "Philadelphia Metro",
        "Conshohocken, PA": "Philadelphia Metro",
        "West Chester, PA": "Philadelphia Metro",
        "Blue Bell, PA": "Philadelphia Metro",
        "Norristown, PA": "Philadelphia Metro",
        "Plymouth Meeting, PA": "Philadelphia Metro",
        "Wayne, PA": "Philadelphia Metro",
        "Horsham, PA": "Philadelphia Metro",
        "Newtown Square, PA": "Philadelphia Metro",

        # --- SEATTLE METRO ---
        "Seattle, WA": "Seattle Metro",
        "Redmond, WA": "Seattle Metro",
        "Bellevue, WA": "Seattle Metro",
        "Renton, WA": "Seattle Metro",
        "Kirkland, WA": "Seattle Metro",
        "Issaquah, WA": "Seattle Metro",
        "Kent, WA": "Seattle Metro",

        # --- DENVER METRO ---
        "Denver, CO": "Denver Metro",
        "Centennial, CO": "Denver Metro",
        "Aurora, CO": "Denver Metro",
        "Boulder, CO": "Denver Metro",
        "Lakewood, CO": "Denver Metro",
        "Greenwood Village, Arapahoe, CO": "Denver Metro",
        "Englewood, CO": "Denver Metro",
        "Littleton, CO": "Denver Metro",
        "Broomfield, CO": "Denver Metro",
        "Louisville, CO": "Denver Metro",
        "Lone Tree, CO": "Denver Metro",

        # --- MINOR METROS / OTHER US ---
        "Gainesville, FL": "Other US",
        "Jacksonville, FL": "Other US",
        "Athens, GA": "Other US",
        "Columbus, OH": "Other US",
        "Westerville, OH": "Other US",
        "Hilliard, OH": "Other US",
        "Dublin, OH": "Other US",
        "Charlotte, NC": "Other US",
        "Huntersville, NC": "Other US",
        "Mooresville, NC": "Other US",
        "Indian Trail, NC": "Other US",
        "Fort Mill, SC": "Other US",
        "Indianapolis, IN": "Other US",
        "Whitestown, IN": "Other US",
        "Carmel, IN": "Other US",
        "Beech Grove, IN": "Other US",
        "Jeffersonville, IN": "Other US",
        "Lawrence, IN": "Other US",
        "Reedley, CA": "Other US",
        "Visalia, CA": "Other US",
        "Hanford, CA": "Other US",
        "Hampton, VA": "Other US",
        "Newport News, VA": "Other US",
        "Portsmouth, VA": "Other US",
        "Suffolk, VA": "Other US",
        "Virginia Beach, VA": "Other US",
        "Yorktown, VA": "Other US",
        "Smithfield, VA": "Other US",
        "Norfolk, VA": "Other US",
        "Chesapeake, VA": "Other US",
    }


    df["Location grouped"] = df["Location"].map(metro_map).fillna("Other")
    dummies = pd.get_dummies(df["Location grouped"], prefix="Location")
    df = pd.concat([df, dummies], axis=1)

    return df



def drop_variables(df):
    df = df.drop(columns=["Salary Estimate"])
    df = df.drop(columns=["Founded"])
    df = df.drop(columns=["Size"])
    df = df.drop(columns=["Revenue"])
    df = df.drop(columns=["Type of ownership"])
    df = df.drop(columns=["Sector"])
    df = df.drop(columns=["Location"])

    # Dimensions que aporten la mateixa informació que altres (o similar)
    df = df.drop(columns=["Industry"]) # Sector
    df = df.drop(columns=["Headquarters"]) # Location 

    return df


def preprocessing(df: pd.DataFrame):
    """
    Funció principal per netejar les dades
    """
    console.rule("[title]Neteja de dades[/title]")
    df = clean_salary(df)
    df = clean_founded(df)
    df = clean_size(df)
    df = clean_revenue(df)
    df = clean_type_of_ownership(df)
    df = clean_sector(df)

    df = drop_variables(df)

    console.print(f"[success]Neteja de dades completa. Dades netejades tenen "
                  f"{df.shape[0]} files i {df.shape[1]} columnes.[/success]")
    return df



if __name__ == "__main__":
    df = load_data()

    df = clean_salary(df)
    print("\nPrimeres files min/max salary:")
    print_table(df[["Salary Estimate", "min_salary", "max_salary"]].head())

    df = clean_founded(df)
    print("\nPrimeres files Company Age:")
    print_table(df[["Founded", "Company Age"]].head())

    df = clean_size(df)
    print("\nPrimeres files Size mean:")
    print_table(df[["Size", "Size mean"]].head())

    df = clean_revenue(df)
    print("\nPrimeres files Revenue mean:")
    print_table(df[["Revenue", "Revenue mean"]].head())

    df = clean_type_of_ownership(df)
    print("\nPrimeres files Ownership:")
    print_table(df[["Type of ownership", "Ownership"]].head())

    df = clean_sector(df)
    print("\nPrimeres files Sector grouped:")
    print_table(df[["Sector", "Sector grouped"]].head())

    df = clean_location(df)
    print("\nPrimeres files Location grouped:")
    print_table(df[["Location", "Location grouped"]].head())
                
    df = drop_variables(df)

