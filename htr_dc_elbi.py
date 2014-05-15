import time

from kadi import events
from utilities import append_to_array, find_first_after, find_last_before, find_closest

close('all')

#inputs
t_start = '2010:001:00:00:00'
t_stop = '2010:099:00:00:00'
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
    
    t_on = array([(on_upswing_fit[i][1] - on_downswing_fit[i][1])/(on_downswing_fit[i][0] - on_upswing_fit[i][0]) for i in arange(len(i_on))])
    t_off = array([(off_upswing_fit[i][1] - off_downswing_fit[i][1])/(off_downswing_fit[i][0] - off_upswing_fit[i][0]) for i in arange(len(i_on))])
    
    temp_on = [on_downswing_fit[i][0]*t_on[i] + on_downswing_fit[i][1] for i in arange(len(i_on))]
    temp_off = [off_downswing_fit[i][0]*t_off[i] + off_downswing_fit[i][1] for i in arange(len(i_on))]

    if plot == True:
        figure()
        for i in arange(len(i_on)):
            plot_cxctime(on_downswing[i][0], on_downswing_fit[i][0]*on_downswing[i][0] + on_downswing_fit[i][1], 'r')
            plot_cxctime(on_upswing[i][0], on_upswing_fit[i][0]*on_upswing[i][0] + on_upswing_fit[i][1], 'g')
            plot_cxctime(off_upswing[i][0], off_upswing_fit[i][0]*off_upswing[i][0] + off_upswing_fit[i][1], 'g')
            plot_cxctime(off_downswing[i][0], off_downswing_fit[i][0]*off_downswing[i][0] + off_downswing_fit[i][1], 'r')
            plot_cxctime(t_on, temp_on, 'k*')
            plot_cxctime(t_off, temp_off, 'k*')
    return [t_on, t_off]

#fetch data
time0 = time.time()
t1 = fetch.Msid('PFDM201T', t_start, t_stop)
t2 = fetch.Msid('PFDM202T', t_start, t_stop)
c = fetch.Msid('ELBI', t_start, t_stop)
if min(t1.times) < 32:
    print('Warning:  Varying sampling intervals')
    
#find rough cycles    
time1 = time.time()
[t_on_t1r, t_off_t1r, i_on_t1r, i_off_t1r] = find_rough_cycles(t1, 58, 69)
[t_on_t2r, t_off_t2r, i_on_t2r, i_off_t2r] = find_rough_cycles(t2, 56.5, 64)

#find exact cycles
time2 = time.time()
[t_on_t1, t_off_t1]  = find_exact_cycles(t1, i_on_t1r, i_off_t1r, plot=False)
[t_on_t2, t_off_t2]  = find_exact_cycles(t2, i_on_t2r, i_off_t2r, plot=False)

#find turn-on "candidates"
time3 = time.time()
dc = diff(c.vals)
up = (dc > .6) & (dc < 1)
down = (dc > -1) & (dc < -.6)
look_ahead = array([any(down[i+296*4:i+335*4]) for i in arange(len(dc)-335*4)])
look_back = array([any(up[i-335*4:i-296*4]) for i in arange(335*4, len(dc))])
cand_on = up[:-335*4] & look_ahead
cand_off = down[335*4:] & look_back

#bookkeeping indices
up_i = nonzero(up)[0]
down_i = nonzero(down)[0]
look_i = nonzero(look_ahead)[0] + 1
cand_on_i = nonzero(cand_on)[0] + 1
cand_off_i = nonzero(cand_off)[0] + 1

#identify candidate times wrt turn-on and turn-off times
time4 = time.time()
#on_match_i1 = find_closest(c.times[cand_on_i], t_on_t1)
#on_match_i2 = find_closest(c.times[cand_on_i], t_on_t2)
#off_match_i1 = find_closest(c.times[cand_off_i], t_off_t1)
#off_match_i2 = find_closest(c.times[cand_off_i], t_off_t2)
#on_rel_t1 = c.times[cand_on_i] - t_on_t1[on_match_i1]
#on_rel_t2 = c.times[cand_on_i] - t_on_t2[on_match_i2]
#off_rel_t1 = c.times[cand_off_i] - t_off_t1[off_match_i1] 
#off_rel_t2 = c.times[cand_off_i] - t_off_t2[off_match_i2]
t_on = mean(array([t_on_t1, t_on_t2]), axis=0)
on_match_i = find_closest(c.times[cand_on_i], t_on)
on_rel = c.times[cand_on_i] - t_on[on_match_i]
within20 = (on_rel > -15) & (on_rel < 5)
perc_t_on_w_hits = 100.0*len(unique(on_match_i[within20]))/len(t_on)
print('Percentage of known heater-on-times with matching ELBI candidates:  ' + str(perc_t_on_w_hits) + '%')

