"""
TITLE: Steam Tag Snagger
DESCRIPTION: This script takes user input and uses it to scrape a Steam
            store page and build a list of the available tags of a game.
            It also includes the name of the game and developer(s)/publisher(s).
AUTHOR: Cedric Pereira (StOoPiD_U)
DATE: September 6th 2024
VERSION: 1.0
"""

import requests
from bs4 import BeautifulSoup


def get_steam_game_info(game_url, timeout=15):
    """
    Fetches and parses information from a supplied Steam store page.
      Args:
        game_url (str): The url of a game's Steam store page.
        timeout (int or tuple): The max number of seconds to wait for a
                              response.
      Returns:
        list: A text list containing the game name, developer/publisher name(s),
              and the Steam game tags.
      Raises:
        requests.RequestException: If there's an error fetching the page.
        requests.Timeout: If the request times out.
        AttributeError: If the expected elements are not found on the page.
    """
    try:
        # Send a GET request to the Steam store page
        response = requests.get(game_url, timeout=timeout)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract game name
        game_name = soup.find('div', class_='apphub_AppName').text.strip()

        # Extract developers
        dev_row = soup.find('div', class_='dev_row')
        developers = [dev.text.strip() for dev in dev_row.find_all('a')]

        # Extract publishers
        pub_row = soup.find_all('div', class_='dev_row')[1]
        publishers = [pub.text.strip() for pub in pub_row.find_all('a')]

        # Find the div containing the tags
        tags_div = soup.find('div', class_='glance_tags popular_tags')

        # Extract all the tags
        tags = [tag.text.strip() for tag in tags_div.find_all('a')]

        # Combine all information
        all_info = [game_name] + developers + publishers + tags

        return all_info

    except requests.Timeout as e_timeout:
        raise requests.Timeout(f"Request timed out after {timeout} seconds") from e_timeout

    except Exception as e_exception:
        print(f"An error occurred: {e_exception}")
        return None  # Indicates a failure

def main():
    """
    Main function to run steam_tag_snapper.py.
    Prompts user for game's Steam store url, fetches info and prints.
    """

    # Repeats the process to do multiple
    while True:
        # Get user input for the Store Page
        game_url = input("Enter the Steam store URL: ")

        try:
            # Get the game information
            info = get_steam_game_info(game_url)

            # Print the information as a comma-separated list
            if info:
                print("Game:")
                print(info[0])
                print("\nSteam Game Information:")
                print(', '.join(info))

                # Write to text file (unused)
                # with open('steam_info.txt', 'w', encoding='utf-8') as f:
                #     f.write(', '.join(info))

                # print("Information has been saved to 'steam_game_info.txt'")
            else:
                print("Failed to retrieve information.")

        except requests.RequestException as e_request:
            print(f"Error fetching the page: {e_request}")
        except AttributeError as e_attribute:
            print(f"Error parsing the page: {e_attribute}")
        except Exception as e_exception:
            print(f"An unexpected error occurred: {e_exception}")

    # # Close the program
    # input("Press Enter to exit...")

if __name__ == "__main__":
    main()
