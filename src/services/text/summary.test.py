import json
from summary_nova_model import handler

event = {
    "body": json.dumps({
        "text": """
            The Little Prince by Antoine de Saint-Exupéry, tells the story of a pilot stranded in the Sahara Desert who encounters a young prince from a distant asteroid. The prince, on a journey of self-discovery, shares his experiences visiting different planets, each inhabited by adults exhibiting peculiar, often absurd, behaviors. Through these encounters, the prince grapples with themes of love, loss, responsibility, and the nature of human relationships, particularly his attachment to his rose. Ultimately, the prince's journey leads him to understand the importance of emotional connection and the value of what cannot be seen with the eyes, but only with the heart. 
            The pilot, initially focused on practical matters of survival, gradually connects with the prince's innocence and wisdom. The prince befriends a fox who teaches him about taming and the significance of forming unique bonds. The fox emphasizes that true understanding comes from investing time and emotion in something, making it special and irreplaceable, just like the prince's rose. 
            The prince's exploration culminates in a poignant farewell, as he prepares to return to his own asteroid, symbolized by a fatal snake bite. The prince's departure highlights the bittersweet nature of love and loss, emphasizing the enduring connection between the prince and the pilot, even across vast distances. The story concludes with the pilot reflecting on the prince's wisdom and the importance of cherishing simple truths and meaningful connections. 
            Through its whimsical narrative and profound insights, "The Little Prince" encourages readers to embrace childhood wonder, question societal norms, and value love, friendship, and the unseen connections that shape our lives. It reminds us that true wisdom often lies in recognizing the importance of what is felt in the heart rather than what is visible to the eye.
      """,
    }),
    "queryStringParameters": {
        "points": "3"
    }
}


response = handler(event, {})
print(response)