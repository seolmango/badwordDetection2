"""단어 탐지를 위한 도구 함수들이 있는 파일입니다"""
# -*- coding:utf-8 -*-

KOREAN_FIRST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ',
              'ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
KOREAN_MIDDLE = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ',
              'ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
KOREAN_LAST = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ',
                'ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ',
                'ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

def detach_word(word : str, option : dict = {"repeat":True, "pro2del":False}) -> list:
  """
  입력된 문자열 중 한국어를 초성, 중성, 종성으로 분해하는 함수입니다.

  :param word: 문자열 타입으로 분해할 문자열입니다.
  :param option: 상세 옵션을 설정할 수 있습니다.
  :return: 리스트 타입으로 각 요소들은 [(분해된 문자), (분해 전 위치)]의 형태입니다.
  """
  result = []
  for i in range(0, len(word)):
    if option['repeat'] and i != 0 and word[i] == word[i-1]:
      pass
    else:
      aski = ord(word[i]) - 44032
      if -1< aski and aski < 11173:
        # 한글이면
        if option['pro2del'] and KOREAN_FIRST[aski // 588] in ['ㅇ']:
          pass
        else:
          result.append([KOREAN_FIRST[aski // 588], i])
        result.append([KOREAN_MIDDLE[(aski // 28) % 21], i])
        if not aski % 28 == 0:
          # 종성이 존재하면
          result.append([KOREAN_LAST[aski % 28], i])
      else:
        #한글이 아니면
        if word[i] != ' ': # 공백 제거
          result.append([word[i], i])
  return result

def compare_text(sentence:list, words:list, base_layer:dict, threshold:float) -> list:
  """
  base_layer의 데이터를 기반으로 sentence에서 word와의 유사도가 threshold 이상인 부분을 찾아냅니다.

  :param sentence: 토큰화가 된 문장입니다.
  :param words: 토큰화가 된 단어 리스트입니다.
  :param base_layer: 한글 자모를 비교할 때의 기준이 되는 데이터입니다.
  :param threshold: 어느 정도 이상의 유사도를 가져야 할지 설정하는 0과 1사이의 실수값입니다.
  :return: 결과를 리스트 형태로 반환합니다.
  """
  sentence_layer = []
  for i in range(0,len(sentence)):
    if sentence[i][0] in base_layer:
      sentence_layer.append([base_layer[sentence[i][0]], sentence[i][1]])
  for i in range(0, len(words)):
    for j in range(0, len(words[i])):
      if words[i][j] in base_layer:
        words[i][j] = base_layer[words[i][j]]
  result = []
  temp = []
  for index in range(0,len(words)):
    word = words[index]
    for i in range(0, len(sentence_layer)-len(word)+1):
      similarity = 0
      for j in range(0, len(word)):
        most_sim_string_loc = None
        for k in range(max(0, i-3), min(len(sentence_layer), i+len(word)+3)):
          if word[j] // 10 == sentence_layer[k][0] // 10:
            if most_sim_string_loc is None:
              most_sim_string_loc = k
            elif abs(k-(i+j)) < abs(most_sim_string_loc-(i+j)):
              most_sim_string_loc = k
        if most_sim_string_loc is not None:
          similarity += 0.1 / pow(2, (abs(most_sim_string_loc-(i+j))))*(10-abs(word[j] - sentence_layer[most_sim_string_loc][0]))
      similarity = similarity / len(word)
      similarity = similarity ** (0.1**((len(word)-3)/10)+1.3)
      if similarity > threshold:
        if sentence_layer[i][1] not in temp:
          result.append([sentence_layer[i][1], sentence_layer[i+len(word)-1][1], index, similarity])
          temp.append(sentence_layer[i][1])
  return result