The code automates the process of downloading Purchase Order data from Zoho Books and sending it via email. Here's an architectural breakdown of the process:

**1. Initialization and Configuration:**

Dependencies: The code imports necessary libraries like pyautogui, time, glob, os, smtplib, ssl, selenium, and email-related modules.

Chrome Options: Configures Chrome WebDriver for headless operation (incognito, no GPU, ignoring certificate errors) to optimize performance and stability, especially in server or automated environments.

Account Data: Stores Zoho Books account IDs in a dictionary for iterating through multiple accounts.

WebDriver Initialization: Creates a Chrome WebDriver instance with the defined options.

**2. Zoho Books Data Extraction Loop:**

Account Iteration: Loops through each Zoho Books account ID in the Account_id dictionary.

New Tab/Window Management: Opens each Zoho Books URL in a new tab and switches to the newly opened tab.

Zoho Books Login: Automates the login process using send_keys_to_element and click_if_exists functions, entering email, password, and handling the "I Understand" button.

Navigation to Purchase Orders: Navigates to the Purchase Orders section within Zoho Books using specified XPaths.

Export Configuration: Initiates the export process, selects the "PO_with_Items" template, and chooses CSV format. This utilizes the select_from_dropdown function to handle the template selection dropdown.

Export Trigger: Clicks the final export button and handles the download prompt (using pyautogui).

Logout: Logs out of the current Zoho Books account.

File Identification: Uses get_latest_downloaded_file_name to retrieve the name of the most recently downloaded CSV file.

**3. Email Sending:**

Email Configuration: Sets sender and receiver email addresses, password, and email subject (using the account name from the dictionary key).

Email Content Creation: Creates a multipart email message, attaches the downloaded CSV file using MIMEBase, and sets appropriate headers.

SMTP Communication: Uses smtplib to connect to a Gmail SMTP server (port 465 for SSL) and sends the email with the attached CSV file.

**4. Error Handling and Cleanup:**

Try-Except Block: Wraps the entire process within a try-except block to catch potential errors during any stage.

Driver Quit: Ensures the WebDriver is closed in the finally block to release resources, regardless of whether errors occurred.

Architecture Diagram (Simplified):

