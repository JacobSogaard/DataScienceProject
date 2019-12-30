from pyspark.ml.linalg import Vectors
from pyspark.ml.clustering import KMeans, KMeansModel
from pyspark.ml.feature import VectorIndexer, VectorAssembler, MinMaxScaler
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.sql import functions as F
from pyspark.sql.window import Window
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

        
        model = self.fit_model(self.featuredf, 42, "features", "clusters") #Fit model to kmeans
        
        #self.save_model(model) #Save model to local file path

        model = self.load_model() #Load saved model from kmeansmodel folder
        predictdf = model.transform(self.featuredf) #Transform to dataframe with cluster added
        #print(predictdf.show(10))

        #print(predictdf.crosstab("category", "cluster").show())
        #crosstab_category_cluster = predictdf.crosstab("category", "cluster")
        #other = predictdf.groupBy('cluster', 'category').count()
        #scaled = self.normalize_counts(other)

        #other_sort = scaled.sort(scaled.count_Scaled.asc()).collect()
        #print(other_sort.show())
        
        print(self.get_cluster_catergories_percent(predictdf).show())

    def save_model(self, model):
        model.save("/home/jacob/Desktop/DataScience/project/DataScienceProject/docker/pysparkExampleImage/kmeansmodel")

    def load_model(self):
        return KMeansModel.load("/home/jacob/Desktop/DataScience/project/DataScienceProject/docker/pysparkExampleImage/kmeansmodel")

    def get_cluster_catergories_percent(self, df):
        k = 42
        categories = df.select("category").distinct()
        clusters = []
        for i in range(k):
            current_cluster = df.filter(df.cluster == i)  #category count
            counts = current_cluster.groupBy('category').count()
            percent = counts.withColumn('percent', F.col('count')/F.sum('count').over(Window.partitionBy()))
            percent = percent.orderBy('percent', ascending=False)
            clusters.append(percent)

        return clusters
       
    #Min max normalize the counts - this might not be nessecary
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

    def fit_model(self, df, k, feauturesCol, predictionCol):
        bkm = KMeans() \
            .setK(k) \
            .setFeaturesCol(feauturesCol) \
            .setPredictionCol(predictionCol)

        model = bkm.fit(df) #fit model to data this model should be saved for easy testing. Should also just be training data
        return model