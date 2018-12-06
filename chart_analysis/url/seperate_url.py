import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def full_range(reading_file, sep):
    ''' 파일의 총 길이를 읽은후
        sep으로 나눈 길이를 반환
        sep에는 int 형 자료 들어감
        sep = 나누고 싶은수
    '''
    full_ranger = 0
    with open(reading_file, 'r') as f_total:
        full_ranger = int(len(f_total.readlines()) / sep)

    return full_ranger + 2


def read_file(reading_file, writing_file, sep):
    '''파일을 읽어서 sep수로 나눈것만큼 파일 생성
                 __________________________________________
        example) | reading_file총 길이 | sep | 생성된 파일 길이 |
                 |         2256      | 100 |      22      |
                 ------------------------------------------

    '''
    with open(reading_file, 'r') as f_total:

        full_ranger = full_range(reading_file, sep)
        for j in range(1, full_ranger):
            new_name = writing_file[:-4] + '_' + str(j) + '.txt'
            with open(new_name, 'a') as f_new:

                for i in range(1, sep +1):
                    row = f_total.readline()
                    f_new.write(row)
            print(str(new_name) + ' 파일이 작성 되었습니다.', end='\n')
    print('총 ' + str(full_ranger)+ ' 개의 파일이 생성되었습니다.')



read_file('total_url.txt', 'seperated.txt', 100)
