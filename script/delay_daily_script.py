#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb, smtplib, os, urllib2, urllib, datetime, base64, random, textwrap
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from django.conf import settings

title = "한양대학교 자동연장 서비스 안내 메일 입니다"
gmail_user = "ok7217@gmail.com"
gmail_pwd = settings.get_env_variable("mail_pw")
mysql_server = "localhost"
mysql_id = "cheyuni"
mysql_passwd = settings.get_env_variable('db_pw')
mysql_target = "delay"

wise = [
'아버지가 물에 빠진 자식을 건지기 위해 물 속에 뛰어드는 것은 사랑의 감정이다. 사랑은 나 이외의 사람에 대한 행복을 위해서 발로된다. 인생에는 허다한 모순이 있지만 그것을 해결할 길은 사랑뿐이다. -톨스토이',
'위대한 행동이라는 것은 없다. 위대한 사랑으로 행한 작은 행동들이 있을 뿐이다. -테레사 수녀',
'어머니는 인생에서 최초의 인간관계의 대상이기 때문에 어머니에게 호감을 가지고 있는 사람은 대체로 인생을 보는 시선이 따뜻하다. -고쿠분 야스타카 [교제심리학]',
'우리 모두는 삶의 중요한 순간에 타인이 우리에게 베풀어준 것으로 인해 정신적으로 건강하게 살아갈 수 있다. -앨버트 슈바이처',
'사랑은 바위처럼 가만히 있는 것이 아니다. 사랑은 빵처럼 늘 새로 다시 만들어야 한다. -어슬러 K. 르귄',
'사랑은 지배하는 것이 아니라 자유를 주는 것이다. -에리히 프롬',
'결혼을 신성하게 할 수 있는 것은 오직 사랑이며, 진정한 결혼은 사랑으로 신성해진 결혼뿐이다. -톨스토이',
'사랑한다는 것은 관심(interest)을 갖는 것이며, 존중(respect)하는 것이다. 사랑한다는 것은 책임감(responsibility)을 느끼는 것이며 이해하는 것이고, 사랑한다는 것은 주는 것(give)이다. -에리히 프롬',
'누군가를 만나 가슴이 울렁거리고 환희에 젖어 그가 없으면 죽을 것 같은 사랑은 길어봐야 2년 반을 넘지 못한다. -신디 하잔 박사',
'‘사랑의 감정’이란 대뇌에서 도파민, 페닐에치아민, 옥시토신의 세가지 물질이 대뇌에서 분비되어 서로 칵테일처럼 섞이는 과정에서 발생하는 화학반응이다. -하잔 박사',
'사랑이란 쉽게 변하기에 더욱 사랑해야 합니다. -서머셋 몸 [레드]', 
'여성은 ‘이상’으로 사랑을 하고, 남성은 ‘속셈’으로 사랑을 한다. -게리 S. 오밀러', 
'성공적인 결혼이란 두 사람이 서로 인격의 조화를 이루어가기까지 많은 선택과 적응을 요하는, 평생을 통해 이뤄야 할 과정입니다. -금병달',
'물리적으로 가까이 있으면 서로에 대한 관심이 그만큼 높아집니다. -M. 그리핀',
'우리는 흔히 훌륭한 사람을 찾기에 분주합니다. 그러나 내가 먼저 훌륭한 사람이 될 때 더 쉽게 훌륭한 사람을 만날 수 있습니다. -금병달',
'결혼의 성공 여부는 이미 혼전에 80퍼센트 가량 예상할 수 있다. -워렌',
'사랑에 빠지기는 쉽다. 사랑에 빠져 있기도 쉽다. 인간은 원래 외로운 존재이므로, 하지만 한 사람 곁에 머물면서 그로부터 한결같은 사랑을 받기란 결코 쉽지 않다. -안나 루이스 스트롱',
'인간은 자신이 사랑하는 사람만은 완벽한 존재일 것이라는 착각에 빠져 산다. -시드니 포이티에 ',
'인생을 돌아보면 제대로 살았다고 생각되는 순간은 사랑하는 마음으로 살았던 순간뿐이다. -헨리 드루먼드', 
'가장 유능한 사람은 가장 배움에 힘쓰는 사람이다. -괴테', 
'공부 잘한 사람만이 사회에서 성공하는 것은 아니다. 배운 것을 응용할 줄 알아야 한다. -손자병법', 
'교활한 사람은 학문을 경멸하고, 단순한 사람은 학문을 찬양하며, 현명한 사람은 학문을 이용한다. -베이컨',
'그대가 배운 것을 돌려줘라. 경험을 나눠라. -도교', 
'기하학에는 왕도가 없다.(학문에는 왕도가 없다.) -유클리드', 
'공부의 원래 의미란 신체의 활동을 통해서 얻어지는 모든 훈련이다. 머리를 쓰는 일이나 청소를 하는 것이나 다 같은 공부인 것이다. -도올 김용옥', 
'나는 스승에게서 많은 것을 배웠고 친구에게서 많이 배웠고 심지어 제자들에게서도 많이 배웠다. -탈무드',
'널리 배우고 자세히 물으며 깊이 생각하고 분명히 분별하며 꾸준히 실천하라. -주자',
'널리 배워서 뜻을 도탑게 하며, 간절하게 묻되 가까운 것부터 잘 생각하면 인(仁)이 그 속에 있다. -공자',
'때맞춰 면학에 힘써라. 세월은 사람을 기다리지 않는다. -도잠',
'뜻을 높이 세우지 않으면 그 사람의 학문도 평범한 것으로 되고 만다. -진관', 
'만난 사람 모두에게서 무언가를 배울 수 있는 사람이 세상에서 제일 현명하다. -탈무드',
'배우고 때때로 익히면, 또한 즐겁지 아니한가? -공자',
'배우고 생각하지 않으면 곧 어둡고, 생각하고 배우지 않으면 곧 혼돈스럽다. -공자',
'배우기를 늘 다하니 못한 것같이 할 것이요. 오직 배운것을 잊지 않도록 하라. -명심보감',
'배우는 길에 있어서는, 이제 그만하자고 끝을 맺을 때가 없는 것이다. 사람은 그 일생을 통하여 배워야 하고, 배우지 않으면 어두운 밤에 길을 걷는 사람처럼 길을 잃고 말 것이다. -태자',
'배우는 바가 적은 사람은 들에서 쟁기를 끄는 늙은 소처럼 몸에 살이 찔지라도 지혜는 늘지 않는다. -법구경',
'배우라, 비교하라, 사실을 수입하라. -파플로프',
'배우려고 하는 학생은 부끄러워해서는 안 된다. -히레르',
'배우지 않으면, 곧 늙고 쇠해진다. -주자', 
'가르침이 옳은지 그른지 알려고 애쓰면서 그대는 스승 밑에서 십 년 동안이라도 열심히 정진할 수 있다. 그러나 그대는 그대의 삶을 살아야 한다. -도교',
'가장 어려운 기술은 살아가는 기술이다. -메이시', 
'거룩하고 즐겁고 활기차게 살아라. 믿음과 열심에는 피곤과 짜증이 없다. -어니스트 핸즈', 
'그들은 먹기 위해 살고, 소크라테스는 살기 위해 먹는다. -아데나이오스', 
'나는 간소하면서 아무 허세도 없는 생활이야말로 모든 사람에게 최상의 것. 육체를 위해서나 정신을 위해서나 최상의 것이라고 생각한다. -아인슈타인', 
'나 자신의 삶은 물론 다른 사람의 삶을 삶답게 만들기 위해 끊임없이 정성을 다하고 마음을 다하는 것처럼 아름다운 것은 없습니다. -톨스토이', 
'남을 위해 산다는 것은 쉬운 일이어서 누구나 잘 하고 있지만, 이참에 나는 여러분에게 자기 자신을 위해 살도록 요청한다. -에머슨',
'내가 아직 살아있는 동안에는 나로 하여금 헛되이 살지 않게 하라. -에머슨', 
'단순하게 살아라. 현대인은 쓸데없는 절차와 일 때문에 얼마나 복잡한 삶을 살아가는가? -이드리스 샤흐',
'딸기가 딸기 맛을 지니고 있듯이, 삶은 행복이란 맛을 지니고 있다. -알랭',
'당신은 수많은 별들과 마찬가지로 거대한 우주의 당당한 구성원이다. 그 사실 하나만으로도 당신은 자신의 삶을 충실히 살아가야 할 권리와 의무가 있다. -맥스 에흐만',
'더 이상 자신있게 사는 것이 불가능하다면 차라리 당당하게 죽음을 택하라. -니체', 
'마치 밤낮으로 삶의 바다로부터 바닷가로 올라오는 것이라고는 그것들이 전부인 것처럼 우리들은 아직도 여전히 바다의 조가비들을 살펴보느라고 바쁘다. -칼릴 지브란', 
'만약 내가 한 마디로 삶의 정의를 내려야 한다면, "삶은 창조이다."라고 말할 것이다. -클로드 베르나르', 
'명상을 통해 내부의 소리를 듣고 밖에 나가 외계를 알아낸다. 두 가지 깨달음은 결국 하나의 원천에서 온 것. 삶이란 하나의 전체이다. -도교', 
'물질적이고 동물적인 것만 추구하는 삶처럼 나쁜 것은 없으며 영혼을 살찌우려는 행위보다 본인 자신과 타인에게 유익한 일은 없습니다. -톨스토이',
'모든 것은 과거이고 남겨진 모든 것은 미래이다. 우리의 삶은 과거와 미래만 있을 뿐, 현재는 없다. -김용삼', 
'방황과 변화를 사랑한다는 것은 살아 있다는 증거이다. -바그너', 
'그 성공이 무엇이든간에 성공은 튼튼해야 하며, 그리고 서서히 와주는 것이 바람직하다. -김용삼', 
'도중에 포기하지 말라. 망설이지 말라. 최후의 성공을 거둘 때까지 밀고 나가자. -데일 카네기',
'당신이 성공하기위해서는 거치는 과정마다 반드시 일의 결과를보아야 한다. 마음먹은 일은 일단 시작했으면 반드시 끝이라는 결과를 모아야만 한다. -김용삼',
'당장 편하자고 남의 손을 빌리면 성공의 기쁨도 영영 남의 것이 된다. -앤드류 매튜스', 
'만약 성공의 비결이란 것이 있다고 하면 그것은 타인의 관점을 잘 포착하여 자기 자신의 입장에서 사물을 볼 줄 아는 재능, 바로 그것이다. -헨리 포드',
'만약 여러분이 인생에 성공하기를 바라거든 견인불발을 벗삼고, 경험을 현명한 조언자로 하며, 주의력을 형으로 삼고, 희망을 수호신으로 하라. -에머슨',
'만족하게 살고, 때때로 웃으며, 많이 사랑한 사람이 성공한다. -A.J. 스탠리',
'먼저 핀 꽃은 먼저 진다. 남보다 먼저 공을 세우려고 조급히 서둘 것이 아니다. -채근담',
'명예롭지 못한 성공은 양념하지 않은 요리와 같아서, 배고픔은 면하게 해주지만 맛은 없다. -조 파테이노', 
'로마에 가면 로마 사람들이 하는 대로 하라는 것처럼 성공의 가장 확실한 법칙은 없다. -버나드 쇼', 
'사람의 일생은 돈과 시간을 쓰는 방법에 의하여 결정된다. 이 두가지 사용법을 잘못하여서는 결코 성공할 수 없다. -다케우치 히토시',
'싸워서 이기기는 쉬워도 이긴 것을 지키기는 어렵다. -오자',
'성공에 대해서 서두르지 않고, 교만하지 않고, 쉬지 않고, 포기하지 않는다. -로버트 H. 슐러', 
'성공은 결과이지 목적은 아니다. -G. 플로베르',
'성공은 그 사람의 성격이나 인격을 높게 한다. -W.S. 모옴',
'성공은 박정한 미인을 닮았다. 그녀를 손에 넣기까지 몇 년의 세월이 지나가서야 겨우 그녀가 몸을 맡길 단계가 됐을 때는 둘 다 나이들고 늙어서 서로 아무 쓸모가 없다. -베르네',
'성공은 성공지향적인 사람에게만 온다. 실패는 스스로 실패할 수밖에 없다고 체념해버리는 사람에게 온다. -나폴레온 힐',
'성공은 수고의 대가라는 것을 기억하라. -소포클레스',
'성공은 수만 번의 실패를 감싸준다. -조지 버나드 쇼',
'성공은 실패가능성과 패배의 위험을 무릅쓰고 얻어야 한다. 위험 없이는 성취의 보람도 없다. -레어 크록', 
'성공을 거두기 위하여 필요한 것은 계산된 모험이다. -디오도어 루빈',
'성공을 하려면 남을 떠밀지 말고, 또 제 힘을 측량해서 무리하지 말고 제 뜻한 일에 한눈팔지 말고 묵묵히 나가야 한다. 평범한 방법이지만 이것이 성공을 가져다주는 것이다. -프랭클린',
'성공을 확신하는 것이 성공에의 첫걸음이다. -로버트 슐러', 
'성공의 가장 빠른 길은 일을 사랑함이다. -츄크',
'성공의 비결이 있다면, 그것은 타인의 입장이 되어서 모든 것을 생각하는 것이다. -헨리 포드',
'성공의 비결은 어떤 직업에 있든 간에 그 분야에서 제 1인자가 되려고 하는 데에 있다. -앤드류 카네기',
'성공의 비결은 "남에게 대접받고자 하는 대로 남을 대접하라."는 황금률에 있는 것이다. -죤 코맥넬',
'성공의 확실한 길은 크게 생각하고, 행동하는 것이다. -스텔링 실', 
'성공이란 대담무쌍하게 가는 아이다. -디즈레일리',
'성공이란 결과이지 목적이어서는 안 된다. -플로베르',
'성공이란 그 결과로 측정하는 게 아니라, 그것에 소비한 노력의 총계로 따져야 할 것이다. -에디슨',
'성공이란, 평범한 보통 사람들이 내린 비상한 결단에 의해 이루어진 결과라고 믿는다. -디오도어 루빈',
'성공이 보이면 지치기 쉽다. -팔만대장경', 
'성공하기를 원하는가? 그렇다면 이미 개척해놓은 성공의 길이 아니라 그 누구도 가지 않는 새로운 길을 개척해야만 한다. -로드 파머스턴',
'성공한 사람들은 어느 일에나 항상 실패의 가능성이 있다는 사실을 알고 있는 사람들이다. 그들은 실패를 두려워하지 않는 태도로 의연하다. -디오도어 루빈',
'성공한 사람은 송곳처럼 어떤 한 점을 향하여 일한다. -C.N. 보비',
'성공한 사람은 실패한 사람의 삶이 얼마나 모진 것인지 깨달아야 한다. -에드가 왓슨 하우',
'성공을 획득하려면 사람에게 사랑받는 덕과 함께 사람을 두렵게 하는 결점도 필요하다. -죠셉 슈베르',
'성공에 중요한 요소는 지식과 창조력이다. -에릭 브리 뉼슨',
'성공은 역경과 번민의 체험을 통하지 않고서는 다가오지 않는다. -김용삼',
'성공하지 못할 거라는 그릇된 믿음을 버리는 것이 성공을 향한 첫걸음이다. -앤드류 매튜스', 
'아무리 위대한 일도 열심히 하지 않고 성공된 예는 없다. -R.W. 에머슨',
'양손을 주머니에 넣고서는 성공의 사다리를 오를 수가 없다. -엘마 윌러',
'어떤 것이든 정상에 오른 순간부터 조금씩 내리막길을 걷기 시작하는 것이다. -그라시안',
'우리는 성공을 향해 전진할수록, 우리들은 사람들로부터 고립될 가능성이 많아지는 것이다. -디오도어 루빈',
'인생에서 성공자가 되기 위한 조건은, 일에 대해서 나날이 흥미를 새롭게 할 수 있을 것과, 일에 끊임없이 마음을 쏟는다는 것, 매일을 무의미하게 지내지 않는다는 것이다. -윌리엄 라이언 펄푸스',
'인생에서의 성공은 어떤 지위에 올랐느냐가 아니라, 장애물을 극복하며 성공하려고 노력하는 과정에 있다. -보커 T. 워싱턴',
'인생에 있어서 성공을 A라 한다면, 그 법칙을 A=X+Y+Z 로 나타낼 수 있다. X는 일, Y는 노는 것이다. 그러면 Z는 무엇인가? 그것은 침묵을 지키는 것이다. -아인슈타인',
'인생에 있어서 성공의 비결은 성공하지 않은 사람들에게 있다. -콜린즈',
'인생의 목적에는 일과 건강과 행복이다. 일에는 즐거움이 있고 건강이 있다. 자기 직분에서 즐거움을 느끼고 보람을 찾는 사람은 틀림없이 성공한다. -헨리 포드',
'일의 성공을 위하여 필요하다면 어떤 조직도 개혁하고 어떤 방법도 폐기하고 어떤 의논도 포기할 각오가 있어야 한다. -헨리 포드', 
'자기 능력은 생각하지 않고 단숨에 몇 계단을 뛰어 올라가려는 사람은 성공하지 못한다. -데일 카네기',
'자기 신뢰가 성공의 제1의 비결이다. -에머슨',
'자신이 실패한 사업을 바보같은 사람들이 훌륭히 성공시킨 것을 보는만큼 뼈저린 굴욕은 없다. -플로베르',
'자신이 제일 좋아하는 것을 해야 성공할 수 있다. -김영세',
'작은 성공을 만족스럽게 생각하는 사람은 큰 성공을 얻지 못한다. -제세 메서 게만',
'장기적 비전을 위해 단기적 손해를 감수한다. 이것이 성공의 비결이다. -빌게이츠',
'하늘의 해는 잴 수도 없을 만큼 풍부하다. 무상한 세계의 중심에 최고의 성공이 있다. -도교',
'한번도 성공한 적이 없는 사람이 가장 감미로운 것으로 생각하는 것은, 그것은 성공하는 것이다. -디킨스',
'행동력을 착실하게 향상시키려면 당신이 해야할 일을 이 순간부터 주저 말고 시작하는 것이며, 전력을 다하여 부딪혀 나가는 일이다. 이외에 성공의 비결이란 절대로 없다. -하라 잇페이', 
'가장 귀중한 재산은 사려깊고 헌신적인 친구이다. -다리우스',
'가치있는 적이 될 수 있는 자는 화해하면, 더 가치있는 친구가 될 것이다. -펠담',
'같은 것을 같이 좋아하고 같이 싫어하는 것은 우정의 끈을 더욱 단단하게 옭아준다. -살루스트',
'결혼이란 제도의 도움으로 연애가 뿌리깊게 계속함이 건전한 것과 같이, 피어나는 우정도 일종의 구속받을 것이 필요하다. -앙드레 모루아',
'고난과 불행이 찾아올 때에, 비로소 친구가 친구임을 안다. -이태백',
'궁핍과 곤란에 처한 때야말로 친구를 시험하기 가장 좋은 기회이다. 어떠한 때에도 곁에 있어 주는 것이 참된 친구이다. -솔로몬 왕',
'그들이 만약 우정 때문에 당신에게 복종한다면 당신은 그들을 배신하는 셈이 된다. 당신에게는 개인으로서 남에게 희생을 요구할 권리 따위는 전혀 없기 때문이다. -생텍쥐베리',
'그 사람을 모르거든 그 벗을 보라. -메난드로스',
'임금을 알고자 하면 먼저 그 신하를 보고, 사람을 알고자 하면 그 벗을 보고, 아버지를 알고자 하면 먼저 그 자식을 보라. 임금이 거룩하면 신하가 충성스럽고, 아버지가 인자하면 자식이 효성스럽다. -왕량', 
'나보다 나을 것이 없고 내게 알맞은 벗이 없거든 차라리 혼자 착하기를 지켜라. 어리석은 사람의 길동무가 되지 말라. -법구경',
'나보다는 상대방을 생각하는 우정, 이러한 우정은 어떠한 어려움도 뚫고 나아간다. -G. 무어',
'나와 벗 사이는 내가 책을 대하는 것과 같다. 하지만 그것을 발견했을 때는 언제까지나 떼어놓지는 않지만 그것을 이용하는 일은 지극히 드물다. -에머슨',
'너를 칭찬하고 따르는 친구도 있을 것이며, 너를 비난하고 비판하는 친구도 있을 것이다. 너를 비난하는 친구와 가까이 지내도록 하고 너를 칭찬하는 친구와 멀리하라. -탈무드',
'누구와도 친구가 되려는 사람은 누구의 친구도 아니다. -부페퍼', 
'다정한 벗을 찾기 위해서라면 천리 길도 멀지 않다. -톨스토이',
'단단한 우정, 또는 영속적인 사랑의 관계를 유지하고 있다면, 그것은 마음이 선량할 뿐만 아니라 굳건한 정신력을 가진 그야말로 인간으로서 매우 중요한 두 가지 조건을 겸비하였다는 좋은 증거다. -윌리암 해즐릿',
'당신의 친구가 당신에게 있어서 벌꿀처럼 달더라도 전부 핥아먹어서는 안 된다. -탈무드',
'대도시에서는 우정이 뿔뿔이 흩어진다. 이웃이라는 가까운 교제는 찾아 볼 수 없다. -베이컨', 
'게으르고 나태한 사람은 죽음에 이르고, 애써 노력하는 사람은 죽는 법이 없다. -법구경', 
'그대가 얻고 싶은 것을 가졌거든 그것을 얻기에 바친 노력만큼 그대도 노력하라. 이 세상 모든 물건은 대가없이 얻을 수 없는 일이다. 남이 노력해서 얻은 것을 그대는 어찌 팔짱을 끼고 바라보고 있는가? -힐티', 
'노력이 적으면 얻는 것도 적다. 인간의 재산은 그의 노고에 달렸다. -헤리크',
'노력하는 데 있어서 이득을 바라지 마라. -도교', 
'독수리는 마지막 성공을 거둘 때까지 온 생명을 바쳐 노력한다. -여안교', 
'목적 이루기 위해서 오랜 인내를 하기보다는 눈부신 노력을 하는 편이 쉽다. 성공하는 데는 두 가지 길밖에 없다. 하나는 자신의 근면, 하나는 타인의 어리석음. -라 브뤼에르', 
'백 명의 환자들을 무덤으로 보내야만 유명한 의사가 될 수 있다. 완성의 순간에 도달할 때까지 부단히 노력해야만 한다. -그라시안', 
'사나운 말도 잘 길들이면 명마가 되고, 품질이 나쁜 쇠붙이도 잘 다루면 훌륭한 그릇이 되듯이 사람도 마찬가지다. 타고난 천성이 좋지 않아도 열심히 노력하면 뛰어난 인물이 될 수 있다. -채근담',
'사람을 강하게 만드는 것은 사람이 하는 일이 아니라, 하고자 노력하는 것이다. -어니스트 헤밍웨이',
'사람이 위대하게 되는 것은 노력에 의하여 얻어진다. 문명이란 참다운 노력의 산물인 것이다. -스마일즈', 
'승리는 노력과 사랑에 의해서만 얻어진다. 승리는 가장 끈기있게 노력하는 사람에게 간다. 어떤 고난의 한가운데 있더라도 노력으로 정복해야 한다. 그것뿐이다. 이것이 진정한 승리의 길이다. -나폴레옹 1세', 
'실패를 걱정하지 말고 부지런히 목표를 향하여 노력하라. 노력한 만큼 보상을 받을 것이다. -노만 V. 필', 
'짧은 인생은 시간의 낭비에 의해 더욱 짧아진다. -S. 존슨', 
'일은 그것이 쓰일 수 있는 시간이 있는 만큼 팽창한다. -파킨스',
'시간을 단축시키는 것은 활동이요, 시간을 견디지 못하게 하는 것은 안일함이다. -괴테', 
'짬을 이용하지 못하는 사람은 항상 짬이 없다. -유럽속담', 
'시간이 모든 것을 말해준다. 시간은 묻지 않았는 데도 말을 해주는 수다쟁이다. -에우리피데스',
'오늘 계란 하나를 가지는 것보다 내일 암탉 한마리를 가지는 쪽이 낫다. -플러', 
'오늘 할 수 있는 일에만 전력을 쏟으라. -뉴턴', 
'나는 장래의 일을 절대로 생각하지 않는다. 그것은 틀림없이 곧 오게 될 테니까. -아인슈타인',
'미래를 신뢰하지 마라, 죽은 과거는 묻어버려라, 그리고 살아있는 현재에 행동하라. -롱펠로', 
'오늘 가장 좋게 웃는 자는 역시 최후에도 웃을 것이다. -니체', 
'오늘이라는 날은 두번 다시 오지 않는다는 것을 잊지 말라. -단테', 
'계획이란 미래에 관한 현재의 결정이다. -드래커', 
'시간은 말로써 나타낼 수 없을 만큼 멋진 만물의 소재이다. -아놀드 버넷', 
'시간을 선택하는 것은 시간을 절약하는 것이다. -베이컨', 
'시간이 덜어주거나 부드럽게 해주지 않는 슬픔이란 하나도 없다. -키케로', 
'시간이 말하는 것을 잘 들어라. 시간은 가장 현명한 법률고문이다. -페리클레스', 
'가라, 달려라, 그리고 세계가 6일 동안에 만들어졌음을 잊지 말라. 그대는 그대가 원하는 것은 무엇이든지 나에게 청구할 수 있지만 시간만은 안된다. -나폴레옹', 
'가장 바쁜 사람이 가장 많은 시간을 갖는다. 부지런히 노력하는 사람이 결국 많은 대가를 얻는다. -알렉산드리아 피네', 
'그대의 하루하루를 그대의 마지막 날이라고 생각하라. -호라티우스', 
'내가 헛되이 보낸 오늘 하루는 어제 죽어간 이들이 그토록 바라던 하루이다. 단 하루면 인간적인 모든 것을 멸망시킬 수 있고 다시 소생시킬 수도 있다. -소포클레스', 
'내일은 시련에 대응하는 새로운 힘을 가져다 줄 것이다. -C.힐티', 
'때가 오면 모든 것이 분명해진다. 시간은 진리의 아버지이다. -타블레', 
'변명 중에서도 가장 어리석고 못난 변명은 "시간이 없어서"라는 변명이다. -에디슨', 
]


