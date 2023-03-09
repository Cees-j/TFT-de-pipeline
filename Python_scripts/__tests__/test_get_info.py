import csv
import sys
import os
sys.path.append('..')
from Get_challengers_euw2.Classes_2 import GetInformation

def test_process_csv_file():
    # Test if process_csv_file correctly extracts specified column for a given CSV file
    with open('test.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([
            ['Name', 'Age', 'City'],
            ['John', '23', 'New York'],
            ['Jane', '27', 'San Francisco'],
            ['Bob', '35', 'Chicago']
        ])
    
    gi = GetInformation(column='City', dl_bucket='bucket-name', dl_filename='file.csv', extract_col=2)
    with open('test.csv', 'r', newline='') as csvfile:
        result_list = gi.process_csv_file(csv.reader(csvfile))
    
    assert result_list == ['New York', 'San Francisco', 'Chicago']
    os.remove('test.csv')
