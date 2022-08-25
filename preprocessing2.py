import pandas as pd
import numpy as np

# movies = pd.read_csv('preprocessed_movies_with_3classes.csv')
# movies = pd.read_csv('preprocessed_movies_with_2classes_mean.csv')
movies = pd.read_csv('preprocessed_movies_with_2classes_median.csv')

# movies['running_time'] = movies['running_time'].apply(lambda x: "상영 시간 정보 없음" if "분" not in x else x)
# # # 가끔 상영 시간이 들어오지 않고 영화의 국적이 들어온 데이터가 있는데 해당 데이터의 상영 시간을 상영 시간 정보 없음으로 바꿔 준다.
# movies['running_time'] = movies['running_time'].apply(lambda x : x[:-1] if "분" in x else x)
# idx = movies[movies['running_time'] == '상영 시간 정보 없음'].index
# tmp = movies.drop(idx)
# running_time_mean = int(np.asarray(tmp['running_time'], dtype=np.float).mean())
# # # 상영 시간의 평균을 구하기 위해 "분"을 제거하고 상영 시간 정보가 있는 것들만으로 평균을 구해 준다.
# movies['running_time'] = movies['running_time'].apply(lambda x : "러닝 타임 평균 이상" if x.isdigit() and int(x) >= running_time_mean else "러닝 타임 평균 미만" if x.isdigit() and int(x) < running_time_mean else x)
# # # 상영 시간의 평균 이상이면 러닝 타임 평균 이상을 상영 시간 평균 미만이면 러닝 타임 평균 미만을 상영 시간 정보 없음은 상영 시간 정보 없음으로 둔다.


movies['running_time'] = movies['running_time'].apply(lambda x: "상영 시간 정보 없음" if "분" not in x else x)
# # 가끔 상영 시간이 들어오지 않고 영화의 국적이 들어온 데이터가 있는데 해당 데이터의 상영 시간을 상영 시간 정보 없음으로 바꿔 준다.
movies['running_time'] = movies['running_time'].apply(lambda x : x[:-1] if "분" in x else x)
idx = movies[movies['running_time'] == '상영 시간 정보 없음'].index
tmp = movies.drop(idx)
running_time_median = int(tmp['running_time'].median())
# # 상영 시간의 중앙값을 구하기 위해 "분"을 제거하고 상영 시간 정보가 있는 것들만으로 중앙값을 구해 준다.
movies['running_time'] = movies['running_time'].apply(lambda x : "러닝 타임 중앙값 이상" if x.isdigit() and int(x) >= running_time_median else "러닝 타임 중앙값 미만" if x.isdigit() and int(x) < running_time_median else x) 
# # 상영 시간의 중앙값 이상이면 러닝 타임 중앙값 이상을 상영 시간 중앙값 미만이면 러닝 타임 중앙값 미만을 상영 시간 정보 없음은 상영 시간 정보 없음으로 둔다.


# movies['dir_movies'] = movies['dir_movies'].apply(lambda x : x[:-1] if "개" in x else x)
# dir_movies_mean = int(np.asarray(movies['dir_movies'], dtype=np.float).mean())
# movies['dir_movies'] = movies['dir_movies'].apply(lambda x : "연출작 개수 평균 이상" if int(x) >= dir_movies_mean else "연출작 개수 평균 미만")
# # # 감독의 연출작 개수의 평균을 구하기 위해 "개"를 제거하고 감독의 연출작 개수의 평균을 구한다.
# # # 감독의 연출작 개수의 평균 이상이면 연출작 개수 평균 이상을 감독의 연출작 개수의 평균 미만이면 연출작 개수 평균 미만으로 한다.


movies['dir_movies'] = movies['dir_movies'].apply(lambda x : x[:-1] if "개" in x else x)
dir_movies_median = int(movies['dir_movies'].median())
movies['dir_movies'] = movies['dir_movies'].apply(lambda x : "연출작 개수 중앙값 이상" if int(x) >= dir_movies_median else "연출작 개수 중앙값 미만")
# # 감독의 연출작 개수의 중앙값을 구하기 위해 "개"를 제거하고 감독의 연출작 개수의 중앙값을 구한다.
# 감독의 연출작 개수의 중앙값 이상이면 연출작 개수 중앙값 이상을 감독의 연출작 개수의 중앙값 미만이면 연출작 개수 중앙값 미만으로 한다. 


# movies['main_role_movies'] = movies['main_role_movies'].apply(lambda x : x[:-1] if "개" in x else x)
# idx = movies[movies['main_role_movies'] == '연기자 없음'].index
# tmp = movies.drop(idx)
# main_role_movies_mean = int(np.asarray(tmp['main_role_movies'], dtype=np.float).mean())
# # # 주연의 출연작 개수의 평균을 구하기 위해 "개"를 제거하고 주연의 출연작 개수 정보가 있는 것들만으로 평균을 구해 준다.
# movies['main_role_movies'] = movies['main_role_movies'].apply(lambda x : "주연의 출연작 개수 평균 이상" if x.isdigit() and int(x) >= main_role_movies_mean else "주연의 출연작 개수 평균 미만" if x.isdigit() and int(x) < main_role_movies_mean else x)
# # # 주연의 출연작 개수의 평균 이상이면 주연의 출연작 개수 평균 이상을 주연의 출연작 개수 평균 미만이면 주연의 출연작 개수 평균 미만을 
# # # 연기자 없음은 연기자 없음으로 둔다.


movies['main_role_movies'] = movies['main_role_movies'].apply(lambda x : x[:-1] if "개" in x else x)
idx = movies[movies['main_role_movies'] == '연기자 없음'].index
tmp = movies.drop(idx)
main_role_movies_median = int(tmp['main_role_movies'].median())
# 주연의 출연작 개수의 중앙값을 구하기 위해 "개"를 제거하고 주연의 출연작 개수 정보가 있는 것들만으로 중앙값을 구해 준다.
movies['main_role_movies'] = movies['main_role_movies'].apply(lambda x : "주연의 출연작 개수 중앙값 이상" if x.isdigit() and int(x) >= main_role_movies_median else "주연의 출연작 개수 중앙값 미만" if x.isdigit() and int(x) < main_role_movies_median else x) 
# # 주연의 출연작 개수의 중앙값 이상이면 주연의 출연작 개수 중앙값 이상을 주연의 출연작 개수 중앙값 미만이면 주연의 출연작 개수 중앙값 미만을 
# # 연기자 없음은 연기자 없음으로 둔다.

# movies.to_csv("final_movies_3classes_with_mean.csv")
# movies.to_csv("final_movies_3classes_with_median.csv")
# movies.to_csv("final_movies_2classes_mean_with_mean.csv")
# movies.to_csv("final_movies_2classes_mean_with_median.csv")
# movies.to_csv("final_movies_2classes_median_with_mean.csv")
movies.to_csv("final_movies_2classes_median_with_median.csv")