def make_secret(id):
    return id[0:2] + "linux for human" + id[2:4] + "hello" + id[4:8] + "ok" + id[8:]

def DecodeAES(c, e):
    return c.decrypt(base64.b64decode(e)).rstrip('c')

def login_shortcut(user_id) :
    login_url = 'https://information.hanyang.ac.kr/ansan/jsp/common/URLlinkGate.jsp'
    values = {"id":user_id, "code":"200", "failURL":"/ansan/jsp/common/LoginForm.jsp", "gubun":"STU_EMP"}
    param  = urllib.urlencode(values)
    request = urllib2.Request(login_url, param)
    response = urllib2.urlopen(request)
    cookie = response.headers.get('Set-Cookie')
    return cookie

def date_delta(base_date):
    yy=int(base_date[:4])
    mm=int(base_date[5:7])
    dd=int(base_date[8:10])
    d=datetime.date(yy,mm,dd)
    return (datetime.date.today() - d).days

def check_usernum(user_id, password) :
    check_url = 'https://information.hanyang.ac.kr/ansan/jsp/common/LoginHandlerPortalHanyang.jsp'
    values = {"id":user_id, "password":password, "returnURL":"/ansan/index.jsp", "siteSub":"Y", "failURL":"/ansan/jsp/common/LoginForm.jsp", "gubun":"STU_EMP"}
    param = urllib.urlencode(values)
    request = urllib2.Request(check_url, param)
    response = urllib2.urlopen(request)
    cookie = response.headers.get('Set-Cookie')
    r = response.read()
    soup = BeautifulSoup(r)
    is_hyu_student = False
    if len(soup.find_all("input", {"name":"code"})) == 1:
        is_hyu_student = True
    return is_hyu_student

