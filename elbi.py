import matplotlib.image as image

from utilities import find_closest

close('all')

x = fetch.Msidset(['ELBI', 'PFDM202T'], '2010:099:06:00:00','2010:099:20:00:00.00')

dt = diff(x['PFDM202T'].vals)

local_min = (append_to_array(dt <= 0., pos=0, val=bool(0)) & 
             append_to_array(dt > 0., pos=-1, val=bool(0)))
local_max = (append_to_array(dt >= 0., pos=0, val=bool(0)) & 
             append_to_array(dt < 0., pos=-1, val=bool(0)))

htr_on_range = x['PFDM202T'].vals < on_range
htr_off_range = x['PFDM202T'].vals > off_range

htr_on = local_min & htr_on_range
htr_off = local_max & htr_off_range

t_on = x['PFDM202T'].times[htr_on]
t_off = x['PFDM202T'].times[htr_off]

match_i = find_first_after(t_on, t_off)
t_off = x['PFDM202T'].times[htr_off][match_i]

dt_on = diff(t_on)
mean_dt_on = mean(dt_on[-5:])
t_pred_on = x['PFDM202T'].times[htr_on][-1] + mean_dt_on * arange(1,4)

dt_off = diff(t_off)
mean_dt_off = mean(dt_off[-5:])
t_pred_off = x['PFDM202T'].times[htr_off][-1] + mean_dt_off * arange(1,4)

figure()
subplot(2,1,1)
x['ELBI'].plot()
title('Load Bus Current')
ylabel('A')
for t in t_on:
    plot_cxctime(array([t, t]), ylim(), 'g:')
for t in t_off:
    plot_cxctime(array([t, t]), ylim(), 'r:') 
for t in t_pred_on:
    plot_cxctime(array([t, t]), ylim(), 'g:')
for t in t_pred_off:
    plot_cxctime(array([t, t]), ylim(), 'r:')    
for i in range(len(t_on)):
    elbi = fetch.Msid('ELBI', t_on[i], t_off[i])
    elbi.plot('r')
for i in range(len(t_pred_on)):
    elbi = fetch.Msid('ELBI', t_pred_on[i], t_pred_off[i])
    elbi.plot('r')

subplot(2,1,2)
x['PFDM202T'].plot()
plot_cxctime(t_on, x['PFDM202T'].vals[htr_on], 'g*', mew=0)
plot_cxctime(t_off, x['PFDM202T'].vals[htr_off][match_i], 'r*', mew=0)
for t in t_on:
    plot_cxctime(array([t, t]), ylim(), 'g:')
for t in t_off:
    plot_cxctime(array([t, t]), ylim(), 'r:') 
for t in t_pred_on:
    plot_cxctime(array([t, t]), ylim(), 'g:')
for t in t_pred_off:
    plot_cxctime(array([t, t]), ylim(), 'r:')    
title('FDM-2 Temp 2')
ylabel('Deg F')
savefig('htr_cycle_all.png')

for i in range(len(t_on)):
    subplot(2,1,1)
    xlim([DateTime(t_on[i]-600).plotdate, DateTime(t_on[i]+900).plotdate])
    subplot(2,1,2)
    xlim([DateTime(t_on[i]-600).plotdate, DateTime(t_on[i]+900).plotdate])
    savefig('htr_cycle_'+str(i+1)+'.png')
    
for i in range(len(t_pred_on)):
    subplot(2,1,1)
    xlim([DateTime(t_pred_on[i]-600).plotdate, DateTime(t_pred_on[i]+900).plotdate])
    subplot(2,1,2)
    xlim([DateTime(t_pred_on[i]-600).plotdate, DateTime(t_pred_on[i]+900).plotdate])
    savefig('htr_cycle_pred_'+str(i+1)+'.png')
