#Author: Sanuli Yapa
#Date: 7/12/2024
#Student ID: 20232619

import csv



# Leap Year Check 
def is_leap_year(year):
    """
    Determines if a given year is a leap year.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)




# Task A: Input Validation
def validate_date_input():
    
    
    
    """
    Prompts the user to enter a date and constructs the file name for the traffic data file.
    """
    while True:
        try:
            #validate day
            while True:
                try:
                    day = int(input("Please enter the day of the survey in the format dd: "))
                    if day < 1 or day > 31:
                        print("Out of Range - values must be in the range 1 and 31.")
                        continue
                    break
                except ValueError:
                    print("Integer required.")

           #validate month
            while True:
                try:
                    month = int(input("Please enter the month of the survey in the format MM: "))
                    if month < 1 or month > 12:
                        print("Out of Range - values must be in the range 1 to 12.")
                        continue
                    break
                except ValueError:
                    print("Integer required.")
            #validate month        
            while True:
                try:
                    year = int(input("Please enter the year of the survey in the format YYYY: "))
                    if year < 2000 or year > 2024:
                        print("Out of Range - values must be in the range 2000 to 2024.")
                        continue
                    break 
                except ValueError:
                    print("Integer required.")
                   

            file_name = f"traffic_data{day:02d}{month:02d}{year}.csv"
            
            print(f"data file selected is {file_name}")
            # Print the validated date
            print(f"The date you entered is: {day:02d}/{month:02d}/{year}")

            # Generate the file name
            print(f"Generated file name: {file_name}")  # Debug print

            # Check if the file exists
            try:
                with open(file_name, 'r') as file:
                    print(f"Found file: {file_name}")
                    return file_name  # Return the file name if it exists
            except FileNotFoundError:
                print(f"File '{file_name}' not found. Please try another date.")
               
        except ValueError:
            print("Integer required. Please try again.")


#check if the user wants to continue
def validate_continue_input():
    """
    Prompts the user to decide whether to process another file.
    
    """
    while True:
        choice = input("Do you want to analyze another dataset? (y/n): ").strip().lower()
        if choice == 'y':
            return True    #user wants to continue
            
        elif choice == 'n':
            print("End of program.")
            return False   #stop
        else:
            print("Invalid input. Enter 'y' or 'n'.")
            


# Task B: Processed outcomes
#Process the traffic data from the csv files
def process_csv_data(file_name):
    """
    Reads the CSV file and calculates various traffic statistics.
    
    """
    #initialize all counters and variables
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    two_wheeled_vehicles = 0
    buses_north_elm = 0
    vehicles_straight = 0
    truck_percentage = 0
    total_bicycles = 0
    bicycle_hours = set()
    avg_bicycles_per_hour = 0
    vehicles_over_limit = 0
    vehicles_through_elm_rabbit = 0
    vehicles_through_han_west = 0
    total_scooters = 0
    total_scooters_elm = 0
    scooter_percentage = 0
    heavy_rain_hours = set()
    light_rain_hours = set()
    total_rainy_hours = 0
    hourly_count = {}
    max_vehicles = 0
    peak_hours = []
    hour = 0
    peak_hours_output = 0

    # Opening the selected file
    with open(file_name, 'r') as file:
        data = csv.reader(file)
        next(data, None)  # Skip header row

        #process each row in the line
        for row in data:
            # Calculate the total number of vehicles passing through all junctions
            total_vehicles += 1

            # Calculate the total number of trucks passing through all junctions
            if row[8] == "Truck":
                total_trucks += 1

            # Calculate the total number of electric vehicles passing through all junctions
            if row[9] == "True":
                total_electric_vehicles += 1

            # Calculate the number of “two-wheeled” vehicles through all junctions
            if row[8].lower() in ["bicycle", "motorcycle", "scooter"]:
                two_wheeled_vehicles += 1

            # Calculate the total number of buses leaving Elm Avenue/Rabbit Road junction heading north
            if (row[0] == "Elm Avenue/Rabbit Road" and
                row[8] == "Buss" and
                row[4] == "N"
            ):
                buses_north_elm += 1

            # Calculate the total number of vehicles passing through both junctions without turning left or right
            if row[3] == row[4]:
                vehicles_straight += 1

            # Calculate the percentage of all vehicles recorded that are trucks
            if total_vehicles > 0:  # Avoid division by zero
                truck_percentage = round((total_trucks / total_vehicles) * 100)
            else:
                truck_percentage = 0

            # Calculate the average number of bicycles per hour
            if row[8] == "Bicycle":
                bicycle_hours.add(row[2][:2])  # Collect the hour for each bicycle
                total_bicycles += 1

            if len(bicycle_hours) > 0:
                avg_bicycles_per_hour = round(total_bicycles / len(bicycle_hours))

            # Calculate the total number of vehicles recorded as over the speed limit
            if row[7].isdigit() and row[6].isdigit():
                if int(row[7]) > int(row[6]):
                    vehicles_over_limit += 1

            # Calculate the total number of vehicles recorded through Elm Avenue/Rabbit Road junction
            if row[0] == "Elm Avenue/Rabbit Road":
                vehicles_through_elm_rabbit += 1
                if row[8] == "Scooter":
                    total_scooters_elm += 1

            # Calculate the total number of vehicles recorded through Hanley Highway/Westway junction
            if row[0] == "Hanley Highway/Westway":
                vehicles_through_han_west += 1

            # Calculate the percentage of scooters at Elm Avenue
            if vehicles_through_elm_rabbit > 0:  # Avoid division by zero
                scooter_percentage = round((total_scooters_elm / vehicles_through_elm_rabbit) * 100)
            else:
                scooter_percentage = 0

            # Calculate the time of the peak traffic hour (or hours) on Hanley Highway/Westway
            if row[0] == "Hanley Highway/Westway":
                hour = row[2][:2]  # Extract the hour from timeOfDay (e.g., "14:30" -> "14")
              

                if hour.isdigit() and 0 <= int(hour) <= 23:
                    # Validate the hour and update its count
                    hourly_count[hour] = hourly_count.get(hour, 0) + 1

            max_vehicles = max(hourly_count.values(), default=0)
            peak_hours = [hour for hour, count in hourly_count.items() if count == max_vehicles]




            # Calculate the total number of hours of rain
            if row[5] == "Heavy Rain":
                heavy_rain_hours.add(row[2][:2])
            elif row[5] == "Light Rain" :
                light_rain_hours.add (row[2][:2])

            total_rainy_hours = len(heavy_rain_hours)+len(light_rain_hours)
            


    #return all calculated results
    return [
        total_vehicles, total_trucks, total_electric_vehicles, two_wheeled_vehicles,
        buses_north_elm, vehicles_straight, truck_percentage, avg_bicycles_per_hour,
        vehicles_over_limit, vehicles_through_elm_rabbit, vehicles_through_han_west,
        total_scooters, total_scooters_elm, scooter_percentage, max_vehicles, peak_hours,
        heavy_rain_hours,total_rainy_hours,hour,
        ]


#Sisplay the processed results
def display_outcomes(results):
    if results:
        print("")
        print(f"The total number of vehicles recorded for this date is: {results[0]}")
        print(f"The total number of trucks recorded for this date is: {results[1]}")
        print(f"The total number of electric vehicles for this date is: {results[2]}")
        print(f"The total number of two-wheeled vehicles for this date is: {results[3]}")
        print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is: {results[4]}")
        print(f"The total number of vehicles through both junctions not turning left or right: {results[5]}")
        print(f"The percentage of total vehicles recorded that are trucks for this date is: {results[6]}%")
        print(f"The average number of bicycles per hour for this date is: {results[7]}")
        print("")
        print(f"The total number of vehicles recorded as over the speed limit for this date is: {results[8]}")
        print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is: {results[9]}")
        print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is: {results[10]}")
        print(f"{results[13]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters")
        print("")
        print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {results[14]}")
        print(f"The most vehicles through Hanley Highway/Westway were recorded between {results[15][0]}:00 and {int(results[15][0]) + 1}:00")
        print(f"The number of hours of rain for this date is : {results[17]}")


#Task C: Save results as a text file
def save_results_to_file(results, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file.
    """
    # Format the results into a single string
    results_str = (
        f"********************************************** \n"
        f"data file selected is traffic_data15062024.csv  \n"
        f"********************************************** \n"
        f"The total number of vehicles recorded for this date is: {results[0]} \n"
        f"The total number of trucks recorded for this date is: {results[1]} \n"
        f"The total number of electric vehicles for this date is: {results[2]} \n"
        f"The total number of two-wheeled vehicles for this date is: {results[3]} \n"
        f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is: {results[4]} \n"
        f"The total number of vehicles through both junctions not turning left or right: {results[5]} \n"
        f"The percentage of total vehicles recorded that are trucks for this date is: {results[6]}% \n"
        f"The average number of bicycles per hour for this date is: {results[7]} \n"
        f"The total number of vehicles recorded as over the speed limit for this date is: {results[8]} \n"
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is: {results[9]} \n"
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is: {results[10]} \n"
        f"{results[13]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters \n"
        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {results[14]} \n"
        f"The most vehicles through Hanley Highway/Westway were recorded between {results[15][0]}:00 and {int(results[15][0]) + 1}:00"
        f"The number of hours of rain for this date is : {results[17]}"
        f"*******************************************************\n"

        
    )

    # Open the file in append mode and write the formatted results
    with open(file_name, "a") as file:
        file.write(results_str)
    print(f"Results saved to {file_name}")



# Main
# Main loop to repeatedly process files until the user decides to stop
while True:
    # Validate and get the file name based on user input
    file_name = validate_date_input()
    # If a valid file name is returned, process the file
    if file_name:
        results = process_csv_data(file_name)
        if results:
            display_outcomes(results)
            save_results_to_file(results, "results.txt")
        else:
            print("No outcome to display.Please try another file.")
    
    else:
        print("Invalid file name. Please try again.") 
       
    # Prompt user for continuation
    continue_choice = validate_continue_input()
    if continue_choice:
        # If the user wants to process another file,restart the loop
        continue
    else:
        #exit the loop
        break
        
        

            
        
    
    






