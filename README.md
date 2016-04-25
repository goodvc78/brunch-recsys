# Word2Vec을 이용하여 브런치 작가를 추천하는 API
* 브런치 추천 글 : https://brunch.co.kr/@goodvc78/7 
* API 데모 페이지 : http://b2v.historie.kr
* 프로토 타이핑 수준으로 IPython Notebook 형태로 코드가 작성 되었습니다. 
* 데이터 수집 : ./01-brunch data crawling.ipynb 
* word2vec 학습 : ./02-brunch data learning by word2vec.ipynb
* 추천 API(Flask) : ./brunch-recsys-flask.py
* 크롤링된 데이터 저장(sqlite) : 

## 추천 API
* 포멧 : http://b2v.historie.kr:1218/most_similar/{writer-id}
* Sample : http://b2v.historie.kr:1218/most_similar/goodvc78
 * most_similar (goodvc78) : http://b2v.historie.kr:1218/most_similar/goodvc78
 * most_similar (goodvc78+suyoung): http://b2v.historie.kr:1218/most_similar/goodvc78:suyoung
 * a to z (goodvc78~suyoung) : http://b2v.historie.kr:1218/most_similar/goodvc78~suyoung
