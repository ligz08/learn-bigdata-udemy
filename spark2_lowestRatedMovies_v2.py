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

    worstMovies = ratingCounts.join(avgRatings, 'movieID').orderBy('avg(rating)', ascending=True).take(10)

    print('Worst movies with more than 10 ratings: (Movie name, Count of ratings, Average rating)')
    for movie in worstMovies:
        print(movieNames[movie['movieID']], movie['count'], '{0:.1f}'.format(movie['avg(rating)']))

    spark.stop()
