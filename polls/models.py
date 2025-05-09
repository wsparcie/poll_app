from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets

class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_valid_tokens(self):
        return self.tokens.filter(
            used=False,
            expires_at__gt=timezone.now()
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.tokens.exists():
            Token.objects.create(
                poll=self,
                expires_at=timezone.now() + timezone.timedelta(days=7)
            )

    def user_can_vote(self, user, token):
        try:
            token_obj = self.tokens.get(token=token)
            if not token_obj.is_valid():
                return False
        except Token.DoesNotExist:
            return False
        if not user.is_authenticated:
            return True
        user_votes = Vote.objects.filter(poll=self, user=user)
        if user_votes.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_answer_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']
            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100
            res.append(d)
        return res
    
    def __str__(self):
        return self.text

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_vote_count(self):
        return self.vote_set.count()
    
    @property
    def get_percentage(self):
        total_votes = self.poll.get_vote_count
        if total_votes == 0:
            return 0
        return (self.get_vote_count / total_votes) * 100
    
    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ('user', 'poll'),
            ('token', 'poll')
        ]

class Token(models.Model):
    token = models.CharField(max_length=64, unique=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="tokens")
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_unique_token()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_token():
        while True:
            token = secrets.token_hex(32)
            if not Token.objects.filter(token=token).exists():
                return token

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at

    def __str__(self):
        return self.token