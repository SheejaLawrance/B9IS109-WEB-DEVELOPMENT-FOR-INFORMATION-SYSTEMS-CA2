from django.db import models
import pandas as pd
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=15)
    
    class Meta:
        verbose_name_plural="Categories"
    
    
    def __str__(self):
        return self.name

class Quiz(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    quiz_file=models.FileField(upload_to='quiz/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural="Quizes"
        
    def __str__(self):
        return self.title
    
    #fetch excel on quizsave
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        if self.quiz_file:
            self.import_quiz_from_excel()
            
    def import_quiz_from_excel(self):
        #read
        #dataframe created
        df=pd.read_excel(self.quiz_file.path)

        #iterate
        for index, row in df.iterrows():
            #extract que, choice and correct answer
            question_text=row['Question']
            option1=row['A']
            option2=row['B']
            option3=row['C']
            option4=row['D']
            correct_ans=row['Answer']
        
            #Question object
            question_obj= Question.objects.get_or_create(quiz=self, text=question_text)
            #Choice obj
            option1_obj=Choice.objects.get_or_create(question=question_obj[0], text=option1, is_correct=correct_ans=='A')
            option2_obj=Choice.objects.get_or_create(question=question_obj[0], text=option2, is_correct=correct_ans=='B')
            option3_obj=Choice.objects.get_or_create(question=question_obj[0], text=option3, is_correct=correct_ans=='C')
            option4_obj=Choice.objects.get_or_create(question=question_obj[0], text=option4, is_correct=correct_ans=='D')
            
class Question(models.Model):
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text=models.TextField()
    
    def __str__(self):
        return self.text[:50]
    
class Choice(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.CharField(max_length=255)
    is_correct=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.question.text[:50]}, {self.text[:20]}"
    
class QuizSubmission(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score=models.IntegerField()
    submitted_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user},{self.quiz.title}"
        
class UserRank(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    rank=models.IntegerField(null=True, blank=True)
    total_score=models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.rank}, {self.user.username}"
 
@receiver(post_save, sender=QuizSubmission)
def update_leaderboard(sender,instance,created,**kwargs):
    if created:
        update_leaderboard()

    
def update_leaderboard():
    #sum the score for all users
    user_scores=(QuizSubmission.objects.values('user').annotate(total_score=Sum('score')).order_by('-total_score'))
    #sort
    rank=1
    for entry in user_scores:
        user_id=entry['user']
        total_score=entry['total_score']

        
        user_rank, created=UserRank.objects.get_or_create(user_id=user_id)
        user_rank.rank=rank
        user_rank.total_score=total_score
        user_rank.save()
        
        rank+=1
    