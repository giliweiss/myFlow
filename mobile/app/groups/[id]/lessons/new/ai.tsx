import { useEffect, useState } from 'react';
import { StyleSheet, ScrollView, Text, Alert, View } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import {
  ScreenContainer,
  TextField,
  Button,
  LoadingState,
} from '../../../../../src/components/ui';
import { theme } from '../../../../../src/theme';
import { strings } from '../../../../../src/i18n/he';
import { useGroup } from '../../../../../src/hooks/use-groups';
import { useExerciseCatalog } from '../../../../../src/hooks/use-exercises';
import { useGenerateLesson } from '../../../../../src/hooks/use-lessons';
import { setLessonPlanReviewDraft } from '../../../../../src/lib/lesson-draft';
import { generatedLessonExercisesToBuilder } from '../../../../../src/lib/lesson-form';
import type { ClarificationQuestion } from '../../../../../src/types/lesson-generation';
import { isClarificationResponse, isReadyLessonResponse } from '../../../../../src/types/lesson-generation';

export default function AiBuildLessonScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;

  const { data: group, isLoading: isGroupLoading } = useGroup(groupId);
  const {
    data: catalogExercises = [],
    isLoading: isCatalogLoading,
    isError: isCatalogError,
  } = useExerciseCatalog();
  const generateLesson = useGenerateLesson(groupId);

  const [intention, setIntention] = useState('');
  const [duration, setDuration] = useState('');
  const [notes, setNotes] = useState('');
  const [intentionError, setIntentionError] = useState('');
  const [clarificationQuestions, setClarificationQuestions] = useState<ClarificationQuestion[]>([]);
  const [clarificationAnswers, setClarificationAnswers] = useState<Record<string, string>>({});

  useEffect(() => {
    if (group?.typical_duration_minutes) {
      setDuration((current) => current || String(group.typical_duration_minutes));
    }
  }, [group?.typical_duration_minutes]);

  const handleSwitchToManual = () => {
    if (!groupId) {
      return;
    }
    router.replace(`/groups/${groupId}/lessons/new/manual`);
  };

  const handleGenerate = async () => {
    if (!intention.trim()) {
      setIntentionError(strings.lessons.intentionRequired);
      return;
    }

    if (!groupId || isCatalogError) {
      Alert.alert(strings.common.error, strings.lessons.catalogLoadError);
      return;
    }

    setIntentionError('');

    const plannedDurationMinutes =
      Number(duration) || group?.typical_duration_minutes || 60;

    const answeredQuestions = clarificationQuestions
      .map((question) => ({
        question_id: question.question_id,
        answer: clarificationAnswers[question.question_id]?.trim() || '',
      }))
      .filter((item) => item.answer.length > 0);

    if (clarificationQuestions.length > 0 && answeredQuestions.length !== clarificationQuestions.length) {
      Alert.alert(strings.common.error, strings.lessons.clarificationRequired);
      return;
    }

    try {
      const generated = await generateLesson.mutateAsync({
        intention: intention.trim(),
        planned_duration_minutes: plannedDurationMinutes,
        notes: notes.trim() || null,
        clarification_answers: answeredQuestions,
      });

      if (isClarificationResponse(generated)) {
        setClarificationQuestions(generated.clarification_questions);
        setClarificationAnswers({});
        return;
      }

      if (!isReadyLessonResponse(generated)) {
        Alert.alert(strings.common.error, strings.lessons.aiGenerateFailed);
        return;
      }

      const exercises = generatedLessonExercisesToBuilder(
        generated.lesson_exercises,
        catalogExercises,
      );

      setLessonPlanReviewDraft({
        groupId,
        intention: intention.trim(),
        duration,
        notes,
        title: generated.title?.trim() || intention.trim(),
        primaryGoal: generated.primary_goal,
        plannedDurationMinutes: generated.planned_duration_minutes,
        instructorNotes: generated.instructor_notes ?? '',
        guidance: generated.guidance,
        builderDraft: {
          title: generated.title?.trim() || intention.trim(),
          primaryGoal: generated.primary_goal,
          notes: generated.instructor_notes ?? '',
          plannedDurationMinutes: generated.planned_duration_minutes,
          exercises,
        },
      });

      router.replace(`/groups/${groupId}/lessons/new/plan-review`);
    } catch {
      Alert.alert(strings.common.error, strings.lessons.aiGenerateFailed);
    }
  };

  if (isGroupLoading || !group) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  if (generateLesson.isPending) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.lessons.aiPlanning} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <Text style={[theme.typography.body, styles.description]}>
          {strings.lessons.buildModeAiDesc}
        </Text>

        <TextField
          label={strings.lessons.intentionLabel}
          placeholder={strings.lessons.intentionPlaceholder}
          value={intention}
          onChangeText={(value) => {
            setIntention(value);
            if (intentionError) {
              setIntentionError('');
            }
            if (clarificationQuestions.length > 0) {
              setClarificationQuestions([]);
              setClarificationAnswers({});
            }
          }}
          error={intentionError}
          multiline
          numberOfLines={4}
        />

        {clarificationQuestions.length > 0 ? (
          <View style={styles.clarificationBlock}>
            <Text style={[theme.typography.subtitle, styles.clarificationTitle]}>
              {strings.lessons.clarificationTitle}
            </Text>
            {clarificationQuestions.map((question) => (
              <TextField
                key={question.question_id}
                label={question.prompt}
                placeholder={question.why_needed || strings.lessons.clarificationAnswerPlaceholder}
                value={clarificationAnswers[question.question_id] || ''}
                onChangeText={(value) => {
                  setClarificationAnswers((current) => ({
                    ...current,
                    [question.question_id]: value,
                  }));
                }}
                multiline
                numberOfLines={3}
              />
            ))}
          </View>
        ) : null}

        <TextField
          label={strings.lessons.duration}
          placeholder={String(group.typical_duration_minutes)}
          value={duration}
          onChangeText={setDuration}
        />

        <TextField
          label={strings.lessons.lessonNotes}
          placeholder={strings.lessons.lessonNotes}
          value={notes}
          onChangeText={setNotes}
          multiline
          numberOfLines={4}
        />

        <Text style={[theme.typography.caption, styles.disclaimer]}>
          {strings.lessons.aiCatalogDisclaimer}
        </Text>

        <Button
          label={strings.lessons.aiPlanLesson}
          onPress={() => {
            void handleGenerate();
          }}
          loading={generateLesson.isPending || isCatalogLoading}
          style={styles.generateButton}
        />

        <Button
          label={strings.lessons.switchToManual}
          onPress={handleSwitchToManual}
          variant="secondary"
          style={styles.manualButton}
        />
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  description: {
    textAlign: 'right',
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  },

  clarificationBlock: {
    marginBottom: theme.spacing.md,
  },

  clarificationTitle: {
    textAlign: 'right',
    marginBottom: theme.spacing.sm,
  },

  disclaimer: {
    textAlign: 'right',
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  },

  generateButton: {
    marginBottom: theme.spacing.md,
  },

  manualButton: {
    marginBottom: theme.spacing.lg,
  },
});