#plot
time5 = time.time()

figure(3) #time interpolation
t2.plot()
t2.plot('.')
#plot_cxctime(t_on_t2r, t2.vals[i_on_t2r], 'g*', mew=0)
#plot_cxctime(t_off_t2r, t2.vals[i_off_t2r], 'r*', mew=0)
title('PFDM202T')
ylabel('Deg F')
savefig('elbi_1.png')

figure(4) # ELBI data
subplot(5,1,1)
c.plot()
x = xlim()
title('Bus Current')
ylabel('A')
subplot(5,1,2)
plot_cxctime(c.times[1:], dc)
plot_cxctime(c.times[1:][up_i], dc[up_i], 'g*')
plot_cxctime(c.times[1:][down_i], dc[down_i], 'r*')
title('Delta Bus Current')
ylabel('A')
xlim(x)
subplot(5,1,3)
plot_cxctime(c.times[:len(look_ahead)], look_ahead, 'b')
xlim(x)
ylim([-1,2])
title('Look Ahead (Down 296-335 sec later)')
subplot(5,1,4)
plot_cxctime(c.times[1:-335*4], cand_on, 'b')
xlim(x)
ylim([-1,2])
title('Candidate On Times (Up AND Down 296 - 335 sec later)')
subplot(5,1,5)
plot_cxctime(c.times[1:-335*4], cand_off, 'b')
xlim(x)
ylim([-1,2])
title('Candidate Off Times (Down AND Up 296 - 335 sec beforehand)')
savefig('elbi_2.png')

figure(5) #candidate ELBI on temps
t2.plot()
#for i in cand_on_i:
#    t_c = c.times[i]
#    plot_cxctime(array([t_c, t_c]), ylim(), 'r:')
t2.plot('.')
title('PFDM202T')
ylabel('Deg F')
legend(['PFDM202T', 'Candidate "On" Time'])
savefig('elbi_3.png')

#figure(6) #candidate times relative to turn-on, turn-offs
#subplot(4,1,1)
#hist(on_rel_t1, range=[-120,120], bins=120)
#title('Candidate On Times (per ELBI) Relative to Heater Turn On (per 1T)')
#xlabel('Sec')
#ylabel('Occurrences')
#xlim([-120,120])
#ylim([0,500])
#subplot(4,1,2)
#hist(on_rel_t2, range=[-120,120], bins=120)
#title('Candidate On Times (per ELBI) Relative to Heater Turn On (per 2T)')
#xlabel('Sec')
#ylabel('Occurrences')
#xlim([-120,120])
#ylim([0,500])
#subplot(4,1,3)
#hist(off_rel_t1, range=[-120,120], bins=120)
#title('Candidate Off Times (per ELBI) Relative to Heater Turn Off (per 1T)')
#xlabel('Sec')
#ylabel('Occurrences')
#xlim([-120,120])
#ylim([0,500])
#subplot(4,1,4)
#hist(off_rel_t2, range=[-120,120], bins=120)
#title('Candidate Off Times (per ELBI) Relative to Heater Turn Off (per 2T)')
#xlabel('Sec')
#ylabel('Occurrences')
#xlim([-120,120])
#ylim([0,500])

figure(7)
hist(on_rel, range=[-120,120], bins=120)
title('Candidate On Times (per ELBI) Relative to Heater Turn On (per mean of 1T & 2T)')
xlabel('Sec')
ylabel('Occurrences')
xlim([-120,120])
ylim([0,500])

figure(8)
plot(t_on[:-1], diff(t_on)/60)
title('Heater Period')
ylabel('min')

print('Processing times:')
print(str(time1 - time0) + ' - fetching data')
print(str(time2 - time1) + ' - rough cycles')
print(str(time3 - time2) + ' - exact cycles')
print(str(time4 - time3) + ' - elbi "candidates"')
print(str(time5 - time4) + ' - elbi patterns')
print(str(time.time() - time5) + ' - plots')


