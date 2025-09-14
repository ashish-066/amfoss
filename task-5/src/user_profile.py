from utils import get_profile, update_profile

class UserProfile:
    
    def __init__(self, username):
        self.username = username
        existing = get_profile(username)
        
        if existing:
            self.score = existing.get('score', 0)
            self.high_score = existing.get('high_score', 0)
            self.difficulty = existing.get('difficulty', 'easy')
        else:
            self.score = 0
            self.high_score = 0
            self.difficulty = 'easy'
            self.save()

    def increase_score(self, points=10):
        self.score += points
        
        if self.score > self.high_score:
            self.high_score = self.score
        
        self.adapt_difficulty()
        self.save()

    def adapt_difficulty(self):
        if self.score > 50:
            self.difficulty = 'hard'
        elif self.score > 20:
            self.difficulty = 'medium'
        else:
            self.difficulty = 'easy'

    def save(self):
        profile_data = {
            "username": self.username,
            "score": self.score,
            "high_score": self.high_score,
            "difficulty": self.difficulty
        }
        update_profile(profile_data)
