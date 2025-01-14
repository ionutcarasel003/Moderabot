from django.db import models

class Rule(models.Model):
    rule_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)
    severity = models.IntegerField()
    status = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return f"Rule {self.id}: {self.description}"

    class Meta:
        managed = False
        db_table = 'rule'



class User(models.Model):
     user_id = models.BigIntegerField(primary_key=True)
     username = models.CharField(max_length=32)
     severity_amount = models.IntegerField(default=0)
     status = models.BooleanField(default=True)
     role_id = models.BigIntegerField(null=True)
     password = models.CharField(max_length=128, null=True)

     def __str__(self):
         return self.username

     class Meta:
         managed = False
         db_table = 'user'

class Violation(models.Model):
    violation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, db_column='rule_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Violation by {self.user_id} for rule {self.rule_id}"

    class Meta:
        managed = False
        db_table = 'violation'