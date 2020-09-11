import os
import pandas as pd

if __name__ == '__main__':
    csv_files = []
    for file in os.listdir():
        if file.endswith('.csv'):
            csv_files.append(file)
            print(file)

    columns = ['username', 'time', 'text', 'tags']

    main_df = pd.DataFrame(columns=columns)
    for file in csv_files:
        df = pd.read_csv(file, header=0)[columns]
        main_df = main_df.append(df.copy())

    main_df.to_csv('tweets.csv', index=False)
