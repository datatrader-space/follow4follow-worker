import threading
import time
class ConcurrentRunner:
    def __init__(self):
        self.task_list=[]
        self.max_concurrent_tasks=10
        self.task_function=None
    def run_tasks_concurrently(self):
        task_index = 0
        running_tasks = []

        while task_index < len(self.task_list) or running_tasks:
            # Check if we can start a new task
            if task_index < len(self.task_list) and len(running_tasks) < self.max_concurrent_tasks:
                task_args = self.task_list[task_index]
                thread = threading.Thread(target=self.task_function,  kwargs=task_args)
                thread.start()
                running_tasks.append(thread)
                task_index += 1
            
            # Check if any tasks have completed
            completed_tasks = []
            for thread in running_tasks:
                if not thread.is_alive():
                    completed_tasks.append(thread)
            
            # Remove completed tasks from the running_tasks list
            for thread in completed_tasks:
                running_tasks.remove(thread)
            
            # Sleep briefly to avoid excessive CPU usage
            time.sleep(0.1)