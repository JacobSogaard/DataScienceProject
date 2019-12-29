from pyspark.ml.linalg import Vectors
from pyspark.ml.clustering import KMeans, KMeansModel
from pyspark.ml.feature import VectorIndexer, VectorAssembler, MinMaxScaler
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

class Mlcluster:

    def __init__(self, dataframe, spark):
        self.dataframe = dataframe #split the data here at some point
        cols = ["longitude", "latitude"]
        self.assembler = VectorAssembler(inputCols=cols, outputCol="features")
        self.featuredf = self.assembler.transform(dataframe)
        print(self.featuredf.show(10))

        #self.dataframe = self.transData(dataframe)
        
        self.spark = spark
        #self.df = self.featureRow.union(self.dataframe)

    def print_input_type(self):
        print(type(self.dataframe))

    def transData(self, data):
        return data.rdd.map(lambda r: [Vectors.dense(r[:1])]).toDF(['features'])


    #Only use part of dataframe (split traing and test data)
    def cluster_data_frame(self):
        
      

        #featureIndexer = VectorIndexer(inputCol="features", \
        #                      outputCol="indexedFeatures").fit(self.dataframe)

        # bkm = KMeans() \
        #     .setK(42) \
        #     .setFeaturesCol("features") \
        #     .setPredictionCol("cluster")

        #model = bkm.fit(self.featuredf) #fit model to data this model should be saved for easy testing. Should also just be training data
        #model.save("/home/jacob/Desktop/DataScience/project/DataScienceProject/docker/pysparkExampleImage/kmeansmodel")
        
        model = KMeansModel.load("/home/jacob/Desktop/DataScience/project/DataScienceProject/docker/pysparkExampleImage/kmeansmodel")
        predictdf = model.transform(self.featuredf) #Transform to dataframe with cluster added
        #print(predictdf.show(10))

        #print(predictdf.crosstab("category", "cluster").show())
        #crosstab_category_cluster = predictdf.crosstab("category", "cluster")
        other = predictdf.groupBy('cluster', 'category').count()
        scaled = self.normalize_counts(other)

        #other_sort = scaled.sort(scaled.count_Scaled.asc()).collect()
        #print(other_sort.show())
        row1 = scaled.agg({"count_scaled": "max"}).collect()[0]
        print(row1)


        # pipeline = Pipeline(stages=[featureIndexer, bkm])

        # model = pipeline.fit(self.dataframe)

        #model.save("/home/jacob/Desktop/DataScience/project/DataScienceProject/docker/pysparkExampleImage/kmeansmodel")
       

        #cluster = model.transform(self.dataframe)
        #print(cluster.show())

        #dummy =  self.get_dummy(self,self.dataframe,"index??",["category"],["latitude","longitude"])


        #data = featureIndexer.transform(self.dataframe)
        #print(data.show(10,True))



        #print(len(centers))
        #print(centers)
        #print(model.hasSummary)
        #print(model.summary.clusterSizes)
       
    #Normalize data
    def normalize_counts(self, df):
        unlist = F.udf(lambda x: round(float(list(x)[0]),2), DoubleType())

        i = "count"

        # VectorAssembler Transformation - Converting column to vector type
        assembler = VectorAssembler(inputCols=[i],outputCol=i+"_Vect")

        # MinMaxScaler Transformation
        scaler = MinMaxScaler(inputCol=i+"_Vect", outputCol=i+"_scaled")

        # Pipeline of VectorAssembler and MinMaxScaler
        pipeline = Pipeline(stages=[assembler, scaler])

        # Fitting pipeline on dataframe
        df = pipeline.fit(df).transform(df).withColumn(i+"_scaled", unlist(i+"_scaled")).drop(i+"_Vect")
        return df


    def print_transposed_data(self):
        print(self.dataframe.describe().toPandas().transpose())



   
    #Dummy dataa for categorial data, assign the dataset to this!
    def get_dummy(self, df,indexCol,categoricalCols,continuousCols):


        indexers = [StringIndexer(inputCol=c, outputCol="{0}_indexed".format(c))
                    for c in categoricalCols ]

        # default setting: dropLast=True
        encoders = [ OneHotEncoder(inputCol=indexer.getOutputCol(),
                    outputCol="{0}_encoded".format(indexer.getOutputCol()))
                    for indexer in indexers ]

        assembler = VectorAssembler(inputCols=[encoder.getOutputCol() for encoder in encoders]
                                    + continuousCols, outputCol="features")

        pipeline = Pipeline(stages=indexers + encoders + [assembler])

        model=pipeline.fit(df)
        data = model.transform(df)

        return data.select(indexCol,'features')
