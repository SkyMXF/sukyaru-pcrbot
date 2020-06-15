from django import forms

class BattleRecordForm(forms.Form):
    boss_stage = forms.IntegerField(label="周目数", widget=forms.TextInput(attrs={'placeholder': "周目数"}))
    boss_id = forms.IntegerField(label="BOSS编号(1-5)", widget=forms.TextInput(attrs={'placeholder': "BOSS编号(1-5)"}))
    damage = forms.IntegerField(label="伤害", widget=forms.TextInput(attrs={'placeholder': "伤害"}))
    record_date = forms.DateTimeField(label="时间", widget=forms.DateTimeInput(attrs={'type':'datetime-local', 'placeholder': "出刀时间"}))
    final_kill = forms.MultipleChoiceField(label="尾刀", widget=forms.CheckboxSelectMultiple())
    comp_flag = forms.MultipleChoiceField(label="补偿刀", widget=forms.CheckboxSelectMultiple())