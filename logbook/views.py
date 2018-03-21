from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from models import Flight, Manufacturer, FAA_part, Make_and_model, Engine, Equipment
from models import FlightForm, MakeModelForm
import datetime

today = datetime.date.today
NUM_RECENT_ENTRIES_DISPLAYED = 3
NUM_RECENT_ENTRIES_DISPLAYED_HOMEPAGE = 20


month_numbered = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul',
     8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}


def total_hours(flight_set):
    return sum([f.duration for f in flight_set])

class Month_Hours():
    def __init__(self, month=0, hours=0):
        self.month = month
        self.hours = hours
    def __repr__(self):
        return str(self.month) + ': ' + str(self.hours)
    
class Year_Hours():
    def __init__(self, year=0, hours=0):
        self.year = year
        self.hours = hours
    def __repr__(self):
        return str(self.year) + ': ' + str(self.hours)

def encoded(date_string):
    sep = re.match(r'\d+([^\d])', date_string).group(1) # get separation character
    m, d, y = tuple([int(s) for s in date_string.split(sep)])
    if y < 100:
        if y < 50:
            y = 2000 + y
        else:
            y = 1900 + y
    return datetime.date(y,m,d)
    
# views:

@login_required
def index(request):
    # Get years:
    years = set()
    Flight.clear_filter(request.user)
    flights = Flight._filtered
    for f in flights:
        years.add(f.date.year)
    years = list(years)
    years.sort(lambda x,y : y - x) # reverse numerical 
    year_hour_data = []
    for y in years:
        hours=total_hours(flights.filter(date__year=y))
        hours = '%0.f' % hours
        year_hour_data.append(Year_Hours(y, hours))

    # Get recent entries:
    recent_entries = flights.order_by('-id')[:NUM_RECENT_ENTRIES_DISPLAYED_HOMEPAGE]

    # Get summary information:
    duration_sum = Flight.duration_sum()
    last_90 = Flight._filtered.filter(date__range=(today()-datetime.timedelta(90),today()))
    last_30 = Flight._filtered.filter(date__range=(today()-datetime.timedelta(90),today()))
    hours_in_last_90 = sum([f.duration for f in last_90])
    hours_in_last_30 = sum([f.duration for f in last_30])
    landings = Flight.total_landings_sum()
    landings_in_last_90 = sum([f.total_landings() for f in last_90]) 
    landings_in_last_30 = sum([f.total_landings() for f in last_30]) 

    context = {'flights':recent_entries, 'flights_label':'Recent entries',
               'year_hour_data':year_hour_data, 'today':today,
               'duration_sum':duration_sum, 'hours_in_last_90':hours_in_last_90,
               'hours_in_last_30':hours_in_last_30,
               'landings':landings, 'landings_in_last_90':landings_in_last_90,
                'landings_in_last_30':landings_in_last_30, 'user':request.user}

    return render(request, 'logbook/index.html', context)

@login_required
def summaries(request):
    context = {}
    return render(request, 'logbook/summaries.html', context)

@login_required
def dispatch(request):
    action = request.POST['action']
    if action == 'Summarize by make and model':
        context = {'make_and_models':Make_and_model.objects.all()}
        return render(request, 'logbook/make_model_choose.html', context)       
    elif action == 'Summarize by equipment complexity':
        context = {'equipments':Equipment.objects.all()}
        return render(request, 'logbook/equipment_choose.html', context)
    elif action == 'Summarize by date range':
        return HttpResponseRedirect(reverse('date_range_choose'))
    else:
        Flight.clear_filter(request.user)
        context = {'Flight':Flight, 'title':'Comprehensive summary of all flying:'}
        return render(request, 'logbook/summary.html', context)
    
class DateRangeForm(forms.Form):
    begin = forms.DateField(label='Beginning date')
    end =  forms.DateField(label='End date')

