
close('all')

#----------------------------------------------
t1 = '2010:099:16:18:00.000'
t2 = DateTime(t1).secs + 3600

x = fetch.Msidset(['PFDM201T','PFDM202T'], t1, t2)

dt1 = x['PFDM201T'].times - DateTime(t1).secs
dt2 = x['PFDM201T'].times - DateTime(t1).secs

for i in range(1,3):
    msid = 'PFDM20' + str(i) + 'T'
    figure(i, figsize=(7.7,3.3))

    subplot(1,2,1)
    plot(dt1/60, x[msid].vals,'b:', alpha=.9, label='last htr cycle')
    title(msid)
    xlabel('Relative Time [min]')
    ylabel('Deg F')
    ylim([56,72])

    subplot(1,2,2)
    plot(dt2/60, x[msid].vals,'b:', alpha=.9, label='last htr cycle')
    title(msid)
    xlabel('Relative Time [min]')
    ylabel('Deg F')
    ylim([56,72])
    tight_layout()


##----------------------------------------------
t1 = '2010:111:20:25:00.000'
t2 = DateTime(t1).secs + 1140

x = fetch.Msidset(['PFDM201T','PFDM202T'], t1, t2)

dt1 = x['PFDM201T'].times - DateTime(t1).secs
dt2 = x['PFDM201T'].times - DateTime(t1).secs

figure(1)
subplot(1,2,1)
plot(dt1/60, x['PFDM201T'].vals,'b', label='mid-spike')
legend()

figure(2)
subplot(1,2,1)
plot(dt2/60, x['PFDM202T'].vals,'b', label='mid-spike')
legend()

##----------------------------------------------

t1 = '2010:114:02:00:00.000'
t2 = DateTime(t1).secs + 3600

x = fetch.Msidset(['PFDM201T','PFDM202T'], t1, t2)

dt1 = x['PFDM201T'].times - DateTime(t1).secs
dt2 = x['PFDM201T'].times - DateTime(t1).secs

figure(1)
subplot(1,2,2)
plot(dt1/60, x['PFDM201T'].vals,'b', label='post-spike')
legend()
savefig('cooling_1T.png')

figure(2)
subplot(1,2,2)
plot(dt2/60, x['PFDM202T'].vals,'b', label='post-spike')
legend()
savefig('cooling_2T.png')






