from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

driver = None

def setup_driver():
    try:
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.get('https://web.whatsapp.com')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        return driver
    except Exception as e:
        print("Failed to setup WebDriver:", str(e))
        return None

def send_message(driver, contact_number, message):
    try:
        search_box = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        search_box.clear()
        search_box.send_keys(contact_number)
        search_box.send_keys(Keys.ENTER)
        sleep(2)

        message_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')))
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        print(f"Message sent to {contact_number}")
        sleep(2) 
        return "Success"
    except Exception as e:
        print(f"Failed to send message to {contact_number}: {str(e)}")
        return "Failure"

@app.route("/sendmsg", methods=["POST"])
def send_whatsapp_messages():
    data = request.json
    message = data.get('message', '')
    details = data.get('details', [])
    results = []

    driver = setup_driver()
    if not driver:
        return jsonify({"error": "Failed to setup WebDriver"})

    try:
        for detail in details:
            phone = detail.get('phone')
            status = send_message(driver, phone, message)
            results.append({"phone": phone, "status": status})
            sleep(2)
    except Exception as e:
        print("Exception while sending messages:", str(e))
    finally:
        pass

    response = {"results": results}
    return jsonify(response)

@app.route("/", methods=["GET"])
def sayHI():
    return jsonify({"message":"Welcome"})

# if __name__ == "__main__":
#     app.run(debug=True)