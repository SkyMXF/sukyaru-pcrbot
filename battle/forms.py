from django import forms

class BattleRecordForm(forms.Form):
    boss_stage = forms.IntegerField(label="周目数", widget=forms.TextInput(attrs={'placeholder': "周目数"}))
    boss_id = forms.IntegerField(label="BOSS编号(1~5)", widget=forms.TextInput(attrs={'placeholder': "BOSS编号(1~5)"}))
    damage = forms.IntegerField(label="伤害(填写数值,不能使用'w'/'W'等简称)", widget=forms.TextInput(attrs={'placeholder': "伤害"}))
    record_date = forms.DateTimeField(label="时间", widget=forms.DateTimeInput(attrs={'type':'datetime-local'}), input_formats=['%Y-%m-%dT%H:%M'])
    final_kill = forms.BooleanField(label="尾刀", label_suffix="", required=False)
    comp_flag = forms.BooleanField(label="补偿刀", label_suffix="", required=False)