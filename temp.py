import progressbar
from time import sleep
a = 100
bar = progressbar.ProgressBar(maxval=a, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
for i in range(1000):
    bar.update(i+1)
    sleep(0.1)
bar.finish()