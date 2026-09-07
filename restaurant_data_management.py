
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import json
import os
import shutil
import io
import unittest
from unittest.mock import patch
from langchain_ollama import ChatOllama


    
FILEPATH = "data/structured_restaurant_data.json"
BACKUP_PATH = 'data/structured_restaurant_data.json.bak'
EXAMPLE_RESTAURANT_PARAGRAPH = "Down in **Santa Monica**, **Mar de Cortez** serves as a **sun-drenched**, **casual taqueria** specializing in **Baja-style seafood**. With a **4.2/5** rating, it captures the salt-air energy of the coast through its signature beer-battered snapper tacos and zesty octopus ceviche, making it a premier spot for open-air dining near the pier. Price range: "

## Exercise 1: Integrate the LLM model from Lesson 1
# You will need the LLMs you defined in lesson 1 to structure new restaurant paragraph inputs. In addition to these functions, you will need to implement a new function `new_data_entry_process(paragraph, itemId)`, which takes inputs:
# -   `paragraph`: the new restaurant paragraph;
# -   `itemId`: the ID of this new item.
# This new function combines and uses the generative models you defined in lesson 1 to structure a given new restaurant paragraph.
# In your `restaurant_data_management.py`, copy and paste the following code block and complete the functions.
#   **Important**: Take a screenshot of your implementation of the `new_data_entry_process()` and name it `M1L3_new_data_entry_process.jpg`.


#Update your restaurant_data_structure_prompt_generation
def restaurant_data_structure_prompt_generation(restaurant_paragraph):
    system_msg = """
        You are an expert data extraction assistant.

        Your task is to extract structured restaurant information from a
        restaurant description.

        Return ONLY valid JSON.
        Do not include markdown, explanations, or ```json``` code fences.

        Extract only information explicitly provided in the paragraph.
        If a field is not available, use null.
        """

    prompt_txt = f"""
        Convert the following restaurant description into structured JSON.

        Restaurant description:
        {restaurant_paragraph}

        Return a JSON object containing the restaurant information.
        The output must be valid JSON and contain no additional text.
        """

    return system_msg, prompt_txt

# Might need to explain why we are using granite here (cheap)
def llm_model(system_msg, prompt_txt, params=None):
    model_id = 'llava:latest'
    model = ChatOllama(
        model=model_id,
        temperature=0
    )
    response = model.invoke([
        ("system", system_msg),
        ("human", prompt_txt)
    ])

    return response.content

def JSON_auto_repair_prompts(response, error_message):

    system_msg = """
        You are a JSON repair assistant.

        Your task is to repair invalid JSON.
        Return ONLY the corrected valid JSON.
        Do not include markdown, explanations, or code fences.
        """

    prompt_txt = f"""
        The following response was supposed to be valid JSON:

        {response}

        It produced the following validation/parsing error:

        {error_message}

        Repair the JSON so that it is valid.
        Preserve all available information.
        Return ONLY the corrected JSON.
        """
    return system_msg, prompt_txt

def new_data_entry_process(paragraph, itemId):

    # 1. Generate the prompts
    system_msg, prompt_txt = restaurant_data_structure_prompt_generation(paragraph)

    # 2. Get the LLM response
    response = llm_model(
        system_msg,
        prompt_txt
    )

    # 3. Try to parse the JSON
    try:
        restaurant_data = json.loads(response)

    except json.JSONDecodeError as e:

        # 4. Ask the LLM to repair invalid JSON
        repair_system_msg, repair_prompt_txt = JSON_auto_repair_prompts(
            response,
            str(e)
        )

        repaired_response = llm_model(
            repair_system_msg,
            repair_prompt_txt
        )

        restaurant_data = json.loads(repaired_response)

    # 5. Add the item ID
    restaurant_data["itemId"] = itemId

    return restaurant_data

