from kadi import events
from utilities import append_to_array, find_first_after, same_limits, heat_map

close('all')

temp = 'PLINE10T'
on_range = 56.5
off_range = 64
t_start = '2004:001'
t_stop = '2010:090'

x = fetch.Msid(temp, t_start, t_stop)
v = fetch.Msid('ELBV', t_start, t_stop, stat='5min')
dt = diff(x.vals)

local_min = (append_to_array(dt <= 0., pos=0, val=bool(0)) & 
             append_to_array(dt > 0., pos=-1, val=bool(0)))
local_max = (append_to_array(dt >= 0., pos=0, val=bool(0)) & 
             append_to_array(dt < 0., pos=-1, val=bool(0)))

htr_on_range = x.vals < on_range
htr_off_range = x.vals > off_range

htr_on = local_min & htr_on_range
htr_off = local_max & htr_off_range

#remove any incomplete heater cycles at end of timeframe
last_off = nonzero(htr_off)[0][-1]
htr_on[last_off:] = 0

t_on = x.times[htr_on]
t_off = x.times[htr_off]

match_i = find_first_after(t_on, t_off)

dur = t_off[match_i] - t_on

voltage_i = find_closest(t_on, v.times)
voltage = v.vals[voltage_i]
pwr = voltage**2/40 * dur/3600 #W-hrs

#compute duty cycles by month
on_dates = DateTime(t_on).iso
on_yrs = [date[0:4] for date in on_dates]
on_mos = [date[5:7] for date in on_dates]
on_freq = zeros(168)
on_time = zeros(168)
acc_pwr = zeros(168)
avg_on_time = zeros(168)
dates = zeros(168)
i = 0
for yr in range(2000, 2014):
    for mo in range(1,13):
        yr_match = array([on_yr == str(yr) for on_yr in on_yrs])
        mo_match = array([on_mo == str(mo).zfill(2) 
                          for on_mo in on_mos])
        on_freq[i] = sum(yr_match & mo_match)
        on_time[i] = sum(dur[yr_match & mo_match])
        acc_pwr[i] = sum(pwr[yr_match & mo_match])
        avg_on_time[i] = mean(dur[yr_match & mo_match])
        dates[i] = DateTime(str(yr) + '-' + str(mo).zfill(2) 
                            + '-01 00:00:00.000').secs
        i = i + 1
dates_range = append(dates, DateTime('2014:001').secs)
months_dur = dates_range[1:] - dates_range[:-1]
dc = on_time / months_dur

figure(1)
plot_cxctime(t_on, dur, 'b.', alpha=.05, mew=0)
#plot_cxctime(t_event, ylim(),'r:')
ylabel('On-Time Durations [sec]')
title('FDM-2 Heater On-Time Durations')
savefig('FDM2_1.png')

#figure(2)
#plot_cxctime(x.times, x.vals, mew=0)
#plot_cxctime(x.times, x.vals, 'b*',mew=0)
#plot_cxctime(x.times[htr_on], x.vals[htr_on], 'c*',mew=0, label='Heater On')
#plot_cxctime(x.times[htr_off], x.vals[htr_off], 'r*',mew=0, label='Heater Off')
#plot_cxctime(t_event, ylim(),'r:')
#legend()

figure(3)
hist(dur, bins=100, normed=True)
#xlabel('On-Time Durations [sec]')
title('FDM-2 Heater On-Time Durations')
savefig('FDM2_3.png')

figure(4)
plot_cxctime(t_on[:-1], dur[:-1]/diff(t_on)*100, 'k', alpha=.1)
plot_cxctime(dates, dc*100, '*', mew=0)
plot_cxctime(dates, dc*100, '-', mew=0)
#plot_cxctime(t_event, ylim(),'r:')
title('FDM-2 Heater Duty Cycle')
ylabel('FDM-2 Heater Duty Cycle by Month [%] \n (Total On-time / Total Time)')
legend(['Range', 'Monthly Mean'])
ylim([0,40])
savefig('FDM2_4.png')

figure(5)
plot_cxctime(dates, on_freq * (30.4375*3600*24 / months_dur), '*', mew=0)
plot_cxctime(dates, on_freq * (30.4375*3600*24 / months_dur), '-', mew=0)
#plot_cxctime(t_event, ylim(),'r:')
title('FDM-2 Heater Cycling Frequency')
ylabel('Heater Cycles per Month (Normalized)')
savefig('FDM2_5.png')

figure(6)
plot_cxctime(dates, on_time/3600 * (30.4375*3600*24 / months_dur), '*', mew=0)
plot_cxctime(dates, on_time/3600 * (30.4375*3600*24 / months_dur), '-', mew=0)
#plot_cxctime(t_event, ylim(),'r:')
title('FDM-2 Heater On-Time')
ylabel('Heater On-Time by Month (Normalized) [hrs]')
savefig('FDM2_6.png')

figure(7)
plot_cxctime(dates, avg_on_time/3600, '*', mew=0)
plot_cxctime(dates, avg_on_time/3600, '-', mew=0)
#plot_cxctime(t_event, ylim(),'r:')
title('FDM-2 Heater Average On-Time')
ylabel('Mean Heater On-Time by Month [hrs]')
savefig('FDM2_7.png')

figure(8)
plot_cxctime(dates, acc_pwr * (30.4375*3600*24 / months_dur), '*', mew=0)
plot_cxctime(dates, acc_pwr * (30.4375*3600*24 / months_dur), '-', mew=0)
#plot_cxctime(t_event, ylim(),'r:')
title('FDM-2 Accumulated Heater Power')
ylabel('Accumulated Heater Power by Month \n (Normalized) [W-hrs]')
savefig('FDM2_8.png')
