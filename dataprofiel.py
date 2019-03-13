import pandas as pd
import pandas_profiling

def main():
    file_location = 'Leidse_regio_data.csv'
    df = pd.read_csv(file_location)

    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile='output.html')

if __name__ == '__main__':
    main()
