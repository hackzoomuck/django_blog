from django.db import models
from django.utils import timezone
from django import forms
# Create your models here.

def min_length_3_validator(value):
     if len(value) < 3:
          raise forms.ValidationError('제목은 3글자 이상 입력해 주세요!')

class Post(models.Model):
    # 작성자
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # 제목
    title = models.CharField(max_length=200, validators=[min_length_3_validator])
    # 내용
    text = models.TextField()
    # 작성일자
    created_date = models.DateTimeField(default=timezone.now)
    # 게시일자
    published_date = models.DateTimeField(blank=True, null=True)
    # 필드 추가 - 삭제할 예정
    #test = models.TextField()
    # 게시일자에 현재날짜시간을 대입해주는 함수
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # 객체주소 대신에 글제목을 반환해주는 toString() 함수
    def __str__(self):
        return self.title

    # 승인된 Comments 만 반환해주는 함수
    def approved_comments(self):
        return self.comments.filter(approved_comment=True) #어디서 참조? post_list

# Post에 달리는 댓글 Comment 클래스
class Comment(models.Model):
    # post 정보
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    # 작성자
    author = models.CharField(max_length=100)
    # 댓글 내용
    text = models.TextField()
    # 댓글 작성일자
    created_date = models.DateTimeField(default=timezone.now)
    # 댓글 승인여부
    approved_comment = models.BooleanField(default=False)

    # 댓글 승인하기
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text