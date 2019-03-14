import pandas as pd
import pandas_profiling

def main():
    file_location = "D:\Downloads\Subsidie_opgeschoonde_data.csv"
    df = pd.read_csv(file_location, sep=';')

    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile='output_subsidies.html')

if __name__ == '__main__':
    main()
