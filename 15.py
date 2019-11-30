import datetime
import calendar

year=1004
day=datetime.date(year, 1, 27)
possible=[]

while year <= 1999:    
    if calendar.isleap(day.year):
        if year % 10 == 6:
            if day.weekday() == 1:            
                possible.append(year)

    year=year+4
    day=day.replace(year)

# he ain't the youngest, he is the second
print possible[-2]
