# -*- coding: utf-8 -*-
# hadoop 위에서 cedec error를 발생시키지 않도록 이 파일의 encdoing type을 정의해 줍니다.

import sys
import codecs
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# hadoop 위에서 cedec error를 발생시키지 않도록 이 파일의 encdoing type을 정의해 줍니다.
spark = SparkSession.builder.appName("predictMovieRatings").getOrCreate()

data = spark.read.load("hdfs:///user/maria_dev/project_with_spark/final_movies_2classes_median_with_median.csv",
                        format="csv", sep=",", inferSchema = "true", header = "true")
           
# sparksession을 열고 분석하고자 하는 data set을 load해 줍니다.

labelIndexer = StringIndexer(inputCol = 'genre', outputCol = 'genre_one_hot_encoding')
data = labelIndexer.fit(data).transform(data)

labelIndexer = StringIndexer(inputCol = 'running_time', outputCol = 'running_time_one_hot_encoding')
data = labelIndexer.fit(data).transform(data)

labelIndexer = StringIndexer(inputCol = 'screening_rat', outputCol = 'screening_rat_one_hot_encoding')
data = labelIndexer.fit(data).transform(data)

labelIndexer = StringIndexer(inputCol = 'dir_movies', outputCol = 'dir_movies_one_hot_encoding')
data = labelIndexer.fit(data).transform(data)

labelIndexer = StringIndexer(inputCol = 'main_role_movies', outputCol = 'main_role_movies_one_hot_encoding')
data = labelIndexer.fit(data).transform(data)

# StringIndexer module을 통해 feature로 활용될 String type의 column을 모두 double type의 column으로 one-hot encoding 해줍니다.

preprocessed_data = data['title','director', 'genre_one_hot_encoding','running_time_one_hot_encoding','screening_rat_one_hot_encoding','dir_movies_one_hot_encoding','main_role_movies_one_hot_encoding', 'rating']
preprocessed_data.show()
preprocessed_data.printSchema()

# features로 쓰이지 않는 title, director, rating과 features로 쓰이기 위해 one-hot encoding 된 나머지 columns만 projection해서 새로운 DataFrame(preprocessed_data)를 생성한다. 

cols = ['genre_one_hot_encoding','running_time_one_hot_encoding','screening_rat_one_hot_encoding','dir_movies_one_hot_encoding','main_role_movies_one_hot_encoding']
assembler = VectorAssembler(inputCols=cols, outputCol="features")
preprocessed_data2 = assembler.transform(preprocessed_data)
preprocessed_data2.show()
# # vector assembler module을 이용하여 model fit에 쓰일 features를 지정 및 새로운 column을 만들어 값들을 assign해줍니다.

labelIndexer = StringIndexer(inputCol = 'rating', outputCol = 'labelIndex')
preprocessed_data3 = labelIndexer.fit(preprocessed_data2).transform(preprocessed_data2)
preprocessed_data3.show()
# # 마지막으로 분류의 기준이 되는 rating에 labelIndex를 붙여 줍니다.

train , test = preprocessed_data3.randomSplit([0.75, 0.25])
# # train 데이터와 test 데이터를 0.75 : 0.25 비율로 랜덤 split 해줍니다.

rf = RandomForestClassifier(featuresCol= "features", labelCol= "labelIndex", numTrees=1000)
rfModel = rf.fit(train)
print(type(rfModel))
predictions = rfModel.transform(test)
predictions.select('title', 'rating', 'labelIndex', 'rawPrediction', 'prediction', 'probability').show(10)
# # train data로 model을 학습시키고 test 데이터로 예측을 진행합니다.

evaluator = MulticlassClassificationEvaluator(labelCol="labelIndex", predictionCol="prediction")
accuracy = evaluator.evaluate(predictions)
print("Accuracy = %s" % round((accuracy), 3))
print("Test Error = %s" % round((1.0 - accuracy), 3))
# # Evaluator module을 사용하여 정답률과 오답률을 각각 확인합니다.
