
close('all')

x = fetch.Msidset(['PFDM201T', 'PFDM202T'], '2010:110', '2010:115')

subplot(1,2,1)
x['PFDM201T'].plot()
ylabel('Deg F')
ylim([50,75])
plot(xlim(), array([56.5,56.5]),'g:')
plot(xlim(), array([72.2, 72.2]),'g:')
title('PFDM201T')

subplot(1,2,2)
x['PFDM202T'].plot()
ylabel('Deg F')
ylim([50,75])
plot(xlim(), array([55.8,55.8]),'g:')
plot(xlim(), array([65.4,65.4]),'g:')
title('PFDM202T')