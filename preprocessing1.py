import pandas as pd
import numpy as np

movies = pd.read_csv('movies_source.csv')

movies.loc[movies.screening_rat == 'G', ('screening_rat')] = "전체 관람가"
movies.loc[movies.screening_rat == 'PG', ('screening_rat')] = "전체 관람가"
movies.loc[movies.screening_rat == 'PG-13', ('screening_rat')] = "12세 관람가"
movies.loc[movies.screening_rat == 'R', ('screening_rat')] = "15세 관람가"
movies.loc[movies.screening_rat == 'NC-17', ('screening_rat')] = "청소년 관람불가"
# 상영등급 통일

# movies['rating'] = movies['rating'].apply(lambda x : "명작" if x >= 8 else "졸작" if x <5 else "범작")
# movies.to_csv("preprocessed_movies_with_3classes.csv")
# # rating을 명작, 범작, 졸작 3개의 class로 mapping

# rating_mean = int(np.asarray(movies['rating'], dtype=np.float).mean())
# movies['rating'] = movies['rating'].apply(lambda x : "평균 평점 이상의 작품" if x >= rating_mean else "평균 평점 미만의 작품")  
# movies.to_csv("preprocessed_movies_with_2classes_mean.csv")
# rating을 평균 평점 이상의 작품, 평균 평점 미만의 작품 2개의 class로 mapping


rating_median = int(movies['rating'].median())
movies['rating'] = movies['rating'].apply(lambda x : "평점 중앙값 이상의 작품" if x >= rating_median else "평점 중앙값 미만의 작품")
movies.to_csv("preprocessed_movies_with_2classes_median.csv")
# rating을 평점 중앙값 이상의 작품, 평점 중앙값 미만의 작품 2개의 class로 mapping





