close('all')

t_start = '2001:001'
t_stop = None

t_event = DateTime('2010:099:16:54:00').secs

x = fetch.Msidset(['PFDM201T','PFDM202T'],t_start, t_stop)
dt=x['PFDM202T'].vals - x['PFDM201T'].vals

y = fetch.Msidset(['PFDM201T','PFDM202T'],t_start, t_stop, stat='daily')
dt_means=y['PFDM202T'].vals - y['PFDM201T'].vals


figure()
subplot(2,1,1)
x['PFDM201T'].plot('b', label='PFDM201T')
x['PFDM202T'].plot('r', label='PFDM202T')
title('FDM-2 Temperatures')
ylabel('Deg F')
legend()
plot_cxctime(array([t_event, t_event]), ylim(), 'r:')

subplot(2,1,2)
plot_cxctime(x['PFDM201T'].times, dt, 'k-', alpha=.1, label='Full Res')
#plot_cxctime(x['PFDM201T'].times, dt, 'k,', label='Full Res')
plot_cxctime(y['PFDM201T'].times, dt_means, 'b', label='Daily Means')
plot_cxctime(array([t_event, t_event]), ylim(), 'r:')
title('PFDM202T minus PFDM201T')
ylabel('Deg F')
legend()

savefig('delta_temps.png')
for i in range(1,3):
    subplot(2,1,i)
    xlim([DateTime('2010:095').plotdate, DateTime('2010:115').plotdate])
savefig('delta_temps_spike.png')


