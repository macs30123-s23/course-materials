from pyspark.sql import SparkSession
import sys

# Get Spark context
spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

# Filter and Map example data, then Reduce
lst = [i for i in range(100)]
lst_p = sc.parallelize(lst)
fm = lst_p.filter(lambda x: x < 10) \
          .map(lambda x: x * 10)

r = fm.reduce(lambda a, b: a + b)

# Write data to S3 bucket of choice
fm.saveAsTextFile('s3://{}/pyspark_example_data'.format(sys.argv[1]))