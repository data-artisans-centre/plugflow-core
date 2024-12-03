class WOEIDLocations:
    """Utility class to manage and select locations by WOEID."""

    @staticmethod
    def get_location_list():
        """
        Provide a comprehensive list of locations with their WOEIDs.
        
        Returns:
            list: A list of dictionaries containing location details.
        """
        locations = [
            {"woeid": 1, "name": "Worldwide", "country": "Global"},
            {"woeid": 23424977, "name": "United States", "country": "United States"},
            {"woeid": 23424975, "name": "United Kingdom", "country": "United Kingdom"},
            {"woeid": 23424848, "name": "Brazil", "country": "Brazil"},
            {"woeid": 23424853, "name": "Canada", "country": "Canada"},
            {"woeid": 23424829, "name": "Australia", "country": "Australia"},
            {"woeid": 23424909, "name": "Indonesia", "country": "Indonesia"},
            {"woeid": 23424916, "name": "Italy", "country": "Italy"},
            {"woeid": 23424955, "name": "Mexico", "country": "Mexico"},
            {"woeid": 23424934, "name": "Japan", "country": "Japan"},
            {"woeid": 23424950, "name": "Malaysia", "country": "Malaysia"},
            {"woeid": 23424948, "name": "Korea", "country": "South Korea"},
            {"woeid": 23424954, "name": "Netherlands", "country": "Netherlands"},
            {"woeid": 23424900, "name": "France", "country": "France"},
            {"woeid": 23424868, "name": "Germany", "country": "Germany"},
            {"woeid": 23424922, "name": "India", "country": "India"},
            {"woeid": 23424964, "name": "Russia", "country": "Russia"},
            {"woeid": 23424969, "name": "Spain", "country": "Spain"},
            {"woeid": 23424787, "name": "Turkey", "country": "Turkey"},
            {"woeid": 23424852, "name": "Argentina", "country": "Argentina"}
        ]
        return locations

    @staticmethod
    def display_locations():
        """
        Display locations in a formatted manner for user selection.
        
        Returns:
            list: A list of dictionaries containing location details.
        """
        locations = WOEIDLocations.get_location_list()
        
        print("Available Locations:")
        print("-" * 50)
        print("{:<5} {:<20} {:<20}".format("Index", "WOEID", "Location"))
        print("-" * 50)
        
        for index, location in enumerate(locations, 1):
            print("{:<5} {:<20} {:<20}".format(
                index, 
                location['woeid'], 
                f"{location['name']} ({location['country']})"
            ))
        
        return locations

    @staticmethod
    def get_woeid_by_index(index):
        """
        Get WOEID by its index in the list.
        
        Args:
            index (int): Index of the location (1-based)
        
        Returns:
            int: WOEID of the selected location
        """
        locations = WOEIDLocations.get_location_list()
        
        if 1 <= index <= len(locations):
            return locations[index - 1]['woeid']
        else:
            raise ValueError("Invalid location index. Please select a valid index.")
    
    @staticmethod
    def find_location_by_name(location_name):
        """
        Find location by its name.
        
        Args:
            location_name (str): The name of the location (case-insensitive)
        
        Returns:
            dict: Location details or None if not found.
        """
        locations = WOEIDLocations.get_location_list()

        # Search for the location, case-insensitively
        for location in locations:
            if location_name.strip().lower() == location['name'].strip().lower():
                return location
        
        return None
