execfile('htr_dc.py')

#1.  FDM-2 Heater
#htr_dc('PFDM202T', 56.5, 64, t_start='2001:001', t_stop='2010:100', name='FDM-2', event='2010:099:16:54:00.000', plot_cycles=False)
#for i in range(3,9):
#    figure(i)
#    xlim([DateTime('2010:080').plotdate, DateTime('2010:105').plotdate])

#2.  5133 Line Heater
htr_dc('PLINE08T', 56, 72, t_start='2001:001', t_stop='2014:100', name='5133 Line', event='2010:099:16:54:00.000', plot_cycles=False)
#htr_dc('PLINE08T', 56, 72, t_start='2010:197', t_stop='2010:199', name='5133 Line', event='2010:099:16:54:00.000', plot_cycles=True)
#htr_dc('PLINE08T', 56, 72, t_start='2010:001', t_stop='2011:001', name='5133 Line', event='2010:099:16:54:00.000', plot_cycles=False)

