from django import forms

class BattleRecordForm(forms.Form):
    boss_stage = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "周目数"}))
    boss_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "BOSS编号(1-5)"}))
    damage = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "伤害"}))
    record_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local', 'placeholder': "出刀时间"}))
    final_kill = forms.BooleanField(label="是尾刀", widget=forms.CheckboxInput(attrs={}))
    comp_flag = forms.BooleanField(label="是补偿刀", widget=forms.CheckboxInput(attrs={}))