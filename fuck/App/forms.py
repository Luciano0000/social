from django import forms

from App.models import Profile

"""
            form 表单验证

Django ｆｏｒｍｓ 表单处理　　类似于Flask的　ＷＴＦ
"""
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile # 指定模型
        fields = (
            # 可以是list 或者 tuple
            'dating_sex',
            'min_distance',
            'location',
            'max_distance',
            'min_dating_age',
            'max_dating_age',
            'vibration',
            'only_matche',
            'auto_play',

        )

    def clean_max_distance(self):                                    # 规范在需要验证的字段前面+clean_
        # 检查最大距离
        cleaned_data = super().clean()                               # forms自带clean()方法
        if cleaned_data['min_distance']>cleaned_data['max_distance']:# 过滤非法操作
            raise forms.ValidationError('提示：最小距离不能大于最大距离') # forms自带ValidationError()用于提示错误信息
        return cleaned_data['max_distance']                          # 返回


    def clean_max_dating_age(self):
        #  检查最大年龄
        cleaned_data = super().clean()
        if cleaned_data['min_dating_age'] > cleaned_data['max_dating_age']:
            raise forms.ValidationError('提示：最小年龄不能大于最大年龄')
        return cleaned_data['max_dating_age']








