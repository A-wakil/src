import requests
import base64

# Load a test image
with open("test.jpg", "rb") as image_file:
    jpg_as_text = base64.b64encode(image_file.read()).decode('utf-8')

response = requests.post(
    "http://10.1.12.47:5000/infer",
    json={"image": jpg_as_text}
)

print("Response Status Code:", response.status_code)
print("Response Text:", response.text)

