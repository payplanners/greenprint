#Forms.py
# Created By: Matt Agresta
# Created On: 9/05/2016
# Holds classes for each payplanner form
#-----------------------------------------------------------#
#Set up Enviroment
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Items, BudgetData, Categories, UserCat, BudgetProfile
from .widgets import RelatedFieldWidgetAddEdit

class UserCreateForm(UserCreationForm):

    """Used in registration process"""
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    
class ExpensesForm(forms.ModelForm):

    """Form to Add Expenses to Items model"""
    
    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('userid')
        super(ExpensesForm, self).__init__(*args, **kwargs)
        #Grab User Categories from UserCat model
        
        catchoices = []
        usercatlist = UserCat.objects.values('cats').filter(user=userid).order_by('cats__catName')
        for usercat in usercatlist:
            catid = usercat.get('cats')
            fullcatlist = Categories.objects.values_list('id','catName').filter(pk=catid)
            catoption = fullcatlist[0]
            catchoices.append(catoption)
        #Populate self.fields['category'] with User categories
        self.fields['category'] = forms.CharField(widget=RelatedFieldWidgetAddEdit(Categories,
                                                                                   'config',
                                                                                   edit_url='settings',
                                                                                   to_page='ExpensesForm',
                                                                                   choices=catchoices)
                                                  )

        
    class Meta:
        model = Items
        exclude = ('skiplst',)
        widgets = {'user': forms.HiddenInput(),
                   'itemType': forms.HiddenInput(),
                   'payCycle': forms.Select(),
                   'nextDueDate': forms.DateInput(attrs={'class': 'datepicker'}),
                   'endDate': forms.DateInput(attrs={'class': 'datepicker'})
                   }

        

class IncomeForm(forms.ModelForm):

    """Form to Add Income to Items model"""
    
    class Meta:
        model = Items
        exclude = ('category','skiplst')
        widgets = {'user': forms.HiddenInput(),
                   'itemType': forms.HiddenInput(),
                   'nextDueDate': forms.DateInput(attrs={'class': 'datepicker'}),
                   'endDate': forms.DateInput(attrs={'class': 'datepicker'})
                   }
        

class EditForm(forms.ModelForm):

    """Form to Edit Line items in budget"""
    
    class Meta:
        model = BudgetData
        exclude = ('effectiveDate',)
        widgets = {'parentItem':forms.HiddenInput(),
                   }
        

        
class UserCatForm(forms.ModelForm):

    """Form to select Categories for user"""
    
    form_errors = {"required": "You must choose at least one expense category"}
    cats = forms.ModelMultipleChoiceField(
        error_messages=form_errors,
        label="",
        queryset=Categories.objects.all(),
        widget=FilteredSelectMultiple("Categories",
                                      is_stacked=False,
                                      attrs={'class':'browser-default'}),
        )
    class Media:
        js = ('js/materialize_SelectFilter2.js', )

        
    class Meta:
        #Name used in save button 
        name = 'User Categories'
        #Tells template to display Add Button
        has_key = True
        #Value used in Add Button
        key_name = 'Category'
        model = UserCat
        fields = "__all__"
        widgets = {'user':forms.HiddenInput(),}


class UserProfileForm(forms.ModelForm):

    """Form for User to edit their profile"""

    class Meta:
        name = "User Profile"
        model = User
        fields = ('first_name','last_name','email')
        
        
class CategoriesForm(forms.ModelForm):

    """Form to add categories"""

    class Meta:
        name = "Category"
        model = Categories
        fields = ('catName',)


class BudgetProfileForm(forms.ModelForm):

    """Form to control budget settings"""

    class Meta:
        name = "Budget Profile"
        model = BudgetProfile
        fields = '__all__'
        widgets = {'user':forms.HiddenInput(),
                   }