def do_delay(cookie, user_id) :
    status = ("normal", "")
    url = "https://information.hanyang.ac.kr/ansan/jsp/myl/renew/RenewController.jsp?act=RenewAction&model=RenewModel&method=doList"
    request = urllib2.Request(url)
    request.add_header('cookie',cookie)
    response = urllib2.urlopen(request)
    r = response.read()

    booked_data = []
    soup = BeautifulSoup(r)
    each_data = soup.find_all("tr", attrs={"class": "board_line1"})
    index = 0

    for data in each_data :  # count, book_info, start, end, in_booked
        booked = {}
        booked['index'] = index
        booked['book_info'] =  data.find("input")['value'].encode('utf-8')
        booked['book_name'] = str(data.find_all("td")[2].text.encode('utf-8')).strip()
        booked['start'] = str(data.find_all("td")[6].text).strip()
        booked['end'] = str(data.find_all("td")[7].text).strip()
        booked['count'] = int(data.find_all("td")[8].text)
        booked['do_delay'] = False
        if date_delta(booked['end']) == 0:
            booked['do_delay'] = True
        index = index + 1
        booked_data.append(booked)

    values = {"model":"RenewModel", "act":"RenewAction", "method":"doRenewal", "menuid":"", "serialno":""}
    param = urllib.urlencode(values)
    count = 0

    for data in booked_data :
        if data['do_delay'] :
            delay_target = urllib.urlencode(dict(checkbox = data['book_info']))
            param = param + "&" + delay_target
            count = count + 1

    for data in booked_data :
        if data['count'] == 10 :
            status = ("delay_limit", "")
            break

    if count != 0 :
    # if count == 0 : #test case
        url = "https://information.hanyang.ac.kr/ansan/jsp/myl/renew/RenewController.jsp"
        request = urllib2.Request(url, param)
        request.add_header('cookie', cookie)
        response = urllib2.urlopen(request)
        r = response.read()        
        # f = open("2008036038_log.txt", 'r') #test case
        # r = f.read()
        
        soup = BeautifulSoup(r)
        results = soup.find_all("tr", attrs={"class": "board_line1"})
        delay_results = []

        for result in results:
            soup2 = BeautifulSoup(str(result))
            value = {} 
            value['book_name'] = soup2.find_all("td")[1].text.strip()
            value['result'] = soup2.find_all("td")[3].text.strip()
            delay_results.append(value)

        log = ""    
        for result in delay_results:
            log = log + result['book_name'].encode('utf-8') + " : " + result['result'].encode('utf-8') + "\n"
        status = ("delay_day", log)
        f = open("/home/cheyuni/delay/log/" + user_id + "_log.txt", "a+")
        f.write(str(datetime.date.today()) + "\n" + log)
    return status


