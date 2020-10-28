# echo "Hello World" | mail -s "Test email" dtsang012@yahoo.com
# -*- coding: utf-8 -*-
import re

#111
# json_str = {
#     "test3": "ttt",
#     "test4": "false"
# }
#
# for key in json_str:
#     print key
#     print json_str[key]
#end 111

#222
#extract vn phone number from text
def extract_phone_number_from_text(org_str):
    if org_str == "":
        return ""
    org_str = org_str.strip()
    raw_str = org_str.replace('.','').replace('-','')
    phones = re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', raw_str)
    new_phones = []
    for phone in phones:
        if phone is not None and phone is not '' and len(phone) < 15:
            new_phones.append(phone.replace(' ',''))
        else:
            new_phones.append(phone)
    return new_phones
org_str = "098.371.5890 - 090.6417188 Bán giá thị trường, sl lon be. 08-098-8876.8 Ban nhanh gd nghiem tuc , lh 0925 782 890 Giá cả thay đổi liên tục (0909)786543 khi thị trường sôi động. Vui lòng liên hệ để cặp nhật giá từng thời điểm. Tks"
# org_str = "CAN MUA KL LON NHO GIA THOA THUAN LH 0916508087 ,0916410299 GAP THAO"
# org_str = "Cần bán kl lớn nhỏ giá tt vui lòng lh. 0938811811."
# org_str = "Liên hệ 0989 975215"
# org_str = "Chức sdt 0938.30.9798 mua MSB giá thị trường số lượng lớn nhỏ. Ban nhanh gd nghiem tuc , lh 0925 782 890"
# print extract_phone_number_from_text(org_str)
#end 222

#patch phone number

#end patch phone number