![image](https://github.com/user-attachments/assets/088f7037-3fd4-4ee5-8aa9-1ce6a776f59c)

**Script:**

```
import pyautogui
import time
import glob
import os
import smtplib
import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Define a function to select an option from a dropdown
def select_from_dropdown(dropdown_xpath, option_xpath, step_name, wait_time=10):
    try:
        click_if_exists(dropdown_xpath, 'Dropdown', wait_time)
        option = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, option_xpath)))
        option.click()
        print(f"Successfully selected: {step_name}")
    except Exception as e:
        print(f"Failed to select {step_name}: {e}")

# Define a function to click an element if it exists
def click_if_exists(xpath, step_name, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        if element.is_displayed():
            element.click()
            print(f"Successfully clicked on: {step_name}")
        else:
            print(f"{step_name} is not displayed.")
    except Exception as e:
        print(f"{step_name} not found or could not be clicked: {e}")

# Define a function to send keys to an element
def send_keys_to_element(xpath, keys, step_name, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.click()
        element.send_keys(keys)
        print(f"Successfully sent keys to: {step_name}")
    except Exception as e:
        print(f"Failed to send keys to {step_name}: {e}")

def get_latest_downloaded_file_name(downloads_folder):
    # Create a pattern for all files in the downloads folder
    pattern = os.path.join(downloads_folder, '*')  # Adjust the pattern as needed

    # Get a list of files matching the pattern
    files = glob.glob(pattern)

    # If there are no files, return None
    if not files:
        return None

    # Get the latest file based on modification time
    latest_file = max(files, key=os.path.getmtime)

    # Return the name of the latest file
    return os.path.basename(latest_file)

# Account details dictionary
Account_id = {
    "Zoho PurchaseOrder_Data(yyyy)": 12345,
    "Zoho PurchaseOrder_Data(yyyy)": 65789,
    "Zoho PurchaseOrder_Data(yyyy)": 16890
}

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
chrome_options.add_argument("--disable-software-rasterizer")  # Ensure smooth operation without GPU
chrome_options.add_argument("--no-sandbox")  # Added for Linux environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems


# Set up the Chrome WebDriver with the modified options
driver = webdriver.Chrome(options=chrome_options)

try:

    for key, value in Account_id.items():
        
        
            # Open URL in a new tab
            driver.execute_script("window.open('https://books.zoho.com/app/{}/#/home/dashboard', '_blank');".format(value))
            time.sleep(5)  # Give some time for the new tab to load

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])  # Switch to the last opened tab

            send_keys_to_element('/html/body/div[5]/div[2]/div[3]/div[4]/form[1]/div[3]/div[1]/div/span/input', 'thangaramanujan.k@optisolbusiness.com', 'Email Input')
            click_if_exists('//*[@id="nextbtn"]', 'Next Button (Email)')

            time.sleep(5)

            send_keys_to_element('/html/body/div[5]/div[2]/div[3]/div[4]/form[1]/div[3]/div[2]/div[2]/input', 'Optisol@2024', 'Password Input')
            click_if_exists('//*[@id="nextbtn"]', 'Next Button (Password)')

            time.sleep(5)

            click_if_exists('//*[@id="continue_button"]', 'I Understand Button')

            time.sleep(3)

            click_if_exists("/html/body/div[6]/div[4]/div[3]/nav/ul/li[6]/ul/li/a", 'Purchases Section')

            time.sleep(3)

            click_if_exists("/html/body/div[6]/div[4]/div[3]/nav/ul/li[6]/ul/li/ul/li[3]/a", 'Purchase Orders')

            time.sleep(5)

            click_if_exists("/html/body/div[6]/div[4]/div[3]/main/div/div[1]/div[1]/div[2]/div[2]/button", 'Dropdown Toggle')

            time.sleep(3)

            click_if_exists("/html/body/div[6]/div[4]/div[3]/main/div/div[1]/div[1]/div[2]/div[2]/div/button[2]", 'Export Button')

            time.sleep(4)

            click_if_exists("/html/body/div[6]/div[7]/div[2]/div/div/div[2]/form/div[2]/div/div/div/div/div[1]/div/div/span", 'Select an Export template')

            time.sleep(2)

            # Select the "PO_with_Items" option
            select_from_dropdown(
                dropdown_xpath='//div[@id="ac-ember979"]',  # The dropdown element
                option_xpath="//span[text()='PO_with_Items']",  # The option to select
                step_name='PO_with_Items Option'
            )

            time.sleep(2)

            click_if_exists("/html/body/div[6]/div[7]/div[2]/div/div/div[2]/form/fieldset[2]/div[2]/div[1]/input", 'CSV')

            click_if_exists("/html/body/div[6]/div[7]/div[2]/div/div/div[3]/button[1]", 'Final Export Button')

            time.sleep(10)

            pyautogui.press('enter')

            click_if_exists("/html/body/div[6]/div[4]/header/div[4]/div/span/img", 'Signout_Image')

            time.sleep(2)

            click_if_exists("/html/body/div[6]/div[3]/div[3]/div[2]/div/div[1]/div[3]/a[2]", 'Sign_out_button')

            time.sleep(1)

            # Get the latest downloaded file
            downloads_folder = r'C:\Users\ashik.roshan\Downloads'
            latest_file_name = get_latest_downloaded_file_name(downloads_folder)

            if latest_file_name:
                print(f'The latest downloaded file is: {latest_file_name}')
            else:
                print('No files found in the downloads folder.')

            # Email sender and receiver
            sender_email = "xxxxx"
            receiver_email = "xxxxx"
            password = "xxxxx"

            # Create the email content
            subject = f"{key}"
            body = ""

            # Create a MIMEText object
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Attach the body to the email
            message.attach(MIMEText(body, "plain"))

            # Path to the CSV file
            file_path = f"C:\\Users\\ashik.roshan\\Downloads\\{latest_file_name}"

            # Open the file in binary mode
            with open(file_path, "rb") as attachment:
                # Create a MIMEBase object
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode the file into ASCII characters for email
            encoders.encode_base64(part)

            # Add header to the attachment
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {latest_file_name}",
            )

            # Attach the file to the email
            message.attach(part)

            # SMTP server settings
            smtp_server = "smtp.gmail.com"
            port = 465  # For SSL

            # Create a secure SSL context
            context = ssl.create_default_context()

            # Connect to Gmail's SMTP server
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                # Send the email
                server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email with attachment sent successfully!")

except Exception as e:
    print(f"An error occurred for {key}: {e}")

finally:
    driver.quit()

```
