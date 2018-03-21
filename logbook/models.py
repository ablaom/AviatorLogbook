from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm, NumberInput, TextInput, SelectDateWidget, DateInput
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Manufacturer(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class FAA_part(models.Model):
    number = models.CharField(max_length=10)
    def __str__(self):
        return self.number

class Engine(models.Model):
    complexity = models.CharField(max_length=20)
    def __str__(self):
        return self.complexity

class Equipment(models.Model):
    class Meta:
        ordering = ['complexity']
    complexity = models.CharField(max_length=20)
    def __str__(self):
        return self.complexity

class Make_and_model(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=50)
    manufacturer =   models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True)
    engine =         models.ForeignKey(Engine, on_delete=models.CASCADE, null=True)
    equipment =      models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name    
     
class Flight(models.Model):
    pilot = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.date.today)
    was_recreational = models.BooleanField(default=False)
    remarks =          models.CharField(max_length=500, blank=True)
    route =            models.CharField(max_length=500, blank=True)
    aircraft_ID =      models.CharField(max_length=10)
    faa_part =         models.ForeignKey(FAA_part, on_delete=models.CASCADE, null=True)
    make_and_model =   models.ForeignKey(Make_and_model, on_delete=models.CASCADE, null=True)
    
    # hours total:
    duration = models.FloatField(default=0.0)

    # hours breakdown
    command_practice = models.FloatField(default=0.0)
    actual =           models.FloatField(default=0.0)
    hood =             models.FloatField(default=0.0)
    night =            models.FloatField(default=0.0)
    CFI =              models.FloatField(default=0.0)
    dual =             models.FloatField(default=0.0)
    XC =               models.FloatField(default=0.0)
    PIC =              models.FloatField(default=0.0)
    SIC =              models.FloatField(default=0.0)
    solo =             models.FloatField(default=0.0)

    
    # hours futher breadown:
    night_actual = models.FloatField(default=0.0)
    XC_actual =    models.FloatField(default=0.0)
    night_hood =   models.FloatField(default=0.0)
    XC_hood =      models.FloatField(default=0.0)
    XC_night =     models.FloatField(default=0.0)
    PIC_XC =       models.FloatField(default=0.0)
    SIC_XC =       models.FloatField(default=0.0)
    solo_XC =      models.FloatField(default=0.0)
    
    # approaches:
    ILS = models.IntegerField(default=0)
    VOR = models.IntegerField(default=0)
    NDB = models.IntegerField(default=0)
    LOC = models.IntegerField(default=0)
    BC =  models.IntegerField(default=0)
    GPS = models.IntegerField(default=0)
    ASR = models.IntegerField(default=0)
    AR =  models.IntegerField(default=0.0)    

    # landings:
    day_landings =   models.IntegerField(default=0.0)
    night_landings = models.IntegerField(default=0.0)

    # class methods to summarize flight info over the class attribute _filtered:
    
    @classmethod
    def clear_filter(cls, user):
        cls._filtered = cls.objects.filter(pilot=user)
    
    # hours total:
    @classmethod
    def duration_sum(cls):
        return sum([flight.duration for flight in cls._filtered])

    # hours breakdown:
    @classmethod
    def command_practice_sum(cls):
        return sum([flight.command_practice for flight in cls._filtered])
    @classmethod
    def actual_sum(cls):
        return sum([flight.actual for flight in cls._filtered])
    @classmethod
    def hood_sum(cls):
        return sum([flight.hood for flight in cls._filtered])
    @classmethod
    def night_sum(cls):
        return sum([flight.night for flight in cls._filtered])
    @classmethod
    def CFI_sum(cls):
        return sum([flight.CFI for flight in cls._filtered])
    @classmethod
    def dual_sum(cls):
        return sum([flight.dual for flight in cls._filtered])
    @classmethod
    def XC_sum(cls):
        return sum([flight.XC for flight in cls._filtered])
    @classmethod
    def PIC_sum(cls):
        return sum([flight.PIC for flight in cls._filtered])
    @classmethod
    def SIC_sum(cls):
        return sum([flight.SIC for flight in cls._filtered])
    @classmethod
    def solo_sum(cls):
        return sum([flight.solo for flight in cls._filtered])
        
    # hours futher breadown:
    @classmethod
    def night_actual_sum(cls):
        return sum([flight.night_actual for flight in cls._filtered])
    @classmethod
    def XC_actual_sum(cls):
        return sum([flight.XC_actual for flight in cls._filtered])
    @classmethod
    def night_hood_sum(cls):
        return sum([flight.night_hood for flight in cls._filtered])
    @classmethod
    def XC_hood_sum(cls):
        return sum([flight.XC_hood for flight in cls._filtered])
    @classmethod
    def XC_night_sum(cls):
        return sum([flight.XC_night for flight in cls._filtered])
    @classmethod
    def PIC_XC_sum(cls):
        return sum([flight.PIC_XC for flight in cls._filtered])
    @classmethod
    def SIC_XC_sum(cls):
        return sum([flight.SIC_XC for flight in cls._filtered])
    @classmethod
    def solo_XC_sum(cls):
        return sum([flight.solo_XC for flight in cls._filtered])
  
    # approaches:
    @classmethod
    def ILS_sum(cls):
        return sum([flight.ILS for flight in cls._filtered])
    @classmethod
    def VOR_sum(cls):
        return sum([flight.VOR for flight in cls._filtered])
    @classmethod
    def NDB_sum(cls):
        return sum([flight.NDB for flight in cls._filtered])
    @classmethod
    def LOC_sum(cls):
        return sum([flight.LOC for flight in cls._filtered])
    @classmethod
    def BC_sum(cls):
        return sum([flight.BC for flight in cls._filtered])
    @classmethod
    def GPS_sum(cls):
        return sum([flight.GPS for flight in cls._filtered])
    @classmethod
    def ASR_sum(cls):
        return sum([flight.ASR for flight in cls._filtered])
    @classmethod
    def AR_sum(cls):
        return sum([flight.AR for flight in cls._filtered])
    @classmethod
    def total_approaches_sum(cls):
        return sum([flight.total_approaches() for flight in cls._filtered])
    
    # landings:
    @classmethod
    def day_landings_sum(cls):
        return sum([flight.day_landings for flight in cls._filtered])
    @classmethod
    def night_landings_sum(cls):
        return sum([flight.night_landings for flight in cls._filtered])
    @classmethod
    def total_landings_sum(cls):
        return sum([flight.total_landings() for flight in cls._filtered])    

    # methods:
    def __str__(self):
        return self.date.strftime('%m.%d.%Y ') + ' ' + self.route  + ' (' + str(self.duration) + ' hours)'

    def within_90_days(self):
        return datetime.date.today() - self.date <= datetime.timedelta(90)

    def within_30_days(self):
        return datetime.date.today() - self.date <= datetime.timedelta(30)

    def within_6_months(self):
        return datetime.date.today() - self.date <= datetime.timedelta(180)

    def within_1_year(self):
        return datetime.date.today() - self.date <= datetime.timedelta(365)

    def total_approaches(self):
        return self.ILS + self.VOR + self.NDB + self.LOC + self.BC + self.GPS + self.ASR

    def total_landings(self):
        return self.day_landings + self.night_landings

    def CFI_actual(self):
        return self.actual if self.CFI > 0 else 0

    def CFI_night(self):
        return self.night if self.CFI > 0 else 0

    def dual_actual(self):
        return self.actual if self.dual > 0 else 0

    def dual_hood(self):
        return self.hood if self.dual > 0 else 0

    def dual_night(self):
        return self.night if self.dual > 0 else 0

    def XC_CFI(self):
        return self.XC if self.CFI > 0 else 0

    def XC_dual(self):
        return self.XC if self.dual > 0 else 0

    def PIC_actual(self):
        return self.actual if self.PIC > 0 else 0

    def PIC_hood(self):
        return self.hood if self.PIC > 0 else 0

    def PIC_night(self):
        return self.night if self.PIC > 0 else 0

    def PIC_CFI(self):
        return self.CFI if abs(self.CFI - self.PIC) < 0.001 else 0

    def PIC_dual(self):
        return self.PIC if self.dual > 0 else 0

    def SIC_actual(self):
        return self.actual if self.SIC > 0 else 0

    def SIC_hood(self):
        return self.hood if self.SIC > 0 else 0

    def SIC_night(self):
        return self.night if self.SIC > 0 else 0

    def SIC_CFI(self):
        return self.CFI if abs(self.CFI - self.SIC) < 0.001 else 0

    def SIC_dual(self):
        return self.SIC if self.dual > 0 else 0

    def solo_actual(self):
        return self.actual if self.solo > 0 else 0

    def solo_night(self):
        return self.night if self.solo > 0 else 0

    def solo_PIC(self):
        return self.PIC if abs(self.solo - self.PIC) < 0.001 else 0

    # more class methods for summarizing:
    @classmethod
    def CFI_actual_sum(cls):
        return sum([flight.CFI_actual() for flight in cls._filtered])
    @classmethod
    def CFI_night_sum(cls):
        return sum([flight.CFI_night() for flight in cls._filtered])
    @classmethod
    def dual_actual_sum(cls):
        return sum([flight.dual_actual() for flight in cls._filtered])
    @classmethod
    def dual_hood_sum(cls):
        return sum([flight.dual_hood() for flight in cls._filtered])
    @classmethod
    def dual_night_sum(cls):
        return sum([flight.dual_night() for flight in cls._filtered])
    @classmethod
    def XC_CFI_sum(cls):
        return sum([flight.XC_CFI() for flight in cls._filtered])
    @classmethod
    def XC_dual_sum(cls):
        return sum([flight.XC_dual() for flight in cls._filtered])
    @classmethod
    def PIC_actual_sum(cls):
        return sum([flight.PIC_actual() for flight in cls._filtered])
    @classmethod
    def PIC_hood_sum(cls):
        return sum([flight.PIC_hood() for flight in cls._filtered])
    @classmethod
    def PIC_night_sum(cls):
        return sum([flight.PIC_night() for flight in cls._filtered])
    @classmethod
    def PIC_CFI_sum(cls):
        return sum([flight.PIC_CFI() for flight in cls._filtered])
    @classmethod
    def PIC_dual_sum(cls):
        return sum([flight.PIC_dual() for flight in cls._filtered])
    @classmethod
    def SIC_actual_sum(cls):
        return sum([flight.SIC_actual() for flight in cls._filtered])
    @classmethod
    def SIC_hood_sum(cls):
        return sum([flight.SIC_hood() for flight in cls._filtered])
    @classmethod
    def SIC_night_sum(cls):
        return sum([flight.SIC_night() for flight in cls._filtered])
    @classmethod
    def SIC_CFI_sum(cls):
        return sum([flight.SIC_CFI() for flight in cls._filtered])
    @classmethod
    def SIC_dual_sum(cls):
        return sum([flight.SIC_dual() for flight in cls._filtered])
    @classmethod
    def solo_actual_sum(cls):
        return sum([flight.solo_actual() for flight in cls._filtered])
    @classmethod
    def solo_night_sum(cls):
        return sum([flight.solo_night() for flight in cls._filtered])
    @classmethod
    def solo_PIC_sum(cls):
        return sum([flight.solo_PIC() for flight in cls._filtered])
   
