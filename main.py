import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import googlemaps
from progress.bar import Bar

load_dotenv()

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

def get_address(business_name: str):
    """

    """

    google_maps_key = os.getenv("GOOGLEAPIKEY")

    gm = googlemaps.Client(key=google_maps_key)
    try:
        candidates, status = gm.find_place(business_name, "textquery", fields=["formatted_address", "geometry"]).values()
        return candidates[0].get("formatted_address")
    except googlemaps.exceptions.HTTPError:
        return None
    except IndexError:
        return None

def get_zip_code(business_address: str):
    """

    """

    try:
        return candidates[0].get("formatted_address")
    except IndexError:
        return None
    

if __name__ == "__main__":
    """
    Script to scrape roasters for a given country from a website 
    that maintains this data but does not give data access
    
    Outputs
    -------
    A CSV that contains all roasters by name, their website URL and region
    """
    
    roasters = {}
    country_roaster_url = "https://coffeebeaned.com/coffee-roaster-list/"
    csv_filename = "roasters"
    field_names = ['Roaster Name', 'Roaster URL', 'Region Code']

    df = pd.DataFrame()

    regions = scrape_regions(country_roaster_url)

    for region in regions.items():
        region_code, region_url = region
        regional_roasters = scrape_roasters(region_code, region_url)

        addresses = []

        with Bar(region_code, max=len(regional_roasters)) as bar:
            for roaster in regional_roasters.keys():
                #roaster_address[roaster] = get_address(roaster)
                addresses.append(get_address(f'{roaster}, {region_code}, USA'))
                bar.next()

        df_region = pd.DataFrame(list(regional_roasters.items()), columns=('Roaster Name', 'Roaster URL'))
        df_region["Roaster Address"] = addresses
        df_region['Region Code'] = region_code

        df_region.to_csv(f'{csv_filename}.{region_code}.csv')

        df = pd.concat([df, df_region])    
                                 
        df.to_csv(f'{csv_filename}.csv')

