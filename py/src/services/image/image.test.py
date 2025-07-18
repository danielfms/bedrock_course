from image import handler
import json

event = {
   "body": json.dumps({"description": "A beautiful sunset over the mountains"})
}

response = handler(event, {})
print(response)