def manage_restaurants(file_path, backup_path):
    while True:
        data = load_data(file_path)

        print(f"\n🏨 RESTAURANT DATABASE | Records: {len(data)}")
        print("1. Browse All (Names)")
        print("2. View Detailed Record")
        print("3. Add New Restaurant")
        print("4. Edit Restaurant Info")
        print("5. Delete Restaurant")
        print("6. Exit")

        choice = input("\nAction: ")

        # ---------------------------------------------------------
        # 1. Browse all restaurant names
        # ---------------------------------------------------------
        if choice == '1':
            print("\n--- Current Listings ---")

            for i, res in enumerate(data):
                print(f"{i}: {res.get('name', 'N/A')}")

        # ---------------------------------------------------------
        # 2. View detailed restaurant record
        # ---------------------------------------------------------
        elif choice == '2':
            try:
                index = int(input("Enter record index: "))

                if 0 <= index < len(data):
                    show_restaurant_card(data, index)
                else:
                    print("invalid index.")

            except ValueError:
                print("invalid index.")

        # ---------------------------------------------------------
        # 3, 4, 5. Write operations
        # ---------------------------------------------------------
        elif choice in ['3', '4', '5']:

            print("\n❗ SECURITY WARNING: You are entering write-mode.")
            print("Changes will be saved to the database immediately.")

            confirm = input(
                "Are you sure? (type 'yes' to proceed): "
            ).lower()

            if confirm != 'yes':
                print("Operation cancelled.")
                continue

            # -----------------------------------------------------
            # 3. ADD NEW DATA
            # -----------------------------------------------------
            if choice == '3':

                itemId = 1000000 + len(data) + 1

                # Ask for restaurant description
                paragraph = input(
                    "\nEnter the new restaurant description:\n"
                )

                # Process paragraph with LLM
                new_restaurant = new_data_entry_process(
                    paragraph,
                    itemId
                )

                # Add to existing data
                data.append(new_restaurant)

                # Save
                save_data(data, file_path)

                print("✅ Restaurant added.")

            # -----------------------------------------------------
            # 4. EDIT DATA
            # -----------------------------------------------------
            elif choice == '4':

                try:
                    index = int(input("Enter record index to edit: "))

                    if 0 <= index < len(data):

                        # Iterate over existing keys
                        for key in data[index].keys():

                            current_value = data[index][key]

                            new_value = input(
                                f"{key} [{current_value}]: "
                            )

                            # Empty input = don't update
                            if new_value.strip() != "":
                                data[index][key] = new_value

                        # Save changes
                        save_data(data, file_path)

                        print("✅ Record updated.")

                    else:
                        print("invalid index.")

                except ValueError:
                    print("invalid index.")

            # -----------------------------------------------------
            # 5. DELETE DATA
            # -----------------------------------------------------
            elif choice == '5':

                try:
                    index = int(input("Enter record index to delete: "))

                    if 0 <= index < len(data):

                        data.pop(index)

                        save_data(data, file_path)

                        print("✅ Record deleted.")

                    else:
                        print("invalid index.")

                except ValueError:
                    print("invalid index.")

        # ---------------------------------------------------------
        # 6. EXIT
        # ---------------------------------------------------------
        elif choice == '6':
            print("Exiting restaurant database.")
            break

        else:
            print("Invalid input.")



class TestRestaurantDatabase(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary clean database for testing."""
        self.test_file = 'data/structured_restaurant_data_unit_test.json'
        self.test_file_backup = 'data/structured_restaurant_data_unit_test.json.bak'
        self.initial_data = [{"name": "Test Cafe", "location": "Test City"}]
        with open(self.test_file, 'w') as f:
            json.dump(self.initial_data, f)

    def tearDown(self):
        """Clean up the test file after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
		if os.path.exists(self.test_file_backup):
			os.remove(self.test_file_backup)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_and_delete_restaurant_success(self, mock_stdout, mock_input):
        """
        Test Scenario: Add a new restaurant.
        Inputs: '3' (Add), 'yes' (Confirm), 'New Burger Joint', '6' (Exit)
        """
        # We mock the sequence of user inputs
        mock_restaurant = 'The Copper Sprout is a high-concept, Modern Appalachian farm-to-table destination that blends an industrial-chic aesthetic with rustic forest charm, featuring reclaimed wood and amber lighting to create a sophisticated yet cozy vibe. Priced in the $$ category, the menu celebrates seasonal foraging and local heritage, headlined by signature dishes like Cast-Iron Smoked Trout with pickled fiddlehead ferns and hand-foraged Wild Mushroom Risotto with aged goat cheese. The experience is designed to be intimate and earthy, making it a premier spot for those seeking high-quality, smokehouse-influenced cuisine in a refined, atmospheric setting.'
        mock_input.side_effect = ['3', 'yes', mock_restaurant, '6']
        
        # Run the app
        try:
            manage_restaurants(self.test_file, self.test_file_backup)
        except SystemExit:
            pass # Handle exit if your script uses sys.exit()

        # Check if the data was actually saved
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        print(data)
        self.assertEqual(len(data), 2)
        self.assertIn("✅ Restaurant added.", mock_stdout.getvalue())

        mock_input.side_effect = ['5', 'yes', 1, '6']
        
        # Run the app
        try:
            manage_restaurants(self.test_file, self.test_file_backup)
        except SystemExit:
            pass # Handle exit if your script uses sys.exit()

        # Check if the data was actually saved
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        print(data)
        self.assertEqual(len(data), 1)

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_security_cancel(self, mock_stdout, mock_input):
        """
        Test Scenario: Try to delete but say 'no' to security warning.
        Inputs: '5' (Delete), 'no' (Cancel), '6' (Exit)
        """
        mock_input.side_effect = ['5', 'no', '6']
        
        manage_restaurants(self.test_file, self.test_file_backup)
        
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1) # Data should remain unchanged
        self.assertIn("Operation cancelled.", mock_stdout.getvalue())
		
if __name__ == "__main__":
    unittest.main() # Unit Test
	# manage_restaurants(FILEPATH, BACKUP_PATH) # Actual UI Call



