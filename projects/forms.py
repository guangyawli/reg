from django import forms
from projects.models import TeamScore
from idea.models import Team


class JudgeForm(forms.ModelForm):
    class Meta:
        model = TeamScore
        exclude = ['team', 'judger_name', 'total_score']
        fields = ('score_applicability', 'score_creativity', 'score_challenge', 'score_completion')
        widgets = {
            'score_applicability': forms.NumberInput(attrs={'min':'0','max':'30'}),
            'score_creativity': forms.NumberInput(attrs={'min':'0','max':'30'}),
            'score_challenge': forms.NumberInput(attrs={'min':'0','max':'20'}),
            'score_completion': forms.NumberInput(attrs={'min':'0','max':'20'})
        }


class CheckTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('stu_check',)
