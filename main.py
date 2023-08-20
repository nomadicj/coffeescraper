import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



def scrape_roasters(region_code: str, region_page_url: str):
    """
    Given a page, scrapes and returns the roasters on that page.
    
    Parameters
    ----------
    region_code : str
        The region code of the page to be scraped
    region_page_url : str
        The URL of the page to be scraped

    Returns
    -------
    roaster_dict
        A dictionary of roasters from the page. 
        In the form {
            'Roaster1 Name': 'Roaster1 URL',
            'Roaster2 Name': 'Roaster2 URL'
            }
    """

    roaster_dict = {}

    print(f'Processing {region_code}.')

    region_page = requests.get(region_page_url)

    soup = BeautifulSoup(region_page.content, "html.parser")

    results = soup.find(class_=re.compile("tablepress tablepress-.*", re.I))

    roaster_elements = results.find_all("a", class_="crl2")

    for roaster_element in roaster_elements:
        try:
            roaster_dict[roaster_element.text] = roaster_element['href']
        except:
            pass

    #print(roaster_dict.items())

    print(f'Found {len(roaster_dict)} roasters in {region_code}.')

    return(roaster_dict)


def scrape_regions(country_page_url: str):
    """
    Given a page, scrapes and returns the region urls on that page.
    
    Parameters
    ----------
    country_page_url : str
        The URL of the page to be scraped

    Returns
    -------
    region_dict
        A dictionary of regions from the page. 
        In the form {
            'Region1 Code': 'Region1 URL',
            'Region2 Code': 'Region2 URL'
            }
    """

    region_dict = {}

    page = requests.get(country_page_url)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_="state-list")

    regions = results.find_all("a")

    for region in regions:
        try:
            region_dict[region.text] = region['href']
        except:
            pass

    print(f'Found {len(region_dict)} regions.')

    return region_dict


def push_to_csv(csv_filename: str, field_names: list, roasters: dict):
    """ 
    Creates a pandas dataframe from a dictionary and column names
    and writes them to a file.
    
    Parameters
    ----------
    csv_filename: str
        The name of the file to be written to
    field_names: list
        The column header names
    roasters: dict
        The dictionary from which the dataframe is to be created

    """

    df = pd.DataFrame(list(roasters.items()), columns=field_names)

    df.to_csv(csv_filename)


if __name__ == "__main__":
    """
    
    """
    
    roasters = {}
    country_roaster_url = "https://coffeebeaned.com/coffee-roaster-list/"
    csv_filename = "roasters.csv"
    field_names = ['Roaster Name', 'Roaster URL']

    regions = scrape_regions(country_roaster_url)

    for region in regions.items():
        region_code, region_url = region
        regional_roasters = scrape_roasters(region_code, region_url)

        for regional_roaster in regional_roasters.items():
            regional_roaster_name, regional_roaster_url = regional_roaster
            roasters[regional_roaster_name] = regional_roaster_url

    push_to_csv(csv_filename, field_names, roasters)


