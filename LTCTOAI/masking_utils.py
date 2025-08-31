# 개인정보 마스킹 함수 모듈
def mask_name(name):
    # 3글자 이름만 마스킹, 그 외는 그대로 반환
    if len(name) == 3:
        return name[0] + '*' + name[2]
    return name

def mask_id(id_number):
    return id_number[:7] + '*' * (len(id_number) - 7)
