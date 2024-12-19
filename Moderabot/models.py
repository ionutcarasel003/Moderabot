from django.db import models

class Rule(models.Model):
    rule_id = models.IntegerField(blank=True,primary_key=True,unique=True,null=False)
    created_at = models.DateTimeField(blank=True,null=False)
    lastUpdate = models.DateTimeField(blank=True)
    severity = models.IntegerField(blank=True,null=False)
    status = models.BooleanField(blank=True,null=False)
    description = models.TextField(blank=True,null=False)

    def __str__(self):
        return f"Rule {self.id}: {self.description}"

    class Meta:
        managed = False
        db_table = 'rule'



class User(models.Model):
     user_id = models.IntegerField(blank=True,null=False,primary_key=True,unique=True)
     username = models.TextField(blank=True,null=False,max_length=32)
     severity_amount = models.IntegerField(blank=True,null=False)
     status = models.BooleanField(blank=True,null=False)
     role_id = models.IntegerField(blank=True,null=True)
     password = models.TextField(blank=True,null=True,max_length=16)

     def __str__(self):
         return self.username

     class Meta:
         managed = False
         db_table = 'user'

class Violation(models.Model):
    violation_id = models.IntegerField(blank=True,null=False,primary_key=True,unique=True)
    user_id = models.IntegerField(blank=True,null=False)
    rule_id = models.IntegerField(blank=True,null=False)
    timestamp = models.DateTimeField(blank=True,null=False)

    def __str__(self):
        return f"Violation by {self.user_id} for rule {self.rule_id}"

    class Meta:
        managed = False
        db_table = 'violation'