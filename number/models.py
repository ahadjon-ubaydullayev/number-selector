from django.db import models

class UserAction(models.Model):
	user_action = models.IntegerField(default=0)


class SimOrder(models.Model):
	full_name = models.CharField(max_length=255, blank=True, null=True)
	order_cost = models.CharField(max_length=255, blank=True, null=True)
	order_number = models.CharField(max_length=255, blank=True, null=True)
	tel_number = models.CharField(max_length=255, blank=True, null=True)
	full_address = models.CharField(max_length=255, blank=True, null=True)
	order_step = models.IntegerField(default=0, blank=True, null=True)
	user_id = models.CharField(max_length=255, blank=True, null=True)
	active = models.BooleanField(default=False)
