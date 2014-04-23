import time

from kadi import events
from utilities import append_to_array, find_first_after, find_last_before, find_closest

close('all')
t0 = time.time()

#inputs
t_start = '2010:097:00:00:00'
t_stop = '2010:097:03:00:00'
t_event = array([DateTime('2010:099:16:54:00.000').secs, 
                 DateTime('2010:099:16:54:00.000').secs])

def find_rough_cycles(x, on_range, off_range):
    #temp should be msid object from fetch.Msid
    
    #find min and max times
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
    
    #find matching cycles
    i_off = unique(find_first_after(t_on, t_off))
    t_off = t_off[i_off] #removes duplicate "offs"
    
    i_on = find_last_before(t_off, t_on)
    t_on = t_on[i_on] #removes duplicate "ons"
    
    #find indices
    i_on = find_first_after(t_on, x.times) - 1
    i_off = find_first_after(t_off, x.times) - 1 
    
    return [t_on, t_off, i_on, i_off]

def find_exact_cycles(temp, i_on, i_off, plot=False):
    
    #create arrays 
    on_downswing = [[temp.times[i-9:i+1], temp.vals[i-9:i+1]] for i in i_on]
    on_upswing = [[temp.times[i:i+6], temp.vals[i:i+6]] for i in i_on]
    off_upswing = [[temp.times[i-5:i+1], temp.vals[i-5:i+1]] for i in i_off]
    off_downswing = [[temp.times[i:i+10], temp.vals[i:i+10]] for i in i_off]
    
    #linear fits
    on_downswing_fit = [polyfit(on_downswing[i][0], on_downswing[i][1], 1) for i in arange(len(i_on))]
    on_upswing_fit = [polyfit(on_upswing[i][0], on_upswing[i][1], 1) for i in arange(len(i_on))]
    off_upswing_fit = [polyfit(off_upswing[i][0], off_upswing[i][1], 1) for i in arange(len(i_on))]
    off_downswing_fit = [polyfit(off_downswing[i][0], off_downswing[i][1], 1) for i in arange(len(i_on))]
    
    t_on = [(on_upswing_fit[i][1] - on_downswing_fit[i][1])/(on_downswing_fit[i][0] - on_upswing_fit[i][0]) for i in arange(len(i_on))]
    t_off = [(off_upswing_fit[i][1] - off_downswing_fit[i][1])/(off_downswing_fit[i][0] - off_upswing_fit[i][0]) for i in arange(len(i_on))]
    
    temp_on = [on_downswing_fit[i][0]*t_on[i] + on_downswing_fit[i][1] for i in arange(len(i_on))]
    temp_off = [off_downswing_fit[i][0]*t_off[i] + off_downswing_fit[i][1] for i in arange(len(i_on))]

    if plot == True:
        for i in arange(len(i_on)):
            plot_cxctime(on_downswing[i][0], on_downswing_fit[i][0]*on_downswing[i][0] + on_downswing_fit[i][1], 'r')
            plot_cxctime(on_upswing[i][0], on_upswing_fit[i][0]*on_upswing[i][0] + on_upswing_fit[i][1], 'g')
            plot_cxctime(off_upswing[i][0], off_upswing_fit[i][0]*off_upswing[i][0] + off_upswing_fit[i][1], 'g')
            plot_cxctime(off_downswing[i][0], off_downswing_fit[i][0]*off_downswing[i][0] + off_downswing_fit[i][1], 'r')
            plot_cxctime(t_on, temp_on, 'k*')
            plot_cxctime(t_off, temp_off, 'k*')
    return [t_on, t_off]

#fetch data
t1 = fetch.Msid('PFDM201T', t_start, t_stop)
t2 = fetch.Msid('PFDM202T', t_start, t_stop)
c = fetch.Msid('ELBI', t_start, t_stop)

#find rough cycles    
[t_on_t2r, t_off_t2r, i_on_t2r, i_off_t2r] = find_rough_cycles(t2, 56.5, 64)

#find exact cycles
x = find_exact_cycles(t2, i_on_t2r, i_off_t2r, plot=True)

#plot
#figure()
t2.plot()
t2.plot('.')
#plot_cxctime(t_on_t2r, t2.vals[i_on_t2r], 'g*', mew=0)
#plot_cxctime(t_off_t2r, t2.vals[i_off_t2r], 'r*', mew=0)


