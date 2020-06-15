from django import forms

class BattleRecordForm(forms.Form):
    boss_stage = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "周目数"}))
    boss_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "BOSS编号(1-5)"}))
    damage = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "伤害"}))
    record_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'date', 'placeholder': "出刀时间"}))
    final_kill = forms.BooleanField(widget=forms.CheckboxInput(label="是尾刀", attrs={}))
    comp_flag = forms.BooleanField(widget=forms.CheckboxInput(label="是补偿刀", attrs={}))