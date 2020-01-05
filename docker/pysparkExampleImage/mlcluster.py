from pyspark.ml.linalg import Vectors
from pyspark.ml.clustering import KMeans, KMeansModel
from pyspark.ml.feature import VectorIndexer, VectorAssembler, MinMaxScaler
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.sql import functions as F
from pyspark.sql.functions import rank,sum,col,lit,array
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType
import psycopg2


class Mlcluster:

    def __init__(self, dataframe, spark, cur, conn):
        self.dataframe = dataframe #split the data here at some point
        cols = ["longitude", "latitude"]
        self.assembler = VectorAssembler(inputCols=cols, outputCol="features")
        self.featuredf = self.assembler.transform(dataframe)
        self.k = 20
        self.conn = conn
        print("init ml")
        #print(self.featuredf.show(10))

        #self.dataframe = self.transData(dataframe)
        
        self.spark = spark
        self.cur = cur
        #self.df = self.featureRow.union(self.dataframe)

    def print_input_type(self):
        print(type(self.dataframe))

    def transData(self, data):
        return data.rdd.map(lambda r: [Vectors.dense(r[:1])]).toDF(['features'])

    #Only use part of dataframe (split traing and test data)
    def cluster_data_frame(self):
        #featureIndexer = VectorIndexer(inputCol="features", \
        #                      outputCol="indexedFeatures").fit(self.dataframe)

        print("Cluster dataframe")
        model = self.fit_model(self.featuredf.limit(300), self.k, "features", "cluster") #Fit model to kmeans. Remove limit(300) to use full dataset
        
        current_model = "kmeansmodel"
        model_path = "/app/models/" + current_model

        #self.save_model(model, model_path) #Save model to local file path
        #model = self.load_model(model_path) #Load saved model from kmeansmodel folder
       
        print("transform model")
        predictdf = model.transform(self.featuredf) #Transform to dataframe with cluster added
        #print(predictdf.show(10))

        #print(predictdf.crosstab("category", "cluster").show())
        #crosstab_category_cluster = predictdf.crosstab("category", "cluster")
        #other = predictdf.groupBy('cluster', 'category').count()
        #scaled = self.normalize_counts(other)

        #other_sort = scaled.sort(scaled.count_Scaled.asc()).collect()
        #print(other_sort.show())
        clusters = self.get_cluster_categories_percent(predictdf, model.clusterCenters())

        print("insert cluster")
        print(clusters)
        try: 
            self.insert_cluster_centers_db(clusters, model.clusterCenters())
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.cur is not None:
                self.cur.close()
      
            
        

    def save_model(self, model, path):
        model.save(path)

    def load_model(self, path):
        return KMeansModel.load(path)

    def get_cluster_categories_percent(self, df, centers):
        print("shooow")
        print(df.show())
        clusters = []
        for i in range(self.k):
            current_cluster = df.filter(df.cluster == i)  #category count
            counts = current_cluster.groupBy('category').count()
            percent = counts.withColumn('percent', F.col('count')/F.sum('count').over(Window.partitionBy()))
            percent = percent.withColumn('cluster_center', array(lit(centers[i][0]), lit(centers[i][1])))
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

    def insert_cluster_centers_db(self, clusters, clustercenters):
        cluster_ids = []
        cluster_centers = []
        for cc in clustercenters:
            latitude = cc.item(1)
            longitude = cc.item(0)
            statement = "INSERT INTO clustercenters(coordinates) VALUES ('{%s, %s}') RETURNING id"
            self.cur.execute(statement, (latitude, longitude))
            id_of_new_row = self.cur.fetchone()[0]
            cluster_ids.append(id_of_new_row)
            cluster_centers.append([latitude, longitude])

        index = 0
        for c in clusters:        
            kmeans_out = c.select("category", "count", "percent").collect()
            print("insert")
            for d in kmeans_out:
                print("Insert kmeans ouput")
                statement_insert_kmeans = "INSERT INTO kmeansoutput(category, counts, normalizedcount, percent, cluster) VALUES (%s, %s, %s, %s, %s);"
                category = d["category"]
                count = d["count"]
                percent = d["percent"]
                self.cur.execute(statement_insert_kmeans, (category, count, 0, percent, cluster_ids[index]))

            index += 1
            self.conn.commit()


        print("all inserted")