import pandas as pd
import matplotlib.pyplot as plt

class analysis:

    def rewards(self, rewards):
        df = pd.DataFrame.from_records(rewards)        
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
    
        print(df)
        plt.xlabel('month')
        plt.ylabel('revenue')
        plt.plot(df.index, df.total_point)
        plt.savefig('img.png')


