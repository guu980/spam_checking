# spam_checking

중간에 한번 컴퓨터가 먹통이되어 parallel HTTP request 를 제대로 구현하지 못했습니다.

Python 을 통해 작성했고 re, requests, beautifulSoup 등의 모듈을 사용하였습니다.

우선 redirection 이 일어날때마다 redir_depth 를 하나씩 감소시켜나가며 spam을 확인해주는 재귀함수의 형태로 구현을 목표로 삼았습니다.

1차적으로 recursive_structure branc 에서 작업해 Content 에서 url 을 추출하기 위해 정규표현식을 위한 파싱, redirection 을 고려하지 않은

직접적인 url string 분석을 통한 spam link 판별 여부를 확인하는 기능을 구현했고 대략적인 구조를 그리고자 했습니다.

2차적으로는 httprequest_handling branch 에서 작업하며 필수적인 기능들을 모두 구현하고자 하였습니다.

우선 병렬처리는 생각하지 않고 http request 를 보내며 2가지 redirection case 중 하나에 해당하는지 확인하고
(1. Status code 301, 302 return, 2. response 의 html 문서에 a href link 보유)

재귀적으로 redirection 하며 redirection 된 링크가 스팸링크에 해당하는지 확인토록 하였습니다.

3차적으로는 parallel branch 에서 작업하며 멀티프로세싱을 통해 하나의 process 당 1~n 개의 request 를 할당해

HTTP request 를 병렬적으로 보내도록 구현하려했으나, 중간에 컴퓨터가 작동을 멈추고 시간부족으로인해 제대로 구현치 못했습니다.

4차적으로는 de_duplicate branch 에서 작업하며 이미 한번 direct 됬던 link 는 검사하지 않고 이전의 결과를 이용하도록 구현하였습니다.

다만 일종의 link 들의 Cycle 이 생기거나 하는 nested 한 경우들은 시간이 부족해 고려하지 못했습니다.

감사합니다.
