import subprocess
import polars as pl
import requests
import json

class ConnectivityChecker:
    def __init__(self, tasks_json):
        self.tasks = json.loads(tasks_json)
        self.results = []

    def check_connectivity(self):
        for task in self.tasks:
            if not task.get('address'):
                self.results.append((task.get('address', ''), 'Invalid Address', task.get('endpoint_id', 'Unknown')))
            else:
                self._perform_check(task)

    def check_single(self, task_json):
        task = json.loads(task_json)
        if not task.get('address'):
            self.results.append((task.get('address', ''), 'Invalid Address', task.get('endpoint_id', 'Unknown')))
        else:
            self._perform_check(task)

    def _perform_check(self, task):
        address = task['address']
        check_type = task['check_type']
        endpoint_id = task.get('endpoint_id', 'Unknown')

        if check_type == 'ping':
            result = self.ping(address)
        elif check_type == 'http':
            result = self.http_request(address)
        else:
            result = (address, 'Invalid check type', endpoint_id)

        self.results.append(result + (endpoint_id,))

    def ping(self, ip_address):
        try:
            subprocess.check_output(["ping", "-c", "1", ip_address])
            return ip_address, 'Ping Success'
        except subprocess.CalledProcessError:
            return ip_address, 'Ping Failed'

    def http_request(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return url, 'HTTP Success'
            else:
                return url, f'HTTP Failed with status code {response.status_code}'
        except requests.RequestException as e:
            return url, f'HTTP Failed with error {e}'

    def to_polars_df(self):
        df = pl.DataFrame(self.results, columns=['Address', 'Status', 'Endpoint ID'])
        return df