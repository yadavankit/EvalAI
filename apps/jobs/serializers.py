import yaml

from rest_framework import serializers

from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):

    participant_team_name = serializers.SerializerMethodField()
    execution_time = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context')
        if context:
            created_by = context.get('request').user
            kwargs['data']['created_by'] = created_by.pk

            participant_team = context.get('participant_team').pk
            kwargs['data']['participant_team'] = participant_team

            challenge_phase = context.get('challenge_phase').pk
            kwargs['data']['challenge_phase'] = challenge_phase

        super(SubmissionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Submission
        fields = ('participant_team', 'participant_team_name', 'execution_time', 'challenge_phase',
                  'created_by', 'status', 'input_file', 'stdout_file', 'stderr_file', 'submitted_at')

    def get_participant_team_name(self, obj):
        return obj.participant_team.team_name

    def get_execution_time(self, obj):
        return obj.execution_time


class LeaderboardSerializer(serializers.ModelSerializer):

    participant_team_name = serializers.SerializerMethodField()
    challenge_phase_name = serializers.SerializerMethodField()
    final_result = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(LeaderboardSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Submission
        fields = ('participant_team_name', 'challenge_phase_name', 'final_result')

    def get_participant_team_name(self, obj):
        return obj.participant_team.team_name

    def get_challenge_phase_name(self, obj):
        return obj.challenge_phase.name

    def get_final_result(self, obj):
        try:
            return yaml.safe_load(obj.output)
        except:
            return None
