import json
from summary_nova_model import handler

event = {
    "body": json.dumps({
        "text": """
            The Little Prince," by Antoine de Saint-Exupéry, tells the story of a pilot stranded in the 
            Sahara Desert who encounters a young prince from a distant asteroid. The prince details his 
            travels to different planets, each inhabited by a peculiar adult figure representing a flawed 
            aspect of human nature, like a conceited man or a businessman obsessed with possessions. 
            The prince's journey culminates on Earth, where he befriends the pilot and a fox who teaches 
            him about love and responsibility through taming. The prince, yearning to return to his rose, 
            allows a snake to bite him, symbolizing his return to his planet. The pilot, deeply affected 
            by the encounter, continues to hear the prince's laughter in the stars and reflects on the 
            prince's wisdom about essential truths not visible to the eye. The story explores themes of love,
            loss, loneliness, and the importance of seeing the world with innocence and a child's perspective.
      """,
    }),
    "queryStringParameters": {
        "points": "3"
    }
}


response = handler(event, {})
print(response)