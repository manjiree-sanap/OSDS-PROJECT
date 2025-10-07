# bankers_logic.py

class BankersAlgorithm:
    def __init__(self, available, max_demand, allocation):
        """
        Initializes the Banker's Algorithm state.
        :param available: A list of available instances for each resource.
        :param max_demand: A 2D list representing the maximum resource demand of each process.
        :param allocation: A 2D list representing the current resource allocation for each process.
        """
        self.num_processes = len(max_demand)
        self.num_resources = len(available)
        
        self.available = list(available)
        self.max_demand = list(max_demand)
        self.allocation = list(allocation)
        
        # Calculate the need matrix
        self.need = [[self.max_demand[i][j] - self.allocation[i][j] 
                      for j in range(self.num_resources)] 
                     for i in range(self.num_processes)]

    def is_safe_state(self):
        """
        Checks if the current system state is safe.
        :return: A tuple (boolean, list) indicating if the state is safe and the safe sequence.
        """
        work = list(self.available)
        finish = [False] * self.num_processes
        safe_sequence = []
        
        while len(safe_sequence) < self.num_processes:
            found_process = False
            for i in range(self.num_processes):
                if not finish[i]:
                    # Check if Need <= Work for process i
                    if all(self.need[i][j] <= work[j] for j in range(self.num_resources)):
                        # If so, "release" the resources
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        
                        finish[i] = True
                        safe_sequence.append(i)
                        found_process = True
                        break # Find the next process
            
            # If no such process was found in the entire loop, the system is not in a safe state
            if not found_process:
                return False, []

        return True, safe_sequence

    def request_resources(self, process_id, request):
        """
        Handles a resource request from a process.
        :param process_id: The ID of the requesting process.
        :param request: A list of requested instances for each resource.
        :return: A tuple (boolean, string) indicating success/failure and a message.
        """
        # 1. Check if Request <= Need
        if not all(request[j] <= self.need[process_id][j] for j in range(self.num_resources)):
            return False, f"Error: Process {process_id} has exceeded its maximum claim."

        # 2. Check if Request <= Available
        if not all(request[j] <= self.available[j] for j in range(self.num_resources)):
            return False, f"Request by P{process_id} denied. Resources not available. Process must wait."

        # 3. Pretend to allocate the resources
        for j in range(self.num_resources):
            self.available[j] -= request[j]
            self.allocation[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]

        # 4. Check if the new state is safe
        is_safe, sequence = self.is_safe_state()

        if is_safe:
            # If safe, the request is granted
            return True, f"Request by P{process_id} granted. Safe sequence: {self._format_sequence(sequence)}"
        else:
            # If not safe, roll back the changes
            for j in range(self.num_resources):
                self.available[j] += request[j]
                self.allocation[process_id][j] -= request[j]
                self.need[process_id][j] += request[j]
            return False, f"Request by P{process_id} denied. Granting request would lead to an unsafe state."

    def _format_sequence(self, sequence):
        return " -> ".join([f"P{i}" for i in sequence])