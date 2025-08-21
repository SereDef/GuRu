# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4==4.13.4",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import requests
    from bs4 import BeautifulSoup
    return BeautifulSoup, requests


@app.cell
def _(BeautifulSoup, requests):
    # Link to the Generation R data wiki
    page = requests.get('https://epi-wiki.erasmusmc.nl/wiki/genrwiki/index.php?title=DataWiki_Generation_R')

    # Parse the html main page
    soup = BeautifulSoup(page.content, "html.parser")
    return (soup,)


@app.cell
def _(soup):
    soup
    return


@app.cell
def _(BeautifulSoup, requests, soup):
    page_links = soup.find_all("a", href=lambda x: x and x.startswith(
        ("/wiki/genrwiki/index.php","https://p-epi-wiki.erasmusmc.nl/wiki/data")))

    def print_page_content(page_links):
    
        for link in page_links:
            page_url = link["href"]

            # Get the parent <p> element's text
            parent_p = link.find_parent("p")
            parent_text = parent_p.get_text() if parent_p else ""

            # Find the closest h2 above this link (this is expected to contain the cohort: GenR or GenR Next)
            closest_h2 = link.find_previous("h2")
            cohort = closest_h2.get_text(strip=True) if closest_h2 else ""

            if cohort in ["Generation R"]: # "Generation R Next"

                # Find the closest h3 above this link (this is expected to contain the pariod)
                closest_h3 = link.find_previous("h3")
                period = closest_h3.get_text(strip=True) if closest_h3 else ""

                # Find the closest h4 above this link (this is expected to contain the data type (e.g. general, measurements...))
                closest_h4 = link.find_previous("h4")
                data_type = closest_h4.get_text(strip=True) if closest_h4 else ""

                if page_url.startswith("https://p-epi-wiki.erasmusmc.nl/wiki/data"):
                
                    # This file is located on the main page 

                    file_url = page_url
                
                    # All download links are expected to be decorated by "Add this file to your basket"
                    # Any notes on the usage of the file (for example, PIs or instructions are after)
                    file_name, file_notes = parent_text.split("Add this file to your basket")
            
                    file_name = file_name.strip()
                    file_notes = file_notes.strip()
                
                    # print(f"File: ~{file_name}~")
                    # print(f"Download URL: ~{file_url}~")
                    # print(f"Notes: ~{file_notes}~")
                    # print(f"Cohort: ~{cohort}~")
                    # print(f"Period: ~{period}~")
                    # print(f"Data type: ~{data_type}~")
                    # print("-" * 50)
    
                else:
                    # This files are nested

                    new_page = requests.get(f"https://epi-wiki.erasmusmc.nl/{page_url}")
                    scoop = BeautifulSoup(new_page.content, "html.parser")

                    scoop_content = scoop.find_all("p")

                    for p in scoop_content:

                        sub_link = p.find("a", href=lambda x: x and x.startswith("https://p-epi-wiki.erasmusmc.nl/wiki/data"))
                    
                        if sub_link:

                            file_url = sub_link["href"]
        
                            # All download links are expected to be decorated by "Add this file to your basket"
                            # Any notes on the usage of the file (for example, PIs or instructions are after)
                            try:
                                file_name, file_notes = p.get_text().split("Add this file to your basket")
                            except:
                                # Only one instance: the link is to the filename directly 
                                file_name = p.get_text()
                                file_notes = ""
                            
                            file_name = file_name.strip()
                            file_notes = file_notes.strip()

                            closest_b = p.find_previous("p.b")
                            parent2 = closest_b.get_text(strip=True) if closest_b else ""
                    
                            # print(f"File: ~{file_name}~")
                            # # print(f"Page URL: ~{page_url}~")
                            # print(f"Download URL: ~{file_url}~")
                            # print(f"Notes: ~{file_notes}~")
                            # print(f"Cohort: ~{cohort}~")
                            # print(f"Period: ~{period}~")
                            # print(f"Data type: ~{data_type}~")
                            # print(f"Parent: ~{parent_text}~")
                            # print(f"Parent2: ~{parent2}~")
                            # print("-" * 50)

                        elif (p.find("b")
                             ) or (p.find("a", href=lambda x: x and x.startswith("https://erasmusmc.sharepoint.com"))
                             ) or (p.get_text().strip() == ""):
                            # This is a (sub)heading or a data dictionary or an empty line 
                            continue
                        else:
                            print(f"Problem: ~{p.get_text()}~")
                            print("-" * 50)

    print_page_content(page_links)
    return


if __name__ == "__main__":
    app.run()
