import repository

def main():   
           
    repo=repository.repository()        
    measurementCount = repo.countvals('101006','T1w')      
    print(f'measurement: {measurementCount}')

if __name__ == '__main__':
    main()
