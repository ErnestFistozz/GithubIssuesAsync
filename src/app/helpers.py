import time
import csv


def convert_utc_epoch_to_seconds(utc_epoch_seconds: int):
    current_time_seconds = time.time()
    remaining_seconds = utc_epoch_seconds - current_time_seconds
    return remaining_seconds


def repositories(file_name: str) -> list | None:
    try:
        with open(file_name, 'r') as file:
            return [line.split()[0].split("/") for line in file]
    except FileNotFoundError as e:
        print(f'required file does not exist, full error details: {e}')
        return None


def save_into_file(file_path: str, data: list) -> None:
    if data:
        try:
            with open(file_path, 'a+', newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                for row in data:
                    writer.writerow(row)
        except Exception as e:
            print(f"Error saving data to {file_path}: {str(e)}")
