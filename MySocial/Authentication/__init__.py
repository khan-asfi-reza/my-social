
# OTP Model
# class OTP(models.Model):
#     # One Time Code
#     otp = models.IntegerField()
#     # Phone Number
#     phone_number = models.CharField(max_length=20)
#     # Country Code
#     country_code = models.CharField(max_length=6,
#                                     verbose_name='Phone number country code',
#                                     default='+1',
#                                     null=False,
#                                     blank=False)
#     # Use Case of otp
#     use_case = models.SmallIntegerField(choices=[(1, "Verify"), (2, "Forget Password"), (3, "Others")], default=1)
#     verified = models.BooleanField(default=False)

