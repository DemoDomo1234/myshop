from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.urls import reverse

class MyUserManager(BaseUserManager):
    def create_user(self, email,  username, number, name, familie ,
    gender, date_of_birth , national_code , password=None , is_admin=False,
    is_staff=False, is_active=True , is_special = False , is_seller = False , is_superuser = False):
        if not username:
            raise ValueError('Users must have an username address')
        elif not email:
            raise ValueError('Users must have an email address')
        elif not password:
            raise ValueError('Users must have an password address')

        else:
            email=self.normalize_email(email),
            user = self.model(username = username, number = number , name = name, familie = familie ,
            gender = gender , date_of_birth = date_of_birth , national_code = national_code )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self , email ,  username , number , name , familie , gender , date_of_birth , national_code , password = None):
        user = self.create_user(username=username , email=email , number = number , name=name , familie=familie ,  password=password , gender = gender , date_of_birth = date_of_birth , national_code = national_code)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=200 , unique=True)
    name = models.CharField(max_length=200 )
    familie = models.CharField(max_length=200 )
    email = models.EmailField(max_length=254 )
    number = models.CharField(max_length=11)
    gender = models.BooleanField()
    date_of_birth = models.DateField()
    national_code = models.CharField(max_length=10)
    date_special = models.DateField(null=True , blank=True)
    is_seller = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'email' , 'number' , 'name' , 'familie' , 'gender' , 'date_of_birth' , 'national_code']

    def __str__(self):
        return self.username
        
    def get_absolute_url(self):
        return reverse("account:login")

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class CompanySeller(models.Model):
    choices = (
        ('d' , 'draft'),
        ('s' , 'special'),
        ('n' , 'normal'),
    )
    user = models.OneToOneField(User , related_name='user_seller_company' , on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=200 , choices = choices)
    fixed_number = models.CharField(max_length=11 )
    economic_code = models.CharField(max_length=11)
    permission_to_sign = models.CharField(max_length=11)
    time = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        return self.user.username

class SellerAccount(models.Model):
    choices = (
        ('d' , 'draft'),
        ('s' , 'special'),
        ('n' , 'normal'),
    )
    choice = (
        ('d' , 'draft'),
        ('s' , 'special'),
        ('n' , 'normal'),
    )
    user = models.OneToOneField(User , related_name='user_seller_account' , on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    shaba_number = models.CharField(max_length=24)
    shop_number = models.CharField(max_length=200 , choices = choices)
    shop_type = models.CharField(max_length=200 , choices = choice)
    tax = models.DateField(null = True , blank = True)
    national_card = models.ImageField()
    time = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        return self.shop_name