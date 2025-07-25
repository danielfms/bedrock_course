from rag import handler
import json

event = {
   "body": json.dumps({"question": "¿Que es un comite de etica?"})
}

response = handler(event, {})
print(response)