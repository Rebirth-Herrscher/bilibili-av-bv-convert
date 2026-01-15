from bilibili_av_bv import convert

print(convert("av170001"))
# BV1xx411c7mD

print(convert("BV1xx411c7mD"))
# av170001

# 批量转换
text = "视频 av170001 和 BV1yy411c7nT 是同一个"
print(convert(text))
# 视频 BV1xx411c7mD 和 av170001 是同一个
