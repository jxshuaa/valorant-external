import uuid
import re
import json
import time
import random
import os

UUID_PATTERN = r'UUID = "([a-f0-9]{32})"'
NUMBER_PATTERN = r'#[a-f0-9]+'

def random_number_string():
    return f"#{random.randint(1000000000000000000000, 9999999999999999999999)}"

def random_number_lines(num_lines=5):
    return "\n".join(random_number_string() for _ in range(num_lines))

def ensure_uuid_and_numbers_in_file(filename, num_lines=5):
    try:
        with open(filename, "r") as f:
            content = f.read()

        new_uuid = uuid.uuid4().hex
        number_lines = random_number_lines(num_lines)

        if not re.search(UUID_PATTERN, content):
            new_content = f'{number_lines}\nUUID = "{new_uuid}"\n{content}\nUUID = "{new_uuid}"\n{number_lines}'
            with open(filename, "w") as f:
                f.write(new_content)
            print(f"Added new UUID and numbers to {filename}: {new_uuid}")
        else:
            content_lines = content.split('\n')
            updated_content = []

            if not all(re.search(NUMBER_PATTERN, line) for line in content_lines[:num_lines]):
                updated_content.append(number_lines)
            
            updated_content.extend(content_lines)

            if not all(re.search(NUMBER_PATTERN, line) for line in content_lines[-num_lines:]):
                updated_content.append(number_lines)
            
            new_content = "\n".join(updated_content)
            with open(filename, "w") as f:
                f.write(new_content)
            print(f"Ensured UUID and numbers in {filename}")
    except Exception as e:
        print(f"Error ensuring UUID and numbers in {filename}: {e}")

def updateUUID_and_numbers_in_file(filename, new_uuid, num_lines=5):
    try:
        with open(filename, "r") as f:
            content = f.read()

        new_uuid_str = f'UUID = "{new_uuid}"'
        number_lines = random_number_lines(num_lines)

        content_new = re.sub(UUID_PATTERN, new_uuid_str, content)

        lines = content_new.split('\n')
        updated_content = []

        if not all(re.search(NUMBER_PATTERN, line) for line in lines[:num_lines]):
            updated_content.append(number_lines)

        updated_content.extend(lines)

        if not all(re.search(NUMBER_PATTERN, line) for line in lines[-num_lines:]):
            updated_content.append(number_lines)

        content_new = "\n".join(updated_content)

        with open(filename, "w") as f:
            f.write(content_new)

        print(f"Done! New UUID and numbers for {filename}: {new_uuid}")
    except Exception as e:
        print(f"Error updating UUID and numbers in {filename}: {e}")

def ensure_uuid_in_json(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        if 'UUID' not in data:
            new_uuid = uuid.uuid4().hex
            data['UUID'] = new_uuid
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Added new UUID to {filename}: {new_uuid}")
    except Exception as e:
        print(f"Error ensuring UUID in {filename}: {e}")

def updateUUID_in_json(filename, new_uuid):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        data['UUID'] = new_uuid

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Done! New UUID for {filename}: {new_uuid}")
    except Exception as e:
        print(f"Error updating {filename}: {e}")

def main():
    files_to_update = ['main.py', 'config.json']
    
    for filename in files_to_update:
        if filename.endswith('.json'):
            ensure_uuid_in_json(filename)
        else:
            ensure_uuid_and_numbers_in_file(filename)

    new_uuids = {
        'main.py': uuid.uuid4().hex,
        'config.json': uuid.uuid4().hex
    }

    for filename, new_uuid in new_uuids.items():
        if filename.endswith('.json'):
            updateUUID_in_json(filename, new_uuid)
        else:
            updateUUID_and_numbers_in_file(filename, new_uuid)
    
    print("Completed updating all files.")
    time.sleep(2)
    
    print("Spoof complete! Would you like to run main.py?")
    while True:
        user_input = input("Enter 'yes' to run or 'no' to skip: ").strip().lower()
        if user_input in ['yes', 'y']:
            os.system('python main.py')
            break
        elif user_input in ['no', 'n']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    
    while True:
        user_input = input("Do you want to run the spoof again? (yes/no): ").strip().lower()
        if user_input in ['yes', 'y']:
            main()
            break
        elif user_input in ['no', 'n']:
            print("Exiting the script.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == '__main__':
    main()