# set up the NumberInput widgets needed for the FlightForm fields and adjust remarks field
# and the TAB ORDER:

def number_widget(i): # returns widget with tabindex `i`
   return NumberInput(attrs={'style':'width:4em', 'min':0, 'max':100, 'tabindex':i})

#   define a dictionary keyed on the names of number fields whose value is the tabindex of that field
tabindex =      {'duration':10,
         'command_practice':0,
                   'actual':14,
                     'hood':0,
                    'night':13,
                      'CFI':0,
                     'dual':0,
                       'XC':12,
                      'PIC':11,
                      'SIC':0,
                     'solo':0,
             'night_actual':15,
                'XC_actual':16,
               'night_hood':0,
                  'XC_hood':0,
                 'XC_night':17,
                   'PIC_XC':18,
                   'SIC_XC':0,
                  'solo_XC':0,
                      'ILS':7,
                      'VOR':0,
                      'NDB':0, 
                      'LOC':0,
                       'BC':0,
                      'GPS':8, # rendered as 'RNAV' in the template 
                      'ASR':0,
                       'AR':9,
             'day_landings':5, 
           'night_landings':6}
#               -- text field tab indices are set below --
fields = tabindex.keys()

class_widgets = dict()
for f in fields:
    class_widgets[f] = number_widget(tabindex[f])