def send_gmail(to, subject, text, attach):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject    
    msg['From'] = gmail_user
    msg['To'] = to

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    # part2 = MIMEText(html, 'html')
    
    msg.attach(MIMEText(text, 'html'))
    
    part = MIMEBase('application','octet-stream')
    if(attach != None):
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment: filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com",587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user,gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()

if __name__ == "__main__" :
    db = MySQLdb.connect(host=mysql_server, user=mysql_id, passwd=mysql_passwd, db=mysql_target)
    cursor = db.cursor()
    cursor.execute('select is_delay, user_num, password, mail from apps_user')
    users = cursor.fetchall()
    # count = 1 #test case
    for each_user in users:
        # if count != 1: #test case
        #     break
        if each_user[0] == 1:
            # count = count + 1
            secret = make_secret(each_user[1])
            cipher = AES.new(secret)
            to = each_user[3]
            if(check_usernum(each_user[1], DecodeAES(cipher, each_user[2]))):
                delay_result = do_delay(login_shortcut(each_user[1]), each_user[1])

                if delay_result[0] == "delay_limit" :
                    selected_wise = wise[random.randint(1, len(wise))]
                    word_list = textwrap.wrap(selected_wise, 80)
                    changed_word = "<br />".join(word_list)
                    message = """\
<html>
  <head></head>
  <body style="color:#1f497d">
    <p>최후의 최후까지 연장하셨네요.</p>
    <p>이제 반납할 때가 되었습니다.</p>
    <p>연체료 내지 마시고 반납하러가세요~ :)</p>
    <br />
    <p>--------------------------------------------------------------------------------</p>
    %s<br /><br />
    <a href="https://delay.cheyuni.net">https://delay.cheyuni.net</a><br />
    <p">--------------------------------------------------------------------------------</p>
  </body>
</html>
""" % changed_word
                    send_gmail(to, title, message, None)
                elif delay_result[0] == "delay_day" :
                    selected_wise = wise[random.randint(1, len(wise))]
                    word_list = textwrap.wrap(selected_wise, 80)
                    changed_word = "<br />".join(word_list)
                    log = delay_result[1]
                    log_nl2br = ""
                    for word in log:
                        if word == '\n':
                            log_nl2br = log_nl2br + '<br />'
                        else:
                            log_nl2br = log_nl2br + word
                    message = """\
<html>
  <head></head>
  <body style="color:#1f497d">
    <p>연장 결과입니다. :)</p>
    <p>%s</p>
    <br />
    <p>--------------------------------------------------------------------------------</p>
    %s<br /><br />
    <a href="https://delay.cheyuni.net">https://delay.cheyuni.net</a><br />
    <p">--------------------------------------------------------------------------------</p>
  </body>
</html>
""" % (log_nl2br, changed_word)
                    send_gmail(to, title, message, None)                    
                else :
                    print "no one to delay"
            else:
                selected_wise = wise[random.randint(1, len(wise))]
                word_list = textwrap.wrap(selected_wise, 80)
                changed_word = "<br />".join(word_list)
                message = """\
<html>
  <head></head>
  <body style="color:#1f497d">
    <p>연장에 실패하였습니다.</p>
    <p>등록하신 학번과 비밀번호를 잘못 입력하셨거나.</p>
    <p>과 홈페이지 비밀번호를 변경하셨기 때문일 수 있어요.</p>
    <p>귀찮아서 개인정보 수정을 안만들었어요. 메일주시면 삭제해드려요. 재가입하시면됩니다.</p>
    <br />
    <p>--------------------------------------------------------------------------------</p>
    %s<br /><br />
    <a href="https://delay.cheyuni.net">https://delay.cheyuni.net</a><br />
    <p">--------------------------------------------------------------------------------</p>
  </body>
</html>
""" % changed_word
                send_gmail(to, title, message, None)
                cursor.execute('update apps_user set is_delay=0 where user_num = "' + each_user[1] + '"')
                db.commit()
    f = open("/home/cheyuni/delay/log/daily_log.txt", "a+")
    f.write(str(datetime.date.today()) + " : success \n")
