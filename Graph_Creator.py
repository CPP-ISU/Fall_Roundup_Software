import matplotlib.pyplot as plt
import _mysql_connector
for i in range (10):
    plt.plot(
        [5, 4, 3], 
        [100, 200, 300] 
    )
    plt.title('Some Title')
    plt.xlabel('Year')
    plt.ylabel('Some measurements')
    ##plt.show()

    plt.savefig(('images/my_plot'+str(i)+'.png'))