class_widgets['date'] =                          DateInput(attrs={'tabindex':1})
class_widgets['aircraft_ID'] =                   TextInput(attrs={'tabindex':2})
class_widgets['route'] =                         TextInput(attrs={'tabindex':3})
class_widgets['remarks'] = TextInput(attrs={'style':'width:30em', 'tabindex':4})
# currently not using this next block:
YEARS = [1980 + i for i in range(60)]
MONTHS = {
    1:'jan', 2:'feb', 3:'mar', 4:'apr',
    5:'may', 6:'jun', 7:'jul', 8:'aug',
    9:'sep', 10:'oct', 11:'nov', 12:'dec'}
# class_widgets['date'] = SelectDateWidget(years=YEARS, months=MONTHS)                                 

class FlightForm(ModelForm):
    class Meta:
        model = Flight
        fields = ['date', 'route', 'was_recreational', 'remarks',
        'aircraft_ID', 'make_and_model', 'faa_part', 'duration', 'command_practice',
        'actual', 'hood', 'night', 'CFI', 'dual', 'XC', 'PIC', 'SIC', 'solo',
        'night_actual', 'XC_actual', 'night_hood', 'XC_hood', 'XC_night', 'PIC_XC', 'SIC_XC',
        'solo_XC', 'ILS', 'VOR', 'NDB', 'LOC', 'BC', 'GPS', 'ASR', 'AR',
        'day_landings', 'night_landings']
        widgets = class_widgets

class MakeModelForm(ModelForm):
    class Meta:
        model = Make_and_model
        fields = ['name', 'manufacturer', 'engine', 'equipment']
