import concurrent.futures
import requests
from selenium import webdriver

# Define a function that represents the task you want to run in processes
def task_function(task, **kwargs):
    # Perform the task here
    try:
        result = perform_task(**kwargs)
        return f"Task {task} completed: {result}"
    except Exception as e:
        return f"Task {task} failed with error: {str(e)}"

# Function that performs the actual task (e.g., Selenium interaction, API request, file saving)
def perform_task(**kwargs):
    task = kwargs.get('task')
    
    # Open a browser using Selenium (you need to have Selenium and a WebDriver installed)
    driver = webdriver.Chrome()
    
    try:
        # Make an API request using requests
        api_url = kwargs.get('api_url', 'https://example.com/api')
        response = requests.get(api_url)
        
        # Save data to a file
        with open(f'data_{task}.txt', 'w') as file:
            file.write(response.text)
            
        return f"Data saved for Task {task}"
    except Exception as e:
        raise e
    finally:
        driver.quit()  # Close the browser

# List of tasks you want to run concurrently, each as a dictionary
task_list = [{'task': 1, 'api_url': 'https://example.com/api'},
             {'task': 2, 'api_url': 'https://example.com/another_api'},
             {'task': 3, 'api_url': 'https://example.com/yet_another_api'}]

# Create a ProcessPoolExecutor with a specified number of processes (e.g., 2)
num_processes = 2

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Submit the tasks to the ProcessPoolExecutor with kwargs
        results = list(executor.map(task_function, task_list))

    # Print the results
    for result in results:
        print(result)
