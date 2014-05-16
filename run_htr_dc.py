execfile('htr_dc.py')

#1.  FDM-2 Heater
#htr_dc('PFDM202T', 57, 64, t_start='2009:197', t_stop='2009:199', name='FDM-2', event='2010:099:16:54:00.000', plot_cycles=True) #troubleshooting
#htr_dc('PFDM202T', 57, 64, t_start='2001:001', t_stop='2010:099', name='FDM-2', event='2010:099:16:54:00.000', plot_cycles=False)
#for i in range(3,9):
#    figure(i)
#    xlim([DateTime('2010:080').plotdate, DateTime('2010:105').plotdate])

#2.  5133 Line Heater
#htr_dc('PLINE08T', 58, 71, t_start='2010:197', t_stop='2010:199', name='5133 Line', event='2010:099:16:54:00.000', plot_cycles=True)  #troubleshooting
htr_dc('PLINE08T', 58, 71, t_start='2001:001', t_stop='2014:100', name='5133 Line', event='2010:099:16:54:00.000', plot_cycles=False)
#htr_dc('PLINE08T', 58, 71, t_start='2010:001', t_stop='2011:001', name='5133 Line', event='2010:099:16:54:00.000', plot_cycles=False)

#2.  5105 Line Heater
#htr_dc('PLINE01T', 59, 67.2, t_start='2010:300', t_stop='2010:330', name='5105 Line', event='2010:099:16:54:00.000', plot_cycles=True, dur_lim=500*60)  #troubleshooting
#htr_dc('PLINE01T', 59, 67.2, t_start='2001:001', t_stop='2014:100', name='5105 Line', event='2010:099:16:54:00.000', plot_cycles=False, dur_lim=70*60)
#htr_dc('PLINE01T', 55.5, 67.2, t_start='2010:001', t_stop='2011:001', name='5105 Line', event='2010:099:16:54:00.000', plot_cycles=False, dur_lim=500*60)
