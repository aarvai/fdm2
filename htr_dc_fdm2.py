from kadi import events
from utilities import append_to_array, find_first_after, same_limits, heat_map, find_closest

close('all')

temp = 'PFDM202T'
on_range = 56.5
off_range = 64
t_start = '2010:098'
#t_stop = None
t_stop = '2010:100'
t_event = DateTime('2010:099:16:54:00').secs

x = fetch.Msidset([temp, 'PITCH'], t_start, t_stop)
dt = diff(x[temp].vals)

local_min = (append_to_array(dt <= 0., pos=0, val=bool(0)) & 
             append_to_array(dt > 0., pos=-1, val=bool(0)))
local_max = (append_to_array(dt >= 0., pos=0, val=bool(0)) & 
             append_to_array(dt < 0., pos=-1, val=bool(0)))

htr_on_range = x[temp].vals < on_range
htr_off_range = x[temp].vals > off_range

htr_on = local_min & htr_on_range
htr_off = local_max & htr_off_range

#remove any incomplete heater cycles at end of timeframe
last_off = nonzero(htr_off)[0][-1]
htr_on[last_off:] = 0

t_on = x[temp].times[htr_on]
t_off = x[temp].times[htr_off]

match_i = find_first_after(t_on, t_off)

dur = t_off[match_i] - t_on

dur_cycle = diff(t_on)

dc = dur[:-1] / dur_cycle

t_mid = t_on[:-1] + dur_cycle/2

PITCH_i = find_closest(t_mid, x['PITCH'].times)
PITCH = x['PITCH'].vals[PITCH_i]

i_event = find_closest(t_event, x[temp].times)
htr_mean = mean(x[temp].vals[:i_event[0]])

figure()
subplot(2,1,1)
plot_cxctime(x[temp].times, x[temp].vals, mew=0)
#plot_cxctime(x[temp].times, x[temp].vals, 'b*',mew=0)
plot_cxctime(array([t_event, t_event]), ylim(), 'r')
plot_cxctime(x[temp].times[htr_on], x[temp].vals[htr_on], 'g*',mew=0, label='Heater On')
plot_cxctime(x[temp].times[htr_off][match_i], x[temp].vals[htr_off][match_i], 'r*',mew=0, label='Heater Off')
plot(xlim(), array([htr_mean, htr_mean]), 'k:', alpha=.5, label='Pre-event Mean')
title('PFDM202T')
ylabel('Deg F')
xlim1 = xlim()
legend()
subplot(2,1,2)
plot_cxctime(t_mid, dc, 'b-')
plot_cxctime(t_mid, dc, 'b*', mew=0)
title('Heater Duty Cycle')
ylabel('Duty Cycle')
ylim([0, .3])
xlim(xlim1)
grid()

figure()
plot(PITCH, dc, '.', alpha=.25)
title('Heater Duty Cycle vs PITCH')
ylabel('Duty Cycle')
xlabel('PITCH Angle [deg]')
ylim([0,.4])

figure()
x['PITCH'].plot()
plot_cxctime(t_mid, PITCH, 'r*')