from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import lit
from pyspark.ml.recommendation import ALS

def loadMovieNames():
    movieNames = {}
    with open('/home/maria_dev/ml-100k/u.item') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

def parseInput(line):
    fields = line.value.split()
    return Row(userID=int(fields[0]), movieID=int(fields[1]), rating=float(fields[2]))


if __name__ == '__main__':
    # Create Spark session, which is a Spark 2.0 style way of doing things
    spark = SparkSession.builder.appName('MovieRecs').getOrCreate()

    movieName = loadMovieNames()

    lines = spark.read.text('hdfs:///user/maria_dev/ml-100k/u.data').rdd    # spark.read.text() returns a data frame, use .rdd to get rdd object
    ratingsRDD = lines.map(parseInput)
    ratings = spark.createDataFrame(ratingsRDD).cache()     # call .cache() so that Spark won't recreate this DataFrame more than once

    als = ALS(maxIter=5, regParam=0.01, userCol='userID', itemCol='movieID', ratingCol='rating')
    model = als.fit(ratings)        # use the ratings DataFrame to fit the ALS model


    # Print out ratings from user 6:
    print('\nRatings for userID 6:')
    userRatings = ratings.filter('userID=6')
    for rating in userRatings.collect():
        print(movieName[rating['movieID']], rating['rating'])


    print('\nTop 20 recommendations:')
    ratingCounts = ratings.groupBy('movieID').count().filter('count>100')
    popularMovies = ratingCounts.select('movieID').withColumn('userID', lit(6))

    recommendations = model.transform(popularMovies)

    topRecommendations = recommendations.sort(recommendations.prediction.desc()).take(20)


    for recommend in topRecommendations:
        print(movieName[recommend['movieID']], recommend['prediction'])

    spark.stop()