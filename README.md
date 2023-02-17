# badwordDetection2

만들다가 실패한 [욕설탐지모듈](https://github.com/seolmango/KoreanBadwordDetection)의 아이디어를 바탕으로 새롭게 만드는 욕설탐지모듈입니다.

## 개발 목표

욕설을 탐지하는 방법은 크게 두가지가 있습니다. 많은 욕설 채팅 데이터를 이용해서 머신러닝을 통해 욕설을 분류하는 방법, 그리고 단순히 금칙어 리스트안에 있는 단어가 글에 존재하는지 확인하는 방법이 있죠.

하지만 두가지 방법 모두 장단점이 있습니다. 머신러닝을 통한 방법은 욕설의 탐지율이 높고 오탐을 할 가능성도 낮다는 장점이 있지만 많은 양의 라벨링된 욕설 데이터가 필요하고 새로운 욕설이나 어떤 집단만의 금칙어를 추가해야하는 경우 그 방법이 복잡합니다.

금칙어 기반의 방식은 어떨까요? 여긴 새로운 욕설의 추가도 쉽고 알고리즘도 단순합니다. 하지만 유저들의 채팅 데이터는 경우가 좀 다르죠. 많은 오타와 수많은 우회법이 있기 때문입니다. 예를 들어볼까요? 우리는 '시간'이라는 말이 욕설이라고 가정해봅시다. 그럼 금칙어리스트에 '시간','sigan','tlrks','ㅅ1간','^ㅣ간' 등의 말들도 추가해줘야합니다. 이런방식으론 실시간으로 대응하기 쉽지 않습니다.

그래서 저는 이 두가지 방식의 장단점을 혼합하고 싶었습니다. 쉽고 빠른 욕설의 추가와 수정이 가능하고 다양한 우회방식에도 욕을 잘 잡아내는 욕설탐지모듈을 만들려고 시도하고 있습니다.

## 원리

이 모듈은 기본적으로 여러 가지의 욕설 탐지 우회 방식에 대응하는 **필터**들이 모아진 구조입니다. 현재 모듈에 포함된 필터들의 정보가 아래 있습니다.

### 1. KoEnKeyBoFilter(filter1)

한국어를 영어 키보드 상태로 치는 욕설을 잡아내는 필터입니다. q는 ㅂ, Q는 ㅃ로 치환시키는 방법으로 탐지합니다. 예를 들어 'Tlqkf'이 입력되면 'ㅆㅣㅂㅏㄹ'로 치환하여 욕설 탐색을 시도합니다. 아래는 치환을 위해 사용하는 데이터입니다.

```python
self.key_change_data = {'q': 'ㅂ', 'Q': 'ㅃ', 'w': 'ㅈ', 'W': 'ㅉ', 'e': 'ㄷ', 'E': 'ㄸ',
                        'r': 'ㄱ', 'R': 'ㄲ', 't': 'ㅅ', 'T': 'ㅆ', 'y': 'ㅛ', 'Y': 'ㅛ',
                        'u': 'ㅕ', 'U': 'ㅕ', 'i': 'ㅑ', 'I': 'ㅑ', 'o': 'ㅐ', 'O': 'ㅒ',
                        'p': 'ㅔ', 'P': 'ㅖ', 'a': 'ㅁ', 'A': 'ㅁ', 's': 'ㄴ', 'S': 'ㄴ',
                        'd': 'ㅇ', 'D': 'ㅇ', 'f': 'ㄹ', 'F': 'ㄹ', 'g': 'ㅎ', 'G': 'ㅎ',
                        'h': 'ㅗ', 'H': 'ㅗ', 'j': 'ㅓ', 'J': 'ㅓ', 'k': 'ㅏ', 'K': 'ㅏ',
                        'l': 'ㅣ', 'L': 'ㅣ', 'z': 'ㅋ', 'Z': 'ㅋ', 'x': 'ㅌ', 'X': 'ㅌ',
                        'c': 'ㅊ', 'C': 'ㅊ', 'v': 'ㅍ', 'V': 'ㅍ', 'b': 'ㅠ', 'B': 'ㅠ',
                        'n': 'ㅜ', 'N': 'ㅜ', 'm': 'ㅡ', 'M': 'ㅡ'}
```

### 2. EnProFilter(filter2)

한국어를 영어 발음으로 적는 욕설을 잡아내는 필터입니다. 발음법은 표준 발음법의 외국어 표기법을 참고하였습니다. 위의 filter1와 같이 치환시키는 방법으로 작동합니다. 예를 들어 'sibal'이 입력되면 'ㅆㅣㅂㅏㄹ'로 치환합니다. 아래는 해당 데이터입니다.

```python
one = {'a':'ㅏ', 'o':'ㅗ', 'u':'ㅜ', 'i':'ㅣ', 'e':'ㅔ', 'g':'ㄱ', 'k':'ㅋ',
       'd':'ㄷ', 't':'ㅌ', 'b':'ㅂ', 'p':'ㅍ', 'j':'ㅈ', 's':'ㅅ', 'h':'ㅎ',
       'n': 'ㄴ', 'm': 'ㅁ', 'r': 'ㄹ', 'l': 'ㄹ', 'c':'씨'}
two = {'ng':'ㅇㅇ', 'ch':'ㅊㅊ', 'kk':'ㄲㄲ', 'tt':'ㄸㄸ', 'pp':'ㅃㅃ', 'ss':'ㅆㅆ', 'jj':'ㅉㅉ',
       'eo':'ㅓㅓ', 'eu':'ㅡㅡ', 'ae':'ㅐㅐ', 'oe':'ㅚㅚ', 'wi':'ㅟㅟ', 'ui':'ㅢㅢ', 'ya':'ㅑㅑ',
       'yo':'ㅛㅛ', 'yu':'ㅠㅠ', 'wa':'ㅘㅘ', 'wo':'ㅟㅟ', 'ye':'ㅖㅖ', 'we':'ㅞㅞ'}
three = {'yeo':'ㅕㅕㅕ', 'yae':'ㅐㅐㅐ', 'wae':'ㅙㅙㅙ'}
```

위의 데이터에서 똑같은 한글이 여러번 반복되게 적혀있는 것은 치환과정에서 글자수가 변하는 것을 방지하기 위함입니다. 치환 이후 진행되는 문장의 전처리 과정에서 중복된 문자열이 제거되기 때문에 이렇게 데이터를 작성해도 탐지에는 문제가 생기지 않습니다.

또한 위의 데이터에는 한가지 예외가 있습니다. 바로 'c'인데, 표준 발음법을 준수한다면 'ㅋ'와 같은 한글로 치환되어야하지만 c는 '씨'라는 발음으로 사용되는 경우가 많다고 생각되어 이처럼 예외로 지정하게 되었습니다.

### 3. ImageFilter(filter3)

이 필터는 입력된 문자열을 사진으로 저장하여 욕설 사진과 템플릿 매칭 시켜서 찾는 방법입니다. 예를 들어

![문자열 사진](https://github.com/seolmango/badwordDetection2/blob/main/sentence.png)

와 같이 문자열을 저장하고 

![욕설 사진](https://github.com/seolmango/badwordDetection2/blob/main/0.png)

와 같이 욕설을 저장하여 사진으로 매칭을 시도합니다. 폰트는 현재 NotoSans-CJK를 사용하고 있습니다.

이 필터는 반드시 opencv가 설치되어 있어야합니다. 또한, 이 모듈이 저장된 경로에 한글이 있으면 opencv의 문제로 작동이 되지 않습니다.

## 직접 필터를 만들고 싶으신가요?

아래의 기본 형식만 지켜주시면 word_detection.py 파일을 조금만 수정해도 추가가 가능합니다.

```python
class filter_example():

  def __init__(self) -> None:
    """
    초기 세팅 함수입니다.
    """
    self.name = "필터 이름"
    self.description = "예시 필터의 설명입니다."
    return None

  def detection(self, sentence:str, words:list, threshold:int) -> list:
    """
    filter을 이용하여 입력된 단어 리스트를 찾는 함수입니다.

    :param sentence: 문자열 타입으로 단어들을 찾을 문장입니다.
    :param words: 찾을 단어들의 리스트입니다.
    :param threshold: 어느정도 이상의 유사도를 가져야 해당 단어라고 판별할지 값입니다.
    :return: 결과를 잘 정리하여 리스트 형태로 반환합니다.
    """
    
    return [['욕설 부분 시작 위치','욕설 부분 종료 위치','욕설의 index','유사도']]
```