@login_required
def date_range_choose(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            Flight.clear_filter(request.user)
            begin = form.cleaned_data['begin'] # in datetime format
            end = form.cleaned_data['end']
            Flight._filtered=Flight._filtered.filter(date__range=(begin,end))
            begin = begin.strftime('%m.%d.%Y') # as string
            end = end.strftime('%m.%d.%Y')
            return HttpResponseRedirect(reverse('date_range', args=(begin, end)))
        else:
            message = 'Something is wrong. Please check the date format is mm.dd.yy'
            context = {'form':form, 'message':message}
            return render(request, 'logbook/date_range_choose.html', context)            
    else:
        today = datetime.date.today()
        ninety_days_ago = today - datetime.timedelta(90)
        form = DateRangeForm({'begin':ninety_days_ago, 'end':today})
        message = 'Enter dates in the format mm.dd.yy (default is for last 90 days).'
        context = {'form':form, 'message':message}
        return render(request, 'logbook/date_range_choose.html', context)

@login_required
def date_range(request, begin, end):
    title = "Summary of flying from " + begin + " to " + end + " (inclusive):"
    context = {'Flight':Flight, 'title':title}
    return render(request, 'logbook/summary.html', context)
            
@login_required
def equipment_process(request):
    id=int(request.POST['id'])
    Flight.clear_filter(request.user)
    Flight._filtered=Flight._filtered.filter(make_and_model__equipment__id=id)
    return HttpResponseRedirect(reverse('equipment', args=(id,)) )
    
@login_required
def equipment(request, id):
    equipment = get_object_or_404(Equipment, id=id)
    title = "Summary of " + equipment.complexity + " flying:"
    context = {'Flight':Flight, 'title':title}
    return render(request, 'logbook/summary.html', context)

@login_required
def make_model_process(request):
    id=int(request.POST['id'])
    Flight.clear_filter(request.user)
    Flight._filtered=Flight._filtered.filter(make_and_model__id=id)
    return HttpResponseRedirect( reverse('make_model', args=(id,)) )

@login_required
def make_model(request, id):
    make_and_model = get_object_or_404(Make_and_model, id=id)
    title = "Summary of flying in the " + make_and_model.name + ":"
    context = {'Flight':Flight, 'title':title}
    return render(request, 'logbook/summary.html', context)

@login_required
def edit_make_model_choose(request):
    make_and_models = Make_and_model.objects.all()
    return render(request, 'logbook/edit_make_model_choose.html', {'make_and_models':make_and_models})

@login_required
def edit_make_model_process(request):
    id=int(request.POST['id'])
    action=(request.POST['action'])
    make_model = get_object_or_404(Make_and_model, id=id).name
    if action == "Delete":
        context={'id':id,'make_model':make_model}
        return render(request, 'logbook/edit_make_model_confirm_delete.html', context)
    elif action == "Edit":
        return HttpResponseRedirect( reverse('edit_make_model', args=(id,)) )
    elif action == "Add a new aircraft make and model":
        return HttpResponseRedirect(reverse('edit_make_model_add'))
    else:
        return HttpResponseRedirect(reverse('index'))    

@login_required
def edit_make_model_delete(reqest, id):
    make_model = get_object_or_404(Make_and_model, id=int(id))
    make_model.delete()
    return HttpResponseRedirect(reverse('edit_make_model_choose'))

@login_required
def edit_make_model(request, id):
    return HttpResponseRedirect(reverse('edit_make_model_choose')) #temporary scaffolding!!

@login_required
def edit_make_model_add(request):
    if request.method == 'POST': # if POST method
        action = request.POST['action']
        if action == "Cancel":
             return HttpResponseRedirect(reverse('edit_make_model_choose'))
        form = MakeModelForm(request.POST)
        if form.is_valid():
            form.save()
        else: # invalid form
            context = {'form':form}
            return render(request, 'logbook/edit_make_model_add', context)
        if action == "Save":
            return HttpResponseRedirect(reverse('edit_make_model_choose'))
        else: # if "Save and add another"
            return HttpResponseRedirect(reverse('edit_make_model_add'))
    else: 
        form = MakeModelForm()
        context = {'form':form}
        return render(request, 'logbook/edit_make_model_add.html', context)
            
@login_required
def edit_make_model(request, id):
    id=int(id)
    if request.method == 'POST': # if a form has already been filled
        action = request.POST['action']
        if action == "Cancel":
             return HttpResponseRedirect(reverse('edit_make_model_choose'))
        make_model=get_object_or_404(Make_and_model, id=id)
        form = MakeModelForm(request.POST,instance=make_model)
        if form.is_valid():
            form.save()
        else: # invalid form
            context = {'form':form, 'id':id}
            return render(request, 'logbook/edit_make_model', context)
        if action == "Save":
            return HttpResponseRedirect(reverse('edit_make_model_choose'))
        else: # if "Save and add another"
            return HttpResponseRedirect(reverse('edit_make_model'))
    else:
        make_model = get_object_or_404(Make_and_model, id=id)
        form = MakeModelForm(instance=make_model)
        context = {'form':form, 'id':id}
        return render(request, 'logbook/edit_make_model.html', context)
                
@login_required
def year(request, year):
    year = int(year)
    # Get months:
    months = set()
    Flight.clear_filter(request.user)
    flights = Flight._filtered.filter(date__year=year) 
    for f in flights:
        months.add(f.date.month)
    months = list(months)
    months.sort(lambda x,y : y - x) # reverse numerical
    month_hour_data = []
    for m in months:
        hours=total_hours(flights.filter(date__month=m))
        month_hour_data.append(Month_Hours(m, hours))

    # Get flights for last month with non-empty entries:
    month = months[0]
    # flights = Flight._filtered.filter(date__year=year, date__month=month).order_by('-date','-id')
    flights = flights.filter(date__month=month).order_by('-date','-id')
    flights_label = str(month) + '.' + str(year)
    context = {'flights':flights, 'flights_label':flights_label,
               'year':year, 'month_hour_data':month_hour_data}
    return render(request, 'logbook/year.html', context)

@login_required
def month(request, year, month):
    year = int(year)
    month = int(month)
    # Get months:
    months = set()
    Flight.clear_filter(request.user)
    flights = Flight._filtered.filter(date__year=year) 
    for f in flights:
        months.add(f.date.month)
    months = list(months)
    months.sort(lambda x,y : y - x) # reverse numerical
    month_hour_data = []
    for m in months:
        hours=total_hours(flights.filter(date__month=m))
        month_hour_data.append(Month_Hours(m, hours))

    # flights = Flight.objects.filter(date__year=year, date__month=month).order_by('-date','-id')
    flights = flights.filter(date__month=month).order_by('-date','-id')
    label = '%d.%d' % (month, year)
    context = {'flights':flights, 'flights_label':label, 'year':year, 'month':month,
               'month_hour_data':month_hour_data}
    return render(request, 'logbook/month.html', context)

@login_required
def flight(request, entry_number):
    # precaution:
    entry_number = int(entry_number)

    # Reset Flight filter to all flights of current user:
    Flight.clear_filter(request.user)

    # Get recent entries:
    recent = Flight._filtered.order_by('-id')[:NUM_RECENT_ENTRIES_DISPLAYED]

    # two cases, POST and GET:
    if request.method == 'POST': # If a form has beem submitted
        action = request.POST['action']
        if action == 'Home':
            return HttpResponseRedirect(reverse('index'))
        if action == 'New':
            return HttpResponseRedirect(reverse('create'))
        if action == 'Delete':
            if entry_number == 0:
                action = 'Cancel'
            else:
                flight = get_object_or_404(Flight, id=entry_number)
                flight.delete()
                previous = Flight._filtered.filter(id__lt=entry_number)
                if len(previous) == 0: # ie no flight records left
                    return HttpResponseRedirect(reverse('index'))
                else:
                    last = previous.last()
                    form = FlightForm(instance=last)
                    context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':last, 'message':' (previous log entry)', 'entry_number':last.id}
                    return render(request, 'logbook/flight.html', context)
        if action == 'Cancel':
            if entry_number == 0:
                flight = Flight._filtered.last()
                message = '(last flight in log). New entry cancelled. '
            else:
                flight = get_object_or_404(Flight, id=entry_number)
                message = '. Changes cancelled.'
            form = FlightForm(instance=flight)
            context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight': flight, 'message':message, 'entry_number':flight.id}
            return render(request, 'logbook/flight.html', context)
        if action == 'First':
            first = Flight._filtered.first()
            form = FlightForm(instance=first)
            context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':first, 'message':' (first log entry)', 'entry_number':first.id}
            return render(request, 'logbook/flight.html', context)
        if action == 'Last':
            last = Flight._filtered.last()
            form = FlightForm(instance=last)
            context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':last, 'message':' (last log entry)', 'entry_number':last.id}
            return render(request, 'logbook/flight.html', context)
        if action == 'Next':
            if entry_number == 0:
                message = 'An unsaved new entry has no \"next\" entry.'
                form = FlightForm(request.POST)
                context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'message':message, 'entry_number':0}
                return render(request, 'logbook/flight.html', context)
            later_entries = Flight._filtered.filter(id__gt=entry_number)
            if later_entries.count() == 0:
                next_entry = Flight._filtered.last()
                message = '. This is the last entry in the log.'
            else:
                next_entry = later_entries.first()
                message = ' (next entry)'
            form = FlightForm(instance=next_entry)
            context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':next_entry, 'message':message, 'entry_number':next_entry.id}
            return render(request, 'logbook/flight.html', context)
        if action == 'Previous':
            if entry_number == 0:
                message = 'An unsaved new entry has no \"previous\" entry.'
                form = FlightForm(request.POST)
                context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'message':message, 'entry_number':0}
                return render(request, 'logbook/flight.html', context)
            earlier_entries = Flight._filtered.filter(id__lt=entry_number)
            if earlier_entries.count() == 0:
                previous_entry = Flight._filtered.first()
                message = '. This is the first entry in the log.'
            else:
                previous_entry = earlier_entries.last()
                message = ' (previous entry)'
            form = FlightForm(instance=previous_entry)
            context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':previous_entry, 'message':message, 'entry_number':previous_entry.id}
            return render(request, 'logbook/flight.html', context)
        # Remaining POST method cases are 'Save' and 'Save and create new': 
        if entry_number == 0:
            form = FlightForm(request.POST) # so that form.save() adds new log entry
        else:
            flight = get_object_or_404(Flight, id=entry_number)
            form = FlightForm(request.POST, instance=flight) # so that form.save() saves *existing* entry
        if form.is_valid():
            form.save()
            entry_number = Flight.objects.last().id # update entry_number if necessary
            flight = get_object_or_404(Flight, id=entry_number)
            # ensure current user is logged as pilot:
            flight.pilot = request.user 
            flight.save()
            if action == 'Save':
                message = '. Entry saved.'
                form = FlightForm(instance=flight)
                context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':flight, 'message':message, 'entry_number':entry_number}
                return render(request, 'logbook/flight.html', context)
            else: # if 'Save and create new'
                return HttpResponseRedirect(reverse('create'))
        else: # invalid form
            if 'date' in form.errors.as_data().keys():
                if entry_number == 0:
                    message = 'Please re-enter the date in the correct format.'
                else:
                    message = '. Please re-enter the date in the correct format.'
            else:
                message = form.errors
            if entry_number == 0:
                context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'message':message, 'entry_number':0}
            else:
                flight = get_object_or_404(Flight, id=entry_number)
                context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':flight, 'message':message, 'entry_number':entry_number}            
            return render(request, 'logbook/flight.html', context)
    else: # if method is GET
        flight = get_object_or_404(Flight, id=entry_number)
        
        form = FlightForm(instance=flight)
        context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'flight':flight, 'message':'', 'entry_number':entry_number}
        return render(request, 'logbook/flight.html', context)

@login_required
def create(request):
    # Get recent entries:
    Flight.clear_filter(request.user)
    recent = Flight._filtered.order_by('-id')[:NUM_RECENT_ENTRIES_DISPLAYED]

    # Create a form and populate it :
    if Flight._filtered.count() == 0:
        form = FlightForm()
    else:
        form = FlightForm(instance=Flight._filtered.last())

    # Display the form to the user for editing and possible saving:
    context = {'flights':recent, 'flights_label':'Recent entries', 'form':form, 'message':'Unsaved new entry: ', 'entry_number':0}
    return render(request, 'logbook/flight.html', context)




        
                                
