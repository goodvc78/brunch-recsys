#!/usr/local/bin/python3

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import gensim.models.word2vec as word2vec
import pprint, pickle
from scipy.spatial import distance 
from flask.ext.cors import CORS

## word2vec model path
model_path = '/Users/goodvc/Data/brunch-recsys/resource/b2v.latest.model'
writer_info_path = '/Users/goodvc/Data/brunch-recsys/resource/writer.pkl'

class BrunchRecsys:
    def __init__(self, model_path, writer_info_path):
        self.model_path = model_path
        self.writer_info_path = writer_info_path
        self.load()

    def load(self):
        ## word2vec model load
        self.b2v = word2vec.Word2Vec.load(self.model_path)
        ## writer_info pickle load
        pkl_file = open(self.writer_info_path, 'rb')
        self.writer_info = pickle.load(pkl_file)
        pkl_file.close()
        ## for A to Z  
        self.NX = self.b2v.syn0

    def parseid(self, writers):
        positive = []
        negative = []
        for wid in writers.split(':'):
            if wid[0] == '+':
                positive.append(wid[1:])
            elif wid[0] == '-':
                negative.append(wid[1:])
            else :
                positive.append(wid)

        return (positive, negative)

    def get_writer_info(self, id):
        if id not in self.writer_info:
            return None
        writer = self.writer_info[id]
        if writer.get('documents',0) < 1 or writer.get('followers',0) < 10 :
            return None
        return writer
       
    def most_similar(self, writers):
        ## parse id 
        (positive, negative) = self.parseid( writers )
        neighbors = self.b2v.most_similar(positive=positive, negative=negative, topn=20)
        
        similars = []
        for (id, similarity) in neighbors:
            writer = self.get_writer_info(id)
            if None == writer:
                continue
            writer['similarity'] = similarity
            similars.append(writer)
        return similars

    def nestest(self, NX, v1):
        dist = distance.cdist( NX, v1.reshape(1,len(v1)), 'cosine' )
        nearest_idx = dist.argmin()
        if (NX[nearest_idx] == v1).all() == True:
            dist[nearest_idx] = 1
        return nearest_idx

    def a2z_writers(self, a, z, max_steps=100):
        av = self.b2v[a]
        zv = self.b2v[z]
        sv = (zv - av) / max_steps
        exists = set([a,z])
        writers = [a]
        for n in range(0,max_steps):
            nv = av+(sv*n)
            idx = self.nestest(self.NX, nv)
            name = self.b2v.index2word[idx]
            if not name in exists :
                writers.append(name)
            exists.add(name)
        writers.append(z)

        result = []
        for name in writers:
            writer = self.get_writer_info(name)
            print(a,name)
            if None != writer:
                writer['similarity'] = self.b2v.similarity(a,name)
                result.append(writer)
        return result

############################################### 

recsys = BrunchRecsys(model_path, writer_info_path)
app = Flask(__name__)
CORS(app)
api = Api(app)

class SimilarTo(Resource):
    def get(self, writers):
        result = { 'result':0 }
        similars = recsys.most_similar(writers) 
        if None == similars or len(similars) < 1:
            result['reason'] = "there is on similars "
            return result
        result['result'] = 1
        result['data'] = similars
        return result
 

class AtoZ(Resource):
    def get(self, writers):
        result = { 'result':0 }
        ids = writers.split(':',1)
        if len(ids) != 2 :
            result['reason'] = "not enough id list : {}".format(writers)
            return result;
        
        atozList = recsys.a2z_writers( ids[0], ids[1] )
        result['data'] = atozList
        result['result'] = 1 if len(atozList)>2 else 0
        return result
 
api.add_resource(SimilarTo, '/most_similar/<string:writers>')
api.add_resource(AtoZ,      '/a2z/<string:writers>')

## test 
def test_similarity():
    pprint.pprint(recsys.most_similar('goodvc78'))

def test_atoz():
    pprint.pprint(recsys.a2z_writers('goodvc78','paranmoja'))


if __name__ == '__main__':
    #app.debug = True
    app.run()
    ##test_similarity();
    ##test_atoz()

