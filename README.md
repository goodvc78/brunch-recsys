# Word2Vec을 이용하여 브런치 작가를 추천하는 API
> prototype이라 주로 ipython으로 작업을 해서 코드가 지저분하네요. 
> 코드를 보면서 설명이 필요한 부분이 있으시면 goodvc78@gmail.com 으로 메일 주세요

* 브런치 추천 글 : https://brunch.co.kr/@goodvc78/7 
* API 데모 페이지 : http://b2v.historie.kr
* 프로토 타이핑 수준으로 IPython Notebook 형태로 코드가 작성 되었습니다. 
* 데이터 수집 : ./01-brunch data crawling.ipynb 
 * 크롤링된 데이터 저장(sqlite) : ./resource/brunch_db.db
* word2vec 학습 : ./02-brunch data learning by word2vec.ipynb
 * 학습 결과 python pickle 파일 : ./resource/b2v.lastest.model, ./resource/writer.pkl
* 추천 API(Flask) : ./brunch-recsys-flask.py

## 추천 API
* 포멧 : http://b2v.historie.kr:1218/most_similar/{writer-id}
* Sample : http://b2v.historie.kr:1218/most_similar/goodvc78
 * most_similar (goodvc78) : http://b2v.historie.kr:1218/most_similar/goodvc78
 * most_similar (goodvc78+suyoung): http://b2v.historie.kr:1218/most_similar/goodvc78:suyoung
 * a to z (goodvc78~suyoung) : http://b2v.historie.kr:1218/most_similar/goodvc78~suyoung
 * API Response 결과 Sample 
<pre>
{
  result: 1,
  data: [
  {
    followings: 17,
    name: "cojette",
    megazines: 2,
    documents: 16,
    followers: 133,
    similarity: 0.98149174451828,
    writerid: "cojette",
    profile: "고매한 인격과 냉철한 지성의 초절정 카리스마 잡덕 잉여 데이터 분석가.",
    imgsrc: "http://t1.daumcdn.net/brunch/service/guest/image/_WANm1SmXVtMD4RudCbhcWzD5F8.png"
  },
  {
  followings: 5,
  name: "이도현",
  megazines: 4,
  documents: 2,
  followers: 23,
  similarity: 0.9750361442565918,
  writerid: "cailhuiris",
  profile: "처음 Scala로 함수형 프로그래밍에 매료되고 지금까지 함수형 프로그래밍의 정수를 찾고 있는 개발자입니다.",
  imgsrc: "http://t1.daumcdn.net/brunch/service/guest/image/-1AvgbIv14sYokarjnzk02iq52c.png"
  }
}
</pre> 
