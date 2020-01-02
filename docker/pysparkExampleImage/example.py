from operator import add
from pyspark import SparkConf, SparkContext, SQLContext
from mlcluster import Mlcluster
from config import config
from database import connect
import os
import locale


print("pwd: " + os.getcwd())
connection = connect()
cur = connection.cursor()


locale.getdefaultlocale()
locale.getpreferredencoding()

conf = SparkConf().set('spark.driver.host', '127.0.0.1')
sc = SparkContext(master='local', appName='myAppName', conf=conf)
sc.setLogLevel("ERROR")
files = "hdfs://172.200.0.2:9000/data.csv"
files = "hdfs://172.200.0.2:9000/data.csv"

# Create an sql context so that we can query data files in sql like syntax
sqlContext = SQLContext(sc)

#df = sqlContext.read.load (files,
#                                format='com.databricks.spark.csv',
#                                header='true',
#                                inferSchema='true').select("location")

df_ml = sqlContext.read.load (files,
                                format='com.databricks.spark.csv',
                                header='true',
                                inferSchema='true').select("longitude", "latitude", "category")



ml = Mlcluster(df_ml, sqlContext, sc)
#ml.print_transposed_data()
#ml.cluster_data_frame()
#ml.print_input_type()
ml.cluster_data_frame()
#ml.print_feature()

                                inferSchema='true').select("location")


def get_keyval(row):
    # get the text from the row entry
    text = row.location

    # lower case text and split by space to get the words


    # for each word, send back a count of 1
    # send a list of lists
    return [[text, 1]]



# for each text entry, get it into tokens and assign a count of 1
# we need to use flat map because we are going from 1 entry to many
#mapped_rdd = df.rdd.flatMap(lambda row: get_keyval(row))

# for each identical token (i.e. key) add the counts
# this gets the counts of each word
#counts_rdd = mapped_rdd.reduceByKey(add)

# get the final output into a list
#word_count = counts_rdd.collect()

#print(word_count)

print(word_count)




