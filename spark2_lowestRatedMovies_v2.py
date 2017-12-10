from pyspark.sql import SparkSession
from pyspark.sql import Row
from spark2_lowestRatedMovies import loadMovieNames, parseInput

if __name__=='__main__':

    spark = SparkSession.builder.appName('WorstMovies').getOrCreate()

    movieNames = loadMovieNames()

    lines = spark.sparkContext.textFile('hdfs:///user/maria_dev/ml-100k/u.data')
    ratings = spark.createDataFrame(lines.map(parseInput))

    ratingCounts = ratings.groupBy('movieID').count().filter('count>10')
    avgRatings = ratings.groupBy('movieID').avg('rating')

    worstMovies = ratingCounts.join(avgRatings, 'movieID').orderBy('avg(rating)', ascending=False).take(10)

    for movie in worstMovies:
        print(movie)

    spark.stop()
