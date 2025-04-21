import random

class ProfileData:
    # List of test usernames with mixed cultural names
    TEST_USERNAMES = [
        {
            "first_name": "Mary",
            "last_name": "Chan"
        },
        {
            "first_name": "David",
            "last_name": "Wong"
        },
        {
            "first_name": "Jennifer",
            "last_name": "Kim"
        },
        {
            "first_name": "Michael",
            "last_name": "Zhang"
        },
        {
            "first_name": "Sarah",
            "last_name": "Lee"
        }
    ]
    
    @staticmethod
    def get_random_username():
        """Return a random username from the list"""
        return random.choice(ProfileData.TEST_USERNAMES)
    
    IMAGE_PATH = "test_data/images/profile.jpg"
    
    NEW_URL = "test-automation"