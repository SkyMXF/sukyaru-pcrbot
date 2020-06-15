from django import forms

class BattleRecordForm(forms.Form):
    boss_stage = forms.IntegerField(label="周目数", widgetwidget=forms.TextInput(attrs={'placeholder': "周目数"}))
    boss_id = forms.IntegerField(label="BOSS编号(1-5)", widgetwidget=forms.TextInput(attrs={'placeholder': "BOSS编号(1-5)"}))
    damage = forms.IntegerField(label="伤害", widgetwidget=forms.TextInput(attrs={'placeholder': "伤害"}))
    record_date = forms.DateTimeField(label="时间", widgetwidget=forms.DateTimeInput(attrs={'type':'datetime-local', 'placeholder': "出刀时间"}))
    final_kill = forms.BooleanField(label="是尾刀", widget=forms.CheckboxInput(attrs={'type':'checkbox'}))
    comp_flag = forms.BooleanField(label="是补偿刀", widget=forms.CheckboxInput(attrs={'type':'checkbox'}))